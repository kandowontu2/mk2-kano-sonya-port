"""Supported CPython read-only diagnostic, actual original native terminal."""
import inspect
import read_live_shang_drain_frames as original


def run():
    source=inspect.getsource(original.run)
    changes=[
        ("r'shang_(?:shrink_id(?:17|18)_age|victim_provenance_age)\\d+\\.png'", "r'[a-z0-9_]+\\.png'"),
        ("assert wanted in records and wanted['ProcessId']==31336 and wanted['ParentProcessId']==30848",
         "terminal=json.loads((OUT/'native_terminal.json').read_text())\n    assert terminal['identity']==wanted and terminal['nativeExit']==0 and not identity.census() and wanted['ProcessId']==31336 and wanted['ParentProcessId']==30848"),
        ("assert host in census_hosts() and wanted in identity.census()",
         "assert host in census_hosts() and not identity.census() and answer['nativePoll']==0"),
    ]
    for before,after in changes:
        assert source.count(before)==1
        source=source.replace(before,after,1)
    scope=dict(vars(original),__file__=__file__,REMOTE=original.ROOT/'tools/read_retained_mk2_frames_remote.py')
    exec(compile(source,__file__+'::same_original_terminal_receipt_and_retained_rasters','exec'),scope)
    scope['run']()


if __name__=='__main__':run()
