"""Diagnose retained actual display failures, without choosing passing buffers."""
import gzip
import hashlib
import json
from pathlib import Path
import numpy as np
import verify_native_floor_display_v602 as display


def need(value,message):
    if not value:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest().upper()


def expected(raw,palette,start,control,tap):
    address=start if control&0x400 else start^0xfffc
    row=(address>>4)&511
    column=((((address&0x7c)<<4)|(tap&0x3fff))*2)&511
    need(row+254<=512 and column+400<=512 and start&3==0,'Bounded original deterministic native crop')
    words=np.frombuffer(raw,dtype='<u2').reshape(512,512)[row:row+254,column:column+400]&0x7fff
    pens=np.frombuffer(palette,dtype='<u4')
    colors=np.stack([(pens>>16)&255,(pens>>8)&255,pens&255],axis=1).astype(np.uint8)
    return colors[words]


def comparison(rgb,target):
    exact=np.all(rgb==target,axis=2)
    return dict(exactPixels=int(np.count_nonzero(exact)),totalPixels=101600,
                differingRows=np.flatnonzero(np.any(~exact,axis=1)).tolist(),
                differingColumns=np.flatnonzero(np.any(~exact,axis=0)).tolist())


def analyze(ram):
    folder=ram['folder']
    output=ram['output']
    path=output/'actual_retained_transition_display_diagnosis.json'
    need(not path.exists(),'Fresh actual failed-target diagnosis, never overwrite results')
    disk=json.loads((folder/'post_scene_records.json').read_text())
    need(disk==ram['post_records'],'Entire native later RGB/buffer/state ledger still bound')
    failed=[r for r in disk if not r['passed']]
    need(failed and len(ram['post_failures'])==min(8,len(failed)),'Actual first failed fields retained atomically')
    ledger={r['frame']:r for r in failed}
    rows=[]
    for held in ram['post_failures']:
        rgb=held['rgb'];state=held['state'];timing=held['timing'];frame=held['frame']
        row=ledger[frame]
        need(digest(rgb.tobytes())==row['rgbSHA256'] and digest(held['latch'])==row['vramSHA256'] and
             digest(held['palette'])==row['paletteSHA256'] and
             digest(held['current'])==row['currentVRAMDiagnosticSHA256'] and timing==row['timing'],
             'Actual failed raster, complete native buffers, palette and timing match immutable recorded digests')
        front=expected(held['latch'],held['palette'],state['start'],state['control'],state['tap'])
        current=expected(held['current'],held['palette'],state['start'],state['control'],state['tap'])
        before=expected(held['current'],held['palette'],timing['flip_before'],state['control'],state['tap'])
        original=comparison(rgb,front)
        need(original['exactPixels']==row['pixels'] and original['differingRows']==row['mismatchedNativeRows'],
             'Exact original comparison failure independently reproduced')
        alternative=comparison(rgb,current)
        need(alternative['exactPixels']==row['currentVRAMDiagnosticMatches'],
             'Exact additional current-VRAM comparison independently reproduced')
        rows.append(dict(frame=frame,nativeTiming=timing,nativeState=state,
                         originalActualLatch=original,currentVRAMDiagnosticOnly=alternative,
                         previousDPYSTRTDiagnosticOnly=comparison(rgb,before),
                         actualRawByteDigests={k:digest(held[k])for k in ('latch','current','palette')},
                         actualRGBSHA256=digest(rgb.tobytes()),noPassingBufferSelected=True))
    native_root=folder.parent/'diagnostic_native_paired_stumble_table_ps7/input_sources/mame-mkp/src'
    files=(native_root/'devices/cpu/tms34010/tms34010.cpp',native_root/'mame/midway/midtunit_v.cpp')
    need(all(p.is_file()for p in files),'Actual compiled native scanline and video source present')
    cpu=files[0].read_text()
    video=files[1].read_text()
    need('IOREG(REG_DPYADR) = IOREG(REG_DPYSTRT)' in cpu and
         'uint16_t dpyadr = IOREG(REG_DPYADR)' in cpu and
         'screen().update_partial(vcount)' in cpu and
         'src[coladdr++ & 0x1ff] & 0x7fff' in video,
         'Original real DPYADR-at-VBLANK and per-scanline native VRAM rendering source, not a snapshot-start assumption')
    before=json.loads((folder/'input_hashes_before.json').read_text())
    need(all(before.get(str(p.resolve()))==digest(p.read_bytes())for p in files),
         'Actual already-bound compiled source bytes, not current uncompiled installation')
    pins=dict(before)
    for p in (Path(__file__),folder/'post_scene_records.json',folder/'post_state_records.json',
              folder/'post_buffer_digests.json',folder/'run.log.gz',folder/'result.json',output/'report.json'):
        pins[str(p.resolve())]=digest(p.read_bytes())
    need(all(digest(Path(p).read_bytes())==h for p,h in pins.items()),'Every actual source/input/failed-target evidence byte unchanged')
    proof=dict(passed=True,diagnosisOnly=True,fullTransitionVisualTrialAccepted=False,
               actualFailedDisplayFields=len(failed),retainedFirstFailedTargets=len(rows),actualTargets=rows,
               fullNativeFields=len(disk),allLaterPixelGatesStillUnmodified=True,
               noTargetSearchOrTolerance=True,wholePortAcceptance=False,goalStatus='active',inputHashes=pins)
    path.write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps(dict(passed=True,diagnosisOnly=True,failedFields=len(failed),
                         targets=[dict(frame=r['frame'],timing=r['nativeTiming'],
                            latchPixels=r['originalActualLatch']['exactPixels'],
                            currentPixels=r['currentVRAMDiagnosticOnly']['exactPixels'],
                            previousStartPixels=r['previousDPYSTRTDiagnosticOnly']['exactPixels'])for r in rows],
                         report=str(path)),indent=2),flush=True)
    return proof
