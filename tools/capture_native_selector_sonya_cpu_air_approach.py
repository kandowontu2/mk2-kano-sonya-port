"""Genuinely distinct real walk/jump trial against naturally deciding Sonya CPU.

Whole current cold windows, native health/state/choices, sparse RGB, full dense
display buffers/source streams and PCM/DAC/ROM transport. Capture proves only
the observed history; no contact/move/outcome is prescribed or inferred.
"""
import inspect
import json
import re
import traceback
from pathlib import Path
from types import FunctionType
import capture_native_selector_sonya_pressure_snapshot as snapshot
import capture_native_selector_sonya_cpu_pressure_bound as previous
import seal_native_selector_sonya_pressure_palette as parent
import verify_native_source_sync as sync

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
BASE=ROOT/'audit_native_selector_sonya_cpu_air_approach_ram'
OUT=ROOT/'audit_native_selector_sonya_cpu_air_approach_capture_checked'
LUA=ROOT/'mk2ks_native_selector_sonya_cpu_air_approach.lua'
KEY='actual_Kano_walk_periodic_jump_natural_Sonya_CPU_boot608_confirm264'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[];AUDIO={};SCOPE=None
DISPLAY=dict(buffers=snapshot.RAMBuffers(),headers={},gfx={},rgb={},rgbHeaders={})


def normalize(line):
    f=snapshot.transport.normalize
    return FunctionType(f.__code__,dict(f.__globals__,DISPLAY=DISPLAY),f.__name__,f.__defaults__)(line)


def prepare(state):
    factory=inspect.getsource(previous.prepare)
    before='"MK2KS_CPU_PAIR_APPROACH=\'pressure_hp\'"'
    need(factory.count(before)==1, 'Only the actual human approach setting changes')
    factory=factory.replace(before,'"MK2KS_CPU_PAIR_APPROACH=\'air_approach\'"',1)
    before='"MK2KS_CPU_CONTINUATION_POLICY=\'guard_hold\'"'
    need(factory.count(before)==1, 'Only real human continuation setting changes')
    factory=factory.replace(before,'"MK2KS_CPU_CONTINUATION_POLICY=\'neutral_hold\'"',1)
    scope=dict(previous.prepare.__globals__)
    exec(compile(factory,__file__+'::same_full_collector_different_real_buttons','exec'),scope)
    original=scope['prepare'](state)['capture']
    need(not original.__closure__, 'Whole original collector namespace')
    bound=dict(original.__globals__,BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,
        normalize=normalize,__file__=__file__)
    decoder=bound['decode_audio']
    bound['decode_audio']=FunctionType(decoder.__code__,dict(decoder.__globals__,AUDIO=AUDIO,KEY=KEY),
        decoder.__name__,decoder.__defaults__)
    bound['capture']=FunctionType(original.__code__,bound,original.__name__,original.__defaults__)
    return bound


def execute(state,preflight=False):
    global SCOPE
    need(not BASE.exists() and not OUT.exists() and not parent.census.identity.census(),
         'Fresh distinct actual movement trial, all older native games terminal')
    original=parent.owners.arithmetic.previous.binding.capture.NATIVE_HANDLES[
        parent.owners.arithmetic.previous.binding.capture.KEY]
    need(original['process'].poll()==0 and original['identity']['ProcessId']==35924,
         'Previous actual handle terminal, never retry after observation timeout')
    proof=json.loads(parent.OUT.read_text());pins=dict(proof['inputHashes'])
    need(proof['passed'] and all(sha(p)==h for p,h in pins.items()) and sync.verify()['passed'],
         'Whole prior source/native proof, all compiled inputs and fixed public/private endpoints')
    for p in (Path(__file__),LUA,Path(snapshot.__file__),Path(previous.__file__),Path(parent.__file__),parent.OUT,
              ROOT/'mk2ks_native_selector_sonya_pressure_snapshot.lua'):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h, 'No prior source or evidence rewritten');pins[key]=h
    lua=LUA.read_text()
    need(lua.count("io.open('mk2ks_native_selector_sonya_cpu_pressure_bound.lua','rb')")==1 and
         'walk_periodic_jump' in lua and not re.search(r':write_[ui]\d+|\.value\s*=(?!=)|load_?state',lua),
         'One genuine human controller, only passive native observers')
    SCOPE=prepare(state)
    guest,gfx,build,gfx32,payload=(state[k] for k in ('guest','gfx','build','gfx32','payload'))
    native,_,_,decode=SCOPE['bindings'](guest,build)
    expected_rom,_=previous.base.original.audio_model.expected_region(pins)
    if preflight:return dict(passed=True,preflightOnly=True,inputHashes=pins,newNativeGames=0,fullPortAcceptance=False)
    AUDIO[KEY]=dict(pcmChunks=[],pcmHeaders=[],dacChunks=[],dacHeaders=[],
        rom={p:bytearray() for p in ('startup','terminal')},expectedROM=expected_rom,audioGuestObserved=False)
    def check(bundle,guest,payload,gfx32):
        whole=previous.base.choices.native_state.gate(bundle['cpuLog'],guest)
        choices=previous.base.choices.choices_gate(bundle['cpuLog'],guest,whole['schedule'])
        return dict(wholeNativeHealthState=whole,allActuallyObservedChoices=choices,
                    airApproachContactQualificationPending=True,fullPortAcceptance=False)
    report=SCOPE['capture']('real_air_approach',2,guest,gfx,gfx32,payload,native,check,decode,pins)
    handle=NATIVE_HANDLES[KEY]
    need(handle['process'].poll()==report['nativeExit'], 'Original actual new game handle really terminal')
    if report['passed']:
        folder,text,images=RAM_CASES[KEY]
        need(text!=previous.RAM_CASES[previous.KEY][1] and 'MK2_CPU_PAIR_AIR_INPUT ' in text,
             'Genuinely different actual control/gameplay history, not accepted-case continuity replay')
        need(len(DISPLAY['rgb'])==1800 and
             [int(h['frame']) for h in DISPLAY['rgbHeaders'].values()]==list(range(1818,3618)),
             'Every actual dense display callback, no nonexistent terminal frame_done')
        for p in folder.rglob('*'):
            if p.is_file():pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()), 'Whole current source and original/new native pins intact')
    value=dict(passed=report['passed'],goalStatus='active',actualNativeIdentity=handle['identity'],
        nativeExit=report['nativeExit'],originalCaptureError=report.get('error'),originalCapture=report,
        actualDenseDisplayCallbacks=len(DISPLAY['rgb']),actualDisplayBuffers=len(DISPLAY['buffers']),
        actualSourceGraphics=len(DISPLAY['gfx']),inputHashes=pins,
        requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        actualCompletedBicycleContactAccepted=False,wholeDisplayedPixelsAccepted=False,
        wholeSourceAudioAccepted=False,allArenaContextsAccepted=False,fullPortAcceptance=False,
        publicPlayableChanged=False,newNativeGames=1,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/('report.json' if report['passed'] else 'failure.json')).write_text(json.dumps(value,indent=2)+'\n')
    return value


def safe_execute(state,preflight=False):
    try:return execute(state,preflight)
    except Exception as error:
        need(not OUT.exists(), 'Preserve actual distinct trial rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
