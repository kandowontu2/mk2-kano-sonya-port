"""Missing native palette-reference stores, same real pressure controller.

Whole original cold/state/controls/body/shadow/PCM/DAC/sparse-RGB collection.
Only metadata is saved; raw media and sound-ROM bytes remain RAM-only.
"""
import json
import re
import traceback
from pathlib import Path
from types import FunctionType
import capture_native_selector_sonya_pressure_effects as previous
import seal_native_selector_sonya_pressure_blood_metadata as parent
import verify_native_source_sync as sync

ROOT, need, sha = previous.ROOT, previous.need, previous.sha
BASE = ROOT/'audit_native_selector_sonya_pressure_palette_ram'
OUT = ROOT/'audit_native_selector_sonya_pressure_palette_capture_checked'
LUA = ROOT/'mk2ks_native_selector_sonya_pressure_palette.lua'
KEY = 'actual_pressure_native_palette_cache_stores'
RAM_CASES = {}; NATIVE_HANDLES = {}; COMPLETED = []; AUDIO = {}; SCOPE = None


def prepare(state):
    f = previous.prepare(state)['capture']
    need(not f.__closure__, 'Whole original collector namespace preserved')
    scope = dict(f.__globals__, BASE=BASE, OUT=OUT, LUA=LUA, KEY=KEY,
                 RAM_CASES=RAM_CASES, NATIVE_HANDLES=NATIVE_HANDLES,
                 COMPLETED=COMPLETED, AUDIO=AUDIO, __file__=__file__)
    decoder = scope['decode_audio']
    scope['decode_audio'] = FunctionType(decoder.__code__,
        dict(decoder.__globals__, AUDIO=AUDIO, KEY=KEY), decoder.__name__, decoder.__defaults__)
    scope['capture'] = FunctionType(f.__code__, scope, f.__name__, f.__defaults__)
    need(scope['capture'].__code__ is f.__code__, 'Original complete capture bytecode')
    return scope


def execute(state, preflight=False):
    global SCOPE
    need(not BASE.exists() and not OUT.exists() and
         not parent.original.census.identity.census(), 'Fresh missing metadata, no live native job')
    old = previous.NATIVE_HANDLES[previous.KEY]
    need(old['process'].poll()==0 and old['identity']['ProcessId']==45272,
         'Actual prior native handle terminal, never timeout-restarted')
    checkpoint=parent.OUT; proof=json.loads(checkpoint.read_text())
    pins=dict(proof['inputHashes'])
    need(proof['passed'] and all(sha(p)==h for p,h in pins.items()) and sync.verify()['passed'],
         'Whole prior effects, source sync and unchanged public/private endpoints')
    for p in (Path(__file__), LUA, Path(previous.__file__), Path(parent.__file__), checkpoint):
        key=str(p.resolve()); h=sha(p)
        need(key not in pins or pins[key]==h, 'No executed predecessor rewritten'); pins[key]=h
    lua=LUA.read_text()
    need(lua.count("dofile('mk2ks_native_selector_sonya_pressure_effects.lua')")==1 and
         not re.search(r':write_[ui]\d+|\.value\s*=(?!=)|load_?state|set_value',lua),
         'One unchanged physical controller and passive palette metadata only')
    SCOPE=prepare(state)
    guest,gfx,build,gfx32,payload=(state[k] for k in ('guest','gfx','build','gfx32','payload'))
    native,_,_,decode=SCOPE['bindings'](guest,build)
    expected_rom,_=previous.reference.base.original.audio_model.expected_region(pins)
    if preflight:
        return dict(passed=True,preflightOnly=True,inputHashes=pins,newNativeGames=0,fullPortAcceptance=False)
    AUDIO[KEY]=dict(pcmChunks=[],pcmHeaders=[],dacChunks=[],dacHeaders=[],
        rom={p:bytearray() for p in ('startup','terminal')},expectedROM=expected_rom,audioGuestObserved=False)
    def check(bundle,guest,payload,gfx32):
        return dict(wholeOriginalPressureMechanics=previous.mechanics.gate(bundle['cpuLog'],guest),
                    nativePaletteStoreQualificationPending=True,fullPortAcceptance=False)
    report=SCOPE['capture']('native_palette_reference_arithmetic',2,guest,gfx,gfx32,payload,native,check,decode,pins)
    handle=NATIVE_HANDLES[KEY]
    need(report['passed'] and handle['process'].poll()==report['nativeExit']==0,
         'Keep actual new native handle; full ordinary controller/state capture passed')
    folder,text,images=RAM_CASES[KEY]; old_text=previous.RAM_CASES[previous.KEY][1]
    tags=('MK2_EFFECT_','MK2_CPU_PAIR_','MK2_P2CPU_','MK2_CPU_ROUND_',
          'MK2_CPU_OVERLAP_','MK2_KNIFE_PAIR_','MK2_CPU_CHOICE_',
          'MK2_STARTUP_PROJECTILE_','MK2_SONYA_HORIZONTAL_','MK2_MAUDIO_',
          'MK2_TOMB_MIX_','MK2_BBAUDIO_PCM_DIGEST ','MK2_NATIVE_DAC_RAM_DIGEST ','MK2_HPHASE_')
    need([s for s in text.splitlines() if s.startswith(tags)]==
         [s for s in old_text.splitlines() if s.startswith(tags)],
         'Whole prior allocator/Main/FIFO/DMA/control/health/choice/body/shadow/audio chronology identical')
    need(images==previous.RAM_CASES[previous.KEY][2], 'All actual sparse RGB bytes identical')
    for key in ('pcmChunks','pcmHeaders','dacChunks','dacHeaders','rom'):
        need(AUDIO[KEY][key]==previous.AUDIO[previous.KEY][key], 'Entire actual sound evidence identical: '+key)
    need(all('MK2_PAL_'+tag+' ' in text for tag in ('WRITE','OWNER','CACHE','RESULT')),
         'Genuinely missing native palette stores and owners present')
    for p in folder.rglob('*'):
        if p.is_file(): pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()), 'Whole old and actual new source/native pins intact')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=handle['identity'],nativeExit=0,
        originalCapture=report,inputHashes=pins,requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        paletteReferenceArithmeticAccepted=False,allHiddenPaletteOwnersAccepted=False,
        fullPortAcceptance=False,publicPlayableChanged=False,newNativeGames=1,newBuilds=0,
        newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print('PASS missing palette stores captured; whole original history/RGB/audio identical',flush=True)
    return value


def safe_execute(state,preflight=False):
    try: return execute(state,preflight)
    except Exception as error:
        need(not OUT.exists(), 'Preserve actual palette capture failure')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
