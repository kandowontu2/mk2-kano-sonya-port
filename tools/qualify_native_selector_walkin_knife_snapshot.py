"""Same source-exact original renderer with genuine current snapshot target.

Old raw-bitmap failures are preserved. Full original source/FIFO/VRAM/palette/
pixel gates remain unchanged. Only recorder namespace and independently
source-defined complete graphics initialization are bound to this new capture.
"""
import inspect
import json
import traceback
from pathlib import Path
import capture_native_selector_walkin_knife_snapshot_ram as capture
import qualify_native_selector_walkin_knife_display_face_rows as names

original=names.original
ROOT,need,sha=names.ROOT,names.need,names.sha
OUT=ROOT/'audit_native_selector_walkin_knife_snapshot_renderer_checked'


def execute(state):
    source=inspect.getsource(original.execute)
    source=original.once(source,'    display=capture.DISPLAY',
        '    display=capture.DISPLAY\n    image=names.runtime_graphics(state,pins)')
    source=original.once(source,"raw==state['gfx32'][first:first+len(raw)]","raw==image[first:first+len(raw)]")
    source=original.once(source,'sources=(Path(__file__).resolve(),',
        'sources=(Path(capture.__file__).resolve(),capture.LUA,Path(names.__file__).resolve(),'
        'Path(original.__file__).resolve(),names.OUT.joinpath("failure.json"),'
        'ROOT.joinpath("audit_native_selector_walkin_knife_vram_checked/report.json"),Path(__file__).resolve(),')
    scope=dict(vars(original),OUT=OUT,__file__=__file__,capture=capture,names=names,original=original)
    exec(compile(source,__file__+'::whole_original_renderer_true_current_snapshot','exec'),scope)
    return scope['execute'](state)


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual current snapshot failure')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
