"""Verify linked native projectile root ABI and effect palette descriptor aliases."""
import json
from pathlib import Path
import re
import struct
from inventory_character_tables import source_tables
PORT=Path(__file__).resolve().parent;BUILD=PORT.parent/'baseline/mk2-rebuild-main/srcp'
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(BUILD/'MK2P.MAP').read_text())}
lanes=[b''.join((BUILD/f'rom/P12{p}.{i}').read_bytes() for p in ('F8','FC')) for i in (0,1)]
program=bytearray(0x100000);program[::2]=lanes[0];program[1::2]=lanes[1]
def read(a,fmt):return struct.unpack_from('<'+fmt,program,(a-0xff800000)//8)
def number(v):return int(v[:-1],16) if v.lower().endswith('h') else int(v)
metadata=json.loads((PORT/'generated_projectiles/PROJECTILE_ROOTS.json').read_text())
descriptors=0
for actor,effect in (('kano','knife'),('sonya','ring')):
    record=metadata['actors'][actor]
    for index,role in ((38,'release'),(39,'effect')):
        assert read(symbols[f'ks_{actor}_anitab1']+index*32,'I')==(symbols[f'ks_{actor}_projectile_{role}'],)
    art=source_tables((PORT/'generated_packed'/f'{actor.upper()}ART.ASM').read_text())
    for original,alias in record['descriptorAliases'].items():
        rows=art[original]['rows']
        dims=list(map(number,rows[0]['values']))
        assert read(symbols[alias],'HHhhIHI')==tuple(dims+[number(rows[1]['values'][0]),number(rows[2]['values'][0]),symbols[f'ks_{effect}_palette']])
        descriptors+=1
    for original,alias in record['compositeAliases'].items():
        frames=[v for row in art[original]['rows'] for v in row['values'] if v!='0']
        expected=[symbols[record['descriptorAliases'][frame]] for frame in frames]+[0]
        assert read(symbols[alias],'I'*len(expected))==tuple(expected)
    expected=[]
    for phase in ('intro','flight'):
        expected += [symbols[record['compositeAliases'][p]] for p in record[phase]]+[0]
    assert read(symbols[f'ks_{actor}_projectile_effect'],'I'*len(expected))==tuple(expected)
    root=symbols[f'ks_{actor}_projectile_release']
    if actor=='kano':
        expected=[symbols[p] for p in record['release']]+[0]
        assert read(root,'I'*len(expected))==tuple(expected)
    else:
        script=read(root,'10I')
        assert script[0]==6 and 0xff800000<=script[1]<=0xffffffff
        assert script[2:6]==tuple(symbols[p] for p in record['charge'])
        assert script[6:]==(6,symbols['player_normpal'],symbols[record['release'][0]],0)
assert descriptors==26
report=dict(ownNativeDispatchCellsVerified=4,effectPaletteDescriptorsVerified=26,
            twoTerminatedEffectPhasesPerActor=True,bodyReleaseAndChargeRestoreVerified=True,
            fullPortVerified=False)
(PORT/'generated_projectiles/PROJECTILE_ROOT_LINK_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
