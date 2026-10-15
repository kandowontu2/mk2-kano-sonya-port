"""Same complete controller after actual original RAM retirement; no -i REPL."""
import code
import inspect
import json
import traceback
from pathlib import Path
import capture_native_paired_stumble_raiden_guard as failed

ROOT, need, sha = failed.ROOT, failed.need, failed.sha
OUT = ROOT / 'audit_native_paired_stumble_raiden_guard_ready'
OLD_INIT = ROOT / 'audit_native_paired_stumble_raiden_guard_ready_previous_initializer'
INIT = ROOT / 'audit_native_paired_stumble_raiden_guard_ready_initializer'
SOURCE = ROOT / 'audit_native_paired_stumble_raiden_guard_ready_source'
RAM = {}


def run():
    predecessor = ROOT / 'audit_native_paired_stumble_raiden_guard_preflight_failure/failure.json'
    need(predecessor.exists() and not json.loads(predecessor.read_text())['nativeGameStarted'],
         'Original preflight-only failure preserved, not a gameplay replay')
    scope = dict(vars(failed),__file__=__file__,OUT=OUT,OLD_INIT=OLD_INIT,INIT=INIT,SOURCE=SOURCE,RAM=RAM,
                 failed_source=failed.__file__,predecessor=predecessor)
    guard = inspect.getsource(failed.source_guard)
    before = 'paths = [Path(__file__),Path(prior.__file__),accepted_path,retired_path,failed_path,'
    after = 'paths = [Path(__file__),Path(failed_source),predecessor,Path(prior.__file__),accepted_path,retired_path,failed_path,'
    need(guard.count(before) == 1, 'Whole original physical source gate and failed-predecessor binding')
    exec(compile(guard.replace(before,after),__file__+'::whole_original_source_guard','exec'),scope)
    exec(compile(inspect.getsource(failed.run),__file__+'::whole_original_repaired_physical_campaign','exec'),scope)
    return scope['run']()


if __name__ == '__main__':
    try:
        captured = run()
    except Exception as error:
        folder = OUT if OUT.exists() else (INIT if INIT.exists() else SOURCE)
        if folder.exists():
            path = folder / 'current_capture_failure.json'; need(not path.exists(),'Preserve actual original failure')
            path.write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
        print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc())),flush=True)
    code.interact(banner='Same actual Raiden guard/leg run; full goal remains open.',local=dict(RAM=RAM))
