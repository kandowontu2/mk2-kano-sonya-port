"""Same exact host reader on the three distinct remaining morph captures."""
import inspect
import read_native_selector_startup_pcm_frames as original


def run():
    source = inspect.getsource(original.run)
    for before,after in (
        ("('cpu_kano_p2_startup_pcm_boot608_confirm264_guard_wait_direct',)", "('square_p1','ball_p2','square_p2')"),
        ('all(0<=n<123 for n in indices)', 'all(0<=n<64 for n in indices)'),
        ('tools/read_native_selector_startup_pcm_frames_remote.py','tools/read_native_selector_morph_remaining_frames_remote.py')):
        assert source.count(before) == 1
        source = source.replace(before,after,1)
    scope = dict(vars(original),__file__=__file__)
    exec(compile(source,__file__+'::same_exact_host_remaining_original_morph_images','exec'),scope)
    return scope['run']()


if __name__ == '__main__': run()
