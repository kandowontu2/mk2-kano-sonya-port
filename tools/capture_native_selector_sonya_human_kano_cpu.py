"""Natural opposite roles: human Sonya selection, unsupplied CPU Kano.

Same current candidate, original physical controller and entire cold/runtime,
state/HP, body/shadow, RGB and19-channel PCM/DAC/ROM observers. Transport is
not all-move, geometry, waveform, campaign or complete-port acceptance.
"""
import ast
import inspect
import json
import struct
from pathlib import Path
import capture_native_selector_sonya_choice_visual_audio as previous
import qualify_native_selector_sonya_repeated_cue_pcm_loaded as parent_audio
import current_kano_cpu_extended_contract_v6291 as kano

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
BASE=ROOT/'audit_native_selector_sonya_human_kano_cpu_ram'
OUT=ROOT/'audit_native_selector_sonya_human_kano_cpu_capture_checked'
LUA=ROOT/'mk2ks_native_selector_sonya_human_kano_cpu.lua'
KEY='human_sonya_natural_cpu_guard_until_close_jump_guard_boot605_confirm265'
PARENT=parent_audio.OUT/'report.json'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[];AUDIO={};SCOPE=None


def gate(text,guest):
    original=previous.choices.native_state.original
    pair=original.pair
    cold=pair.rows_prefix(text,'MK2_P2CPU_COLD_LIVE ')
    selected=pair.rows_prefix(text,'MK2_P2CPU_SELECT_RESULT ')
    need(len(cold)==len(selected)==1,'One actual physical Sonya selection and cold fight')
    c,s=cold[0],selected[0]
    need(c['human']==s['human']=='sonya' and c['human_id']==s['human_id']==18 and
         c['cpu_id']==s['initial_cpu']==17 and c['stage']==0 and c['frame']==s['live'] and
         s['checks']==50 and s['errors']==0 and 700<s['css']<s['exit']<s['live'] and
         all(r['writes']==0 and r['assistance']=='none' for r in (c,s)),
         'True human Sonya18 / naturally selected CPU Kano17, no proxy or forced opponent')
    table=struct.unpack_from('<I',guest,(0xff8a11f0-0xff800000)//8)[0]
    expected=pair.expected_orders();rom=pair.rows(text,'ROM')
    need(table==0xfffa2c00 and len(rom)==6 and [r['order'] for r in rom]==list(range(6)),
         'Whole native ladder inventory')
    for i,r in enumerate(rom):
        pointer=struct.unpack_from('<I',guest,(table+i*32-0xff800000)//8)[0]
        ids=struct.unpack_from('<17H',guest,(pointer-0xff800000)//8)
        need(r['table']==table and r['list']==pointer==0xfffa3000+i*0x180 and
             tuple(map(int,r['ids'].split(',')))==ids==expected[i] and
             r['writes']==0 and r['assistance']=='none','All six full source-derived native lists')
    orders=[r['order'] for r in rom if r['list']==c['schedule']]
    need(len(orders)==1 and expected[orders[0]][0]==17,'Unsupplied native schedule actually begins with Kano')
    health=inspect.getsource(original.health_ledger)
    state=inspect.getsource(original.state_ledgers)
    changes=[("expected_ids=f'{pair.HUMANS[player]},18'","expected_ids=f'{pair.HUMANS[player]},17'"),
             ("row['schedule']==0xfffa3180","row['schedule']==schedule"),
             ("(18 if row['slot']==2 else pair.HUMANS[player])","(17 if row['slot']==2 else pair.HUMANS[player])")]
    for before,after in changes:health=previous.choices.current.replace(health,before,after)
    for before,after in [("==(18,pair.HUMANS[player])","==(17,pair.HUMANS[player])"),
                         ("==(18,18,pair.HUMANS[player],pair.HUMANS[player],0,1,2)","==(17,17,pair.HUMANS[player],pair.HUMANS[player],0,1,2)")]:
        state=previous.choices.current.replace(state,before,after)
    scope=dict(vars(original),schedule=c['schedule'])
    exec(compile(health+'\n'+state,__file__+'::whole_original_ledgers_actual_opposite_roles','exec'),scope)
    hp,by=scope['health_ledger'](text,guest,'sonya')
    stores=scope['state_ledgers'](text,guest,'sonya',by)
    need(hp['first']==c['frame'] and hp['last']-hp['first']==1800,'Entire original match, not truncated live fields')
    module_source=Path(kano.__file__).read_text()
    node=next(n for n in ast.parse(module_source).body if isinstance(n,ast.Assign) and
              any(isinstance(t,ast.Name) and t.id=='choices' for t in n.targets))
    choice_source=ast.get_source_segment(module_source,node)
    choice_source=previous.choices.current.replace(choice_source,'"==0xfffa3180":"==0xfffa3000"',
        '"==0xfffa3180":"=='+hex(c['schedule'])+'"')
    choice_scope=dict(vars(kano));exec(compile(choice_source,__file__+'::whole_Kano_RNG_actual_native_schedule','exec'),choice_scope)
    choices=choice_scope['choices'](kano.original.choice_rows(text),guest)
    return dict(passed=True,trueHumanID=18,trueCPUID=17,actualNativeTower=orders[0],schedule=c['schedule'],
        wholeNativeHealthLedger=hp,wholeNativeStateLedger=stores,actualCPUChoices=choices,
        fullMovePhaseAcceptance=False,wholeGeometryWaveformAcceptance=False,fullPortAcceptance=False)


def prepare(state):
    scope=dict(vars(previous.original),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,__file__=__file__)
    exec(compile(inspect.getsource(previous.original.decode_audio),__file__+'::whole_sound_transport','exec'),scope)
    source=inspect.getsource(previous.original.functions)
    for before,after in [("MK2KS_TEST_FIGHTER='kano'","MK2KS_TEST_FIGHTER='sonya'"),
                         ("MK2KS_TEST_BOOT_FRAME='607'","MK2KS_TEST_BOOT_FRAME='605'"),
                         ("MK2KS_CPU_PAIR_CONFIRM_AGE='264'","MK2KS_CPU_PAIR_CONFIRM_AGE='265'"),
                         ("MK2KS_CPU_PAIR_APPROACH='original'","MK2KS_CPU_PAIR_APPROACH='guard_until_close'"),
                         ("MK2KS_CPU_CONTINUATION_POLICY='guard_hold'","MK2KS_CPU_CONTINUATION_POLICY='jump_guard'")]:
        source=previous.choices.current.replace(source,before,after)
    exec(compile(source,__file__+'::whole_collector_normal_opposite_role_inputs','exec'),scope)
    return scope['functions'](state)


def execute(state,preflight=False):
    global SCOPE
    scope=dict(vars(previous),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,PARENT=PARENT,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,
        prepare=prepare,gate=gate,__file__=__file__)
    source=inspect.getsource(previous.execute)
    for before,after in [('whole=choices.native_state.gate(b[\'cpuLog\'],guest)',"whole=gate(b['cpuLog'],guest)"),
                         ("branches=choices.choices_gate(b['cpuLog'],guest,whole['schedule'])","branches=whole['actualCPUChoices']"),
                         ("sources=[LUA,*(ROOT/name for name in (","sources=[LUA,ROOT/'mk2ks_native_selector_cpu_projectile_pcm_startup_direct.lua',*(ROOT/name for name in ("),
                         ("'sonya_choices_visual_audio',2","'sonya_human_kano_cpu',2")]:
        source=previous.choices.current.replace(source,before,after)
    exec(compile(source,__file__+'::whole_native_opposite_role_capture','exec'),scope)
    result=scope['execute'](state,preflight)
    SCOPE=scope['SCOPE']
    return result
