"""Same terminal-confirmed real route; new passive native bulk-reset evidence."""
import inspect
from pathlib import Path
import capture_native_selector_sonya_death_raw_lifetime as previous
import qualify_native_selector_sonya_death_raw_sequence as checkpoint

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
BASE=ROOT/'audit_native_selector_sonya_death_raw_drain_ram'
OUT=ROOT/'audit_native_selector_sonya_death_raw_drain_capture_checked'
LUA=ROOT/'mk2ks_native_selector_sonya_death_raw_drain.lua'
KEY='same_sonya_human_kano_cpu_inputs_passive_raw_drain'
PARENT=checkpoint.OUT/'report.json'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[];AUDIO={};SCOPE=None


def prepare(state):
    scope=dict(vars(previous.previous),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,PARENT=PARENT,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,__file__=__file__)
    exec(compile(inspect.getsource(previous.previous.prepare),__file__+'::same_physical_inputs','exec'),scope)
    return scope['prepare'](state)


def execute(state,preflight=False):
    global SCOPE
    need(previous.NATIVE_HANDLES[previous.KEY]['process'].poll()==0,
         'Original47752 genuinely terminal; not an observation-timeout restart')
    scope=dict(vars(previous.previous),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,PARENT=PARENT,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,
        prepare=prepare,__file__=__file__)
    source=inspect.getsource(previous.previous.execute)
    before="sources=[LUA,ROOT/'mk2ks_native_selector_sonya_throw_late_views.lua'"
    after="sources=[LUA,ROOT/'mk2ks_native_selector_sonya_death_raw_objects.lua',ROOT/'mk2ks_native_selector_sonya_death_raw_lifetime.lua',ROOT/'mk2ks_native_selector_sonya_throw_late_views.lua'"
    need(source.count(before)==1,'Exact native raw observer source inventory')
    source=source.replace(before,after,1)
    need(source.count("'sonya_death_raw_objects',2")==1,'Exact previous raw capture label')
    source=source.replace("'sonya_death_raw_objects',2","'sonya_death_raw_drain',2",1)
    exec(compile(source,__file__+'::unchanged_native_capture_plus_bulk_reset','exec'),scope)
    result=scope['execute'](state,preflight)
    SCOPE=scope['SCOPE']
    return result
