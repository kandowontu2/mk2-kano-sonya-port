"""Pure readable-PGM to native backbreaker art rebuild, without output side effects."""
import hashlib
import json
from pathlib import Path

PORT=Path(__file__).resolve().parent
sha=lambda raw:hashlib.sha256(raw).hexdigest().upper()

def build(prefix_path):
    source=PORT/'assets/backbreak'
    manifest=json.loads((source/'BACKBREAK_SOURCE.json').read_text())
    assert manifest['format']=='MK2KS-BACKBREAK-PALETTE-INDEX-PGM-1'
    prefix=Path(prefix_path).read_bytes();packed=bytearray(prefix)
    lines=['; Authored back-break sprite DATA. No imported executable words.',
        '        .include mainequ.asm','        .ref ks_kano_primary_palette,ks_sonya_primary_palette','        .data']
    records={};pins={'BACKBREAK_SOURCE.json':sha((source/'BACKBREAK_SOURCE.json').read_bytes())}
    for actor in ('kano','sonya'):
        records[actor]=[]
        frames=manifest['actors'][actor]['frames']
        assert [frame['phase'] for frame in frames]==[0,1,2]
        for frame in frames:
            name=frame['file'];assert Path(name).name==name and name.endswith('.pgm')
            raw=(source/name).read_bytes();assert sha(raw)==frame['fileSHA256'];pins[name]=sha(raw)
            words=' '.join(line.split('#',1)[0] for line in raw.decode('ascii').splitlines()).split()
            assert words[0]=='P2'
            width,height,maximum=map(int,words[1:4]);indices=bytes(map(int,words[4:]))
            assert (width,height,maximum)==(frame['width'],frame['height'],63)
            assert len(indices)==width*height and max(indices)<=63 and sha(indices)==frame['indexSHA256']
            payload=bytearray((len(indices)*6+7)//8)
            for index,value in enumerate(indices):
                at,shift=divmod(index*6,8)
                payload[at]|=value<<shift&255
                if shift>2:payload[at+1]|=value>>(8-shift)
            offset=len(packed);packed.extend(payload)
            label=f'ks_bk_{actor}_frame{frame["phase"]}';pose=f'ks_bk_{actor}_pose{frame["phase"]}'
            lines += [f'        .def {pose}',label,
                f'        .word {width},{height},{frame["xOffset"]},{frame["yOffset"]}',
                f'        .long 0{(0xc00000+offset)*8:08x}h','        .word 06000h',
                f'        .long ks_{actor}_primary_palette',pose,f'        .long {label},0']
            records[actor].append(dict(frame,packedByteOffset=offset,packedSHA256=sha(payload)))
        name=f'ks_{actor}_back_broke'
        lines += [f'        .def {name}',name,
            f'        .long ks_bk_{actor}_pose0,ani_adjustxy','        .word 0,10',
            f'        .long ks_bk_{actor}_pose0,ani_adjustxy','        .word 0,48',
            f'        .long ks_bk_{actor}_pose0,ks_bk_{actor}_pose1,ks_bk_{actor}_pose2,0',
            f'        .long ks_bk_{actor}_pose1,ks_bk_{actor}_pose0,0']
    assert packed[:len(prefix)]==prefix and len(packed)<0x600000
    # Match the established Windows-authored source encoding deterministically.
    outputs={'KSBKART.ASM':('\r\n'.join(lines)+'\r\n').encode('ascii'),
        'fighter_ui_finish_backbreak_graphics.bin':bytes(packed)}
    region=packed+bytes(0x600000-len(packed));sockets={};rebuilt=bytearray(0x600000)
    for bank,size in ((0,0x100000),(1,0x80000)):
        for lane in range(4):
            chip=121-bank*4-lane;name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
            start=bank*0x400000+lane;raw=bytes(region[start:start+size*4:4])
            assert len(raw)==size;outputs[name]=raw;sockets[name]=sha(raw)
            rebuilt[start:start+size*4:4]=raw
    assert rebuilt==region
    report=dict(records=records,prefixSHA256=sha(prefix),prefixBytes=len(prefix),
        appendedBytes=len(packed)-len(prefix),totalGraphicsBytes=len(packed),
        stockSocketRoundTripVerified=True,sockets=sockets,visualAcceptance=False,
        nativePaletteVerified=False,runtimeVerified=False,fullPortVerified=False)
    outputs['BACKBREAK_DATA.json']=(json.dumps(report,indent=2)+'\r\n').encode('ascii')
    return outputs,dict(sourceFiles=pins,allFrames=6,releaseReady=False)
