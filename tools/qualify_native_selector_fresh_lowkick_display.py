"""Whole retained current scanouts and independently replayed saved native passes."""
import hashlib
import json
import traceback
from pathlib import Path
import qualify_native_selector_fresh_lowkick_controls as controls
import qualify_native_selector_sonya_pressure_snapshot_binding as scan
import qualify_native_selector_walkin_knife_display_ram as renderer
import qualify_native_selector_walkin_knife_display_face_rows as names
import qualify_native_selector_walkin_knife_vram as ram
import verify_native_source_sync as sync

OUT=sync.ROOT/'audit_native_selector_fresh_lowkick_display_checked'
CONTEXT=None


def main(prepared,recovered_scoped):
    global CONTEXT
    try:
        sync.need(not OUT.exists(),'Fresh immutable actual display proof')
        capture=json.loads(controls.CAPTURE.read_text()); key=prepared.SCOPE['KEY']
        handle=prepared.NATIVE_HANDLES[key]
        sync.need(capture['passed'] and handle['process'].poll()==0 and handle['identity']==capture['actualNativeIdentity'],
                  'Same actual completed capture, no replay')
        pins=dict(capture['inputHashes'])
        sync.need(all(sync.sha(p)==h for p,h in pins.items()),'Whole actual inputs unchanged')
        folder,text,_=prepared.RAM_CASES[key]; display=prepared.DISPLAY
        native=controls.gate(text,prepared.STATE['guest'])
        transport=ram.verify_transport(display)
        image=recovered_scoped(names).runtime_graphics(prepared.STATE,pins)
        ram.graphics(display,image)
        snaps,fields,targets,states=scan.schema(text,display)
        records=[]
        for snap,field in zip(snaps,fields,strict=True):
            frame=int(snap['frame'])
            records.append(dict(frame=frame,mode=int(states[frame]['mode']),held='reason' in targets[frame],
                                **scan.one(snap,field,targets[frame],display)))
        sync.need(len(records)==1800 and sum(r['pixels'] for r in records)==1800*101600,
                  'Every complete actual scanout accounted')
        groups,*_=renderer.data(text,display)
        CONTEXT=dict(groups=groups,renderer=renderer.bindings(text,display))
        OUT.mkdir(); (OUT/'scanout.json').write_text(json.dumps(dict(passed=True,records=records),indent=2)+'\n')
        print('Fresh whole scanout passed; native saved-pass replay starting',flush=True)
        replay=CONTEXT['renderer'](folder)
        expected=sorted(r['snapshot'] for r in groups['FLOOR_LATCH'])
        sync.need([r['frame'] for r in replay['records']]==expected and all(
            r['vram_mismatches']==r['displayed_mismatches']==r['shadow_mismatches']==0 for r in replay['records']),
                  'Every original independently predicted CPU/DMA pass matches full native VRAM/display/shadows')
        sync.need(len(expected)+sum(r['held'] for r in records)==1800,'All flip and held callbacks accounted')
        for p in (Path(__file__),Path(scan.__file__),Path(renderer.__file__),Path(renderer.original.__file__),
                  Path(renderer.scaling.__file__),Path(names.__file__),Path(ram.__file__),controls.CAPTURE):
            pins[str(p.resolve())]=sync.sha(p)
        sync.need(all(sync.sha(p)==h for p,h in pins.items()),'All whole source/capture pins intact')
        report=dict(passed=True,actualNativeIdentity=capture['actualNativeIdentity'],wholeNativeAndControls=native,
                    currentSnapshots=len(records),exactCurrentPixels=sum(r['pixels'] for r in records),
                    heldSnapshots=sum(r['held'] for r in records),wholeNativeTransport=transport[0],
                    wholeSourceGraphicsStreams=len(display['gfx']),nativeSavedPassReplay=replay,
                    wholeExactVRAMWords=len(expected)*512*512,inputHashes=pins,
                    allUnsavedErasureAccepted=False,allEffectOwnershipAccepted=False,visualReviewAccepted=False,
                    rendererFaultSuiteAccepted=False,fullPortAcceptance=False,newGames=0,newBuilds=0,newRawMediaFiles=0)
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n'); return report
    except BaseException:
        OUT.mkdir(exist_ok=True)
        (OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=traceback.format_exc()),indent=2)+'\n')
        raise
