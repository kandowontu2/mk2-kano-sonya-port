"""Keep the UI graphics model in the same verified historical namespace."""
import inspect
import json
from pathlib import Path

import prepare_native_selector_lowkick_after_host_exit as prior

OUT = prior.ROOT / 'audit_native_selector_lowkick_after_host_exit_scoped_preflight'
BASE = prior.ROOT / 'audit_native_selector_lowkick_after_host_exit_scoped_ram'
STATE, RAM_CASES, NATIVE_HANDLES, COMPLETED, AUDIO = {}, {}, {}, [], {}
failed = json.loads((prior.OUT / 'failure.json').read_text())
assert not failed['passed'] and 'verify_native_split_blood_v1133.py' in failed['traceback']


def prepare(windows, recovered_scoped):
    source = inspect.getsource(prior.prepare)
    old = 'gfx = current.models.prior.native_base.ui.graphics.expected_gfx()'
    new = 'gfx = recovered_scoped(current.models.prior.native_base.ui.graphics).expected_gfx()'
    assert source.count(old) == 1, 'Only graphics model namespace binding changes'
    source = source.replace(old, new, 1)
    scope = dict(vars(prior), OUT=OUT, BASE=BASE, STATE=STATE, RAM_CASES=RAM_CASES,
                 NATIVE_HANDLES=NATIVE_HANDLES, COMPLETED=COMPLETED, AUDIO=AUDIO,
                 recovered_scoped=recovered_scoped, __file__=__file__)
    exec(compile(source, __file__ + '::original_preflight_same_verified_model_namespace', 'exec'), scope)
    result = scope['prepare'](windows)
    globals().update(SCOPE=scope.get('SCOPE'), DISPLAY=scope.get('DISPLAY'))
    return result
