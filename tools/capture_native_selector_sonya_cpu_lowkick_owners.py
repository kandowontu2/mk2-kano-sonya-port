"""New ordinary lowkick/CPU context with actual saved voice-owner observations.

All original independent cold byte proofs, native health/state/choices, dense
display and PCM/DAC/ROM transports retained unchanged in RAM. No build or ROM
copies. No outcome prescribed; missing owner transitions remain missing.
"""
import json,re,traceback
from pathlib import Path
from types import FunctionType
import capture_native_selector_sonya_cpu_air_approach_checked as previous
import seal_native_selector_sonya_cpu_air_channels_horizontal as parent

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
BASE=ROOT/'audit_native_selector_sonya_cpu_lowkick_owners_ram'
OUT=ROOT/'audit_native_selector_sonya_cpu_lowkick_owners_capture_checked'
LUA=ROOT/'mk2ks_native_selector_sonya_cpu_lowkick_owners.lua'
KEY='ordinary_Kano_walk_lowkick_native_Sonya_CPU_actual_voice_owners'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[];AUDIO={};SCOPE=None
DISPLAY=dict(buffers=previous.snapshot.RAMBuffers(),headers={},gfx={},rgb={},rgbHeaders={})


def normalize(line):
    f=previous.snapshot.transport.normalize
    return FunctionType(f.__code__,dict(f.__globals__,DISPLAY=DISPLAY),f.__name__,f.__defaults__)(line)


def prepare(state):
    f=previous.prepare(state)['capture']
    need(not f.__closure__,'Whole original native collector namespace')
    scope=dict(f.__globals__,BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,RAM_CASES=RAM_CASES,
        NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,normalize=normalize,__file__=__file__)
    decoder=scope['decode_audio']
    scope['decode_audio']=FunctionType(decoder.__code__,dict(decoder.__globals__,AUDIO=AUDIO,KEY=KEY),
                                      decoder.__name__,decoder.__defaults__)
    scope['capture']=FunctionType(f.__code__,scope,f.__name__,f.__defaults__)
    need(scope['capture'].__code__ is f.__code__,'Original full collector bytecode unchanged')
    return scope


def execute(state,preflight=False):
    global SCOPE
    need(not BASE.exists() and not OUT.exists() and not parent.previous.census.identity.census(),
         'Fresh missing-owner/different-control capture; no live game restarted')
    old=previous.NATIVE_HANDLES[previous.KEY]
    need(old['process'].poll()==0 and old['identity']['ProcessId']==50372,
         'Previous actual game terminal, never restart on observation timeout')
    need(sha(parent.OUT)=='D5503E6E3DE7C59E235FF1DF35DE99D2EB5D225945CB0CBB16FD79CC554EE2A3',
         'Exact integrated previous evidence receipt intact')
    proof=json.loads(parent.OUT.read_text()); pins=dict(proof['inputHashes'])
    need(proof['passed'] and all(sha(p)==h for p,h in pins.items()) and
         parent.previous.storage.source.verify()['passed'],'All whole current compiled/source/evidence inputs intact')
    for p in (Path(__file__),LUA,parent.OUT,Path(previous.__file__),Path(parent.__file__),
              ROOT/'mk2ks_native_selector_sonya_cpu_pressure.lua',
              ROOT/'mk2ks_native_selector_sonya_pressure_snapshot.lua'):
        key=str(p.resolve()); h=sha(p)
        need(key not in pins or pins[key]==h,'No old executed source rewritten'); pins[key]=h
    lua=LUA.read_text()
    need('MK2_VOICE_OWNER_ITEM' in lua and 'saved.actor:read(slot)' in lua and
         'walk_lowkick' in lua and "fields['P1 Low Kick']:set_value(1)" in lua and
         not re.search(r':write_[ui]\d+|\.value\s*=(?!=)|load_?state|:write\(|:write_block\(',lua),
         'Ordinary physical inputs plus actual read-only saved owner fields, no game/state writes')
    SCOPE=prepare(state)
    guest,gfx,build,gfx32,payload=(state[k] for k in ('guest','gfx','build','gfx32','payload'))
    native,_,_,decode=SCOPE['bindings'](guest,build)
    expected_rom,_=previous.previous.base.original.audio_model.expected_region(pins)
    if preflight:return dict(passed=True,preflightOnly=True,inputHashes=pins,newNativeGames=0,fullPortAcceptance=False)
    AUDIO[KEY]=dict(pcmChunks=[],pcmHeaders=[],dacChunks=[],dacHeaders=[],
        rom={p:bytearray() for p in ('startup','terminal')},expectedROM=expected_rom,audioGuestObserved=False)
    def check(bundle,guest,payload,gfx32):
        ledger=previous.previous.base.choices
        whole=ledger.native_state.gate(bundle['cpuLog'],guest)
        choices=ledger.choices_gate(bundle['cpuLog'],guest,whole['schedule'])
        return dict(wholeNativeHealthState=whole,allActuallyObservedChoices=choices,
                    voiceOwnerQualificationPending=True,fullPortAcceptance=False)
    report=SCOPE['capture']('ordinary_lowkick_actual_voice_owners',2,guest,gfx,gfx32,payload,native,check,decode,pins)
    held=NATIVE_HANDLES[KEY]
    need(held['process'].poll()==report['nativeExit'],'Same actual new handle really terminal, retain original evidence')
    if report['passed']:
        folder,text,images=RAM_CASES[KEY]
        need(text!=previous.RAM_CASES[previous.KEY][1] and 'MK2_CPU_PAIR_LOWKICK_INPUT ' in text,
             'Genuinely different physical/gameplay history, not a replay of an accepted case')
        rows=previous.previous.base.choices.native_state.rows
        items=rows(text,'MK2_VOICE_OWNER_ITEM'); owners=rows(text,'MK2_VOICE_OWNER')
        need(len(items)==5 and {r['field'] for r in items}=={'actor','main','health','id','mode'} and owners and
             {r['phase'] for r in owners}=={'frame','sound','stop'},'Actual saved owner layouts and all observation phases')
        need(len(DISPLAY['rgb'])==1800 and [int(h['frame']) for h in DISPLAY['rgbHeaders'].values()]==list(range(1818,3618)),
             'Entire original dense current display transport retained')
        for p in folder.rglob('*'):
            if p.is_file():pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Full original/new source and native metadata pins unchanged')
    result=dict(passed=report['passed'],goalStatus='active',actualNativeIdentity=held['identity'],
        nativeExit=report['nativeExit'],originalCapture=report,inputHashes=pins,
        actualDenseDisplayCallbacks=len(DISPLAY['rgb']),actualDisplayBuffers=len(DISPLAY['buffers']),
        actualPCMCallbacks=len(AUDIO[KEY]['pcmHeaders']),requirements=proof['requirements'],
        remainingGroups=proof['remainingGroups'],privateOwnerRetirementAccepted=False,
        wholeDisplayedPixelsAccepted=False,wholeSourceAudioAccepted=False,allArenaContextsAccepted=False,
        fullPortAcceptance=False,publicPlayableChanged=False,newNativeGames=1,newBuilds=0,
        newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir(); (OUT/('report.json' if report['passed'] else 'failure.json')).write_text(json.dumps(result,indent=2)+'\n')
    return result


def safe_execute(state,preflight=False):
    try:return execute(state,preflight)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual missing-owner capture rejection')
        OUT.mkdir(); (OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
