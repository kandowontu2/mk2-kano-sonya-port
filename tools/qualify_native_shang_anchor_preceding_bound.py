"""Bind the inherited digest utility explicitly for the new capture module."""
import inspect
from types import SimpleNamespace
import qualify_native_shang_anchor_preceding_campaign as original

def run():
    capture=SimpleNamespace(**vars(original.capture))
    capture.corrected=original.capture.original.corrected
    scope=dict(vars(original),capture=capture,__file__=__file__)
    exec(compile(inspect.getsource(original.run),__file__+'::explicit_complete_capture_digest_binding','exec'),scope)
    return scope['run']()

if __name__=='__main__':run()
