"""Retain complete transition trial; correct source-only transformation count."""
import json
import sys
import traceback
from pathlib import Path
import run_native_tomb_transition_rejoin as original

failure = original.ROOT / 'audit_native_tomb_transition_rejoin_source_count_failure'
if not failure.exists():
    try:
        original.extension_source_guard()
    except ValueError as error:
        original.need(str(error) == 'Exact declared whole-original source adaptations' and
                      not original.previous.census.census(), 'Exact preflight-only failure, no native trial')
        failure.mkdir()
        (failure/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),nativeBootOccurred=False,
            inputHashes={str(p):original.sha(p) for p in (Path(original.__file__),*original.LUA)},
            fullPortAcceptance=False),indent=2)+'\n')
old = json.loads((failure/'failure.json').read_text())
original.need(all(original.sha(p)==h for p,h in old['inputHashes'].items()),'Original source-only failure preserved')
source = Path(original.__file__).read_text()
source = original.once(source,"driver.count('once(') == 8","driver.count('once(') == 7")
scope = dict(__name__=__name__, __file__=__file__)
exec(compile(source,__file__+'::whole_original_with_actual_transformation_count','exec'),scope)
globals().update({k:v for k,v in scope.items() if not k.startswith('__')})
