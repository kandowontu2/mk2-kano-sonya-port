"""Native CPU source/linked-dispatch checks; not an AI gameplay qualification."""
import hashlib
import json
from pathlib import Path
import re
import struct
import zipfile
from drone_source import DISPATCH_EXTENSIONS,DISPATCH_TABLES,audit
from inventory_character_tables import source_tables

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline/mk2-rebuild-main'
text=(BASE/'srcp/MKDRONE.ASM').read_text()
with zipfile.ZipFile('C:/Users/kando/Downloads/mk2-rebuild-main.zip') as archive:
    old=source_tables(archive.read('mk2-rebuild-main/src/MKDRONE.ASM').decode('cp437').replace('\r\n','\n'))
tables=source_tables(text)
symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(BASE/'srcp/MK2P.MAP').read_text())}
program=bytearray(0x100000)
for lane in (0,1):
    program[lane::2]=b''.join((BASE/f'srcp/rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC'))
def values(table):return [v for row in table['rows'] for v in row['values']]
def read(address,kind):return struct.unpack_from('<H' if kind=='word' else '<I',program,(address-0xff800000)//8)[0]
for name,extra in DISPATCH_EXTENSIONS.items():
    original=values(old[name]);current=values(tables[name])
    assert len(original)==17 and current==original+list(extra),name
    kind=tables[name]['rows'][0]['type'];stride=16 if kind=='word' else 32
    for i,target in enumerate(extra,17):
        if target in symbols:expected=symbols[target]
        elif target in original:expected=read(symbols[name]+stride*original.index(target),kind)
        else:expected=int(target)&(65535 if kind=='word' else 0xffffffff)
        assert read(symbols[name]+stride*i,kind)==expected,(name,i,target)
name='ochar_fatality_distances'
assert values(tables[name])[:24]==values(old[name])
expected=[0,0,0,0,0xa0,0x50,0xa0,0x50,0x4a,0x4a,0x40,0xc0,0xc0,0xe0]
assert len(values(tables[name]))==38
assert [read(symbols[name]+16*i,'word') for i in range(24,38)]==expected
ai=(PORT/'asm/KSAI.ASM').read_bytes()
assert ai==(BASE/'srcp/KSAI.ASM').read_bytes()
assert all(name in ai.decode() for name in ('ks_kano_ball','ks_kano_blade','ks_kano_choke','ks_kano_knife','ks_sonya_leg','ks_sonya_bike','ks_sonya_ring','ks_sonya_square'))
result=audit(text)
assert result['allListedTablesCoverAddedIDs']
result.update(originalDispatchRowsPreserved=True,linkedAddedDispatchVerified=True,
              ownAISourceSHA256=hashlib.sha256(ai).hexdigest().upper(),
              programSHA256=hashlib.sha256(program).hexdigest().upper())
(PORT/'DRONE_TABLE_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'listedTables':len(result['tables']),'linkedAddedDispatchVerified':True,'cpuGameplayVerified':False,'fullPortVerified':False}))
