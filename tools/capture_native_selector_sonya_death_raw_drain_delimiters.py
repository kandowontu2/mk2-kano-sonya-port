"""Observer-only Lua delimiter repair after genuine native45428 terminal3."""
import inspect
from pathlib import Path
import capture_native_selector_sonya_death_raw_drain as failed

ROOT,need,sha=failed.ROOT,failed.need,failed.sha
BASE=ROOT/'audit_native_selector_sonya_death_raw_drain_delimiters_ram'
OUT=ROOT/'audit_native_selector_sonya_death_raw_drain_delimiters_capture_checked'
LUA=ROOT/'mk2ks_native_selector_sonya_death_raw_drain_delimiters.lua'
KEY='same_sonya_human_kano_cpu_inputs_passive_raw_drain_delimiters'
PARENT=failed.PARENT
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[];AUDIO={};SCOPE=None


def prepare(state):
    scope=dict(vars(failed),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,PARENT=PARENT,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,__file__=__file__)
    exec(compile(inspect.getsource(failed.prepare),__file__+'::same_inputs_new_observer_delimiters','exec'),scope)
    return scope['prepare'](state)


def execute(state,preflight=False):
    global SCOPE
    held=failed.NATIVE_HANDLES[failed.KEY]
    need(held['process'].poll()==3 and held['identity']['ProcessId']==45428,
         'Exact failed observer original native45428 genuinely terminal, not timeout')
    folder=failed.RAM_CASES[failed.KEY][0]
    need('syntax error' in (folder/'stderr.log').read_text() and len(failed.RAM_CASES[failed.KEY][2])==0,
         'Preserve genuine pre-game Lua delimiter failure, no fictitious gameplay pass')
    scope=dict(vars(failed),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,PARENT=PARENT,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,
        prepare=prepare,__file__=__file__)
    source=inspect.getsource(failed.execute)
    before="sources=[LUA,ROOT/'mk2ks_native_selector_sonya_death_raw_objects.lua'"
    after="sources=[LUA,ROOT/'mk2ks_native_selector_sonya_death_raw_drain.lua',ROOT/'tools/capture_native_selector_sonya_death_raw_drain.py',*(p for p in folder.rglob('*') if p.is_file()),ROOT/'mk2ks_native_selector_sonya_death_raw_objects.lua'"
    need(source.count(before)==1,'Exact complete observer/failure source inventory')
    source=source.replace(before,after,1)
    scope['folder']=folder
    exec(compile(source,__file__+'::entire_original_capture_delimiter_fix_only','exec'),scope)
    result=scope['execute'](state,preflight)
    SCOPE=scope['SCOPE']
    return result
