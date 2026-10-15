"""Direct original capture scope with corrected Lua and literal failure pins."""
import inspect
from pathlib import Path
import capture_native_selector_sonya_death_raw_lifetime as native
import capture_native_selector_sonya_death_raw_drain as failed
import capture_native_selector_sonya_death_raw_drain_delimiters as preflight_failed
import qualify_native_selector_sonya_death_raw_sequence as checkpoint

ROOT,need,sha=native.ROOT,native.need,native.sha
BASE=ROOT/'audit_native_selector_sonya_death_raw_pool_ram'
OUT=ROOT/'audit_native_selector_sonya_death_raw_pool_capture_checked'
LUA=ROOT/'mk2ks_native_selector_sonya_death_raw_drain_delimiters.lua'
KEY='same_sonya_human_kano_cpu_inputs_passive_raw_pool'
PARENT=checkpoint.OUT/'report.json'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[];AUDIO={};SCOPE=None


def prepare(state):
    scope=dict(vars(native.previous),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,PARENT=PARENT,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,__file__=__file__)
    exec(compile(inspect.getsource(native.previous.prepare),__file__+'::same_physical_inputs','exec'),scope)
    return scope['prepare'](state)


def execute(state,preflight=False):
    global SCOPE
    need(native.NATIVE_HANDLES[native.KEY]['process'].poll()==0 and failed.NATIVE_HANDLES[failed.KEY]['process'].poll()==3,
         'Original47752 and failed45428 genuinely terminal; not timeout replay')
    scope=dict(vars(native.previous),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,PARENT=PARENT,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,
        prepare=prepare,__file__=__file__)
    source=inspect.getsource(native.previous.execute)
    before="sources=[LUA,ROOT/'mk2ks_native_selector_sonya_throw_late_views.lua'"
    after="sources=[LUA,ROOT/'mk2ks_native_selector_sonya_death_raw_drain.lua',ROOT/'tools/capture_native_selector_sonya_death_raw_drain.py',ROOT/'tools/capture_native_selector_sonya_death_raw_drain_delimiters.py',ROOT/'audit_native_selector_sonya_death_raw_drain_preflight_failure.json',*(p for p in (ROOT/'audit_native_selector_sonya_death_raw_drain_ram/same_sonya_human_kano_cpu_inputs_passive_raw_drain').rglob('*') if p.is_file()),ROOT/'mk2ks_native_selector_sonya_death_raw_objects.lua',ROOT/'mk2ks_native_selector_sonya_death_raw_lifetime.lua',ROOT/'mk2ks_native_selector_sonya_throw_late_views.lua'"
    need(source.count(before)==1,'Literal entire immutable observer/failure source inventory')
    source=source.replace(before,after,1)
    need(source.count("'sonya_death_raw_objects',2")==1,'Exact native raw capture label')
    source=source.replace("'sonya_death_raw_objects',2","'sonya_death_raw_pool',2",1)
    exec(compile(source,__file__+'::whole_original_capture_direct_literal_pool_scope','exec'),scope)
    result=scope['execute'](state,preflight)
    SCOPE=scope['SCOPE']
    return result
