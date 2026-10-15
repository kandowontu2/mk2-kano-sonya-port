"""Preserve preflight inspection failure; read the actual defining factory.

No native game was launched by the failed preflight. Keep the whole new
walk/jump/controller/health/display/audio contract; only source retrieval changes.
"""
import json
from pathlib import Path
import capture_native_selector_sonya_cpu_air_approach as original

failure_path=original.OUT/'failure.json'
failed=json.loads(failure_path.read_text())
original.need(not failed['passed'] and failed['error']=="OSError('lineno is out of bounds')" and
              not original.BASE.exists(), 'Actual original preflight failure, no native launch or replay')
source=Path(original.__file__).read_text()
for before,after in (
    ('inspect.getsource(previous.prepare)','inspect.getsource(previous.original.prepare)'),
    ("OUT=ROOT/'audit_native_selector_sonya_cpu_air_approach_capture_checked'",
     "OUT=ROOT/'audit_native_selector_sonya_cpu_air_approach_bound_capture_checked'"),
    ('for p in (Path(__file__),LUA,Path(snapshot.__file__),',
     'for p in (Path(__file__),Path(original.__file__),failure_path,LUA,Path(snapshot.__file__),')):
    original.need(source.count(before)==1, 'Only explicit defining-source/failure-preservation boundary')
    source=source.replace(before,after,1)
exec(compile(source,__file__+'::whole_air_trial_original_defining_source','exec'))
