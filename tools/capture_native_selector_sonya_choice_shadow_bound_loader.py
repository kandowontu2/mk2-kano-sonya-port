"""Preserve actual pregame loader rejection; fix one ambiguous helper spelling."""
import inspect
import capture_native_selector_sonya_choice_shadow_bound as previous

ROOT=previous.ROOT
BASE=ROOT/'audit_native_selector_sonya_choice_shadow_bound_loader_ram'
OUT=ROOT/'audit_native_selector_sonya_choice_shadow_bound_loader_capture_checked'
LUA=ROOT/'mk2ks_native_selector_sonya_choice_shadow_bound_loader.lua'
KEY='natural_sonya_original_approach_jump_guard_bound_loader_boot608_confirm264'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[];AUDIO={};SCOPE=None


def execute(state,preflight=False):
    global SCOPE
    factory=inspect.getsource(previous.functions)
    factory=previous.need and factory.replace(
        'sources=[LUA,previous.LUA,*(ROOT/name for name in (',
        "sources=[LUA,previous.LUA,ROOT/'mk2ks_native_selector_sonya_choice_shadow_bound.lua',*(ROOT/name for name in (")
    scope=dict(vars(previous),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,
               RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,__file__=__file__)
    exec(compile(factory,__file__+'::whole_original_capture_plus_corrected_helper_loader','exec'),scope)
    SCOPE=scope['functions']()
    return SCOPE['execute'](state,preflight)
