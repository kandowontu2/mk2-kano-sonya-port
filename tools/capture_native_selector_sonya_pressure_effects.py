"""Actual missing stock effect allocator/task/palette/FIFO observations.

Original controller, cold-window proofs, health/state, PCM and sparse RGB
transport bytecode unchanged. One new observation job, no game-state writes,
build/ROM/media copies. This capture alone is not effects acceptance.
"""
import json
import re
import traceback
from pathlib import Path
from types import FunctionType
import capture_native_selector_sonya_cpu_pressure_bound as reference
import capture_native_selector_sonya_pressure_snapshot as snapshot
import qualify_native_selector_sonya_cpu_pressure_interrupt as mechanics
import seal_native_selector_sonya_pressure_stock_clear as parent
import verify_native_source_sync as sync

ROOT,need,sha=reference.ROOT,reference.need,reference.sha
BASE=ROOT/'audit_native_selector_sonya_pressure_effects_ram'
OUT=ROOT/'audit_native_selector_sonya_pressure_effects_capture_checked'
LUA=ROOT/'mk2ks_native_selector_sonya_pressure_effects.lua'
KEY='actual_pressure_stock_effect_palette_pool_and_scheduler'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[];AUDIO={};SCOPE=None


def prepare(state):
    collector=reference.prepare(state);f=collector['capture']
    need(not f.__closure__,'Whole original pressure collector has no alternate hidden namespace')
    scope=dict(f.__globals__,BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,RAM_CASES=RAM_CASES,
        NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,__file__=__file__)
    decoder=scope['decode_audio']
    need(not decoder.__closure__,'Whole original sound decoder retains original operations')
    scope['decode_audio']=FunctionType(decoder.__code__,dict(decoder.__globals__,AUDIO=AUDIO,KEY=KEY),
                                     decoder.__name__,decoder.__defaults__)
    scope['capture']=FunctionType(f.__code__,scope,f.__name__,f.__defaults__)
    need(scope['capture'].__code__ is f.__code__,'Original complete physical/cold/PCM collector bytecode')
    return scope


def execute(state,preflight=False):
    global SCOPE
    need(not BASE.exists()and not OUT.exists()and not reference.base.choices.current.prior.identity.census(),
         'Fresh genuinely missing palette/task metadata; all old native handles terminal')
    old=snapshot.NATIVE_HANDLES[snapshot.KEY]
    need(old['process'].poll()==0 and old['identity']['ProcessId']==47004,
         'Original47004 genuinely terminal, no restart after observation timeout')
    checkpoint=parent.OUT;proof=json.loads(checkpoint.read_text());pins=dict(proof['inputHashes'])
    need(proof['passed']and all(sha(p)==h for p,h in pins.items())and sync.verify()['passed'],
         'Whole original source/pressure/hide evidence and unchanged compiled/public endpoints')
    for p in (Path(__file__),LUA,Path(reference.__file__),Path(mechanics.__file__),
              Path(snapshot.__file__),Path(parent.__file__),checkpoint,
              ROOT/'mk2ks_native_selector_sonya_cpu_pressure_bound.lua'):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'Never replace executed source/evidence');pins[key]=h
    lua=LUA.read_text()
    need(lua.count("dofile('mk2ks_native_selector_sonya_cpu_pressure_bound.lua')")==1 and
         'palette_source='in lua and 'mainFree='in lua and
         not re.search(r':write_[ui]\d+|\.value\s*=(?!=)|load_?state|set_value',lua),
         'Exactly one unchanged controller plus passive metadata only')
    SCOPE=prepare(state)
    guest,gfx,build,gfx32,payload=(state[k]for k in ('guest','gfx','build','gfx32','payload'))
    native,_,_,decode=SCOPE['bindings'](guest,build)
    expected_rom,_=reference.base.original.audio_model.expected_region(pins)
    if preflight:return dict(passed=True,preflightOnly=True,inputHashes=pins,newNativeGames=0,fullPortAcceptance=False)
    AUDIO[KEY]=dict(pcmChunks=[],pcmHeaders=[],dacChunks=[],dacHeaders=[],
        rom={p:bytearray()for p in ('startup','terminal')},expectedROM=expected_rom,audioGuestObserved=False)
    def check(bundle,guest,payload,gfx32):
        return dict(wholeOriginalPressureMechanics=mechanics.gate(bundle['cpuLog'],guest),
                    actualEffectsQualificationPending=True,fullPortAcceptance=False)
    report=SCOPE['capture']('stock_effect_ownership',2,guest,gfx,gfx32,payload,native,check,decode,pins)
    held=NATIVE_HANDLES[KEY]
    need(held['process'].poll()==report['nativeExit'],'Keep actual original new native handle through terminal')
    if report['passed']:
        folder,text,_=RAM_CASES[KEY];old_text=reference.RAM_CASES[reference.KEY][1]
        tags=('MK2_CPU_PAIR_','MK2_P2CPU_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_',
              'MK2_KNIFE_PAIR_','MK2_CPU_CHOICE_','MK2_STARTUP_PROJECTILE_',
              'MK2_SONYA_HORIZONTAL_','MK2_MAUDIO_','MK2_TOMB_MIX_',
              'MK2_BBAUDIO_PCM_DIGEST ','MK2_NATIVE_DAC_RAM_DIGEST ','MK2_HPHASE_')
        need([s for s in text.splitlines()if s.startswith(tags)]==
             [s for s in old_text.splitlines()if s.startswith(tags)],
             'Entire actual original control/state/health/choice/body/shadow/audio chronology identical, not forced')
        need(all(('MK2_EFFECT_'+tag+' ')in text for tag in ('HEAD','QUEUE','DMA','LISTS','TASK','RESULT')),
             'Missing native stock effect observations actually present')
        for p in folder.rglob('*'):
            if p.is_file():pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every whole source and capture pin intact')
    value=dict(passed=report['passed'],goalStatus='active',actualNativeIdentity=held['identity'],
        nativeExit=report['nativeExit'],originalCaptureError=report.get('error'),
        originalCapture=report,inputHashes=pins,requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        individualEffectOwnershipAccepted=False,fullPortAcceptance=False,publicPlayableChanged=False,
        newNativeGames=1,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/('report.json'if report['passed']else'failure.json')).write_text(json.dumps(value,indent=2)+'\n')
    print('Actual missing stock effect metadata capture '+('PASS'if report['passed']else'FAIL'),flush=True)
    return value


def safe_execute(state,preflight=False):
    try:return execute(state,preflight)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual native metadata rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
