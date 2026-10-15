"""Complete native progression/refill/fault suite with explicit pin paths.

The predecessor completed its positive/negative checks but could not write
its receipt because injected pin variables were outside the compiled scope.
Preserve that host failure; no new game replay or health-data changes.
"""
import inspect
import json
from pathlib import Path
import qualify_native_sonya_first_four_ladder_health_stores as previous

ROOT, need, sha = previous.ROOT, previous.need, previous.sha
OUT=ROOT/'audit_native_sonya_first_four_ladder_bound_inputs_checked'


def run():
    failed=previous.OUT/'failure.json'
    need(previous.OUT.exists() and not any(previous.OUT.iterdir()), 'Actual empty failed receipt directory, not an existing accepted report')
    failed.write_text(json.dumps(dict(passed=False,phase='report_input_hash_binding',error="NameError: name 'this_terminal' is not defined",
        originalPositiveAndFaultChecksReachedReportPhase=True,nativeGameplayAccepted=False,
        originalExecutedCheckerSHA256=sha(previous.__file__),fullPortAcceptance=False),indent=2)+'\n')
    source=inspect.getsource(previous.run)
    old='new="for p in (this_terminal,this_failed,Path(refill.__file__).resolve(),previous_failure,Path(prior.__file__).resolve(),failure,INIT/\'report.json\',ROOT/\'mk2/mk2-maincpu.bin\',Path(audio.__file__).resolve()):"'
    files=[Path(previous.__file__).resolve(),failed,Path(previous.terminal.__file__).resolve(),previous.terminal.OUT/'failure.json',
        Path(previous.terminal.refill.__file__).resolve(),previous.terminal.refill.OUT/'failure.json']
    literal="for p in ("+','.join('Path('+repr(str(p))+')' for p in files)+",Path(prior.__file__).resolve(),failure,INIT/'report.json',ROOT/'mk2/mk2-maincpu.bin',Path(audio.__file__).resolve()):"
    need(source.count(old)==1, 'Only scope-broken pin path expression corrected; entire positive/fault/native refill contracts unchanged')
    source=source.replace(old,'new='+repr(literal))
    scope=dict(vars(previous),__file__=__file__,OUT=OUT)
    exec(compile(source,__file__+'::whole_original_positive_refill_and_fault_contracts_bound_inputs','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    try: run()
    except Exception as error:
        need(not OUT.exists(),'Preserve actual final scope qualification failure')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),fullPortAcceptance=False),indent=2)+'\n')
        raise
