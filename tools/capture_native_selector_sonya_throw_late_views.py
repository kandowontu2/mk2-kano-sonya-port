"""Terminal-confirmed observer comparison: same real inputs, late throw views.

Keep all cold windows, native state/HP/RNG, full body/shadow and audio transport.
No outcome, guest, CPU, HP, RNG, location or register writes; no new build.
"""
import inspect
from pathlib import Path
import capture_native_selector_sonya_human_kano_cpu as parent
import qualify_native_selector_opposite_roles_throw_floor_hidden_json as geometry

ROOT,need,sha=parent.ROOT,parent.need,parent.sha
BASE=ROOT/'audit_native_selector_sonya_throw_late_views_ram'
OUT=ROOT/'audit_native_selector_sonya_throw_late_views_capture_checked'
LUA=ROOT/'mk2ks_native_selector_sonya_throw_late_views.lua'
KEY='same_sonya_human_kano_cpu_inputs_passive_late_throw_views'
PARENT=geometry.OUT/'report.json'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[];AUDIO={};SCOPE=None


def prepare(state):
    scope=dict(vars(parent),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,PARENT=PARENT,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,__file__=__file__)
    exec(compile(inspect.getsource(parent.prepare),__file__+'::unchanged_opposite_role_physical_inputs','exec'),scope)
    return scope['prepare'](state)


def execute(state,preflight=False):
    global SCOPE
    need(parent.NATIVE_HANDLES[parent.KEY]['process'].poll()==0,
         'Original38692 genuinely terminal; new observation coverage not timeout restart')
    scope=dict(vars(parent.previous),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,PARENT=PARENT,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,
        prepare=prepare,gate=parent.gate,__file__=__file__)
    source=inspect.getsource(parent.previous.execute)
    for before,after in [
        ('Fresh distinct actual input policy, never replay solely an observation timeout',
         'Fresh passive observer comparison after original terminal, not an observation-timeout replay'),
        ("whole=choices.native_state.gate(b['cpuLog'],guest)","whole=gate(b['cpuLog'],guest)"),
        ("branches=choices.choices_gate(b['cpuLog'],guest,whole['schedule'])","branches=whole['actualCPUChoices']"),
        ("sources=[LUA,*(ROOT/name for name in (",
         "sources=[LUA,ROOT/'mk2ks_native_selector_sonya_human_kano_cpu.lua',ROOT/'mk2ks_native_selector_cpu_projectile_pcm_startup_direct.lua',*(ROOT/name for name in ("),
        ("'sonya_choices_visual_audio',2","'sonya_throw_late_views',2")]:
        source=parent.previous.choices.current.replace(source,before,after)
    exec(compile(source,__file__+'::whole_original_capture_additional_passive_throw_views','exec'),scope)
    result=scope['execute'](state,preflight)
    SCOPE=scope['SCOPE']
    return result
