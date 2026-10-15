"""Preserve v1 failed trailing-blank line-count gate; use actual diff bounds."""
from pathlib import Path
p=Path(__file__).with_name('audit_current_cpu_feature_composition_20261015.py')
s=p.read_text()
old="len(inserts[1].splitlines())==1329"
assert s.count(old)==1
s=s.replace(old,"changes[1][4]-changes[1][3]==1329")
exec(compile(s,str(p), 'exec'))
