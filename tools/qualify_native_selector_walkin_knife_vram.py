"""Same terminal capture, full saved-pass source/ownership/VRAM qualification.

The screen:pixels adapter reads m_curbitmap AFTER update_quads swaps it; it
is not snapshot/current texture evidence. Preserve that actual RGB rejection.
This proves every recorded VRAM word, never substitutes raw bitmap for displayed
pixels, and leaves proper scanout plus unsaved inter-pass erasure open.
"""
import copy
import hashlib
import inspect
import json
import traceback
from pathlib import Path
import numpy as np
import qualify_native_selector_walkin_knife_display_face_rows as names

original=names.original
capture=original.capture
ROOT,need,sha=names.ROOT,names.need,names.sha
OUT=ROOT/'audit_native_selector_walkin_knife_vram_checked'


def vram_rectangle(image,raw,palette,start,control,tap):
    need(image.shape==(254,400,3) and len(raw)==524288 and len(palette)==131072,
         'Entire recorded VRAM/palette and raw bitmap sizes; not a displayed RGB comparison')
    address=start if control&0x400 else start^0xfffc
    row=(address>>4)&511;column=((((address&0x7c)<<4)|(tap&0x3fff))*2)&511
    need(row+254<=512 and column+400<=512 and start&3==0,'Actual nonwrapped latched VRAM rectangle')
    return dict(row=row,column=column,pixels=0)


def renderer(text,display):
    function=original.bindings(text,display)
    scope=dict(function.__globals__,check_latch=vram_rectangle)
    from types import FunctionType
    return FunctionType(function.__code__,scope,function.__name__,function.__defaults__)


def verify_transport(display):
    for file,raw in display['buffers'].items():
        header=display['headers'][file]
        need(len(raw)==int(header['bytes']) and hashlib.sha256(raw).hexdigest().upper()==header['sha256'],
             'Every original whole RAM drawing buffer digest')
    for file,rgb in display['rgb'].items():
        h=display['rgbHeaders'][file];raw=np.empty((254,400,4),np.uint8);raw[:,:,:3]=rgb[:,:,::-1]
        matches=[]
        for alpha in (0,255):
            raw[:,:,3]=alpha
            if hashlib.sha256(raw.tobytes()).hexdigest().upper()==h['sha256']:matches.append(alpha)
        need(len(matches)==1,'Every full original raw bitmap callback digest')
    return len(display['buffers']),len(display['rgb'])


def graphics(display,image):
    for r in display['gfx'].values():
        raw=r['raw'];first=int(r['first'])
        need(len(raw)==int(r['bytes']) and hashlib.sha256(raw).hexdigest().upper()==r['sha256'],
             'Every actually drawn packed source stream digest')
        need(raw==image[first:first+len(raw)],'Every actual packed source equals complete independent initialized graphics')


def positive(folder,text,display,image,state):
    verify_transport(display);graphics(display,image)
    groups,*_=original.data(text,display)
    owned=original.ownership(groups,state['payload'],state['guest'])
    value=renderer(text,display)(folder)
    need(value['frames']==106==len(display['rgb']) and all(
        r['vram_mismatches']==r['displayed_mismatches']==r['shadow_mismatches']==0 for r in value['records']),
        'Every whole independently replayed saved pass VRAM word exact')
    need(value['cpu_writes']==0,'This actual window contains zero CPU VRAM writes; do not infer CPU-write coverage')
    return value,owned


def execute(state):
    need(not OUT.exists(),'Fresh additive original VRAM evidence')
    failure=names.OUT/'failure.json';failed=json.loads(failure.read_text())
    need(not failed['passed'] and failed['error']==
         "ValueError('Every screenshot pixel matches the actual newly displayed VRAM and palette')",
         'Keep original screen-pixels versus displayed-texture failure unchanged')
    parent_path=capture.OUT/'report.json';parent=json.loads(parent_path.read_text())
    held=capture.NATIVE_HANDLES[capture.KEY]
    need(parent['passed'] and held['process'].poll()==parent['nativeExit']==0 and
         held['identity']==parent['actualNativeIdentity'],'Same actual original terminal game, no replay')
    pins=dict(parent['inputHashes']);need(all(sha(p)==d for p,d in pins.items()),'All original whole pins unchanged')
    image=names.runtime_graphics(state,pins);folder,text,_=capture.RAM_CASES[capture.KEY]
    display=capture.DISPLAY
    value,owned=positive(folder,text,display,image,state)
    faults=[]
    def reject(label,action):
        try:action()
        except (ValueError,AssertionError) as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Actual effective counterexample accepted: '+label)
    for label,first in (('wrong_source_name',0x1e00000),('wrong_source_knife_intro',0x1e04000),
                        ('wrong_source_knife_flight',0x1e60000)):
        changed=bytearray(image);changed[first]^=1
        reject(label,lambda:graphics(display,changed));graphics(display,image)
    for label,file in (('changed_original_prepass','display_pre_2256.bin'),
                       ('changed_original_target','display_vram_2257.bin'),
                       ('changed_original_palette','display_palette_2257.bin')):
        changed=dict(display,buffers=dict(display['buffers']));raw=bytearray(changed['buffers'][file]);raw[0]^=1
        changed['buffers'][file]=bytes(raw)
        reject(label,lambda:verify_transport(changed));verify_transport(display)
    for file in ('display_pre_2256.bin','display_vram_2257.bin'):
        changed=dict(display,buffers=dict(display['buffers']));raw=bytearray(changed['buffers'][file]);raw[-1]^=1
        changed['buffers'][file]=bytes(raw)
        def test_model():
            result=renderer(text,changed)(folder)
            need(all(r['vram_mismatches']==0 for r in result['records']),'Whole VRAM corruption rejected by independent replay')
        reject('effective_full_vram_'+file,test_model)
    groups,*_=original.data(text,display)
    child=next(i for i,q in enumerate(groups['FLOOR_QUEUE']) if q['slot']==3)
    for key in ('actor','main','parent','source','size','xy','bank'):
        changed=copy.deepcopy(groups);changed['FLOOR_QUEUE'][child][key]^=1
        reject('actual_child_queue_'+key,lambda:original.ownership(changed,state['payload'],state['guest']))
        original.ownership(groups,state['payload'],state['guest'])
    value,owned=positive(folder,text,display,image,state)
    source_paths=(Path(__file__),Path(names.__file__),Path(names.previous.__file__),Path(original.__file__),
        failure,names.previous.OUT/'failure.json',names.previous.FAILURE,parent_path,
        ROOT/'mame-mkp/src/emu/screen.cpp',ROOT/'mame-mkp/src/emu/video.cpp',
        ROOT/'mame-mkp/src/frontend/mame/luaengine.cpp')
    for path in source_paths:
        key=str(path.resolve());digest=sha(path);need(key not in pins or pins[key]==digest,'All executed source bytes immutable');pins[key]=digest
    need(all(sha(p)==d for p,d in pins.items()),'Every whole source/evidence pin after positives and counterexamples')
    report=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        actualSourceFIFOAndDMA=owned,wholeSavedNativeVRAMPasses=value,
        independentlyExactVRAMWords=512*512*value['frames'],sourceGraphicsStreams=len(display['gfx']),
        effectiveFaultsRejected=faults,positiveRestored=True,inputHashes=pins,
        requirements=parent['requirements'],remainingGroups=parent['remainingGroups'],
        sourceAndFIFOAndFullSavedVRAMAccepted=True,displayedRGBPixelsAccepted=False,
        rawScreenBitmapIsNotCurrentSnapshot=True,originalRGBFailurePreserved=True,
        CPUVRAMWriteCoverageAccepted=False,interPassEraseAccepted=False,allArenaCPUContextsAccepted=False,
        fullPortAcceptance=False,publicPlayableChanged=False,newNativeGames=0,newBuilds=0,newROMCopies=0,
        newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS source/FIFO/full106 VRAM passes; current displayed RGB explicitly unaccepted',flush=True)
    return report


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual VRAM rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
