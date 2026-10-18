"""Apply the reviewed scalar extension and record remaining native AI gaps."""
import hashlib
import json
from pathlib import Path
from drone_source import integrate,audit,SCALAR_EXTENSIONS
from inventory_character_tables import source_tables

PORT=Path(__file__).resolve().parent
source=PORT.parent/'baseline/mk2-rebuild-main/srcp/MKDRONE.ASM'
before=source.read_text()
after=integrate(before)
old=source_tables(before);new=source_tables(after)
for name in old:
    oldrows=[(row['type'],row['values']) for row in old[name]['rows']]
    newrows=[(row['type'],row['values']) for row in new[name]['rows']]
    assert newrows[:len(oldrows)]==oldrows,name
    if name not in SCALAR_EXTENSIONS:assert newrows==oldrows,name
source.write_text(after)
result=audit(after)
result['sourceSHA256']=hashlib.sha256(after.encode()).hexdigest().upper()
result['originalTypedRowsPreserved']=True
(PORT/'DRONE_TABLE_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
