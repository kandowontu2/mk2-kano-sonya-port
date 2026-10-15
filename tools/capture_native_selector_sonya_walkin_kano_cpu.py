"""Distinct actual human walk-in inputs against naturally selected Kano CPU.

Same cold native Sonya selection and unchanged current build, complete native
state/HP/choices, render/shadow, RGB and PCM/DAC/ROM transport. No forced move,
opponent, AI, RNG, HP, position, saved state or registers. Transport acceptance
alone never substitutes for attack recovery, art/audio or full-port proof.
"""
import inspect
from pathlib import Path
import capture_native_selector_sonya_human_kano_cpu as original
import capture_native_selector_sonya_death_raw_pool as terminal
import qualify_native_selector_sonya_death_raw_pool_palette_word as checkpoint

ROOT,need,sha=original.ROOT,original.need,original.sha
BASE=ROOT/'audit_native_selector_sonya_walkin_kano_cpu_ram'
OUT=ROOT/'audit_native_selector_sonya_walkin_kano_cpu_capture_checked'
LUA=original.LUA
KEY='human_sonya_natural_kano_cpu_walkin_jump_guard_boot605_confirm265'
PARENT=checkpoint.OUT/'report.json'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[];AUDIO={};SCOPE=None


def prepare(state):
    scope=dict(vars(original),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,PARENT=PARENT,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,__file__=__file__)
    source=inspect.getsource(original.prepare)
    before='"MK2KS_CPU_PAIR_APPROACH=\'guard_until_close\'"'
    after='"MK2KS_CPU_PAIR_APPROACH=\'original\'"'
    need(source.count(before)==1,'Only genuine human walk-in instead of standing guard approach')
    source=source.replace(before,after,1)
    exec(compile(source,__file__+'::same_original_collector_distinct_human_walkin','exec'),scope)
    return scope['prepare'](state)


def execute(state,preflight=False):
    global SCOPE
    need(terminal.NATIVE_HANDLES[terminal.KEY]['process'].poll()==0,
         'Original38516 genuinely terminal; different real input case, not timeout replay')
    scope=dict(vars(original),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,PARENT=PARENT,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,
        prepare=prepare,gate=original.gate,__file__=__file__)
    source=inspect.getsource(original.execute)
    need(source.count("'sonya_human_kano_cpu',2")==1,'Exact current native pairing transport label')
    source=source.replace("'sonya_human_kano_cpu',2","'sonya_walkin_kano_cpu',2",1)
    exec(compile(source,__file__+'::whole_original_opposite_roles_new_walkin_inputs','exec'),scope)
    result=scope['execute'](state,preflight)
    SCOPE=scope['SCOPE']
    return result
