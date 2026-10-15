"""Preserve source-pin module/dict collision; complete original faults unchanged."""
import json
from pathlib import Path
from types import FunctionType
import qualify_native_selector_sonya_pressure_renderer_faults_serialized as serialized

ROOT,need,sha=serialized.ROOT,serialized.need,serialized.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_renderer_faults_bound_checked'
FAILURE=serialized.OUT/'failure.json'
need(json.loads(FAILURE.read_text())['error']==
     'AttributeError("\'dict\' object has no attribute \'__file__\'")',
     'Actual local body command collided with storage-source module alias; keep immutable rejection')
source=serialized.source
for before,after in (
    ('Path(__file__),Path(body.__file__),FAILURE,Path(original.__file__),body.FAILURE,parent.OUT,',
     'Path(__file__),Path(serialized.__file__),FAILURE,Path(body_module.__file__),serialized.FAILURE,Path(original.__file__),body_module.FAILURE,parent.OUT,'),
    ('originalJSONBodyKeyFailurePreserved=True,',
     'originalJSONBodyKeyFailurePreserved=True,originalStorageModuleAliasFailurePreserved=True,')):
    need(source.count(before)==1,'Only exact source-module alias and failed-source preservation boundary')
    source=source.replace(before,after,1)
scope=dict(serialized.scope,OUT=OUT,__file__=__file__,serialized=serialized,body_module=serialized.body,
           FAILURE=FAILURE,CONTEXT=None)
exec(compile(source,__file__+'::whole_native_faults_explicit_storage_module_alias','exec'),scope)
execute=scope['execute']
safe_execute=FunctionType(serialized.body.original.safe_execute.__code__,dict(scope,execute=execute),
    serialized.body.original.safe_execute.__name__,serialized.body.original.safe_execute.__defaults__)
