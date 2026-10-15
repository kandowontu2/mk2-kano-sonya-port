"""Original retirement checks after both actual Python REPLs are closed.

The first retirement check correctly rejected the still-live '-i' fallback
REPL. The next collector then stopped in preflight; neither started a game.
"""
import json
from pathlib import Path
import retire_native_paired_stumble_handoff as prior


def run():
    folder = prior.ROOT / 'audit_native_paired_stumble_raiden_guard_preflight_failure'
    prior.need(not folder.exists(), 'Preserve original host-lifecycle/preflight failure exactly once')
    failed_script = prior.ROOT / 'tools/capture_native_paired_stumble_raiden_guard.py'
    folder.mkdir()
    (folder / 'failure.json').write_text(json.dumps(dict(passed=False,
        phase='collector_preflight', nativeGameStarted=False, originalPreflightRAMParent=183740,
        originalReviewedRAMParent=64112, originalReviewedNativeGame=129056,
        error='Required retirement receipt did not yet exist because Python -i kept a second REPL alive.',
        bothOriginalParentsNowActuallyRetired=True,
        inputHashes={str(failed_script):prior.sha(failed_script), str(Path(__file__).resolve()):prior.sha(__file__)},
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
    prior.retire()


if __name__ == '__main__':
    run()
