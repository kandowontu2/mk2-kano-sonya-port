"""Same exact retained host, actual terminal walk-in game's RAM-only rasters."""
import inspect
import read_native_selector_startup_pcm_frames as original


def run():
    source=inspect.getsource(original.run)
    for before,after in (
        ("('cpu_kano_p2_startup_pcm_boot608_confirm264_guard_wait_direct',)",
         "('human_sonya_natural_kano_cpu_walkin_jump_guard_boot605_confirm265',)"),
        ('all(0<=n<123 for n in indices)','all(0<=n<256 for n in indices)'),
        ('tools/read_native_selector_startup_pcm_frames_remote.py','tools/read_native_selector_sonya_walkin_frames_remote.py')):
        assert source.count(before)==1
        source=source.replace(before,after,1)
    scope=dict(vars(original),__file__=__file__)
    exec(compile(source,__file__+'::same_native_host_reader_actual_walkin','exec'),scope)
    return scope['run']()


if __name__=='__main__':run()
