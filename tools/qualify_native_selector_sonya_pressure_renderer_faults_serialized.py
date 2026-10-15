"""Whole original fault suite; exact native result across JSON key boundary.

JSON converts the original body keys1/2/3/4 to strings. Keep the actual failed
comparison, serialize the entire restored original result before comparing,
and retain every native word/pixel/pass and counterexample assertion.
"""
import json
from pathlib import Path
from types import FunctionType
import qualify_native_selector_sonya_pressure_renderer_faults_body as body

ROOT,need,sha=body.ROOT,body.need,body.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_renderer_faults_serialized_checked'
FAILURE=body.OUT/'failure.json'
need(json.loads(FAILURE.read_text())['error']==
     "ValueError('Every original whole1746-pass positive restored byte-for-byte after actual renderer faults')",
     'Actual original int-versus-JSON-string body-key failure preserved')
source=body.source
for before,after in (
    ("need(restored==baseline['completeActualPassReplay']",
     "need(json.loads(json.dumps(restored))==baseline['completeActualPassReplay']"),
    ('Path(__file__),Path(original.__file__),FAILURE,parent.OUT,',
     'Path(__file__),Path(body.__file__),FAILURE,Path(original.__file__),body.FAILURE,parent.OUT,'),
    ('originalOpeningBodyContextFailurePreserved=True,',
     'originalOpeningBodyContextFailurePreserved=True,originalJSONBodyKeyFailurePreserved=True,')):
    need(source.count(before)==1,'Only complete whole-result JSON representation/failure provenance boundary')
    source=source.replace(before,after,1)
scope=dict(body.scope,OUT=OUT,__file__=__file__,body=body,FAILURE=FAILURE)
exec(compile(source,__file__+'::entire_native_positive_exact_JSON_representation','exec'),scope)
execute=scope['execute']
safe_execute=FunctionType(body.original.safe_execute.__code__,dict(scope,execute=execute),
                          body.original.safe_execute.__name__,body.original.safe_execute.__defaults__)
