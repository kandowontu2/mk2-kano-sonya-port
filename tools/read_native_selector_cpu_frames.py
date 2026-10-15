"""Read retained actual CPU rasters; bind exact original host/kernel identity."""
import inspect
import read_native_selector_special_frames as prior


def run():
    source=inspect.getsource(prior.run)
    changes=(("for p in('special','air')", "for p in('cpu','cpu_leg')"),
        ("tuple(f'{move}_p{side}'for move in('ball','knife','blade','choke','ring','square','bicycle','leg')for side in(1,2))",
         "('choke_cpu_kano_human_kano','leg_cpu_sonya_p2_human_sonya_p1_children_guard_wait')"),
        ("'tools/read_native_selector_special_frames_remote.py'", "'tools/read_native_selector_cpu_frames_remote.py'"))
    for before,after in changes:
        assert source.count(before)==1
        source=source.replace(before,after,1)
    scope=dict(vars(prior),__file__=__file__)
    exec(compile(source,__file__+'::entire_original_bounded_viewer_cpu_profile','exec'),scope)
    return scope['run']()


if __name__=='__main__':run()
