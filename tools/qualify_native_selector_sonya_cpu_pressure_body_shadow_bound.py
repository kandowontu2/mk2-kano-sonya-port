"""Original full body/shadow suite; map physical human Y to its actual vypos.

Preserve the rejected checker/result. The old pair schema calls human Y vypos,
while vy is CPU vertical velocity. No geometry, pose, floor or fault rule waived.
"""
import json
from pathlib import Path
import qualify_native_selector_sonya_cpu_pressure_body_shadow as original

original_source=Path(original.__file__)
original_failure=original.OUT/'failure.json'
need=original.need
need(json.loads(original_failure.read_text())['error']==
     "ValueError('Every actual final body/shadow source word equals independent next physical actor/Main field')",
     'Actual original physical-schema comparison rejection remains preserved')
source=original_source.read_text()
for before,after in (
    ("OUT=ROOT/'audit_native_selector_sonya_cpu_pressure_body_shadow_checked'",
     "OUT=ROOT/'audit_native_selector_sonya_cpu_pressure_body_shadow_bound_checked'"),
    ('==p[prefix+k]for k in','==p[\'vypos\' if s==1 and k==\'y\' else prefix+k]for k in'),
    ('Path(__file__),parent,Path(mechanics.__file__),',
     'Path(__file__),original_source,original_failure,parent,Path(mechanics.__file__),')):
    need(source.count(before)==1,'Only exact actual physical-coordinate column/source preservation boundary')
    source=source.replace(before,after,1)
exec(compile(source,str(original_source)+'::whole_original_model_actual_human_Y_column','exec'))
