"""Preserve first recovery failure; create the required initializer parent."""
import inspect
import json
from pathlib import Path

import recover_native_selector_models_after_host_exit as original

ROOT, RAM = original.ROOT, {}
OUT = ROOT / 'audit_native_selector_models_after_host_exit_parents'
failure = original.OUT / 'failure.json'
old = json.loads(failure.read_text())
original.sync.need(not old['passed'] and 'previous_initializer' in old['traceback']
                   and old['newNativeGames'] == 0, 'Exact first missing-parent failure retained')
source = inspect.getsource(original.recover)
before = "    wanted = startup.expected(OUT / 'independent_initializer')"
original.sync.need(source.count(before) == 1, 'One exact model-directory boundary')
source = source.replace(before, "    (OUT / 'independent_initializer').mkdir()\n" + before, 1)
scope = dict(vars(original), OUT=OUT, RAM=RAM, __file__=__file__)
exec(compile(source, __file__ + '::original_models_with_existing_parent', 'exec'), scope)
recover = scope['recover']

if __name__ == '__main__':
    try:
        report = recover()
        print(json.dumps(dict(passed=True, modelBytes=report['modelBytes'], newNativeGames=0)), flush=True)
    except Exception as error:
        if OUT.exists():
            original.sync.need(not (OUT / 'failure.json').exists(), 'Preserve successor failure')
            (OUT / 'failure.json').write_text(json.dumps(dict(passed=False, error=repr(error),
                traceback=original.traceback.format_exc(), nativeRuntimeAccepted=False,
                newNativeGames=0, fullPortAcceptance=False), indent=2) + '\n')
        print(json.dumps(dict(passed=False, error=repr(error), traceback=original.traceback.format_exc())), flush=True)
    original.code.interact(banner='Parent-bound recovery retained; no native game launched.', local=dict(RAM=RAM))
