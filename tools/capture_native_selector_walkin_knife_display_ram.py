"""Same physical route, newly complete actual Knife FIFO/DMA/scanout evidence.

Clone the existing full current capture bytecode into fresh data bindings;
original controls, five cold proofs, sound, exact identity and terminal-first
behavior remain unchanged. Added native display buffers stay solely in RAM.
This collector alone is NOT independent renderer or complete-port acceptance.
"""
import hashlib
import json
import re
import traceback
from pathlib import Path
from types import FunctionType
import numpy as np
import capture_native_selector_sonya_walkin_kano_cpu as previous

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
BASE=ROOT/'audit_native_selector_walkin_knife_display_ram'
OUT=ROOT/'audit_native_selector_walkin_knife_display_capture_checked'
LUA=ROOT/'mk2ks_native_selector_walkin_knife_display_ram.lua'
KEY='original_sonya_walkin_kano_CPU_complete_Knife_display'
PARENT=ROOT/'audit_native_selector_sonya_walkin_knife_pool_operand_checked/report.json'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[];AUDIO={}
DISPLAY=dict(buffers={},headers={},gfx={},rgb={},rgbHeaders={})
SCOPE=None


def normalize(line):
    if line.startswith(('MK2_PROJECTILE_RAM ','MK2_PROJECTILE_RGB ')):
        tag=line.split()[0];pairs=re.findall(r'(\w+)=([^\s]+)',line);h=dict(pairs)
        need(len(pairs)==len(h),'Unique complete native display metadata')
        raw=bytes.fromhex(h.pop('hex'))
        need(len(raw)==int(h['bytes']) and h['writes']=='0' and h['assistance']=='none',
             'Entire RAM-only native display transport, no raw files')
        file=h['file'];need(Path(file).name==file,'Only declared volatile buffer keys')
        digest=hashlib.sha256(raw).hexdigest().upper()
        if tag=='MK2_PROJECTILE_RAM':
            need(file not in DISPLAY['buffers'],'One original independent buffer per declared filename')
            DISPLAY['buffers'][file]=raw;DISPLAY['headers'][file]=dict(h,sha256=digest)
        else:
            need(h['width']=='400' and h['height']=='254' and len(raw)==406400 and file not in DISPLAY['rgb'],
                 'Complete original unscaled400x254 native RGB buffer')
            DISPLAY['rgb'][file]=np.frombuffer(raw,np.uint8).reshape(254,400,4)[:,:,2::-1].copy()
            DISPLAY['rgbHeaders'][file]=dict(h,sha256=digest)
        return tag+'_DIGEST '+' '.join(k+'='+str(v) for k,v in h.items())+' sha256='+digest+'\n'
    if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_GFX '):
        pairs=re.findall(r'(\w+)=([^\s]+)',line);h=dict(pairs)
        need(len(pairs)==len(h) and h['key'] not in DISPLAY['gfx'],'Unique actual native DMA graphics stream')
        raw=bytes.fromhex(h.pop('data'));need(len(raw)==int(h['bytes']),'Entire native graphics stream')
        DISPLAY['gfx'][h['key']]=dict(h,raw=raw,sha256=hashlib.sha256(raw).hexdigest().upper())
        return 'MK2_NAT_CAMPAIGN_FLOOR_GFX_DIGEST '+' '.join(k+'='+str(v) for k,v in h.items())+' sha256='+DISPLAY['gfx'][h['key']]['sha256']+'\n'
    return previous.original.previous.original.physical.normalize(line)


def prepare(state):
    collector=previous.prepare(state)
    scope=dict(collector['capture'].__globals__,BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,
        AUDIO=AUDIO,normalize=normalize,__file__=__file__)
    decode=scope['decode_audio']
    need(not decode.__closure__,'Original complete audio decoder has no hidden alternate capture bindings')
    scope['decode_audio']=FunctionType(decode.__code__,dict(decode.__globals__,AUDIO=AUDIO,KEY=KEY),
                                     decode.__name__,decode.__defaults__)
    function=collector['capture']
    need(not function.__closure__,'Original physical capture bytecode has no hidden alternate data bindings')
    scope['capture']=FunctionType(function.__code__,scope,function.__name__,function.__defaults__)
    need(scope['capture'].__code__ is function.__code__,'Exact entire original full physical transport bytecode')
    return scope


def execute(state,preflight=False):
    global SCOPE
    need(not BASE.exists() and not OUT.exists() and not previous.original.previous.choices.current.prior.identity.census(),
         'Fresh additional passive display capture; original27520 terminal, never timeout replay')
    need(previous.NATIVE_HANDLES[previous.KEY]['process'].poll()==0,'Original physical reference genuinely terminal')
    parent=json.loads(PARENT.read_text());pins=dict(parent['inputHashes'])
    need(parent['passed'] and all(sha(p)==d for p,d in pins.items()),'Entire preceding source and physical/pool proof unchanged')
    SCOPE=prepare(state)
    # Resolve the unchanged decoder and candidate before a native process exists.
    guest,gfx,build,gfx32,payload=(state[k] for k in ('guest','gfx','build','gfx32','payload'))
    native,_,_,decode=SCOPE['bindings'](guest,build)
    need(native.NAME==previous.original.previous.choices.current.startup.NAME and guest==state['WINDOWS']['high'],
         'Exact complete independent current candidate, no new initializer/build/ROM')
    for path in (Path(__file__).resolve(),LUA,ROOT/'mk2ks_human_projectile_full_display_v1289.lua',PARENT):
        digest=sha(path);key=str(path.resolve());need(key not in pins or pins[key]==digest,'No executed old source/evidence changed');pins[key]=digest
    lua=LUA.read_text()
    need("dofile('mk2ks_native_selector_sonya_human_kano_cpu.lua')" in lua and
         "once(\"dofile('mk2ks_human_special_matrix_v3.lua')\"" in lua and
         'MK2_PROJECTILE_RAM' in lua and 'MK2_PROJECTILE_RGB' in lua and
         "once('screen:snapshot(file)'" in lua,
         'Declared one unchanged physical driver and RAM-only full native observer adapter')
    expected_rom,_=previous.original.previous.original.audio_model.expected_region(pins)
    if preflight:
        return dict(passed=True,preflightOnly=True,completeOriginalCaptureBytecodeRetained=True,
                    inputHashes=pins,newNativeGames=0,fullPortAcceptance=False)
    AUDIO[KEY]=dict(pcmChunks=[],pcmHeaders=[],dacChunks=[],dacHeaders=[],
        rom={p:bytearray() for p in ('startup','terminal')},expectedROM=expected_rom,audioGuestObserved=False)
    def check(bundle,guest,payload,gfx32):
        return dict(wholeNativeStateHealthChoices=previous.original.gate(bundle['cpuLog'],guest),
                    completeDisplayQualificationPending=True,fullPortAcceptance=False)
    report=SCOPE['capture']('walkin_knife_display',2,guest,gfx,gfx32,payload,native,check,decode,pins)
    held=NATIVE_HANDLES[KEY]
    need(held['process'].poll()==report['nativeExit'] and not previous.original.previous.choices.current.prior.identity.census(),
         'Same original additional native process genuinely terminal')
    if report['passed']:
        folder,text,_=RAM_CASES[KEY]
        reference=previous.RAM_CASES[previous.KEY][1]
        tags=('MK2_CPU_PAIR_','MK2_P2CPU_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_',
              'MK2_KNIFE_PAIR_','MK2_CPU_CHOICE_','MK2_STARTUP_PROJECTILE_')
        actual=[s for s in text.splitlines() if s.startswith(tags)]
        old=[s for s in reference.splitlines() if s.startswith(tags)]
        need(actual==old,'Every original physical input/identity/health/state/projectile/pool event unchanged by added passive display observation')
        need(len(DISPLAY['rgb'])>100 and len(DISPLAY['buffers'])>300 and DISPLAY['gfx'],
             'Complete additional native drawing, independent buffers and original sampled scanouts actually captured')
    need(all(sha(p)==d for p,d in pins.items()),'Full executed source/evidence inventory unchanged')
    receipt=dict(passed=report['passed'],originalCaptureError=report.get('error'),goalStatus='active',
        actualNativeIdentity=held['identity'],nativeExit=report['nativeExit'],inputHashes=pins,
        requirements=parent['requirements'],remainingGroups=parent['remainingGroups'],
        wholeOriginalPhysicalChronologyUnchanged=bool(report['passed']),
        displayBuffers=len(DISPLAY['buffers']),wholeNativeRGBCallbacks=len(DISPLAY['rgb']),
        actualDMAStreams=len(DISPLAY['gfx']),displayBufferHeaders=DISPLAY['headers'],
        originalRGBHeaders=DISPLAY['rgbHeaders'],newNativeGames=1,newBuilds=0,newROMCopies=0,
        newRawMediaFiles=0,newZIPs=0,publicPlayableChanged=False,independentRendererAccepted=False,fullPortAcceptance=False)
    OUT.mkdir();(OUT/('report.json' if report['passed'] else 'failure.json')).write_text(json.dumps(receipt,indent=2)+'\n')
    print('Additional complete Knife display transport '+('PASS' if receipt['passed'] else 'FAIL'),flush=True)
    return receipt


def safe_execute(state,preflight=False):
    try:
        return execute(state,preflight)
    except Exception as error:
        need(not OUT.exists(),'Preserve original additional capture rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
