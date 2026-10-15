"""Same terminal game's passive viewer with repaired exception quotation."""
import inspect
import read_native_selector_cpu_sonya_continuous_frames as prior


def run():
    source=inspect.getsource(prior.run)
    before='tools/read_native_selector_cpu_sonya_continuous_frames_remote.py'
    assert source.count(before)==1
    source=source.replace(before,'tools/read_native_selector_cpu_sonya_continuous_frames_remote_bound.py',1)
    namespace=dict(vars(prior),__file__=__file__)
    exec(compile(source,__file__+'::whole_passive_viewer_quote_bound','exec'),namespace)
    return namespace['run']()


if __name__=='__main__':run()
