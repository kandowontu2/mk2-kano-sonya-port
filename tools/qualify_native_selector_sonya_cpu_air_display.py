"""Whole actual airborne-trial scanout and original CPU/DMA saved-pass replay.

All1800 native current snapshots, held fields, graphics streams and full VRAM
words included. No artistic/heard/contact/unobserved erasure acceptance inferred.
"""
import hashlib
import json
import traceback
from collections import ChainMap
from pathlib import Path
import qualify_native_selector_sonya_cpu_air_control as control
import qualify_native_selector_sonya_pressure_snapshot_binding as scan
import qualify_native_selector_walkin_knife_display_ram as renderer
import qualify_native_selector_walkin_knife_display_face_rows as names
import qualify_native_selector_walkin_knife_vram as ram

ROOT,need,sha=control.ROOT,control.need,control.sha
OUT=ROOT/'audit_native_selector_sonya_cpu_air_display_checked'
CONTEXT=None


def execute(state):
    global CONTEXT
    need(not OUT.exists(), 'Fresh immutable whole current air-trial display proof')
    capture=control.capture;handle=capture.NATIVE_HANDLES[capture.KEY]
    parent_path=control.OUT/'report.json';proof=json.loads(parent_path.read_text())
    need(proof['passed'] and handle['process'].poll()==0 and handle['identity']==proof['actualNativeIdentity'],
         'Same actual new terminal handle and whole accepted human/native chronology')
    pins=dict(proof['inputHashes']);need(all(sha(p)==h for p,h in pins.items()), 'Whole earlier source/current capture pins')
    folder,text,_=capture.RAM_CASES[capture.KEY];meta=json.loads((folder/'result.json').read_text())
    windows={'cold_high':state['WINDOWS']['high'],'cold_owned':state['WINDOWS']['owned'],
             'cold_graphics':state['WINDOWS']['graphics'],'guest':state['guest'],'gfx':state['gfx']}
    need(set(meta['proofs'])==set(windows) and all(meta['proofs'][key]==
         dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest().upper(),everyActualByteComparedInRAM=True)
         for key,raw in windows.items()), 'All five complete independent startup byte models proven in this actual new game')
    display=capture.DISPLAY;transport=ram.verify_transport(display)
    image=names.runtime_graphics(state,pins);ram.graphics(display,image)
    snaps,fields,targets,states=scan.schema(text,display)
    records=[]
    for snap,field in zip(snaps,fields):
        f=int(snap['frame']);result=scan.one(snap,field,targets[f],display)
        records.append(dict(frame=f,mode=int(states[f]['mode']),held='reason' in targets[f],**result))
    faults=[]
    def reject(label,action):
        try:action()
        except (ValueError,AssertionError) as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Effective actual air-display counterexample accepted: '+label)
    # Source-scheduled landmarks chosen by actual mode transitions, plus full
    # opening/end. No green-frame filtering or invented terminal image.
    selected={1818,3617}
    selected.update(r['frame'] for i,r in enumerate(records) if i and r['mode']!=records[i-1]['mode'])
    for f in sorted(selected):
        i=f-1818;snap,field=snaps[i],fields[i]
        changed=dict(display,rgb=ChainMap({snap['file']:display['rgb'][snap['file']].copy()},display['rgb']))
        changed['rgb'][snap['file']][100,100,0]^=1
        reject('actual_current_pixel_'+str(f),lambda:scan.one(snap,field,targets[f],changed))
    for label,file in (('whole_terminal_VRAM','display_vram_3617.bin'),
                       ('whole_opening_palette','display_palette_1818.bin'),
                       ('whole_opening_prepass','display_pre_1817.bin')):
        raw=bytearray(display['buffers'][file]);raw[-1]^=1
        changed=dict(display,buffers=ChainMap({file:bytes(raw)},display['buffers']))
        reject(label,lambda:ram.verify_transport(changed))
    bad=dict(display,rgbHeaders=dict(display['rgbHeaders']));bad['rgbHeaders'].pop('display_1818.png')
    reject('missing_actual_opening_header',lambda:scan.schema(text,bad))
    first=next(iter(display['gfx'].values()));bad_image=bytearray(image);bad_image[int(first['first'])]^=1
    reject('actual_source_graphics_byte',lambda:ram.graphics(display,bad_image))
    need(all(scan.one(s,f,targets[int(s['frame'])],display)['pixels']==101600
             for s,f in zip(snaps,fields)), 'All entire original actual scanouts restored after effective faults')
    ram.verify_transport(display);ram.graphics(display,image)
    groups,*_=renderer.data(text,display)
    CONTEXT=dict(groups=groups,renderer=renderer.bindings(text,display))
    replay=CONTEXT['renderer'](folder)
    expected=sorted(r['snapshot'] for r in groups['FLOOR_LATCH'])
    need([r['frame'] for r in replay['records']]==expected and all(
        r['vram_mismatches']==r['displayed_mismatches']==r['shadow_mismatches']==0 for r in replay['records']),
        'Every original source-predicted full512x512 native CPU/DMA saved pass equals actual current VRAM/display')
    need(len(expected)+sum(r['held'] for r in records)==1800, 'Whole actual flip and held snapshot timeline accounted')
    for p in (Path(__file__),parent_path,Path(scan.__file__),Path(renderer.__file__),
              Path(renderer.original.__file__),Path(renderer.scaling.__file__),Path(names.__file__),Path(ram.__file__)):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h, 'No source or current evidence edited');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()), 'Whole source/native inventory intact after full replay')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=handle['identity'],nativeExit=0,
        completeCurrentSnapshots=len(records),exactCurrentPixels=sum(r['pixels'] for r in records),
        allWholeNativeTransportBuffers=transport[0],allWholeSourceGraphicsStreams=len(display['gfx']),
        modeCounts=dict((m,sum(r['mode']==m for r in records)) for m in sorted({r['mode'] for r in records})),
        heldSnapshotCount=sum(r['held'] for r in records),wholeExactNativePassVRAMWords=len(expected)*512*512,
        sourceExactSavedPassCPUandDMAReplay=replay,scanoutRecords=records,effectiveScanoutFaultsRejected=faults,
        wholeCurrentScanoutAndNativeSavedPassesAccepted=True,rendererSpecificFaultSuiteAccepted=False,
        allUnsavedErasureAccepted=False,allEffectOwnershipAccepted=False,actualVisualReviewAccepted=False,
        wholeSourceAudioAccepted=False,fullPortAcceptance=False,publicPlayableChanged=False,inputHashes=pins,
        requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n');return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(), 'Preserve actual whole airborne display proof failure')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
