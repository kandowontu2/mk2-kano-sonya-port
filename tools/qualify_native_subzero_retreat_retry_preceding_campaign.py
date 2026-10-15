"""Entire original eleven-fight/48-fault gate, current retreat handle bound."""
import inspect
import qualify_native_subzero_ring_preceding_campaign as original
import run_native_sonya_subzero_retreat_retry_bound_campaign as capture

OUT=capture.ROOT/'audit_native_subzero_retreat_retry_preceding_campaign_checked'


def run():
    once=capture.original.previous.original.previous.once
    body=inspect.getsource(original.run)
    body=once(body,"identity['ProcessId'] == 30832","identity['ProcessId'] == 33316")
    body=once(body,"identity['ParentProcessId'] == 14408","identity['ParentProcessId'] == 13692")
    body=once(body,"identity['createdUnix'] == 1791703089.4675903","identity['createdUnix'] == 1791706829.0646973")
    scope=dict(vars(original),__file__=__file__,capture=capture,OUT=OUT)
    exec(compile(body,__file__+'::whole_original_exact_live_handle_prefix_gate','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    run()
