"""Complete saved initializer namespace for the same actual Pit sound buffers.

The previous wrapper omitted gfx/build when extracting the full runtime tail.
Preserve that failure; add only the two already-retained RAM bindings.
"""
import inspect
import json
import traceback
from pathlib import Path
import qualify_native_current_cross_pit_19_audio_context as previous

ROOT, need, sha = previous.ROOT, previous.need, previous.sha
FAILURE = ROOT/'audit_native_current_cross_pit_19_audio_ram_context_failure/failure.json'


def qualify(ram):
    if not FAILURE.exists():
        try:
            previous.qualify(ram)
        except NameError as error:
            need(str(error)=="name 'gfx' is not defined", 'Exact saved initializer namespace failure')
            FAILURE.parent.mkdir()
            FAILURE.write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                failureBeforeAudioRecomputation=True,newNativeBoots=0,
                inputHashes={str(Path(previous.__file__)):sha(previous.__file__)},fullPortAcceptance=False),indent=2)+'\n')
        else:
            raise ValueError('Expected original missing saved namespace failure no longer reproduces')
    failure=json.loads(FAILURE.read_text())
    need(not failure['passed'] and all(sha(p)==h for p,h in failure['inputHashes'].items()), 'Actual predecessor and failure frozen')
    body=inspect.getsource(previous.qualify)
    body=previous.original.once(body,'failure_path=failure_path,fighter=meta[\'fighter\'],side=meta[\'side\'])',
        'failure_path=failure_path,fighter=meta[\'fighter\'],side=meta[\'side\'],gfx=ram[\'gfx\'],build=ram[\'build\'])')
    body=previous.original.once(body,"Path(__file__),Path(original.__file__),failure_path,original.SOURCE/'report.json'",
        "Path(__file__),Path(previous.__file__),Path(original.__file__),FAILURE,failure_path,original.SOURCE/'report.json'")
    namespace=dict(vars(previous),__file__=__file__,previous=previous,FAILURE=FAILURE)
    exec(compile(body,__file__+'::whole_same_capture_with_complete_saved_initializer_namespace','exec'),namespace)
    return namespace['qualify'](ram)
