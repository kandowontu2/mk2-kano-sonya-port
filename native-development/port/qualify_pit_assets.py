"""Linked native Pit data/table checks; not a live cinematic qualification."""
import json
import re
import struct
import zipfile
from pathlib import Path
from inventory_character_tables import source_tables
from qualify_bubble import HERE,SRC,sha

out=HERE/'generated_pit'
data=json.loads((out/'PIT_DATA.json').read_text())
assert sha(out/'KSPITART.ASM')==data['sourceSHA256']
assert (SRC/'KSPITART.ASM').read_bytes()==(out/'KSPITART.ASM').read_bytes()
assert 'No Errors,  No Warnings' in (SRC.parent/'PPITART.LOG').read_text()
with zipfile.ZipFile('C:/Users/kando/Downloads/mk2-rebuild-main.zip') as z:
    original=z.read('mk2-rebuild-main/src/MKFALL.ASM').decode('cp437')
old=source_tables(original);new=source_tables((SRC/'MKFALL.ASM').read_text())
def values(table):return [v for row in table['rows'] for v in row['values']]
for label in ['ochar_fall_coor','ochar_pit_falls']:
    assert len(values(old[label]))==12 and len(values(new[label]))==19
    assert values(new[label])[:12]==values(old[label])
assert values(new['ochar_pit_falls'])[17:]==['ks_pit_kano_sequence','ks_pit_sonya_sequence']
rom=bytearray(1048576)
for lane in [0,1]:rom[lane::2]=b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ['F8','FC'])
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
def read(address):return struct.unpack_from('<I',rom,(address-0xff800000)//8)[0]
pair=struct.pack('<II',symbols['ks_pit_kano_sequence'],symbols['ks_pit_sonya_sequence'])
assert rom.count(pair)==1
packed=(out/'fighter_ui_finish_pit_graphics.bin').read_bytes()
prefix=(HERE/'generated_friendship/fighter_ui_finish_friend_graphics.bin').read_bytes()
assert packed[:len(prefix)]==prefix and sha(HERE/'generated_friendship/fighter_ui_finish_friend_graphics.bin')==data['prefixSHA256']
region=bytearray(0x600000)
for bank,size in [(0,0x100000),(1,0x80000)]:
    for lane in range(4):
        chip=121-bank*4-lane;name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
        raw=(out/name).read_bytes();assert len(raw)==size and sha(out/name)==data['sockets'][name]
        start=bank*0x400000+lane;region[start:start+size*4:4]=raw
assert region==packed+bytes(0x600000-len(packed))
for name,record in data['records'].items():
    sequence=symbols[f'ks_pit_{name}_sequence']
    words=[read(sequence+i*32) for i in range(10)]
    assert words[5:8]==[1,sequence,0] and words[-1]==0
    groups=words[:5]+[words[8]];assert len(set(groups))==6
    assert record['frames'][-1]['height']==131
    for group,frame in zip(groups,record['frames']):
        descriptor=read(group);assert read(group+32)==0
        values_=struct.unpack_from('<4hIH',rom,(descriptor-0xff800000)//8)
        assert values_==(frame['width'],frame['height'],frame['xOffset'],frame['yOffset'],
                         (0xc00000+frame['packedByteOffset'])*8,0x6000)
        assert read(descriptor+112)==symbols[f'ks_{name}_primary_palette']
        size=(frame['width']*frame['height']*6+7)//8;start=frame['packedByteOffset']
        import hashlib
        assert hashlib.sha256(packed[start:start+size]).hexdigest().upper()==frame['compressedSHA256']
report=dict(scope='native data-only Pit assembly/link, twelve own descriptors, nineteen-row tables and socket reconstruction',
            sourceKind=data['sourceKind'],originalTwelveRowsPreserved=True,ownFrames=12,
            appendedBytes=data['appendedBytes'],oldExecutableCodeImported=False,
            visualAcceptance=False,runtimeVerified=False,releaseReady=False)
paths=[out/'PIT_DATA.json',out/'KSPITART.ASM',SRC/'KSPITART.OBJ',SRC/'MKFALL.ASM',SRC/'MK2P.OUT',SRC/'MK2P.MAP',
       SRC.parent/'PPITART.LOG',HERE/'recover_pit_art.py',HERE/'pit_source.py',HERE/'prepare_game_candidate.py',Path(__file__)]
paths += [HERE/'build_pit_assets.py',HERE/'PIT_SOURCE_ROUNDTRIP.json',HERE/'assets/pit/PIT_SOURCE.json']
paths += sorted((HERE/'assets/pit').glob('*.pgm'))
report['pins']={str(p):sha(p) for p in paths}
(out/'qualification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='pins'},indent=2))
