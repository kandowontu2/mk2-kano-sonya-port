"""Three actually chosen Sonya Rings, newly absent full display evidence.

Reuse original startup guard route/capture bytecode. No forced CPU, RNG,
HP, position, outcome or state writes. Native full RGB/VRAM/GFX/PCM RAM only.
"""
import hashlib
import json
import re
from pathlib import Path
from types import FunctionType,SimpleNamespace
import capture_native_selector_cpu_projectile_pcm_startup_direct as reference
import capture_native_selector_walkin_knife_display_ram as transport
import qualify_native_selector_natural_state_health_bound as physical
import verify_native_source_sync as migration

ROOT,need,sha=transport.ROOT,transport.need,transport.sha
BASE=ROOT/'audit_native_selector_cpu_rings_snapshot_ram'
OUT=ROOT/'audit_native_selector_cpu_rings_snapshot_capture_checked'
LUA=ROOT/'mk2ks_native_selector_cpu_rings_snapshot_ram.lua'
KEY='three_natural_sonya_CPU_rings_Kano_human_original_guard_start'
PARENT=ROOT/'audit_native_selector_walkin_knife_snapshot_sealed/report.json'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[];AUDIO={};SCOPE=None
DISPLAY={n:dict(buffers={},headers={},gfx={},rgb={},rgbHeaders={})for n in (1,2,3)}


def normalize(line):
    if line.startswith(('MK2_PROJECTILE_RAM ','MK2_PROJECTILE_RGB ','MK2_NAT_CAMPAIGN_FLOOR_GFX ')):
        fields=dict(re.findall(r'(\w+)=([^\s]+)',line));window=int(fields['window'])
        need(window in DISPLAY,'Exactly three declared independent actual display observers')
        f=transport.normalize
        scope=dict(f.__globals__,DISPLAY=DISPLAY[window])
        return FunctionType(f.__code__,scope,f.__name__,f.__defaults__)(line)
    return transport.previous.original.previous.original.physical.normalize(line)


def prepare(state):
    f=reference.SCOPE['functions'];scope=dict(f.__globals__,BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,__file__=__file__)
    decoder=reference.SCOPE['decode_audio']
    scope['decode_audio']=FunctionType(decoder.__code__,dict(decoder.__globals__,AUDIO=AUDIO,KEY=KEY),
                                     decoder.__name__,decoder.__defaults__)
    scope['physical']=SimpleNamespace(**dict(vars(scope['physical']),normalize=normalize))
    factory=FunctionType(f.__code__,scope,f.__name__,f.__defaults__)
    need(factory.__code__ is f.__code__,'Whole original physical collector factory bytecode')
    collector=factory(state)
    need(collector['capture'].__globals__['normalize'] is normalize and
         collector['capture'].__globals__['KEY']==KEY,'Actual original complete collector uses new RAM namespace only')
    return collector


def execute(state,preflight=False):
    global SCOPE
    need(not BASE.exists()and not OUT.exists()and not transport.previous.original.previous.choices.current.prior.identity.census(),
         'Original accepted jobs terminal; fresh genuinely absent three-shot displayed data, no timeout replay')
    held=reference.NATIVE_HANDLES[reference.KEY]
    need(held['process'].poll()==0 and held['identity']['ProcessId']==46264,
         'Retained original startup/audio/state reference really terminal')
    parent=json.loads(PARENT.read_text());pins=dict(parent['inputHashes'])
    need(parent['passed']and all(sha(p)==h for p,h in pins.items()),'All whole current source/evidence pins unchanged')
    need(migration.verify()['passed'],'Complete current compiled source and explicit old-pin preservation')
    SCOPE=prepare(state)
    guest,gfx,build,gfx32,payload=(state[k]for k in ('guest','gfx','build','gfx32','payload'))
    native,_,_,decode=SCOPE['bindings'](guest,build)
    need(native.NAME==transport.previous.original.previous.choices.current.startup.NAME and guest==state['WINDOWS']['high'],
         'Entire same independently reconstructed current candidate and full cold windows')
    for path in (Path(__file__),LUA,PARENT,Path(reference.__file__),ROOT/'mk2ks_human_projectile_full_display_v1289.lua',
                 ROOT/'tools/qualify_native_selector_natural_state_health.py',Path(physical.__file__)):
        key=str(path.resolve());h=sha(path);need(key not in pins or pins[key]==h,'No executed source/evidence edits');pins[key]=h
    lua=LUA.read_text()
    need(lua.count("dofile('mk2ks_native_selector_cpu_projectile_pcm_startup_direct.lua')")==1 and
         'for window=1,3 do' in lua and '0xfffc7000' in lua and 'snapshot_pixels()' in lua and
         'snapshot_size()' in lua and 'admission_count~=WINDOW_TOKEN' in lua and
         not re.search(r':write_[ui]\d+|\.value\s*=(?!=)|load_?state',lua),
         'Single unchanged driver, three source-bound child observers and genuine current rendered RAM snapshots')
    expected_rom,_=transport.previous.original.previous.original.audio_model.expected_region(pins)
    if preflight:return dict(passed=True,preflightOnly=True,inputHashes=pins,newNativeGames=0,fullPortAcceptance=False)
    AUDIO[KEY]=dict(pcmChunks=[],pcmHeaders=[],dacChunks=[],dacHeaders=[],
        rom={p:bytearray()for p in ('startup','terminal')},expectedROM=expected_rom,audioGuestObserved=False)
    def check(bundle,guest,payload,gfx32):
        return dict(wholeNativeStateHealth=physical.gate(bundle['cpuLog'],guest),fullRingRasterQualificationPending=True,
                    fullPortAcceptance=False)
    report=SCOPE['capture']('three_CPU_rings_snapshot',2,guest,gfx,gfx32,payload,native,check,decode,pins)
    held=NATIVE_HANDLES[KEY]
    need(held['process'].poll()==report['nativeExit'],'Actual original native handle terminal; retain it')
    if report['passed']:
        folder,text,_=RAM_CASES[KEY];old=reference.RAM_CASES[reference.KEY][1]
        tags=('MK2_CPU_PAIR_','MK2_P2CPU_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_',
              'MK2_KNIFE_PAIR_','MK2_CPU_CHOICE_','MK2_STARTUP_PROJECTILE_')
        need([l for l in text.splitlines()if l.startswith(tags)]==[l for l in old.splitlines()if l.startswith(tags)],
             'Every physical input/state/HP/owned projectile/retirement event equals original; no prescribed outcome')
        need(all(len(d['rgb'])==106 and len(d['buffers'])>300 and d['gfx']for d in DISPLAY.values()),
             'All three actually observed full source/VRAM/palette/current RGB windows present')
    need(all(sha(p)==h for p,h in pins.items()),'Whole current native/source/evidence inventory unchanged')
    receipt=dict(passed=report['passed'],nativeExit=report['nativeExit'],error=report.get('error'),
        goalStatus='active',actualNativeIdentity=held['identity'],inputHashes=pins,
        requirements=parent['requirements'],remainingGroups=parent['remainingGroups'],
        wholeOriginalPhysicalChronologyUnchanged=bool(report['passed']),
        windows={n:dict(buffers=len(d['buffers']),gfxStreams=len(d['gfx']),rgbFrames=len(d['rgb']),
                       headers=d['headers'],rgbHeaders=d['rgbHeaders'])for n,d in DISPLAY.items()},
        independentRendererAccepted=False,fullPortAcceptance=False,publicPlayableChanged=False,
        newNativeGames=1,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/('report.json'if report['passed']else'failure.json')).write_text(json.dumps(receipt,indent=2)+'\n')
    print('Three current native CPU Ring snapshot capture '+('PASS'if report['passed']else'FAIL'),flush=True)
    return receipt
