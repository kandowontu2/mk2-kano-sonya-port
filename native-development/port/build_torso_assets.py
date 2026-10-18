"""Build typed native multipart torso data; no legacy executable payload."""
import json
from pathlib import Path
import re
import sys
from generate_head_sources import PORT,sha
OUT=PORT/'generated_torso'
def main(prefix_path=None,output=None,template_root=None,emit_sockets=True):
    global OUT
    if output is not None:OUT=Path(output)
    assert not OUT.exists() or '--refresh-generated' in sys.argv
    manifest=json.loads((PORT/'assets/torso/TORSO_SOURCE.json').read_text())
    assert manifest['format']=='MK2KS-TORSO-PALETTE-INDEX-PGM-1'
    prefix=(Path(prefix_path) if prefix_path is not None else PORT/'generated_drain/fighter_ui_finish_drain_graphics.bin').read_bytes()
    packed=bytearray(prefix)
    lines=['; Authored native multipart torso DATA, no executable words.',
           '        .include mainequ.asm','        .data']
    native=(PORT.parent/'baseline/mk2-rebuild-main/srcw/MKLK.ASM').read_text()
    reaction=native[native.index('\na_torso_ripped\n'):native.index('\nLKRIPTORSO1\n',native.index('\na_torso_ripped\n'))]
    swipe=native[native.index('\na_swipe_torso\n'):native.index('\na_head',native.index('\na_swipe_torso\n'))]
    records={}
    for actor in ('kano','sonya'):
        lines += [f'        .ref ks_{actor}_primary_palette']
        template=((Path(template_root) if template_root is not None else PORT/'generated_templates_candidate')/f'{actor.upper()}ANI.ASM').read_text()
        recoil=re.search(r'(?m)^ks_'+actor+r'_main_10\s*\n\s*\.long\s+(\w+)',template)[1]
        lines += [f'        .ref {recoil}']
        mapping={'a_torso_ripped':f'ks_{actor}_torso_ripped','a_swipe_torso':f'ks_{actor}_swipe_torso',
                 'LKSTUMBLE5':recoil,'LKDEADLEG1':f'ks_tr_{actor}_pose6'}
        records[actor]=[]
        for frame in manifest['actors'][actor]['frames']:
            phase=frame['phase'];path=PORT/'assets/torso'/frame['file'];raw=path.read_bytes()
            assert sha(raw)==frame['fileSHA256']
            words=' '.join(s.split('#',1)[0] for s in raw.decode('ascii').splitlines()).split()
            assert words[0]=='P2'
            w,h,maximum=map(int,words[1:4]);indices=bytes(map(int,words[4:]))
            assert (w,h,maximum)==(frame['width'],frame['height'],63)
            assert len(indices)==w*h and max(indices)<=63 and sha(indices)==frame['indexSHA256']
            count=frame['componentCount'];tiles=[];rebuilt=bytearray(w*h);names=[]
            for column in range(count):
                x0,x1=column*w//count,(column+1)*w//count
                tile=bytes(v for y in range(h) for v in indices[y*w+x0:y*w+x1])
                assert any(tile)
                payload=bytearray((len(tile)*6+7)//8)
                for i,v in enumerate(tile):
                    at,shift=divmod(i*6,8);payload[at]|=v<<shift&255
                    if shift>2:payload[at+1]|=v>>(8-shift)
                scalar=int.from_bytes(payload,'little')
                decoded=bytes(scalar>>(i*6)&63 for i in range(len(tile)))
                assert decoded==tile
                for y in range(h):rebuilt[y*w+x0:y*w+x1]=decoded[y*(x1-x0):(y+1)*(x1-x0)]
                offset=len(packed);packed.extend(payload)
                name=f'ks_tr_{actor}_frame{phase}_{column}';names.append(name)
                lines += [f'        .def {name}',name,
                    f'        .word {x1-x0},{h},{frame["xOffset"]-x0},{frame["yOffset"]}',
                    f'        .long 0{(0xc00000+offset)*8:08x}h','        .word 06000h',
                    f'        .long ks_{actor}_primary_palette']
                tiles.append(dict(label=name,column=[x0,x1],packedByteOffset=offset,packedSHA256=sha(payload)))
            assert bytes(rebuilt)==indices
            pose=f'ks_tr_{actor}_pose{phase}'
            lines += [f'        .def {pose}',pose,'        .long '+','.join(names+['0'])]
            if phase<6:mapping[f'LKRIPTORSO{phase+1}']=pose
            records[actor].append(dict(frame,components=tiles))
        for root,body in (('torso_ripped',reaction),('swipe_torso',swipe)):
            if root=='swipe_torso':
                frame=records[actor][5];names=[]
                for column,tile in enumerate(frame['components']):
                    x0,x1=tile['column'];name=f'ks_sw_{actor}_frame5_{column}';names.append(name)
                    lines += [f'        .def {name}',name,
                        f'        .word {x1-x0},{frame["height"]},{frame["xOffset"]-x0},{frame["yOffset"]-16}',
                        f'        .long 0{(0xc00000+tile["packedByteOffset"])*8:08x}h','        .word 06000h',
                        f'        .long ks_{actor}_primary_palette']
                pose=f'ks_sw_{actor}_pose5'
                lines += [f'        .def {pose}',pose,'        .long '+','.join(names+['0'])]
                mapping['LKRIPTORSO6']=pose
            translated=re.sub(r'\b[A-Za-z_]\w*\b',lambda m:mapping.get(m[0],m[0]),body)
            code='\n'.join(line.split(';',1)[0] for line in translated.splitlines() if not line.lstrip().startswith('*'))
            assert 'LKRIPTORSO' not in code and 'LKDEADLEG' not in code and 'LKSTUMBLE' not in code
            lines += [f'        .def ks_{actor}_{root}',translated]
    assert packed[:len(prefix)]==prefix and len(packed)<0x600000
    OUT.mkdir(exist_ok=True)
    (OUT/'KSTRART.ASM').write_text('\n'.join(lines)+'\n')
    (OUT/'fighter_ui_finish_torso_graphics.bin').write_bytes(packed)
    region=packed+bytes(0x600000-len(packed));rebuilt=bytearray(0x600000);sockets={}
    for bank,size in ((0,0x100000),(1,0x80000)):
        for lane in range(4):
            chip=121-bank*4-lane;name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
            start=bank*0x400000+lane;payload=region[start:start+size*4:4]
            assert len(payload)==size
            if emit_sockets:
                (OUT/name).write_bytes(payload)
            rebuilt[start:start+size*4:4]=payload;sockets[name]=sha(payload)
    assert rebuilt==region
    report=dict(records=records,sockets=sockets,prefixSHA256=sha(prefix),prefixBytes=len(prefix),
        appendedBytes=len(packed)-len(prefix),totalGraphicsBytes=len(packed),
        independentTileDecodeVerified=True,fullPoseReassemblyVerified=True,stockSocketRoundTripVerified=True,
        runtimeVerified=False,fullVisualAcceptance=False,fullPortVerified=False)
    (OUT/'TORSO_DATA.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('records','sockets')}))
if __name__=='__main__':main()
