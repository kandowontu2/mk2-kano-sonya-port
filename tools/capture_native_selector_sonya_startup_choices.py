"""Newly absent actual Sonya AI decisions; same real accepted guard route.

Original collector/controller bytecode and all native cold/state/HP/audio
observations retained. Only a passive true18 choice observer is added. No
prescribed RNG/choice/opponent/outcome or extra build/ROM/raw-media files.
"""
import hashlib
import json
import re
import traceback
from pathlib import Path
from types import FunctionType
import capture_native_selector_cpu_rings_snapshot_ram as previous
import seal_native_selector_cpu_rings_current_evidence as combined
import verify_native_source_sync as migration

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
BASE=ROOT/'audit_native_selector_sonya_startup_choices_ram'
OUT=ROOT/'audit_native_selector_sonya_startup_choices_capture_checked'
LUA=ROOT/'mk2ks_native_selector_sonya_startup_choices.lua'
KEY='actual_Sonya_AI_choice_source_Kano_human_original_startup_guard'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[];AUDIO={};SCOPE=None
normalize=previous.transport.previous.original.previous.original.physical.normalize


def prepare(state):
    f=previous.prepare
    scope=dict(f.__globals__,BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,RAM_CASES=RAM_CASES,
        NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,normalize=normalize,__file__=__file__)
    return FunctionType(f.__code__,scope,f.__name__,f.__defaults__)(state)


def execute(state,preflight=False):
    global SCOPE
    need(not BASE.exists()and not OUT.exists()and
         not previous.transport.previous.original.previous.choices.current.prior.identity.census(),
         'Original games actually terminal; fresh previously absent actual Sonya AI records')
    held=previous.NATIVE_HANDLES[previous.KEY]
    need(held['process'].poll()==0 and held['identity']['ProcessId']==16764,
         'Retain accepted original three-Ring terminal; no timeout replay')
    path=combined.OUT/'report.json';parent=json.loads(path.read_text());pins=dict(parent['inputHashes'])
    need(parent['passed']and all(sha(p)==h for p,h in pins.items())and migration.verify()['passed'],
         'Whole latest source/native/display/audio/contact inventory intact')
    oldtext=previous.RAM_CASES[previous.KEY][1]
    need(not any(l.startswith('MK2_SONYA_STARTUP_CHOICE_')for l in oldtext.splitlines()),
         'Required actual true Sonya choice observations genuinely absent from completed reference')
    lua=LUA.read_text()
    need(lua.count("dofile('mk2ks_native_selector_cpu_projectile_pcm_startup_direct.lua')")==1 and
         "once('MK2_CPU_CHOICE_%s','MK2_SONYA_STARTUP_CHOICE_%s')"in lua and
         not re.search(r':write_[ui]\d+|\.value\s*=(?!=)|load_?state',lua),
         'One unmodified physical root plus passive source-qualified choice observation')
    for p in (Path(__file__),LUA,path,Path(previous.__file__),
              ROOT/'mk2ks_physical_p2_cpu_choice_trace_v3303.lua'):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'No executed source or evidence changed');pins[key]=h
    SCOPE=prepare(state)
    guest,gfx,build,gfx32,payload=(state[k]for k in ('guest','gfx','build','gfx32','payload'))
    native,_,_,decode=SCOPE['bindings'](guest,build)
    expected_rom,_=previous.transport.previous.original.previous.original.audio_model.expected_region(pins)
    if preflight:return dict(passed=True,preflightOnly=True,inputHashes=pins,newNativeGames=0,fullPortAcceptance=False)
    AUDIO[KEY]=dict(pcmChunks=[],pcmHeaders=[],dacChunks=[],dacHeaders=[],
        rom={p:bytearray()for p in ('startup','terminal')},expectedROM=expected_rom,audioGuestObserved=False)
    def check(bundle,guest,payload,gfx32):
        return dict(wholeNativeStateHealth=previous.physical.gate(bundle['cpuLog'],guest),
                    actualSonyaChoiceQualificationPending=True,fullPortAcceptance=False)
    report=SCOPE['capture']('true_Sonya_startup_choices',2,guest,gfx,gfx32,payload,native,check,decode,pins)
    held=NATIVE_HANDLES[KEY]
    need(held['process'].poll()==report['nativeExit'],'Original exact Popen terminal, never observation-timeout replay')
    need(report['passed'],'Full original native cold/state/health/terminal capture genuinely passes')
    folder,text,_=RAM_CASES[KEY]
    choice=[l for l in text.splitlines()if l.startswith('MK2_SONYA_STARTUP_CHOICE_EVENT ')]
    need(choice,'Actual previously absent true Sonya source-executed AI decisions present')
    tags=('MK2_CPU_PAIR_','MK2_P2CPU_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_',
          'MK2_KNIFE_PAIR_','MK2_CPU_CHOICE_','MK2_STARTUP_PROJECTILE_')
    need([l for l in text.splitlines()if l.startswith(tags)]==[l for l in oldtext.splitlines()if l.startswith(tags)],
         'Every original actual input/HP/state/identity/projectile history unchanged by passive observer')
    for p in (folder/'result.json',*(p for p in folder.rglob('*')if p.is_file())):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Whole current immutable collector/source/native evidence inventory')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=report['nativeExit'],
        actualSonyaChoiceEvents=len(choice),wholeOriginalPhysicalChronologyUnchanged=True,
        originalNativeCapture=report,requirements=parent['requirements'],remainingGroups=parent['remainingGroups'],
        inputHashes=pins,allChoiceMechanicsAccepted=False,allArenaCPUContextsAccepted=False,fullPortAcceptance=False,
        publicPlayableChanged=False,newNativeGames=1,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print('PASS actual true Sonya AI observation capture; full mechanics qualification separately required',flush=True)
    return value


def safe_execute(state,preflight=False):
    try:return execute(state,preflight)
    except Exception as error:
        need(not OUT.exists(),'Keep actual new source-choice capture failure')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
