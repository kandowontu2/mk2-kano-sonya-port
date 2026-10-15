"""Keep the failed Windows nested-path wrapper; bind a literal forward-slash path."""
import inspect
from pathlib import Path
import qualify_native_shang_anchor_terminal_bound as previous

def verify(ram):
    source=inspect.getsource(previous.verify)
    before='repr(previous.__file__)'
    assert source.count(before)==1
    source=source.replace(before,'repr(Path(previous.__file__).as_posix())',1)
    scope=dict(vars(previous),Path=Path,__file__=__file__)
    exec(compile(source,__file__+'::literal_forward_slash_diagnostic_path','exec'),scope)
    return scope['verify'](ram)
