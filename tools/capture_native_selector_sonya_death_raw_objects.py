"""Same physical route after terminal11004: observe missing zero-pose raw objects."""
import inspect
from pathlib import Path
import capture_native_selector_sonya_throw_late_views as previous
import qualify_native_selector_sonya_throw_late_lifetime as checkpoint

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
BASE=ROOT/'audit_native_selector_sonya_death_raw_objects_ram'
OUT=ROOT/'audit_native_selector_sonya_death_raw_objects_capture_checked'
LUA=ROOT/'mk2ks_native_selector_sonya_death_raw_objects.lua'
KEY='same_sonya_human_kano_cpu_inputs_passive_raw_death_objects'
PARENT=checkpoint.OUT/'report.json'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[];AUDIO={};SCOPE=None


def prepare(state):
    scope=dict(vars(previous),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,PARENT=PARENT,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,__file__=__file__)
    exec(compile(inspect.getsource(previous.prepare),__file__+'::unchanged_original_physical_inputs','exec'),scope)
    return scope['prepare'](state)


def execute(state,preflight=False):
    global SCOPE
    need(previous.NATIVE_HANDLES[previous.KEY]['process'].poll()==0,
         'Original11004 handle genuinely terminal; new raw coverage not timeout replay')
    scope=dict(vars(previous),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,PARENT=PARENT,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,
        prepare=prepare,__file__=__file__)
    source=inspect.getsource(previous.execute)
    before="sources=[LUA,ROOT/'mk2ks_native_selector_sonya_human_kano_cpu.lua'"
    after="sources=[LUA,ROOT/'mk2ks_native_selector_sonya_throw_late_views.lua',ROOT/'mk2ks_native_selector_sonya_human_kano_cpu.lua'"
    need(source.count(before)==1,'Exact original loaded source inventory')
    source=source.replace(before,after,1)
    need(source.count("'sonya_throw_late_views',2")==1,'Exact original capture label')
    source=source.replace("'sonya_throw_late_views',2","'sonya_death_raw_objects',2",1)
    exec(compile(source,__file__+'::whole_original_capture_plus_passive_raw_lifecycle','exec'),scope)
    result=scope['execute'](state,preflight)
    SCOPE=scope['SCOPE']
    return result
