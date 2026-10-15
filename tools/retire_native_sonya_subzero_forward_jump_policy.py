"""Whole failed-policy stop/preservation/retirement, actual forward-jump bound.

Keep every original protected losing-policy gate. Change only actual child,
parent, birth, capture and preceding qualified receipt. Never game acceptance.
"""
import inspect
import json
from pathlib import Path
import retire_native_sonya_subzero_ring_policy as original
import run_native_sonya_subzero_forward_jump_bound_campaign as capture

ROOT, need, sha = capture.ROOT, capture.need, capture.sha
GAME, PARENT = 5364, 34076
OUT = ROOT / 'audit_native_sonya_subzero_forward_jump_policy_preserved'
RETIRED = ROOT / 'audit_native_sonya_subzero_forward_jump_policy_retirement'


def scope():
    return dict(vars(original), __file__=__file__, capture=capture, GAME=GAME, PARENT=PARENT,
                OUT=OUT, RETIRED=RETIRED)


def stop():
    body = original.once(inspect.getsource(original.stop),
                         "identity['createdUnix'] == 1791703089.4675903",
                         "identity['createdUnix'] == 1791704540.427082")
    body = body.replace('Sonya Ring', 'Sonya forward jumpkick')
    bound = scope()
    exec(compile(body, __file__ + '::whole_original_identity_safe_losing_policy_stop', 'exec'), bound)
    return bound['stop']()


def prepare(ram):
    body = original.once(inspect.getsource(original.prepare),
        "audit_native_subzero_ring_preceding_campaign_checked/report.json",
        "audit_native_subzero_forward_jump_preceding_campaign_checked/report.json")
    bound = scope()
    exec(compile(body, __file__ + '::whole_original_failed_transport_and_full_sources_preservation', 'exec'), bound)
    return bound['prepare'](ram)


def retire():
    bound = scope()
    exec(compile(inspect.getsource(original.retire), __file__ + '::whole_original_exact_retirement', 'exec'), bound)
    return bound['retire']()


if __name__ == '__main__':
    import sys
    {'stop':stop, 'retire':retire}[sys.argv[1]]()
