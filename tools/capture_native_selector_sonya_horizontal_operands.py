"""Previously absent actual Bicycle write operands; same original real route.

Keep original collector/controller bytecode and cold/state/health/choices/
body/shadow/audio RAM data. No forced outcome or timeout replay. Only passive
missing A6/A7/A9/A10/A11/A12/A14/status fields are added to real write taps.
"""
import json
import re
import traceback
from pathlib import Path
from types import FunctionType
import capture_native_selector_sonya_choice_shadow_bound_loader as reference
import capture_native_selector_sonya_choice_visual_audio as base
import qualify_native_selector_sonya_startup_choices_bound as parent_model

ROOT,need,sha=base.ROOT,base.need,base.sha
BASE=ROOT/'audit_native_selector_sonya_horizontal_operands_ram'
OUT=ROOT/'audit_native_selector_sonya_horizontal_operands_capture_checked'
LUA=ROOT/'mk2ks_native_selector_sonya_horizontal_operands.lua'
KEY='natural_Sonya_Bicycle_actual_all_horizontal_operands_jump_guard'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[];AUDIO={};SCOPE=None


def prepare(state):
    f=base.prepare
    scope=dict(f.__globals__,BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,RAM_CASES=RAM_CASES,
        NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,__file__=__file__)
    return FunctionType(f.__code__,scope,f.__name__,f.__defaults__)(state)


def legacy(text):
    tags=('MK2_CPU_PAIR_','MK2_P2CPU_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_',
          'MK2_KNIFE_PAIR_','MK2_CPU_CHOICE_','MK2_STARTUP_PROJECTILE_',
          'MK2_HPHASE_','MK2_SONYA_CHOICE_','MK2_SONYA_NATIVE_FALL',
          'MK2_SONYA_HORIZONTAL_STORE','MK2_SONYA_HORIZONTAL_RESULT','MK2_SONYA_SHADOW_BIND')
    result=[]
    for l in text.splitlines():
        if not l.startswith(tags):continue
        if l.startswith('MK2_SONYA_HORIZONTAL_STORE '):
            l=re.sub(r'\s(?:a6|a7|a9|a10|a11|a12|a14|status)=\S+','',l)
        result.append(l)
    return result


def execute(state,preflight=False):
    global SCOPE
    need(not BASE.exists()and not OUT.exists()and not base.choices.current.prior.identity.census(),
         'Actual completed games terminal; fresh genuinely missing horizontal operand coverage')
    held=reference.NATIVE_HANDLES[reference.KEY]
    need(held['process'].poll()==0 and held['identity']['ProcessId']==44988,
         'Original boundary-only proof retained terminal, not timeout replay')
    _,old,_=reference.RAM_CASES[reference.KEY]
    oldstores=base.choices.native_state.rows(old,'MK2_SONYA_HORIZONTAL_STORE')
    need(oldstores and all('a7'not in r and 'a9'not in r for r in oldstores),
         'Actual source/data/address operands genuinely absent from prior observations')
    parent=parent_model.OUT/'report.json';proof=json.loads(parent.read_text());pins=dict(proof['inputHashes'])
    need(proof['passed']and all(sha(p)==h for p,h in pins.items())and base.choices.migration.verify()['passed'],
         'Whole latest full-scope source/native/evidence pins intact before distinct instrumentation')
    for p in (Path(__file__),LUA,parent,Path(reference.__file__),Path(base.__file__),
              ROOT/'mk2ks_native_selector_sonya_choice_shadow_bound.lua',
              ROOT/'mk2ks_native_selector_sonya_choice_shadow_bound_loader.lua',
              ROOT/'audit_native_selector_sonya_shadow_bound_faults_words_checked/report.json'):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'Never edit or replace executed source/evidence');pins[key]=h
    lua=LUA.read_text()
    need('regs.A7.value,regs.A9.value'in lua and not re.search(r':write_[ui]\d+|\.value\s*=(?!=)|load_?state',lua),
         'Only passive full register observations, no game/HP/RNG/AI/control/register writes')
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
            actualOperandQualificationPending=True,fullPortAcceptance=False)
    report=SCOPE['capture']('Sonya_horizontal_operands',2,guest,gfx,gfx32,payload,native,check,decode,pins)
    held=NATIVE_HANDLES[KEY]
    need(report['passed']and held['process'].poll()==report['nativeExit']==0,
         'Original actual native handle/cold/state/health/choice capture terminal0')
    folder,text,_=RAM_CASES[KEY]
    need(legacy(text)==legacy(old),'Every original physical/state/health/choice/pose/shadow/position/velocity record identical')
    stores=base.choices.native_state.rows(text,'MK2_SONYA_HORIZONTAL_STORE')
    need(len(stores)==len(oldstores)and all(set('a6 a7 a9 a10 a11 a12 a14 status'.split())<=set(r)for r in stores),
         'Every actual existing horizontal write now has all missing native registers')
    for p in (folder/'result.json',*(p for p in folder.rglob('*')if p.is_file())):pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Entire current source/native/evidence inventory preserved')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        actualHorizontalWriteRows=len(stores),wholeOriginalPhysicalChronologyUnchanged=True,
        originalNativeCapture=report,requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        inputHashes=pins,completeWriteOperandQualificationAccepted=False,wholeBicycleLifecycleAccepted=False,
        allArenaCPUContextsAccepted=False,fullPortAcceptance=False,publicPlayableChanged=False,
        newNativeGames=1,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print('PASS actual missing horizontal registers captured with every original gameplay record unchanged',flush=True)
    return value


def safe_execute(state,preflight=False):
    try:return execute(state,preflight)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual new horizontal capture failure')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
