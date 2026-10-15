"""Full actual current Knife snapshot proof and effective RGB/VRAM faults.

Finite missed CPU Knife in Prison, true Sonya P1/Kano P2, not universal hit,
guard, arena, priority, erasure or complete-port acceptance. No game replay.
"""
import hashlib
import json
from pathlib import Path
import numpy as np
import qualify_native_selector_walkin_knife_snapshot as checked
import qualify_native_selector_walkin_knife_vram as ram

ROOT,need,sha=checked.ROOT,checked.need,checked.sha
capture,original=checked.capture,checked.original
OUT=ROOT/'audit_native_selector_walkin_knife_snapshot_sealed'


def execute(state):
    need(not OUT.exists(),'Fresh actual native snapshot seal')
    path=checked.OUT/'report.json';proof=json.loads(path.read_text())
    views_path=ROOT/'audit_native_selector_walkin_knife_snapshot_actual_views.json'
    views=json.loads(views_path.read_text());held=capture.NATIVE_HANDLES[capture.KEY]
    need(proof['passed'] and proof['independentRendererAccepted'] and views['passed'] and
         held['process'].poll()==proof.get('nativeExit',0)==0 and
         held['identity']==proof['actualNativeIdentity']==views['actualNativeIdentity'],
         'Same retained terminal0 native handle, full pixel proof and actually inspected views')
    pins=dict(proof['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'Whole source/evidence pins before seal')
    folder,text,_=capture.RAM_CASES[capture.KEY];display=capture.DISPLAY
    ram.verify_transport(display);image=checked.names.runtime_graphics(state,pins);ram.graphics(display,image)
    expected_frames=(2257,2259,2272,2280,2300,2317)
    need(tuple(int(v['header']['frame'])for v in views['actualViewedCallbacks'])==expected_frames and
         views['identityRevalidatedBeforeAndAfter'],'All six exact actually viewed current snapshot callbacks')
    for v in views['actualViewedCallbacks']:
        header=v['header'];rgb=display['rgb'][header['file']]
        need(display['rgbHeaders'][header['file']]==header and
             hashlib.sha256(rgb.tobytes()).hexdigest().upper()==v['nativeRGBSHA256'],
             'Every actually seen complete native RGB buffer unchanged')
    faults=[]
    def run(d):
        result=original.bindings(text,d)(folder)
        need(result['frames']==106 and all(r['vram_mismatches']==r['displayed_mismatches']==
             r['shadow_mismatches']==0 for r in result['records']),
             'Every saved current whole VRAM/RGB/shadow pass exact')
        return result
    def reject(label,action):
        try:action()
        except (ValueError,AssertionError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Effective actual render counterexample accepted: '+label)
    for frame in (2257,2272,2300,2317):
        file=f'display_{frame}.png';changed=dict(display,rgb=dict(display['rgb']))
        changed['rgb'][file]=display['rgb'][file].copy();changed['rgb'][file][100,100,0]^=1
        reject('changed_actual_current_RGB_'+str(frame),lambda:run(changed))
    for file in ('display_pre_2256.bin','display_vram_2257.bin'):
        changed=dict(display,buffers=dict(display['buffers']));raw=bytearray(display['buffers'][file]);raw[-1]^=1
        changed['buffers'][file]=bytes(raw)
        reject('changed_full_VRAM_'+file,lambda:run(changed))
    groups,*_=original.data(text,display);latch=groups['FLOOR_LATCH'][0]
    addr=latch['start'] if latch['control']&0x400 else latch['start']^0xfffc
    row=(addr>>4)&511;col=((((addr&0x7c)<<4)|(latch['tap']&0x3fff))*2)&511
    words=np.frombuffer(display['buffers'][latch['file']],dtype='<u2').reshape(512,512)
    pen=int(words[row+100,col+100]&0x7fff);file='display_palette_2257.bin'
    changed=dict(display,buffers=dict(display['buffers']));raw=bytearray(display['buffers'][file]);raw[pen*4]^=1
    changed['buffers'][file]=bytes(raw);reject('changed_actually_used_palette_pen',lambda:run(changed))
    for label,at in (('wrong_independent_HUD_graphics',0x1e00000),
                     ('wrong_independent_Knife_intro',0x1e04000),('wrong_independent_Knife_flight',0x1e60000)):
        changed=bytearray(image);changed[at]^=1
        reject(label,lambda:ram.graphics(display,changed));ram.graphics(display,image)
    positive=run(display);ram.verify_transport(display)
    for p in (Path(__file__),Path(checked.__file__),Path(ram.__file__),path,views_path,
              ROOT/'tools/read_native_selector_knife_snapshot_frames.py',
              ROOT/'tools/read_native_selector_knife_snapshot_frames_remote.py'):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'No executed source or receipt edits');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'Entire source/native/evidence inventory after final restored positive')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        originalRendererReportSHA256=sha(path),actualVisualReviewSHA256=sha(views_path),
        actualSourceFIFOAndDMA=proof['actualSourceFIFOAndDMA'],wholeSavedNativePasses=positive,
        actualRGBFrames=106,actualViewedFrames=6,exactWholeDisplayedPixels=106*400*254,
        exactWholeVRAMWords=106*512*512,effectiveActualRenderFaultsRejected=faults,
        originalFailedRawScreenCapturePreserved=True,positiveRestored=True,inputHashes=pins,
        requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        fullFiniteMissedCPUKnifeSavedPassRenderingAccepted=True,
        actualShotHitOrGuardAccepted=False,interPassEraseAccepted=False,allArenaCPUContextsAccepted=False,
        universalArtisticAcceptance=False,fullPortAcceptance=False,publicPlayableChanged=False,
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print('PASS106 current Knife displayed passes,10 effective render faults,6 actual views',flush=True)
    return value
