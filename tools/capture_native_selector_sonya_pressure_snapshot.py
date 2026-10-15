"""Genuinely absent current pixels for full retained pressure trajectory.

Single unchanged real controller. Complete original native FIFO/CPU/DMA/flip/
palette/VRAM observer across ALL1801 callbacks, not a sparse green subset.
Whole raw drawing buffers are losslessly compressed in RAM, never on disk.
No guest/CPU/HP/RNG/state writes, new build, media or ROM copies.
"""
import hashlib
import json
import re
import traceback
import zlib
from collections.abc import MutableMapping
from pathlib import Path
from types import FunctionType
import capture_native_selector_sonya_cpu_pressure_bound as reference
import capture_native_selector_walkin_knife_display_ram as transport
import qualify_native_selector_sonya_cpu_pressure_interrupt as mechanics
import seal_native_selector_sonya_cpu_pressure_audio as parent
import verify_native_source_sync as migration

ROOT,need,sha=reference.ROOT,reference.need,reference.sha
BASE=ROOT/'audit_native_selector_sonya_pressure_snapshot_ram'
OUT=ROOT/'audit_native_selector_sonya_pressure_snapshot_capture_checked'
LUA=ROOT/'mk2ks_native_selector_sonya_pressure_snapshot.lua'
KEY='same_real_Kano_pressure_Sonya_CPU_whole_current_snapshot_1818_3618'
PARENT=parent.OUT
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[];AUDIO={};SCOPE=None


class RAMBuffers(MutableMapping):
    """Every distinct header/key preserved; exact original bytes on access."""
    def __init__(self):self.blocks={}
    def __getitem__(self,key):return zlib.decompress(self.blocks[key])
    def __setitem__(self,key,value):self.blocks[key]=zlib.compress(value,1)
    def __delitem__(self,key):del self.blocks[key]
    def __iter__(self):return iter(self.blocks)
    def __len__(self):return len(self.blocks)


DISPLAY=dict(buffers=RAMBuffers(),headers={},gfx={},rgb={},rgbHeaders={})


def normalize(line):
    f=transport.normalize
    scope=dict(f.__globals__,DISPLAY=DISPLAY)
    return FunctionType(f.__code__,scope,f.__name__,f.__defaults__)(line)


def prepare(state):
    collector=reference.prepare(state)
    f=collector['capture']
    need(not f.__closure__,'Whole original pressure collector has no hidden capture namespace')
    scope=dict(f.__globals__,BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,RAM_CASES=RAM_CASES,
        NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,normalize=normalize,__file__=__file__)
    decoder=scope['decode_audio']
    need(not decoder.__closure__,'Whole original sound decoder has no hidden alternate state')
    scope['decode_audio']=FunctionType(decoder.__code__,dict(decoder.__globals__,AUDIO=AUDIO,KEY=KEY),
                                     decoder.__name__,decoder.__defaults__)
    scope['capture']=FunctionType(f.__code__,scope,f.__name__,f.__defaults__)
    need(scope['capture'].__code__ is f.__code__ and scope['capture'].__globals__['normalize'] is normalize,
         'Entire original physical/cold/audio collector bytecode, new passive display namespace only')
    return scope


def execute(state,preflight=False):
    global SCOPE
    need(not BASE.exists()and not OUT.exists()and not reference.base.choices.current.prior.identity.census(),
         'Fresh truly missing current snapshot evidence; original accepted native jobs terminal')
    old=reference.NATIVE_HANDLES[reference.KEY]
    need(old['process'].poll()==0 and old['identity']['ProcessId']==44780,
         'Original exact44780 terminal, never restart because an observation timed out')
    proof=json.loads(PARENT.read_text());pins=dict(proof['inputHashes'])
    need(proof['passed']and all(sha(p)==h for p,h in pins.items())and migration.verify()['passed'],
         'Whole original pressure geometry/audio, current compiled inputs and public endpoints unchanged')
    for p in (Path(__file__),LUA,PARENT,Path(reference.__file__),Path(transport.__file__),Path(mechanics.__file__),
              ROOT/'mk2ks_human_projectile_full_display_v1289.lua',
              ROOT/'mk2ks_native_selector_sonya_cpu_pressure_bound.lua'):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'Never replace executed source/evidence pins');pins[key]=h
    lua=LUA.read_text()
    need(lua.count("dofile('mk2ks_native_selector_sonya_cpu_pressure_bound.lua')")==1 and
         'f<=origin+1801'in lua and 'snapshot_pixels()'in lua and 'snapshot_size()'in lua and
         not re.search(r':write_[ui]\d+|\.value\s*=(?!=)|load_?state',lua),
         'One unchanged physical driver, whole dense current snapshots and passive original display observer')
    SCOPE=prepare(state)
    guest,gfx,build,gfx32,payload=(state[k]for k in ('guest','gfx','build','gfx32','payload'))
    native,_,_,decode=SCOPE['bindings'](guest,build)
    expected_rom,_=reference.base.original.audio_model.expected_region(pins)
    # Test lossless storage and namespace isolation before any native process.
    test=RAMBuffers();sample=bytes(range(256))*2048;test['entire']=sample
    need(test['entire']==sample and len(test)==1 and len(test.blocks['entire'])<len(sample),
         'Complete524288-byte lossless volatile storage; no dropped or duplicated bytes')
    if preflight:return dict(passed=True,preflightOnly=True,inputHashes=pins,newNativeGames=0,fullPortAcceptance=False)
    AUDIO[KEY]=dict(pcmChunks=[],pcmHeaders=[],dacChunks=[],dacHeaders=[],
        rom={p:bytearray()for p in ('startup','terminal')},expectedROM=expected_rom,audioGuestObserved=False)
    def check(bundle,guest,payload,gfx32):
        return dict(wholeOriginalPressureMechanics=mechanics.gate(bundle['cpuLog'],guest),
                    currentDisplayedPixelQualificationPending=True,fullPortAcceptance=False)
    report=SCOPE['capture']('whole_Sonya_pressure_current_snapshot',2,guest,gfx,gfx32,payload,native,check,decode,pins)
    held=NATIVE_HANDLES[KEY]
    need(held['process'].poll()==report['nativeExit'],'Same original new capture handle truly terminal; retain it')
    if report['passed']:
        folder,text,images=RAM_CASES[KEY];old_text=reference.RAM_CASES[reference.KEY][1]
        tags=('MK2_CPU_PAIR_','MK2_P2CPU_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_',
              'MK2_KNIFE_PAIR_','MK2_CPU_CHOICE_','MK2_STARTUP_PROJECTILE_',
              'MK2_SONYA_HORIZONTAL_','MK2_MAUDIO_','MK2_TOMB_MIX_',
              'MK2_BBAUDIO_PCM_DIGEST ','MK2_NATIVE_DAC_RAM_DIGEST ','MK2_HPHASE_')
        need([l for l in text.splitlines()if l.startswith(tags)]==
             [l for l in old_text.splitlines()if l.startswith(tags)],
             'Every original input/state/HP/choices/body-shadow/PCM/DAC/channel event identical, no prescribed outcome')
        frames=list(range(1818,3619))
        rows=reference.base.choices.native_state.rows
        dma_frames=sorted({int(r['frame'])for r in rows(text,'MK2_NAT_CAMPAIGN_FLOOR_DMA')
                           if 1817<=int(r['frame'])<=3617})
        pre=rows(text,'MK2_NAT_CAMPAIGN_FLOOR_PRE_FRAME')
        need([int(r['frame'])for r in pre]==dma_frames,
             'Every first native DMA before each requested next callback has one complete independent prepass')
        expected={'guest_maincpu.bin','display_base.bin'}
        expected.update('display_pre_%d.bin'%f for f in dma_frames)
        expected.update('display_%s_%d.bin'%(kind,f)for f in frames for kind in ('vram','palette'))
        need([int(h['frame'])for h in DISPLAY['rgbHeaders'].values()]==frames and
             set(DISPLAY['buffers'])==expected and DISPLAY['gfx'],
             'Every dense live/nonlive callback and all source-scheduled VRAM/palette/prepass buffers; no guessed count')
    need(all(sha(p)==h for p,h in pins.items()),'Every complete original and new observer pin intact')
    value=dict(passed=report['passed'],goalStatus='active',nativeExit=report['nativeExit'],error=report.get('error'),
        actualNativeIdentity=held['identity'],inputHashes=pins,requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        wholeOriginalTrajectoryUnchanged=bool(report['passed']),wholeCurrentSnapshotCallbacks=len(DISPLAY['rgb']),
        volatileBuffers=len(DISPLAY['buffers']),volatileStoredBytes=sum(len(v)for v in DISPLAY['buffers'].blocks.values()),
        actualGFXStreams=len(DISPLAY['gfx']),displayBufferHeaders=DISPLAY['headers'],rgbHeaders=DISPLAY['rgbHeaders'],
        independentRendererAccepted=False,fullPortAcceptance=False,publicPlayableChanged=False,
        newNativeGames=1,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/('report.json'if report['passed']else'failure.json')).write_text(json.dumps(value,indent=2)+'\n')
    print('Whole actual pressure current snapshot capture '+('PASS'if report['passed']else'FAIL'),flush=True)
    return value


def safe_execute(state,preflight=False):
    try:return execute(state,preflight)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual complete snapshot preflight/capture rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
