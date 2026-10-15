"""Same original pre-failure two-stage prefix, bind actual terminal not live.

The original live-only qualification failed because this exact native process
had already stopped on real corruption. No replay or whole campaign success.
"""
import inspect
import json
import traceback
from pathlib import Path
import qualify_native_sonya_kano_leg_guard_prefix as original

ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_native_sonya_kano_leg_guard_terminal_prefix_checked'


def run():
    need(not OUT.exists(),'Fresh terminal-bound original two-stage prefix')
    failure=json.loads((original.OUT/'failure.json').read_text())
    need(not failure['passed'] and 'Exact original live PID/parent/path/birth/full command' in failure['error'],
         'Original live-only missing-handle failure preserved, not a replay trigger')
    source=inspect.getsource(original.run)
    before="need(actual==identity and actual['ParentProcessId']==PARENT,'Exact original live PID/parent/path/birth/full command')"
    after="""terminal=json.loads((folder/'native_terminal.json').read_text())
    metadata=json.loads((folder/'result.json').read_text())
    capture_failure=json.loads((folder/'current_capture_failure.json').read_text())
    need(actual is None and terminal['nativeExit']==0 and terminal['identity']==identity and
         identity['ProcessId']==GAME and identity['ParentProcessId']==PARENT and
         metadata['nativeCacheOverrunObserved'] and not capture_failure['passed'] and
         'No original cache writes into global state' in capture_failure['error'],
         'Exact original native naturally terminal on true later cache corruption; never replay')
    actual=identity"""
    edits=[(before,after),
           ("need(actual_after==actual,'Same original real live job after replay, never restarted')",
            "need(actual_after is None and json.loads((folder/'native_terminal.json').read_text())==terminal,'Same original terminal native remains absent; no replay')"),
           ('actualCampaignStillLive=True','actualCampaignStillLive=False'),
           ("nextAction='Continue observing the same original session7157/native176712/parent186024 to actual terminal. Never restart on an observation timeout.'",
            "laterCurrentCacheFailurePreserved=True,nextAction='Diagnose actual Raiden/Sonya native cache decode corruption at callback54865; preserve this finite earlier physical prefix only.'")]
    for before,after in edits:
        need(source.count(before)==1,'Exact whole original terminal-provenance adaptation')
        source=source.replace(before,after,1)
    scope=dict(vars(original),__file__=__file__,OUT=OUT)
    exec(compile(source,__file__+'::whole_original_terminal_bound_actual_prefix','exec'),scope)
    scope['run']()
    # No changes to the original function/state/input/ownership/fault algorithms.


if __name__=='__main__':
    try: run()
    except Exception as error:
        need(not OUT.exists(),'Preserve original terminal-prefix result');OUT.mkdir()
        (OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
            fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
        print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc())),flush=True)
