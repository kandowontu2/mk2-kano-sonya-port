"""Keep full native scanout trial; correct source-only helper export lookup."""
import json
import runpy
import traceback
from pathlib import Path
import run_native_tomb_transition_timing as previous

original=Path(__file__).with_name('run_native_tomb_transition_scanout.py')
failure=previous.ROOT/'audit_native_tomb_transition_scanout_source_alias_failure'
if not failure.exists():
    try:runpy.run_path(str(original),run_name='source_only_failed_original')
    except AttributeError as error:
        previous.need("has no attribute 'once'" in str(error) and not previous.previous.census.census(),
                      'Exact source-only exported helper error, no native game boot')
        failure.mkdir()
        (failure/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),nativeBootOccurred=False,
            inputHashes={str(original):previous.sha(original)},fullPortAcceptance=False),indent=2)+'\n')
    else:raise ValueError('Original helper export failure no longer reproduces')
retained=json.loads((failure/'failure.json').read_text())
previous.need(all(previous.sha(p)==h for p,h in retained['inputHashes'].items()),'Actual original source-only failure frozen')
source=original.read_text()
previous.need(source.count('previous.previous.once(')==3,'Exactly three original source-only lookup sites')
source=source.replace('previous.previous.once(','previous.once(')
source=previous.once(source,"scope=dict(__name__=__name__,__file__=__file__)",
    "source=previous.once(source,\"    scope['LUA']=tuple(scope['LUA'])+TIMING_LUA\","
    "\"    scope['LUA']=tuple(scope['LUA'])+TIMING_LUA+(ROOT/'tools/run_native_tomb_transition_scanout.py',"
    "ROOT/'audit_native_tomb_transition_scanout_source_alias_failure/failure.json')\")\n"
    "scope=dict(__name__=__name__,__file__=__file__)")
scope=dict(__name__=__name__,__file__=__file__)
exec(compile(source,__file__+'::whole_scanout_trial_exported_helper_lookup_only','exec'),scope)
globals().update({k:v for k,v in scope.items()if not k.startswith('__')})
