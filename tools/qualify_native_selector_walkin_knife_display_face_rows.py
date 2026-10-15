"""Same retained native Knife display; source-faithful conditional HUD ramp.

Preserve both executed renderer failures. Native init permits empty mask rows
without gold, but requires gold for each actually drawn face pixel. No game,
observed graphics, target pixels or historical sources are modified.
"""
import inspect
import json
import traceback
from pathlib import Path
import qualify_native_selector_walkin_knife_display_initialized as previous

original=previous.original
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_native_selector_walkin_knife_display_face_rows_checked'


def native_name_source(source):
    source=original.once(source,
        "  need(best!=0,'Actual original native HUD gold ramp');ramp.append(best)",
        '  ramp.append(best)')
    source=original.once(source,
        "    pen=ramp[y]if face(x,y)else 2 if x and(face(x-1,y)or(y and face(x-1,y-1)))else 0",
        "    if face(x,y):need(ramp[y]!=0,'Actual native gold ramp required at every face pixel')\n"
        "    pen=ramp[y]if face(x,y)else 2 if x and(face(x-1,y)or(y and face(x-1,y-1)))else 0")
    return source


def runtime_graphics(state,pins):
    name=original.capture.previous.original.previous.choices.current.startup.NAME
    code=(ROOT/name/'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp').read_text()
    need('std::array<uint8_t, 10> ramp{};' in code and
         'if (face(x, y))\n\t\t\t\t{\n\t\t\t\t\tif (!ramp[y])' in code,
         'Actual compiled name code initializes zero rows and tests ramp only for a face pixel')
    source=inspect.getsource(previous.runtime_graphics)
    source=original.once(source,'    name_source=NAME_MODEL.read_text()',
        '    name_source=native_name_source(NAME_MODEL.read_text())')
    scope=dict(vars(previous),native_name_source=native_name_source)
    exec(compile(source,__file__+'::whole_original_init_conditional_face_requirement','exec'),scope)
    return scope['runtime_graphics'](state,pins)


def execute(state):
    path=previous.OUT/'failure.json';failure=json.loads(path.read_text())
    need(not failure['passed'] and failure['error']=="ValueError('Actual original native HUD gold ramp')",
         'Actual original overstrict blank-row rejection remains failed and immutable')
    source=inspect.getsource(previous.execute)
    scope=dict(vars(previous),OUT=OUT,__file__=__file__,runtime_graphics=runtime_graphics)
    exec(compile(source,__file__+'::whole_initialized_renderer_native_face_rows','exec'),scope)
    # Include both failed successor source and receipt in the original pins.
    source2=inspect.getsource(original.execute)
    source2=original.once(source2,'    display=capture.DISPLAY',
        '    display=capture.DISPLAY\n    image=runtime_graphics(state,pins)')
    source2=original.once(source2,"raw==state['gfx32'][first:first+len(raw)]","raw==image[first:first+len(raw)]")
    source2=original.once(source2,'sources=(Path(__file__).resolve(),',
        'sources=(Path(previous.__file__).resolve(),previous.OUT.joinpath("failure.json"),'
        'previous.FAILURE,previous.NAME_MODEL,Path(original.__file__).resolve(),Path(__file__).resolve(),')
    bound=dict(vars(original),OUT=OUT,__file__=__file__,runtime_graphics=runtime_graphics,
               previous=previous,original=original)
    exec(compile(source2,__file__+'::unchanged_full_renderer_face_rows','exec'),bound)
    return bound['execute'](state)


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual native-face renderer failure')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
