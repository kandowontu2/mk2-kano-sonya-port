"""Distinct actual human walk/punch pressure against natural Sonya CPU.

Keep full current cold memory, native state/health/choices, body/shadow,
horizontal operands and RAM PCM/DAC/ROM transport. One real physical controller.
No prescribed move, forced result, timeout replay, new build or media copies.
"""
import inspect
import json
import re
import traceback
from pathlib import Path
from types import FunctionType
import capture_native_selector_sonya_horizontal_operands as previous
import capture_native_selector_sonya_choice_visual_audio as base
import seal_native_selector_sonya_bicycle_journal_storage as parent

ROOT,need,sha=base.ROOT,base.need,base.sha
BASE=ROOT/'audit_native_selector_sonya_cpu_pressure_ram'
OUT=ROOT/'audit_native_selector_sonya_cpu_pressure_capture_checked'
LUA=ROOT/'mk2ks_native_selector_sonya_cpu_pressure.lua'
KEY='human_Kano_walk_HighPunch_pressure_natural_Sonya_CPU_boot608_confirm264'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[];AUDIO={};SCOPE=None


def prepare(state):
    f=base.prepare
    scope=dict(f.__globals__,BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,RAM_CASES=RAM_CASES,
        NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,__file__=__file__)
    source=inspect.getsource(f)
    marker="    exec(compile(source,__file__+'::whole_original_collector_distinct_actual_inputs','exec'),scope)"
    addition='''    source=choices.current.replace(source,"MK2KS_CPU_PAIR_APPROACH='original'", "MK2KS_CPU_PAIR_APPROACH='pressure_hp'")
    source=choices.current.replace(source,"MK2KS_CPU_CONTINUATION_POLICY='jump_guard'", "MK2KS_CPU_CONTINUATION_POLICY='guard_hold'")
'''
    need(source.count(marker)==1,'One exact original collector environment boundary')
    source=source.replace(marker,addition+marker,1)
    exec(compile(source,__file__+'::same_whole_collector_distinct_real_pressure_buttons','exec'),scope)
    return scope['prepare'](state)


def execute(state,preflight=False):
    global SCOPE
    need(not BASE.exists()and not OUT.exists()and not base.choices.current.prior.identity.census(),
         'Fresh genuinely distinct human pressure; all original native games terminal')
    need(previous.NATIVE_HANDLES[previous.KEY]['process'].poll()==0,
         'Original42616 terminal, never restarted because of observation timeout')
    checkpoint=parent.OUT;proof=json.loads(checkpoint.read_text());pins=dict(proof['inputHashes'])
    need(proof['passed']and all(sha(p)==h for p,h in pins.items())and base.choices.migration.verify()['passed'],
         'Full prior requirements, all source/native pins and synchronized current compile inputs')
    for p in (Path(__file__),LUA,checkpoint,Path(parent.__file__),Path(previous.__file__),Path(base.__file__),
              ROOT/'mk2ks_native_selector_sonya_choice_shadow_bound.lua',
              ROOT/'mk2ks_physical_p2_cpu_continuation_v3300.lua',
              ROOT/'mk2ks_current_kano_cpu_extended_ram_v6290.lua'):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'Never replace executed source/evidence');pins[key]=h
    lua=LUA.read_text()
    need('pressure_hp'in lua and "fields['P1 High Punch']:set_value(1)"in lua and
         not re.search(r':write_[ui]\d+|\.value\s*=(?!=)|load_?state',lua),
         'Only normal human controller inputs, no guest/CPU/RNG/HP/position/register writes')
    SCOPE=prepare(state)
    guest,gfx,build,gfx32,payload=(state[k]for k in ('guest','gfx','build','gfx32','payload'))
    native,_,_,decode=SCOPE['bindings'](guest,build)
    expected_rom,_=base.original.audio_model.expected_region(pins)
    if preflight:return dict(passed=True,preflightOnly=True,inputHashes=pins,newNativeGames=0,fullPortAcceptance=False)
    AUDIO[KEY]=dict(pcmChunks=[],pcmHeaders=[],dacChunks=[],dacHeaders=[],
        rom={p:bytearray()for p in ('startup','terminal')},expectedROM=expected_rom,audioGuestObserved=False)
    def check(b,guest,payload,gfx32):
        whole=base.choices.native_state.gate(b['cpuLog'],guest)
        return dict(wholeNativeStateHealth=whole,
            actualNativeChoices=base.choices.choices_gate(b['cpuLog'],guest,whole['schedule']),
            completePressureMoveRecoveryAccepted=False,fullPortAcceptance=False)
    report=SCOPE['capture']('Sonya_CPU_real_pressure',2,guest,gfx,gfx32,payload,native,check,decode,pins)
    held=NATIVE_HANDLES[KEY]
    need(report['passed']and held['process'].poll()==report['nativeExit']==0,
         'Original actual native pressure game terminal0; whole state/health/choice capture passed')
    folder,text,images=RAM_CASES[KEY]
    need(base.choices.native_state.rows(text,'MK2_PRESSURE_BIND')==[dict(count='1',controller='original_physical_P1',
          inputs='walk_high_punch',writes='0',assistance='none')], 'One actual original controller pressure binding')
    inputs=base.choices.native_state.rows(text,'MK2_CPU_PAIR_PRESSURE_INPUT')
    need(inputs and any(r['toward']=='1'for r in inputs)and any(r['punch']=='1'for r in inputs),
         'Actual new human walk and High Punch input commands occurred')
    need(previous.legacy(text)!=previous.legacy(previous.RAM_CASES[previous.KEY][1]),
         'Genuinely different physical/gameplay history, not accepted-case continuity replay')
    for p in (folder/'result.json',*(p for p in folder.rglob('*')if p.is_file())):pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All complete original and distinct new source/native pins intact')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        originalNativeCapture=report,pressureInputCallbacks=len(inputs),actualRAMRasters=len(images),
        actualPCMCallbacks=len(AUDIO[KEY]['pcmChunks']),requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        inputHashes=pins,completePressureMoveRecoveryAccepted=False,wholeDisplayedPixelsAccepted=False,
        wholeSourceAudioAccepted=False,allArenaCPUContextsAccepted=False,fullPortAcceptance=False,publicPlayableChanged=False,
        newNativeGames=1,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print('PASS distinct real human pressure capture, natural Sonya AI and full native health/state',flush=True)
    return value


def safe_execute(state,preflight=False):
    try:return execute(state,preflight)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual pressure preflight/native rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
