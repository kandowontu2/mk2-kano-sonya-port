"""Read-only linked native head ABI verification; not runtime acceptance."""
import json
from pathlib import Path
import re
import struct
PORT=Path(__file__).resolve().parent
BUILD=PORT.parent/'baseline/mk2-rebuild-main/srcp'
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(BUILD/'MK2P.MAP').read_text())}
lanes=[b''.join((BUILD/f'rom/P12{p}.{lane}').read_bytes() for p in ('F8','FC')) for lane in (0,1)]
program=bytearray(0x100000)
program[::2]=lanes[0];program[1::2]=lanes[1]
def read(address,fmt):
    return struct.unpack_from('<'+fmt,program,(address-0xff800000)//8)
data=json.loads((PORT/'generated_heads/HEAD_DATA.json').read_text())
for actor in ('kano','sonya'):
    root=symbols[f'ks_{actor}_head']
    assert read(symbols[f'ks_{actor}_anitab1']+61*32,'I')==(root,)
    expected=[symbols[f'ks_hd_{actor}_frame{i}'] for i in range(7)]
    assert read(root,'9I')==tuple(expected+[1,root])
    for pointer,frame in zip(expected,data['records'][actor]):
        assert read(pointer,'HHhhIHI')==(frame['width'],frame['height'],frame['xOffset'],frame['yOffset'],
            (0xc00000+frame['packedByteOffset'])*8,0x6000,symbols[f'ks_{actor}_primary_palette'])
body=json.loads((PORT/'generated_decap/DECAP_DATA.json').read_text())
for actor in ('kano','sonya'):
    root=symbols[f'ks_{actor}_decapfall']
    assert read(symbols[f'ks_{actor}_anitab1']+60*32,'I')==(root,)
    poses=[symbols[f'ks_dc_{actor}_pose{i}'] for i in range(7)]
    grammar=[poses[i] if i is not None else 0 for i in (0,1,2,None,3,2,3,2,3,2,None,3,4,5,6,None)]
    assert read(root,'16I')==tuple(grammar)
    for phase,frame in enumerate(body['records'][actor]):
        pointer=symbols[f'ks_dc_{actor}_frame{phase}']
        assert read(poses[phase],'2I')==(pointer,0)
        assert read(pointer,'HHhhIHI')==(frame['width'],frame['height'],frame['xOffset'],frame['yOffset'],
            (0xc00000+frame['packedByteOffset'])*8,0x6000,symbols[f'ks_{actor}_primary_palette'])
drain=json.loads((PORT/'generated_drain/DRAIN_DATA.json').read_text())
for actor in ('kano','sonya'):
    root=symbols[f'ks_{actor}_drain_reaction']
    assert read(symbols[f'ks_{actor}_anitab1']+56*32,'I')==(root,)
    script=read(root,'17I')
    assert script[0]==4 and script[1]==((-19&65535)<<16|(-72&65535)) and script[3]==0
    assert [script[i] for i in (4,7,10,13)]==[4]*4 and script[-1]==0
    poses=[symbols[f'ks_dr_{actor}_pose{i}'] for i in range(3)]
    assert read(symbols[f'ks_{actor}_drain_shrink'],'9I')==tuple(poses+[0,poses[1],poses[0],poses[1],poses[2],0])
    for phase,frame in enumerate(drain['records'][actor]):
        pointer=symbols[f'ks_dr_{actor}_frame{phase}']
        assert read(poses[phase],'2I')==(pointer,0)
        assert read(pointer,'HHhhIHI')==(frame['width'],frame['height'],frame['xOffset'],frame['yOffset'],
            (0xc00000+frame['packedByteOffset'])*8,0x6000,symbols[f'ks_{actor}_primary_palette'])
from inventory_character_tables import source_tables
tables=source_tables((BUILD/'MKFX.ASM').read_text())
for name,count in (('drain_table',19),('alternate_suck_pals',19)):
    assert sum(len(r['values']) for r in tables[name]['rows'])==count
result=dict(linkedMainIndex61Verified=True,linkedMainIndex60Verified=True,linkedMainIndex56Verified=True,
            ownDrainShrinkLoops=2,drainTables19Rows=True,
            nativeThreeSectionBodyScripts=2,directImageHeaders=14,nativeSevenFrameLoops=2,
            runtimeVerified=False,fullPortVerified=False)
(PORT/'generated_heads/HEAD_LINK_QUALIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
