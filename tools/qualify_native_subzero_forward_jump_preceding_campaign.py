"""Whole original eleven-fight conservation gate, exact live successor bound.

Change only the capture/receipt paths and observed PID/birth/parent identity.
All original rows, health, wins, inputs,48 actual faults and finite scope stay.
"""
import inspect
from pathlib import Path
import qualify_native_subzero_ring_preceding_campaign as original
import run_native_sonya_subzero_forward_jump_bound_campaign as capture

OUT = capture.ROOT / 'audit_native_subzero_forward_jump_preceding_campaign_checked'


def run():
    body = inspect.getsource(original.run)
    body = capture.original.previous.once(body, "identity['ProcessId'] == 30832",
                                          "identity['ProcessId'] == 5364")
    body = capture.original.previous.once(body, "identity['ParentProcessId'] == 14408",
                                          "identity['ParentProcessId'] == 34076")
    body = capture.original.previous.once(body, "identity['createdUnix'] == 1791703089.4675903",
                                          "identity['createdUnix'] == 1791704540.427082")
    scope = dict(vars(original), __file__=__file__, capture=capture, OUT=OUT)
    exec(compile(body, __file__ + '::whole_original_exact_identity_bound_prefix', 'exec'), scope)
    return scope['run']()


if __name__ == '__main__':
    run()
