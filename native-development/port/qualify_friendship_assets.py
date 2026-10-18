"""Linked native Friendship data checks; deliberately no gameplay acceptance."""
import json
import re
import struct
from pathlib import Path
import generate_friendship_data as gen
from qualify_bubble import SRC,sha

HERE=gen.HERE
out=HERE/'generated_friendship'
data=json.loads((out/'FRIEND_DATA.json').read_text())
assert data['sourceSHA256']==sha(out/'KSFRART.ASM')
assert (SRC/'KSFRART.ASM').read_bytes()==(out/'KSFRART.ASM').read_bytes()
log=SRC.parent/'PFRART.LOG'
assert 'No Errors,  No Warnings' in log.read_text()
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
rom=bytearray(1048576)
for lane in [0,1]:rom[lane::2]=b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ['F8','FC'])
def at(address):return (address-0xff800000)//8
def read(address):return struct.unpack_from('<I',rom,at(address))[0]
packed=(out/'fighter_ui_finish_friend_graphics.bin').read_bytes()
prefix=(HERE/'generated_names/fighter_ui_finish_names_graphics.bin').read_bytes()
assert packed[:len(prefix)]==prefix and sha(HERE/'generated_names/fighter_ui_finish_names_graphics.bin')==data['prefixSHA256']
region=bytearray(0x600000)
for bank,size in [(0,0x100000),(1,0x80000)]:
    for lane in range(4):
        chip=121-bank*4-lane;name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
        raw=(out/name).read_bytes();assert len(raw)==size and sha(out/name)==data['sockets'][name]
        start=bank*0x400000+lane;region[start:start+size*4:4]=raw
assert region==packed+bytes(0x600000-len(packed))
# Frame labels are intentionally local. Each composite exports its exact linked
# frame pointers, permitting validation without relying on local MAP symbols.
frames={}
donor=(gen.art.ROOT/'mk3/mk3-maincpu.bin').read_bytes()
assert gen.art.sha(donor)==data['inputProgramSHA256']
for groups in data['groups'].values():
    for value in groups:
        group=int(value,16);address=symbols[f'ks_friend_pose_{group:08x}']
        original=gen.p.frame_group(donor,group,group,group+0x200)
        for i,frame in enumerate(original):
            pointer=read(address+i*32)
            assert frame not in frames or frames[frame]==pointer
            frames[frame]=pointer
        assert read(address+len(original)*32)==0
assert len(frames)==data['uniqueFrames']==56
for pin in data['framePins']:
    frame=int(pin['sourceFrame'],16);address=frames[frame]
    actual=struct.unpack_from('<HHhhIH',rom,at(address))
    original=struct.unpack_from('<HHhhIH',donor,gen.p.stock_file(frame))
    assert actual[:4]==original[:4] and actual[5]==original[5]
    assert actual[4]==(0xc00000+pin['packedByteOffset'])*8
    size=(pin['bits']+7)//8;start=pin['packedByteOffset']
    assert gen.art.sha(packed[start:start+size])==pin['compressedSHA256']
    assert read(address+112)==symbols[pin['palette']]
report=dict(scope='source assembly/link, geometry, native palette references, compressed pixels and socket round-trip only',
            compositePoses=36,uniqueFrames=56,appendedBytes=data['appendedBytes'],
            nativeActionsImplemented=False,runtimeVerified=False,releaseReady=False)
paths=[out/'KSFRART.ASM',out/'FRIEND_DATA.json',SRC/'MK2P.OUT',SRC/'MK2P.MAP',SRC/'KSFRART.OBJ',log,Path(__file__),HERE/'generate_friendship_data.py']
report['pins']={str(p):sha(p) for p in paths}
(out/'qualification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='pins'},indent=2))
