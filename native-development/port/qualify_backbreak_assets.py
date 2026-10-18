"""Independent source-index, packed-bitstream and stock-socket round trip."""
import hashlib
import json
from pathlib import Path
PORT=Path(__file__).resolve().parent
source=PORT/'assets/backbreak'
built=PORT/'generated_backbreak'
manifest=json.loads((source/'BACKBREAK_SOURCE.json').read_text())
metadata=json.loads((built/'BACKBREAK_DATA.json').read_text())
packed=(built/'fighter_ui_finish_backbreak_graphics.bin').read_bytes()
prefix=(PORT/'generated_pit/fighter_ui_finish_pit_graphics.bin').read_bytes()
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
assert packed[:len(prefix)]==prefix
assert len(prefix)==metadata['prefixBytes'] and sha(prefix)==metadata['prefixSHA256']
assert len(packed)==metadata['totalGraphicsBytes']<0x600000
frames=[]
for actor in ('kano','sonya'):
    assert len(manifest['actors'][actor]['frames'])==3
    for original,record in zip(manifest['actors'][actor]['frames'],metadata['records'][actor]):
        raw=(source/original['file']).read_bytes()
        assert sha(raw)==original['fileSHA256']
        words=' '.join(line.split('#',1)[0] for line in raw.decode('ascii').splitlines()).split()
        assert words[0]=='P2'
        w,h,maximum=map(int,words[1:4]);indices=bytes(map(int,words[4:]))
        assert (w,h,maximum)==(record['width'],record['height'],63)
        assert len(indices)==w*h and max(indices)<=63 and any(indices)
        assert sha(indices)==record['indexSHA256']
        offset=record['packedByteOffset'];size=(len(indices)*6+7)//8
        payload=packed[offset:offset+size]
        assert sha(payload)==record['packedSHA256']
        # Decode independently of the builder's shift/OR writer.
        bits=int.from_bytes(payload,'little')
        decoded=bytes((bits>>(i*6))&63 for i in range(len(indices)))
        assert decoded==indices
        frames.append({'actor':actor,'phase':record['phase'],'indexSHA256':sha(decoded),'packedBytes':size})
region=bytearray(0x600000)
for bank,size in ((0,0x100000),(1,0x80000)):
    for lane in range(4):
        chip=121-bank*4-lane;name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
        payload=(built/name).read_bytes()
        assert len(payload)==size and sha(payload)==metadata['sockets'][name]
        start=bank*0x400000+lane;region[start:start+size*4:4]=payload
assert region[:len(packed)]==packed and not any(region[len(packed):])
assembly=(built/'KSBKART.ASM').read_text()
assert '.text' not in assembly and '.include mainequ.asm' in assembly
result={'sourceIndexAndPackedRoundTripVerified':True,'stockSocketRoundTripVerified':True,
        'earlierGraphicsPrefixPreserved':True,'frames':frames,'totalGraphicsBytes':len(packed),
        'assemblySHA256':sha((built/'KSBKART.ASM').read_bytes()),'fullVisualAcceptance':False,'fullPortVerified':False}
(PORT/'BACKBREAK_ASSET_QUALIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({key:value for key,value in result.items() if key!='frames'}))
