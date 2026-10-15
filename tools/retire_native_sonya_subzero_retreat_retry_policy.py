"""Preserve the actual failed retreat trial with the entire original stop gate.

Only capture, receipt and observed process identity change. A losing input
policy is not game acceptance or evidence permitting native rules changes.
"""
import inspect
import retire_native_sonya_subzero_ring_policy as original
import run_native_sonya_subzero_retreat_retry_bound_campaign as capture

ROOT, need, sha = capture.ROOT, capture.need, capture.sha
GAME, PARENT = 33316, 13692
OUT = ROOT / 'audit_native_sonya_subzero_retreat_retry_policy_preserved'
RETIRED = ROOT / 'audit_native_sonya_subzero_retreat_retry_policy_retirement'


def scope():
    return dict(vars(original), __file__=__file__, capture=capture, GAME=GAME,
                PARENT=PARENT, OUT=OUT, RETIRED=RETIRED)


def stop():
    body = original.once(inspect.getsource(original.stop),
                         "identity['createdUnix'] == 1791703089.4675903",
                         "identity['createdUnix'] == 1791706829.0646973")
    body = body.replace('Sonya Ring', 'Sonya early retreat retry')
    bound = scope()
    exec(compile(body, __file__ + '::whole_original_identity_safe_losing_stop', 'exec'), bound)
    return bound['stop']()


def prepare(ram):
    body = original.once(inspect.getsource(original.prepare),
        'audit_native_subzero_ring_preceding_campaign_checked/report.json',
        'audit_native_subzero_retreat_retry_preceding_campaign_checked/report.json')
    bound = scope()
    exec(compile(body, __file__ + '::whole_original_failed_transport_preservation', 'exec'), bound)
    return bound['prepare'](ram)


def retire():
    bound = scope()
    exec(compile(inspect.getsource(original.retire), __file__ + '::whole_original_exact_retirement', 'exec'), bound)
    return bound['retire']()


if __name__ == '__main__':
    import sys
    {'stop': stop, 'retire': retire}[sys.argv[1]]()
