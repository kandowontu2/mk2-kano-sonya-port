"""Bind the original verifier module explicitly; retain the failed wrapper."""
import inspect
import qualify_native_shang_anchor_terminal as previous

def verify(ram):
    source=inspect.getsource(previous.verify)
    before='scope=dict(vars(original),capture=capture,OUT=OUT,__file__=__file__)'
    assert source.count(before)==1
    source=source.replace(before,'scope=dict(vars(original),original=original,capture=capture,OUT=OUT,__file__=__file__)')
    before='Path(capture.__file__),Path(original.__file__),prior_path'
    assert source.count(before)==1
    source=source.replace(before,'Path(capture.__file__),Path(original.__file__),Path('+repr(previous.__file__)+'),prior_path')
    scope=dict(vars(previous),__file__=__file__)
    exec(compile(source,__file__+'::explicit_original_verifier_module','exec'),scope)
    return scope['verify'](ram)
