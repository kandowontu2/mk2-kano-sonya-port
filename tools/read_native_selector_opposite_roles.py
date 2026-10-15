"""Original opposite-role game/host; no replay or persistent image files."""
import inspect
import read_native_selector_startup_pcm_frames as original


def run():
    source=inspect.getsource(original.run)
    for before,after in (
        ("('cpu_kano_p2_startup_pcm_boot608_confirm264_guard_wait_direct',)",
         "('human_sonya_natural_cpu_guard_until_close_jump_guard_boot605_confirm265',)"),
        ('all(0<=n<123 for n in indices)','all(0<=n<30 for n in indices)'),
        ('tools/read_native_selector_startup_pcm_frames_remote.py','tools/read_native_selector_opposite_roles_remote.py')):
        assert source.count(before)==1
        source=source.replace(before,after,1)
    scope=dict(vars(original),__file__=__file__)
    exec(compile(source,__file__+'::whole_original_exact_identity_reader','exec'),scope)
    return scope['run']()


if __name__=='__main__':run()
