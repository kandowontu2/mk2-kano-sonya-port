"""Recover independent current models after confirmed original host exit.

No native game or completed matrix is replayed. Keep recovered models in
this new host's RAM; persist only bounded provenance and failure metadata.
"""
import code
import json
import traceback
from pathlib import Path

import verify_native_selector_layers_startup as startup
import verify_native_source_sync as sync

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'audit_native_selector_models_after_host_exit'
RAM = {}


def recover():
    sync.need(not OUT.exists(), 'Fresh recovery evidence; preserve all previous results')
    sync.need(not startup.initial.identity.census(), 'No native game live before model recovery')
    OUT.mkdir()
    source = sync.verify()
    wanted = startup.expected(OUT / 'independent_initializer')
    old = json.loads((startup.OUT / 'report.json').read_text())
    observed = {k: startup.initial.digest(v) for k, v in wanted.items()}
    sync.need(observed == old['actualWindowHashes'], 'Recovered independent models match all current initialized windows')
    RAM.update(wanted)
    report = dict(passed=True, sourceOnlyAccepted=True, nativeRuntimeAccepted=False,
                  goalStatus='active', fullPortAcceptance=False,
                  reason='Original host38752 and terminal26156 confirmed absent; fresh model recovery, not timeout replay',
                  expectedWindowHashes=observed, modelBytes={k: len(v) for k, v in wanted.items()},
                  currentSourceSync=source, newNativeGames=0, newBuilds=0,
                  newROMCopies=0, newRawMedia=0, newZIPs=0, latestPlayableChanged=False,
                  inputHashes={str(Path(__file__).resolve()): sync.sha(__file__),
                               str(startup.OUT / 'report.json'): sync.sha(startup.OUT / 'report.json')})
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    try:
        report = recover()
        print(json.dumps(dict(passed=True, modelBytes=report['modelBytes'], newNativeGames=0)), flush=True)
    except Exception as error:
        if OUT.exists():
            failure = OUT / 'failure.json'
            sync.need(not failure.exists(), 'Preserve original model-recovery failure')
            failure.write_text(json.dumps(dict(passed=False, error=repr(error), traceback=traceback.format_exc(),
                                               nativeRuntimeAccepted=False, newNativeGames=0,
                                               fullPortAcceptance=False), indent=2) + '\n')
        print(json.dumps(dict(passed=False, error=repr(error), traceback=traceback.format_exc())), flush=True)
    code.interact(banner='Recovered models/failure retained; no game was launched.', local=dict(RAM=RAM))
