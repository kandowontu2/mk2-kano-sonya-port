"""Ground-throw construction is conserved, not part of inserted victim block."""
from pathlib import Path
p=Path(__file__).with_name('audit_current_cpu_feature_composition_20261015.py')
s=p.read_text()
for old,new in [("len(inserts[1].splitlines())==1329", "changes[1][4]-changes[1][3]==1329"),
                ("'ground_throw_lookup' in inserts[1]", "'PAIRED_STUMBLE_TABLE_END' in inserts[1]")]:
    assert s.count(old)==1
    s=s.replace(old,new)
exec(compile(s,str(p),'exec'))
