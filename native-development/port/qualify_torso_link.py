"""Read-only native torso ROM ABI verification; not fatality acceptance."""
import json
from pathlib import Path
import re
import struct
from inventory_character_tables import source_tables
PORT=Path(__file__).resolve().parent
BUILD=PORT.parent/'baseline/mk2-rebuild-main/srcp'
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(BUILD/'MK2P.MAP').read_text())}
lanes=[b''.join((BUILD/f'rom/P12{p}.{i}').read_bytes() for p in ('F8','FC')) for i in (0,1)]
program=bytearray(0x100000);program[::2]=lanes[0];program[1::2]=lanes[1]
def raw(a,size):return bytes(program[(a-0xff800000)//8:(a-0xff800000)//8+size])
def read(a,fmt):return struct.unpack('<'+fmt,raw(a,struct.calcsize('<'+fmt)))
def value(token):
    if token in symbols:return symbols[token]
    if token in ('ani_adjustxy','ani_calla'):return {'ani_adjustxy':4,'ani_calla':6}[token]
    return int(token[:-1],16) if token.lower().endswith('h') else int(token)
tables=source_tables((PORT/'generated_torso/KSTRART.ASM').read_text())
metadata=json.loads((PORT/'generated_torso/TORSO_DATA.json').read_text())
count=0
for actor in ('kano','sonya'):
    for index,role in ((57,'torso_ripped'),(65,'swipe_torso')):
        root=f'ks_{actor}_{role}'
        assert read(symbols[f'ks_{actor}_anitab1']+index*32,'I')==(symbols[root],)
        expected=bytearray()
        for row in tables[root]['rows']:
            bits=32 if row['type']=='long' else 16
            for token in row['values']:expected.extend((value(token)&((1<<bits)-1)).to_bytes(bits//8,'little'))
        assert raw(symbols[root],len(expected))==expected
    for frame in metadata['records'][actor]:
        pointers=[]
        for tile in frame['components']:
            name=tile['label'];x0,x1=tile['column'];pointers.append(symbols[name])
            assert read(symbols[name],'HHhhIHI')==(x1-x0,frame['height'],frame['xOffset']-x0,frame['yOffset'],
                (0xc00000+tile['packedByteOffset'])*8,0x6000,symbols[f'ks_{actor}_primary_palette'])
            count+=1
        pose=symbols[f'ks_tr_{actor}_pose{frame["phase"]}']
        assert read(pose,'I'*(len(pointers)+1))==tuple(pointers+[0])
    frame=metadata['records'][actor][5];pointers=[]
    for column,tile in enumerate(frame['components']):
        pointer=symbols[f'ks_sw_{actor}_frame5_{column}'];pointers.append(pointer)
        x0,x1=tile['column']
        assert read(pointer,'HHhhIHI')==(x1-x0,frame['height'],frame['xOffset']-x0,frame['yOffset']-16,
            (0xc00000+tile['packedByteOffset'])*8,0x6000,symbols[f'ks_{actor}_primary_palette'])
        count+=1
    assert read(symbols[f'ks_sw_{actor}_pose5'],'III')==tuple(pointers+[0])
assert count==32
report=dict(linkedOwnRoots=4,nativeMultipartDescriptors=32,scorpionFinalAnchorDeltaY=16,compositeTerminationsVerified=True,
            generatedScriptBytesVerified=True,runtimeVerified=False,fullPortVerified=False)
(PORT/'generated_torso/TORSO_LINK_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
