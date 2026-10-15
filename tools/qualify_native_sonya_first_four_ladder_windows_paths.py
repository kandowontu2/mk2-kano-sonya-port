"""Same complete finite qualification; forward-slash literal Windows pins."""
import inspect
import json
from pathlib import Path
import qualify_native_sonya_first_four_ladder_bound_inputs as bounded

ROOT,need,sha=bounded.ROOT,bounded.need,bounded.sha
OUT=ROOT/'audit_native_sonya_first_four_ladder_windows_paths_checked'


def run():
    original_failure=bounded.OUT/'failure.json'
    need(original_failure.exists() and 'unicodeescape' in json.loads(original_failure.read_text())['error'],
         'Actual Windows literal-path compilation failure preserved')
    source=inspect.getsource(bounded.run)
    first=source.index("    need(previous.OUT.exists()")
    last=source.index('    source=inspect.getsource(previous.run)',first)
    source=source[:first]+"    need(failed.exists() and not json.loads(failed.read_text())['passed'], 'Actual original pin-scope failure remains frozen')\n"+source[last:]
    before="repr(str(p))"
    need(source.count(before)==1, 'Only embedded Windows file literal slash representation changes')
    source=source.replace(before,'repr(p.as_posix())')
    before='files=[Path(previous.__file__).resolve(),failed,'
    after='files=[Path(bounded.__file__).resolve(),original_failure,Path(previous.__file__).resolve(),failed,'
    need(source.count(before)==1, 'Actual original bounded-input checker and path failure also pinned')
    source=source.replace(before,after)
    scope=dict(vars(bounded),__file__=__file__,OUT=OUT,bounded=bounded,original_failure=original_failure)
    exec(compile(source,__file__+'::whole_original_progression_health_refill_and_fault_suite','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    try: run()
    except Exception as error:
        need(not OUT.exists(),'Preserve actual Windows-path qualification outcome')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),fullPortAcceptance=False),indent=2)+'\n')
        raise
