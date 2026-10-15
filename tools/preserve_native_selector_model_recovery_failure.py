"""Preserve the actual retained console exception before any successor work."""
import json
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def preserve():
    error = sys.last_exc
    need = ROOT / 'audit_native_selector_models_after_host_exit_parents/failure.json'
    assert not need.exists(), 'Preserve actual failure once'
    assert isinstance(error, AssertionError), 'Actual historical source-pin assertion, not inferred failure'
    text = ''.join(traceback.format_exception(error))
    assert 'verify_native_split_blood_v1133.py' in text
    value = dict(passed=False, error=repr(error), traceback=text,
                 nativeRuntimeAccepted=False, newNativeGames=0, fullPortAcceptance=False)
    need.write_text(json.dumps(value, indent=2) + '\n')
    return dict(preserved=True, path=str(need), newNativeGames=0)
