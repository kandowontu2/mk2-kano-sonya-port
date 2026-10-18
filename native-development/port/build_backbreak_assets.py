"""Build typed back-break ASM and unchanged stock Wolf graphics sockets."""
import hashlib
import json
import sys
from pathlib import Path
PORT=Path(__file__).resolve().parent
OUT=PORT/'generated_backbreak'
assert not OUT.exists() or '--refresh-generated' in sys.argv
OUT.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
source=PORT/'assets/backbreak'
manifest=json.loads((source/'BACKBREAK_SOURCE.json').read_text())
assert manifest['format']=='MK2KS-BACKBREAK-PALETTE-INDEX-PGM-1'
prefix=(PORT/'generated_pit/fighter_ui_finish_pit_graphics.bin').read_bytes()
packed=bytearray(prefix)
lines=['; Authored back-break sprite DATA. No imported executable words.',
       '        .include mainequ.asm','        .ref ks_kano_primary_palette,ks_sonya_primary_palette','        .data']
records={}
for actor in ('kano','sonya'):
    records[actor]=[]
    for frame in manifest['actors'][actor]['frames']:
        path=source/frame['file'];raw=path.read_bytes()
        assert sha(raw)==frame['fileSHA256']
        words=' '.join(line.split('#',1)[0] for line in raw.decode('ascii').splitlines()).split()
        assert words[0]=='P2'
        w,h,maximum=map(int,words[1:4]);indices=bytes(map(int,words[4:]))
        assert (w,h,maximum)==(frame['width'],frame['height'],63) and len(indices)==w*h
        assert max(indices)<=63 and sha(indices)==frame['indexSHA256']
        payload=bytearray((len(indices)*6+7)//8)
        for i,value in enumerate(indices):
            bit=i*6;at=bit//8;shift=bit&7
            payload[at]|=value<<shift&255
            if shift>2:payload[at+1]|=value>>(8-shift)
        offset=len(packed);packed.extend(payload)
        label=f'ks_bk_{actor}_frame{frame["phase"]}'
        pose=f'ks_bk_{actor}_pose{frame["phase"]}'
        lines.extend([f'        .def {pose}',label,
            f'        .word {w},{h},{frame["xOffset"]},{frame["yOffset"]}',
            f'        .long 0{(0xc00000+offset)*8:08x}h','        .word 06000h',
            f'        .long ks_{actor}_primary_palette',pose,f'        .long {label},0'])
        records[actor].append(dict(frame,packedByteOffset=offset,packedSHA256=sha(payload)))
    name=f'ks_{actor}_back_broke'
    lines.extend([f'        .def {name}',name,
        f'        .long ks_bk_{actor}_pose0,ani_adjustxy','        .word 0,10',
        f'        .long ks_bk_{actor}_pose0,ani_adjustxy','        .word 0,48',
        f'        .long ks_bk_{actor}_pose0,ks_bk_{actor}_pose1,ks_bk_{actor}_pose2,0',
        f'        .long ks_bk_{actor}_pose1,ks_bk_{actor}_pose0,0'])
assert packed[:len(prefix)]==prefix and len(packed)<0x600000
(OUT/'KSBKART.ASM').write_text('\n'.join(lines)+'\n')
(OUT/'fighter_ui_finish_backbreak_graphics.bin').write_bytes(packed)
region=packed+bytes(0x600000-len(packed));rebuilt=bytearray(0x600000)
sockets={}
for bank,size in ((0,0x100000),(1,0x80000)):
    for lane in range(4):
        chip=121-bank*4-lane;name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
        start=bank*0x400000+lane;payload=region[start:start+size*4:4]
        assert len(payload)==size
        (OUT/name).write_bytes(payload);rebuilt[start:start+size*4:4]=payload;sockets[name]=sha(payload)
assert rebuilt==region
result={'records':records,'prefixSHA256':sha(prefix),'prefixBytes':len(prefix),
        'appendedBytes':len(packed)-len(prefix),'totalGraphicsBytes':len(packed),
        'stockSocketRoundTripVerified':True,'sockets':sockets,'visualAcceptance':False,
        'nativePaletteVerified':False,'runtimeVerified':False,'fullPortVerified':False}
(OUT/'BACKBREAK_DATA.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('records','sockets')}))
