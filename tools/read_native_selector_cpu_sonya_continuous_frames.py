"""Exact retained original continuous-guard native frames, no game/media copy."""
import inspect
import read_native_selector_cpu_guard_frames as prior


def run():
    source=inspect.getsource(prior.run)
    for before,after in(
        ('cpu_kano_p2_guard_hold_confirm265','cpu_sonya_p2_continuous_guard_boot606_confirm264_bound'),
        ('tools/read_native_selector_cpu_guard_frames_remote.py','tools/read_native_selector_cpu_sonya_continuous_frames_remote.py')):
        assert source.count(before)==1;source=source.replace(before,after,1)
    namespace=dict(vars(prior),__file__=__file__)
    exec(compile(source,__file__+'::whole_original_bound_host_continuous_guard_reader','exec'),namespace)
    return namespace['run']()


if __name__=='__main__':run()
