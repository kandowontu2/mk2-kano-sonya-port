"""Preserve diagnostic __file__ rejection; same full original RAM reader."""
import inspect
import read_native_selector_opposite_roles as previous


def run():
    source=inspect.getsource(previous.run)
    before='tools/read_native_selector_opposite_roles_remote.py'
    assert source.count(before)==1
    scope=dict(vars(previous),__file__=__file__)
    exec(compile(source.replace(before,'tools/read_native_selector_opposite_roles_remote_bound.py',1),
        __file__+'::whole_original_reader_explicit_remote_path','exec'),scope)
    return scope['run']()


if __name__=='__main__':run()
