"""Read original Sonya-choice-game RAM; exact original live host binding."""
import inspect
import read_native_selector_startup_pcm_frames as original

def run():
    source = inspect.getsource(original.run)
    changes = (
        ("('cpu_kano_p2_startup_pcm_boot608_confirm264_guard_wait_direct',)",
         "('human_kano_cpu_natural_guard_until_close_neutral_boot608_confirm264',)"),
        ('all(0<=n<123 for n in indices)', 'all(0<=n<89 for n in indices)'),
        ('tools/read_native_selector_startup_pcm_frames_remote.py',
         'tools/read_native_selector_sonya_choices_frames_remote.py'),
    )
    for before, after in changes:
        assert source.count(before) == 1
        source = source.replace(before, after, 1)
    scope = dict(vars(original), __file__=__file__)
    exec(compile(source, __file__ + '::whole_original_bound_reader', 'exec'), scope)
    return scope['run']()

if __name__ == '__main__':
    run()
