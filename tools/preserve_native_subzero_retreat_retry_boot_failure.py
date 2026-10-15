"""Whole original pre-game failure preservation, exact retreat-loader bound."""
import inspect
import preserve_native_subzero_forward_jump_boot_failure as original
import run_native_sonya_subzero_retreat_retry_campaign as capture

ROOT, need, sha = capture.ROOT, capture.need, capture.sha
OUT = ROOT/'audit_native_subzero_retreat_retry_boot_failure_preserved'
RETIRED = ROOT/'audit_native_subzero_retreat_retry_boot_failure_retired'
PARENT, GAME = 30444, 4744


def prepare(ram):
    body = inspect.getsource(original.prepare)
    body = capture.previous.original.previous.once(body,
        "identity['createdUnix'] == 1791704398.65547", "identity['createdUnix'] == 1791706553.9021301")
    body = capture.previous.original.previous.once(body,
        "attempt to call a nil value (global 'read')", "unexpected symbol near ']'")
    scope = dict(vars(original), __file__=__file__, original=capture, OUT=OUT, RETIRED=RETIRED,
                 PARENT=PARENT, GAME=GAME)
    exec(compile(body, __file__+'::whole_original_actual_pre_game_failure', 'exec'), scope)
    return scope['prepare'](ram)


def retire():
    scope = dict(vars(original), __file__=__file__, original=capture, OUT=OUT, RETIRED=RETIRED,
                 PARENT=PARENT, GAME=GAME)
    exec(compile(inspect.getsource(original.retire), __file__+'::whole_original_identity_retirement', 'exec'), scope)
    return scope['retire']()


if __name__=='__main__':
    retire()
