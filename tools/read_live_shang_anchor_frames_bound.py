"""Exact native birth identities and explicit remote diagnostic script binding."""
import inspect
from pathlib import Path
import read_live_shang_anchor_frames as original

def run():
    source=inspect.getsource(original.run)
    for before,after in (('1791725473.170991','1791725473.170992'),
                         ('1791725456.132396','1791725456.1323967')):
        assert source.count(before)==1
        source=source.replace(before,after,1)
    scope=dict(vars(original),REMOTE=original.ROOT/'tools/read_live_shang_anchor_frames_remote_bound.py',__file__=__file__)
    exec(compile(source,__file__+'::exact_census_identities_and_explicit_remote_path','exec'),scope)
    return scope['run']()

if __name__=='__main__':run()
