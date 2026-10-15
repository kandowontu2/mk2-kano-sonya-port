"""Whole passive Ring-diagnosis successor for the actually failed jump trial.

Same complete terminal scan and actual fields/damage/wins/losses. This tactic
uses ordinary jump/kick/uppercut/block buttons and has no custom move entries.
"""
import inspect
import diagnose_native_subzero_ring_loss as original
import run_native_sonya_subzero_forward_jump_bound_campaign as capture

OUT = capture.ROOT / 'audit_native_subzero_forward_jump_loss_diagnosed'


def run():
    body = inspect.getsource(original.run)
    body = capture.original.previous.once(body,
        'audit_native_sonya_subzero_ring_policy_preserved/report.json',
        'audit_native_sonya_subzero_forward_jump_policy_preserved/report.json')
    body = capture.original.previous.once(body,
        'audit_native_sonya_subzero_ring_policy_retirement/report.json',
        'audit_native_sonya_subzero_forward_jump_policy_retirement/report.json')
    body = capture.original.previous.once(body,
        "    assert activations and all(q['move'] == 'ring' and q['id'] == q['roster'] == '18' for q in activations)",
        "    assert not activations and counts['SPECIAL'] == 0, 'Actual physical jumpkick strategy has no custom special dispatch'\n"
        "    assert actions['512'] > 0 and decisions == {'native_forward_jumpkick_feedback': counts['RANGE_FIELD']}, 'Actual air-kick stores and whole original feedback decisions observed'")
    body = capture.original.previous.once(body, 'allActualNativeRingActivations=activations',
        'allActualNativeSpecialActivations=activations')
    before = "    print(json.dumps({k: report[k] for k in ('completeTargetRows', 'counts', 'decisionCounts',\n                                           'nativeHumanActionStores', 'nativeCPUActionStores', 'firstActualEvents')}, indent=2))"
    after = "    print(json.dumps({k: report[k] for k in ('completeTargetRows', 'counts', 'decisionCounts', 'nativeHumanActionStores', 'nativeCPUActionStores')}, indent=2))"
    body = capture.original.previous.once(body, before, after)
    scope = dict(vars(original), __file__=__file__, FOLDER=capture.OUT, OUT=OUT)
    exec(compile(body, __file__ + '::whole_original_complete_terminal_diagnosis_no_special_tactic', 'exec'), scope)
    return scope['run']()


if __name__ == '__main__':
    run()
