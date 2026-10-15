"""Bound exact original retained host and callback-distinct CPU guard rasters."""
import inspect
import read_native_selector_special_frames as prior


def run():
    source=inspect.getsource(prior.run)
    changes=(("for p in('special','air')","for p in('guard',)"),
        ("tuple(f'{move}_p{side}'for move in('ball','knife','blade','choke','ring','square','bicycle','leg')for side in(1,2))",
         "('cpu_kano_p2_guard_hold_confirm265',)"),
        ("'tools/read_native_selector_special_frames_remote.py'",
         "'tools/read_native_selector_cpu_guard_frames_remote.py'"))
    for before,after in changes:
        assert source.count(before)==1;source=source.replace(before,after,1)
    # The original anchor reader has a bounded80-frame request limit. This
    # completed guard run has177 genuine callbacks; never alter their frame IDs.
    original=prior.original
    anchor=inspect.getsource(original.run)
    assert anchor.count('0<=n<80')==1
    anchor=anchor.replace('0<=n<80','0<=n<200',1)
    scope=dict(vars(original),__file__=__file__)
    exec(compile(anchor,__file__+'::bounded200_original_callback_reader','exec'),scope)
    proxy=type('OriginalReader',(),dict(vars(original),run=staticmethod(scope['run'])))
    namespace=dict(vars(prior),original=proxy,__file__=__file__)
    # prior.run obtains inspect.getsource(original.run); the actual source above
    # remains available through linecache under the synthetic filename.
    import linecache
    linecache.cache[__file__+'::bounded200_original_callback_reader']=(len(anchor),None,anchor.splitlines(True),__file__)
    exec(compile(source,__file__+'::whole_original_guard_profile','exec'),namespace)
    return namespace['run']()


if __name__=='__main__':run()
