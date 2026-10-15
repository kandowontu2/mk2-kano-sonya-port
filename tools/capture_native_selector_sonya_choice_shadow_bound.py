"""Correct actual nested Lua environment; collect real boundary/velocity stores.

Same physical input policy for a controlled instrumentation comparison, not a
timeout restart. One original controller; no game/AI/register/HP/RNG writes.
Full cold/health/choices/19-channel PCM/DAC/ROM/raster capture remains intact.
"""
import inspect
from pathlib import Path
import capture_native_selector_sonya_choice_visual_audio as previous

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
BASE=ROOT/'audit_native_selector_sonya_choice_shadow_bound_ram'
OUT=ROOT/'audit_native_selector_sonya_choice_shadow_bound_capture_checked'
LUA=ROOT/'mk2ks_native_selector_sonya_choice_shadow_bound.lua'
KEY='natural_sonya_original_approach_jump_guard_bound_observers_boot608_confirm264'
PARENT=ROOT/'audit_native_selector_sonya_choice_av_observed_bound_checked/report.json'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[];AUDIO={};SCOPE=None


def functions():
    scope=dict(vars(previous),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,PARENT=PARENT,
               RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,__file__=__file__)
    exec(compile(inspect.getsource(previous.prepare),__file__+'::whole_original_collector_and_controls','exec'),scope)
    source=inspect.getsource(previous.execute)
    source=previous.choices.current.replace(source,'sources=[LUA,*(ROOT/name for name in (',
        "sources=[LUA,previous.LUA,*(ROOT/name for name in (")
    source=previous.choices.current.replace(source,"report=SCOPE['capture']('sonya_choices_visual_audio',2,guest,gfx,gfx32,payload,native,check,decode,pins)",
        "report=SCOPE['capture']('sonya_choices_shadow_bound',2,guest,gfx,gfx32,payload,native,check,decode,pins)")
    scope['previous']=previous
    exec(compile(source,__file__+'::whole_original_capture_correct_actual_lua_binding','exec'),scope)
    return scope


def execute(state,preflight=False):
    global SCOPE
    SCOPE=functions()
    return SCOPE['execute'](state,preflight)
