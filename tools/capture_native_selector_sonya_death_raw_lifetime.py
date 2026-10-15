"""Same passive raw lifecycle capture with legitimate native pool reuse."""
import inspect
from pathlib import Path
import capture_native_selector_sonya_death_raw_objects as previous

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
BASE=ROOT/'audit_native_selector_sonya_death_raw_lifetime_ram'
OUT=ROOT/'audit_native_selector_sonya_death_raw_lifetime_capture_checked'
LUA=ROOT/'mk2ks_native_selector_sonya_death_raw_lifetime.lua'
KEY='same_sonya_human_kano_cpu_inputs_passive_raw_lifetime'
PARENT=previous.PARENT
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[];AUDIO={};SCOPE=None


def prepare(state):
    scope=dict(vars(previous),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,PARENT=PARENT,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,__file__=__file__)
    exec(compile(inspect.getsource(previous.prepare),__file__+'::same_original_physical_inputs','exec'),scope)
    return scope['prepare'](state)


def execute(state,preflight=False):
    global SCOPE
    scope=dict(vars(previous),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,PARENT=PARENT,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,
        prepare=prepare,__file__=__file__)
    source=inspect.getsource(previous.execute)
    before="sources=[LUA,ROOT/'mk2ks_native_selector_sonya_throw_late_views.lua'"
    after="sources=[LUA,ROOT/'mk2ks_native_selector_sonya_death_raw_objects.lua',ROOT/'mk2ks_native_selector_sonya_throw_late_views.lua'"
    need(source.count(before)==1,'Exact complete actual raw-observer source inventory')
    source=source.replace(before,after,1)
    need(source.count("'sonya_death_raw_objects',2")==1,'Exact raw capture label')
    source=source.replace("'sonya_death_raw_objects',2","'sonya_death_raw_lifetime',2",1)
    exec(compile(source,__file__+'::whole_raw_capture_legitimate_lifetime_only','exec'),scope)
    result=scope['execute'](state,preflight)
    SCOPE=scope['SCOPE']
    return result
