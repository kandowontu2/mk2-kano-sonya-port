"""Keep both actual preflight failures; bind the source module without collision."""
import json
from pathlib import Path
import capture_native_selector_sonya_cpu_air_approach as source_capture
import capture_native_selector_sonya_cpu_air_approach_bound as prior_bound

first_failure=source_capture.OUT/'failure.json'
second_failure=prior_bound.OUT/'failure.json'
for path,error in ((first_failure,"OSError('lineno is out of bounds')"),
                   (second_failure,"AttributeError(\"'dict' object has no attribute '__file__'\")")):
    failed=json.loads(path.read_text())
    source_capture.need(not failed['passed'] and failed['error']==error,
                        'Both actual preflight failures preserved')
source_capture.need(not source_capture.BASE.exists(), 'Neither failed preflight launched a native game')
source=Path(source_capture.__file__).read_text()
for before,after in (
    ('inspect.getsource(previous.prepare)','inspect.getsource(previous.original.prepare)'),
    ("OUT=ROOT/'audit_native_selector_sonya_cpu_air_approach_capture_checked'",
     "OUT=ROOT/'audit_native_selector_sonya_cpu_air_approach_ready_capture_checked'"),
    ('for p in (Path(__file__),LUA,Path(snapshot.__file__),',
     'for p in (Path(__file__),Path(source_capture.__file__),Path(prior_bound.__file__),first_failure,second_failure,LUA,Path(snapshot.__file__),')):
    source_capture.need(source.count(before)==1, 'Only defining-source and noncolliding input pin boundaries')
    source=source.replace(before,after,1)
exec(compile(source,__file__+'::whole_original_air_trial_preflight_alias_bound','exec'))
