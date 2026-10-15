"""Fresh stock preflight: compare source bytes, not __main__ module identity.

Running4640 as __main__ and importing it by name creates two Python module
objects. Neither changes its bytes or native controls. Keep every old guard;
bind the generated source to the exact intended file/hash before boot.
"""
import inspect
from pathlib import Path
import qualify_stock_scorpion_secondary_native_scene_v4640 as original
source=inspect.getsource(original.main)
before="generated.__globals__['source']is sys.modules[__name__]"
after="Path(generated.__globals__['source'].__file__).resolve()==Path(original.__file__).resolve() and sha(generated.__globals__['source'].__file__)==sha(original.__file__)"
original.need(source.count(before)==1,'Only actual Python source-module identity guard corrected')
source=source.replace(before,after,1)
scope=dict(vars(original),__file__=__file__,original=original)
exec(compile(source,__file__+'::whole4640_source_bytes_not_module_alias_identity','exec'),scope)
if __name__=='__main__':scope['main']()
