"""Build named native Pit DATA from standalone readable authored PGM sources."""
import argparse
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent

def sha(raw):return hashlib.sha256(raw).hexdigest().upper()

def build(prefix_path=None):
    source_dir=HERE/'assets/pit'
    manifest=json.loads((source_dir/'PIT_SOURCE.json').read_text())
    assert manifest['format']=='MK2KS-PIT-PALETTE-INDEX-PGM-1'
    assert manifest['transparentIndex']==0 and manifest['maxIndex']==63
    prefix_path=Path(prefix_path) if prefix_path is not None else HERE/'generated_friendship/fighter_ui_finish_friend_graphics.bin'
    prefix=prefix_path.read_bytes()
    packed=bytearray(prefix)
    lines=['; Recovered authored dedicated Pit sprite DATA only, no old executable payload.',
           '        .include mainequ.asm','        .ref ks_kano_primary_palette,ks_sonya_primary_palette','        .data']
    pins={str(source_dir/'PIT_SOURCE.json'):sha((source_dir/'PIT_SOURCE.json').read_bytes())}
    pins[str(prefix_path)]=sha(prefix)
    frames_built=0
    records={}
    for name,actor in [('kano',17),('sonya',18)]:
        record=manifest['actors'][name]
        assert record['actorID']==actor and record['coordinate']==(64<<16)|192
        assert len(record['frames'])==6
        records[name]=dict(actorID=actor,coordinate=record['coordinate'],frames=[])
        for phase,frame in enumerate(record['frames']):
            assert frame['phase']==phase
            filename=frame['file'];assert Path(filename).name==filename and filename.endswith('.pgm')
            path=source_dir/filename;raw_source=path.read_bytes()
            assert sha(raw_source)==frame['fileSHA256'];pins[str(path)]=sha(raw_source)
            words=' '.join(line.split('#',1)[0] for line in raw_source.decode('ascii').splitlines()).split()
            assert words[0]=='P2';w,h,maximum=map(int,words[1:4])
            assert (w,h,maximum)==(frame['width'],frame['height'],63)
            values=list(map(int,words[4:]));assert len(values)==w*h and all(0<=v<=63 for v in values)
            indices=bytes(values);assert sha(indices)==frame['indexSHA256']
            raw=bytearray((len(indices)*6+7)//8)
            for i,value in enumerate(indices):
                bit=i*6;at=bit//8;shift=bit&7
                raw[at]|=(value<<shift)&255
                if shift>2:raw[at+1]|=value>>(8-shift)
            assert sha(raw)==frame['packedSHA256']
            offset=len(packed);packed.extend(raw)
            label=f'ks_pit_{name}_frame{phase}'
            lines += [label,f'        .word {w},{h},{frame["xOffset"]},{frame["yOffset"]}',
                      f'        .long 0{(0xc00000+offset)*8:08x}h','        .word 06000h',
                      f'        .long ks_{name}_primary_palette',f'ks_pit_{name}_pose{phase}',f'        .long {label},0']
            frames_built+=1
            records[name]['frames'].append(dict(phase=phase,width=w,height=h,xOffset=frame['xOffset'],
                yOffset=frame['yOffset'],packedByteOffset=offset,compressedSHA256=sha(raw),indexSHA256=sha(indices)))
        lines += [f'        .def ks_pit_{name}_sequence',f'ks_pit_{name}_sequence']
        lines += [f'        .long ks_pit_{name}_pose{i}' for i in range(5)]
        lines += [f'        .long ani_jump,ks_pit_{name}_sequence,0',f'        .long ks_pit_{name}_pose5,0']
    assert packed[:len(prefix)]==prefix and len(packed)<0x600000
    outputs={'KSPITART.ASM':('\n'.join(lines)+'\n').encode(),'fighter_ui_finish_pit_graphics.bin':bytes(packed)}
    region=packed+bytes(0x600000-len(packed));rebuilt=bytearray(0x600000)
    for bank,size in [(0,0x100000),(1,0x80000)]:
        for lane in range(4):
            chip=121-bank*4-lane;name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
            start=bank*0x400000+lane;raw=region[start:start+size*4:4]
            assert len(raw)==size;outputs[name]=bytes(raw);rebuilt[start:start+size*4:4]=raw
    assert rebuilt==region and frames_built==12
    metadata=dict(sourceKind=manifest['sourceKind'],sourcePayloadSHA256=manifest['historicalAssetPayloadSHA256'],
                  sourceSHA256=sha(outputs['KSPITART.ASM']),records=records,prefixSHA256=sha(prefix),
                  prefixBytes=len(prefix),appendedBytes=len(packed)-len(prefix),totalGraphicsBytes=len(packed),
                  sockets={name:sha(raw) for name,raw in outputs.items() if name.endswith(tuple(f'.u{i}' for i in range(114,122)))},
                  stockSocketRoundTripVerified=True,oldExecutableCodeImported=False,
                  standaloneAuthoredSources=True,visualAcceptance=False,runtimeVerified=False,releaseReady=False)
    outputs['PIT_DATA.json']=(json.dumps(metadata,indent=2)+'\n').encode()
    report=dict(scope='standalone authored palette-index Pit source round-trip',sourceImages=12,
                inputs=pins,outputs={name:sha(raw) for name,raw in outputs.items()},
                oldPackageOrDriverRequired=False,losslessIndexAndPackedHashesVerified=True,
                graphicsPrefixPreserved=True,stockSocketRoundTripVerified=True,runtimeVerified=False,releaseReady=False)
    return outputs,report

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-existing',action='store_true')
    parser.add_argument('--output',type=Path,default=HERE/'generated_pit')
    args=parser.parse_args();outputs,report=build()
    if args.verify_existing:
        assert args.output.is_dir()
        for name,raw in outputs.items():
            if name=='PIT_DATA.json':
                # Earlier recovery metadata has extra provenance fields; engine
                # outputs must be byte-identical and common metadata must agree.
                before=json.loads((args.output/name).read_text());after=json.loads(raw)
                for key in ('sourceSHA256','prefixSHA256','appendedBytes','totalGraphicsBytes','sockets'):
                    assert before[key]==after[key],key
            else:assert (args.output/name).read_bytes()==raw,name
        receipt=HERE/'PIT_SOURCE_ROUNDTRIP.json'
        report['byteIdenticalVerifiedFiles']=[name for name in outputs if name!='PIT_DATA.json']
        report['metadataComparedSemantically']=True
    else:
        assert not args.output.exists(),'Never overwrite generated evidence'
        args.output.mkdir(parents=True)
        for name,raw in outputs.items():(args.output/name).write_bytes(raw)
        receipt=args.output/'standalone_build.json'
    report['builderSHA256']=sha(Path(__file__).read_bytes())
    receipt.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('inputs','outputs')},indent=2))
