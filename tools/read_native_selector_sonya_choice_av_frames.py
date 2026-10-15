"""Actual174 rasters from original Sonya-choice/audio game; no replay."""
import inspect
import read_native_selector_startup_pcm_frames as original

def run():
    source=inspect.getsource(original.run)
    for before,after in (
        ("('cpu_kano_p2_startup_pcm_boot608_confirm264_guard_wait_direct',)",
         "('natural_sonya_original_approach_jump_guard_boot608_confirm264',)"),
        ('all(0<=n<123 for n in indices)','all(0<=n<174 for n in indices)'),
        ('tools/read_native_selector_startup_pcm_frames_remote.py','tools/read_native_selector_sonya_choice_av_frames_remote.py')):
        assert source.count(before)==1
        source=source.replace(before,after,1)
    scope=dict(vars(original),__file__=__file__)
    exec(compile(source,__file__+'::whole_original_bound_reader','exec'),scope)
    return scope['run']()

if __name__=='__main__':run()
