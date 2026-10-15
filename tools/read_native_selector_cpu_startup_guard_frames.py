"""Passive viewer for the original terminal guard-from-start native game."""
import inspect
import read_native_selector_cpu_guard_frames as prior


def run():
    source=inspect.getsource(prior.run)
    for before,after in(
        ('cpu_kano_p2_guard_hold_confirm265','cpu_kano_p2_guard_from_start_confirm265'),
        ('tools/read_native_selector_cpu_guard_frames_remote.py',
         'tools/read_native_selector_cpu_startup_guard_frames_remote.py')):
        assert source.count(before)==1;source=source.replace(before,after,1)
    namespace=dict(vars(prior),__file__=__file__)
    exec(compile(source,__file__+'::whole_original_retained_host_reader_startup_profile','exec'),namespace)
    return namespace['run']()


if __name__=='__main__':run()
