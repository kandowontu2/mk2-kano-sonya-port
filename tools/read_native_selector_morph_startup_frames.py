"""Read original terminal46572 images from exact retained native capture host."""
import inspect
import read_native_selector_startup_pcm_frames as original


def run():
    source = inspect.getsource(original.run)
    changes = (
        ("('cpu_kano_p2_startup_pcm_boot608_confirm264_guard_wait_direct',)", "('ball_p1',)"),
        ('all(0<=n<123 for n in indices)', 'all(0<=n<64 for n in indices)'),
        ('tools/read_native_selector_startup_pcm_frames_remote.py', 'tools/read_native_selector_morph_startup_frames_remote.py'),
    )
    # original.run is itself a declared adapter of the actual native host reader.
    # Apply these replacements to its stored adapter source before compilation.
    for before, after in changes:
        assert source.count(before) == 1
        source = source.replace(before, after, 1)
    scope = dict(vars(original), __file__=__file__)
    exec(compile(source, __file__+'::same_exact_host_original_morph_images', 'exec'), scope)
    return scope['run']()


if __name__ == '__main__': run()
