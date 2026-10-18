"""Native table coverage/source-preservation proof, not AI gameplay acceptance."""
import json
import re
import struct
import zipfile
from pathlib import Path
from inventory_character_tables import source_tables
from qualify_bubble import HERE,SRC,sha

original_zip=Path('C:/Users/kando/Downloads/mk2-rebuild-main.zip')
with zipfile.ZipFile(original_zip) as z:
    original=z.read('mk2-rebuild-main/src/MKFRIEND.ASM').decode('cp437')
current=(SRC/'MKFRIEND.ASM').read_text()
old=source_tables(original);new=source_tables(current)
def values(table):return [v for row in table['rows'] for v in row['values']]
for label in ['ochar_friendship_combos','friendship_jumps']:
    before=values(old[label]);after=values(new[label])
    assert len(before)==12 and len(after)==19 and after[:12]==before
assert values(new['friendship_jumps'])[17:]==['ks_kano_friend','ks_sonya_friend']
assert values(new['ochar_friendship_combos'])[17:]==['ks_fs_kano_buttons','ks_fs_sonya_directions']
assert '        calla fs_check' in (SRC/'KSCMD.ASM').read_text()
assert (SRC/'KSCMD.ASM').read_bytes()==(HERE/'asm/KSCMD.ASM').read_bytes()
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
rom=bytearray(1048576)
for lane in [0,1]:rom[lane::2]=b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ['F8','FC'])
actions=struct.pack('<II',symbols['ks_kano_friend'],symbols['ks_sonya_friend'])
assert rom.count(actions)==1
kano=struct.pack('<7H',0x50,3,2,2,4,0,0)
# Switch codes come from the actual native constants, not assumptions.
equ=(SRC/'MAINEQU.ASM').read_text()
codes={k:int(v) for k,v in re.findall(r'^(sw_\w+)\s+\.set\s+(\d+)\b',equ,re.M)}
sonya=struct.pack('<13H',0x38,codes['sw_down'],codes['sw_left'],codes['sw_right'],codes['sw_left'],0,0,
                  codes['sw_down'],codes['sw_right'],codes['sw_left'],codes['sw_right'],0,0)
assert rom.count(kano)==rom.count(sonya)==1
command_pair=struct.pack('<II',0xff800000+rom.index(kano)*8,0xff800000+rom.index(sonya)*8)
assert rom.count(command_pair)==1
report=dict(scope='native nineteen-row tables, linked own command/action pointers, original twelve entries preserved',
            nativeFriendshipDispatchCoverage=True,originalEntriesPreserved=True,AIExecutionQualified=False,
            fullPortVerified=False,releaseReady=False)
paths=[SRC/'MKFRIEND.ASM',SRC/'KSCMD.ASM',SRC/'MK2P.OUT',SRC/'MK2P.MAP',
       HERE/'friendship_source.py',HERE/'prepare_game_candidate.py',Path(__file__)]
report['pins']={str(p):sha(p) for p in paths}
(HERE/'FRIENDSHIP_DISPATCH_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='pins'},indent=2))
