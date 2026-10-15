"""Whole eleven-fight gate bound to the actual new guard-pressure process."""
import inspect
import qualify_native_subzero_ring_preceding_campaign as original
import run_native_sonya_subzero_guard_pressure_campaign as capture

OUT = capture.ROOT/'audit_native_subzero_guard_pressure_preceding_campaign_checked'


def run():
    body = inspect.getsource(original.run)
    body = capture.original.once(body,"identity['ProcessId'] == 30832","identity['ProcessId'] == 7268")
    body = capture.original.once(body,"identity['ParentProcessId'] == 14408","identity['ParentProcessId'] == 21628")
    body = capture.original.once(body,"identity['createdUnix'] == 1791703089.4675903","identity['createdUnix'] == 1791708051.8534794")
    scope = dict(vars(original),__file__=__file__,capture=capture,OUT=OUT)
    exec(compile(body,__file__+'::whole_original_exact_live_handle_prefix_gate','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    run()
