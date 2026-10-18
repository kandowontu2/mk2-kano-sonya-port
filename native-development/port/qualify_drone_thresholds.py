"""Check five explicit scalar AI extensions in source and native linked ROM."""
import hashlib
import json
from pathlib import Path
import re
import struct
import zipfile
from drone_source import SCALAR_EXTENSIONS,DISPATCH_TABLES,audit
from inventory_character_tables import source_tables

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline/mk2-rebuild-main'
with zipfile.ZipFile('C:/Users/kando/Downloads/mk2-rebuild-main.zip') as archive:
    original=source_tables(archive.read('mk2-rebuild-main/src/MKDRONE.ASM').decode('cp437').replace('\r\n','\n'))
current=(BASE/'srcp/MKDRONE.ASM').read_text()
tables=source_tables(current)
symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(BASE/'srcp/MK2P.MAP').read_text())}
program=bytearray(0x100000)
for lane in (0,1):
    program[lane::2]=b''.join((BASE/f'srcp/rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC'))
def number(value):return int(value[:-1],16) if value.lower().endswith('h') else int(value)
for name,extra in SCALAR_EXTENSIONS.items():
    old=[v for row in original[name]['rows'] for v in row['values']]
    new=[v for row in tables[name]['rows'] for v in row['values']]
    assert len(old)==17 and new==old+list(extra),name
    offset=(symbols[name]-0xff800000)//8
    assert struct.unpack_from('<19H',program,offset)==tuple(map(number,new)),name
for name in original.keys() & tables.keys():
    if name not in SCALAR_EXTENSIONS and name not in DISPATCH_TABLES:
        assert [(r['type'],r['values']) for r in original[name]['rows']]==[(r['type'],r['values']) for r in tables[name]['rows']],name
result=audit(current)
result.update(scalarSourceAndROMVerified=True,originalTypedRowsPreserved=True,
              programSHA256=hashlib.sha256(program).hexdigest().upper())
(PORT/'DRONE_SCALAR_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'scalarSourceAndROMVerified':True,'extendedTables':len(SCALAR_EXTENSIONS),'cpuGameplayVerified':False,'fullPortVerified':False}))
