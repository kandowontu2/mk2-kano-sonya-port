"""Passive original first-round capture viewer; no new game/media copies."""
import inspect
import read_native_selector_cpu_guard_frames as prior


def run():
    source=inspect.getsource(prior.run)
    for before,after in(
        ('cpu_kano_p2_guard_hold_confirm265','cpu_kano_p2_first_round_forward_guard_hold_confirm264'),
        ('tools/read_native_selector_cpu_guard_frames_remote.py','tools/read_native_selector_cpu_first_round_frames_remote.py')):
        assert source.count(before)==1;source=source.replace(before,after,1)
    namespace=dict(vars(prior),__file__=__file__)
    exec(compile(source,__file__+'::whole_bound_original_first_round_viewer','exec'),namespace)
    return namespace['run']()


if __name__=='__main__':run()
