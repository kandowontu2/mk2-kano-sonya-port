"""Preserve the actual timing diagnosis, native visual review and failed gate."""
import copy
import gzip
import hashlib
import inspect
import json
import re
from pathlib import Path
import numpy as np
import preserve_native_tomb_transition_trial as previous
import verify_native_floor_display_v602 as display

need,sha,state_facts = previous.need,previous.sha,previous.state_facts


def retire(ram, newly_viewed_frames):
    folder,output=ram['folder'],ram['output']
    receipt=output/'actual_timing_diagnosis_visual_review_and_ram_retirement.json'
    need(not receipt.exists() and not previous.census.census(),'Fresh retirement of actually normal terminal native timing capture')
    report=json.loads((output/'report.json').read_text())
    base_path=output.parent/(output.name+'_original_scene_report.json')
    base=json.loads(base_path.read_text())
    meta=json.loads((folder/'result.json').read_text())
    need(not report['passed'] and base==json.loads(json.dumps(ram['base_report'])) and base['passed'] and
         meta==json.loads(json.dumps(ram['terminal'])) and meta['exit_code']==0 and not meta['modelErrors'] and
         not (folder/'stderr.log').read_text(),'Full original scene passes; original later wrong-start failure remains failed; guarded observer has no Lua error')
    records=json.loads((folder/'post_scene_records.json').read_text())
    states=json.loads((folder/'post_state_records.json').read_text())
    need(records==ram['post_records'] and states==ram['post_states'] and
         json.loads((folder/'continuous_scene_records.json').read_text())==ram['scene'].records,
         'All actual original/later native records still bound to RAM')
    failed=[r for r in records if not r['passed']]
    need(len(failed)==1 and failed[0]['frame']==9626 and len(records)==1354,
         'Exact actual one-field native delayed-start mismatch, no dropped later rasters')
    text=gzip.open(folder/'run.log.gz','rt').read()
    # Entire original actual twelve-state/input fault suite, unchanged.
    body=inspect.getsource(previous.retire)
    begin=body.index('    facts = state_facts(text,states)')
    end=body.index('    need(set(viewed_later_frames)',begin)
    code='def actual_states(text,states):\n'+body[begin:end]+'    return facts,rejected\n'
    scope=dict(vars(previous));exec(compile(code,__file__+'::whole_original_actual_state_and_input_fault_suite','exec'),scope)
    facts,rejected=scope['actual_states'](text,states)
    diagnosis_path=output/'actual_retained_transition_display_diagnosis.json'
    diagnosis=json.loads(diagnosis_path.read_text())
    need(diagnosis['passed'] and diagnosis['actualFailedDisplayFields']==1 and
         diagnosis['actualTargets'][0]['previousDPYSTRTDiagnosticOnly']['exactPixels']==101600 and
         all(sha(p)==h for p,h in diagnosis['inputHashes'].items()),'Actual complete retained failed-target diagnosis frozen')
    held=ram['post_failures'][0];timing=held['timing'];state=held['state']
    check=lambda rgb,raw:display.check_latch(rgb,raw,held['palette'],timing['flip_before'],state['control'],state['tap'])
    check(held['rgb'],held['current'])
    negative=[]
    bad_rgb=held['rgb'].copy();bad_rgb[0,0,0]^=1
    try:check(bad_rgb,held['current'])
    except ValueError:negative.append('actual retained native RGB bit')
    else:raise ValueError('Actual native RGB target fault incorrectly admitted')
    bad_vram=bytearray(held['current'])
    addr=timing['flip_before'] if state['control']&0x400 else timing['flip_before']^0xfffc
    row=(addr>>4)&511;col=((((addr&0x7c)<<4)|(state['tap']&0x3fff))*2)&511
    words=np.frombuffer(held['current'],dtype='<u2')
    pens=np.frombuffer(held['palette'],dtype='<u4')
    at=row*512+col
    old=int(words[at]);replacement=next(p for p in range(32768)if pens[p]!=pens[old&0x7fff])
    bad_vram[at*2:at*2+2]=replacement.to_bytes(2,'little')
    try:check(held['rgb'],bytes(bad_vram))
    except ValueError:negative.append('actual retained native VRAM color target')
    else:raise ValueError('Actual native VRAM target fault incorrectly admitted')
    check(held['rgb'],held['current'])
    root=folder.parent
    prior_path=root/'audit_native_tomb_transition_rejoin_live_kano_p1_checked/failed_observer_trial_preservation_and_ram_retirement.json'
    prior=json.loads(prior_path.read_text())
    need(prior['passed'] and all(sha(p)==h for p,h in prior['inputHashes'].items()),'Every earlier inspected identical bitmap remains frozen')
    original_path=root/'audit_native_current_cross_tomb_kano_p1_render_checked/native_visual_review_and_ram_retirement.json'
    original=json.loads(original_path.read_text())
    known={r['frame']:r['rgbSHA256']for r in original['individuallyViewedFields']}
    known.update({r['frame']:r['rgbSHA256']for r in prior['individuallyViewedLaterFields']})
    images=ram['review_images']
    need(set(newly_viewed_frames)==set(images)-set(known) and
         len(newly_viewed_frames)==len(set(newly_viewed_frames)),'Every new actual raster individually reviewed')
    ledger={r['frame']:r for r in records}
    ledger.update({r['frame']:r for r in ram['scene'].records})
    views=[]
    for frame,rgb in sorted(images.items()):
        digest=hashlib.sha256(rgb.tobytes()).hexdigest().upper()
        need(rgb.shape==(254,400,3) and digest==ledger[frame]['rgbSHA256'],'Every actual reviewed raster is bound to native chronology')
        if frame in known:need(digest==known[frame],'Earlier-viewed bitmap is byte-identical at the same native field')
        views.append(dict(frame=frame,rgbSHA256=digest,individuallyViewedNow=frame in newly_viewed_frames,
                          exactSamePreviouslyViewedRaster=frame in known))
    live=[r for r in records if facts['admitted']<=r['frame']<=facts['completed']]
    need(all(r['passed']and r['pixels']==101600 for r in live),'Every resumed gameplay raster independently binds to native display')
    positions=[r['timing']for r in live]
    need(max(r['x1']for r in positions)>positions[0]['x1'] and min(r['x2']for r in positions)<positions[0]['x2'] and
         min(r['y1']for r in positions)<positions[0]['y1'] and positions[-1]['y1']==positions[0]['y1'],
         'Actual native forward walks, airborne jump and landed recovery, not only button presses')
    # Earlier emitter called HCOUNT "vcount". Preserve the bytes and explain,
    # never credit that scalar as a measured vertical counter.
    header=root/'diagnostic_native_paired_stumble_table_ps7/input_sources/mame-mkp/src/devices/cpu/tms34010/tms34010.h'
    names=re.search(r'enum\s*\{([^}]+REG_REFCNT[^}]+)\}',header.read_text(),re.S)
    need(names and 'REG_HCOUNT,\n\tREG_VCOUNT,\n\tREG_DPYADR' in names[1],
         'Actual TMS34010 HCOUNT/VCOUNT/DPYADR ordering checked, not34020 register order')
    pins=dict(base['inputHashes'])
    for p in (Path(__file__),Path(previous.__file__),base_path,output/'report.json',diagnosis_path,
              folder/'post_scene_records.json',folder/'post_state_records.json',header,prior_path,original_path):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Whole actual successful prefix, failed display gate, source and reviewed evidence unchanged')
    proof=dict(passed=True,preservationAndRetirementOnly=True,fullOriginalTransitionTrialAccepted=False,
               originalIndependentSceneFields=537,laterActualNativeFields=1354,
               originalLaterRequestedStartBindings=1353,retainedPreviousStartDiagnosticPixels=101600,
               actualNativeGameplayFacts=facts,actualStateAndInputFaultsRejected=rejected,
               actualRetainedNativePixelTargetFaultsRejected=negative,
               actualObserverRouteErrorCorrected=True,actualObserverStderrEmpty=True,
               actualNativeMovementAndJumpObserved=True,individuallyReviewedFields=views,
               actualVisualObservation='Native continue shutters, dedicated selected portraits and numbered borders, own locked poses, proper Battle3 Kano/Sonya portraits; CSS clears before Wasteland fight. Both real bodies have visible floor shadows; native jumping/landing/low-kick contact and black-shadowed KANO/SONYA lifebars viewed.',
               correctedRegisterInterpretation='Earlier timing.vcount and flip_vcount actually read HCOUNT atC00001C0. VCOUNT isC00001D0. DPYADR atC00001E0 and DPYSTRT atC0000090 are correct. No old HCOUNT value credited as a vertical phase.',
               nextRequired='Use actual completed native DPYADR scanout rather than immediately queued DPYSTRT; collect proper vertical-count/blanking registers and reverify the entire transition.',
               fullPortAcceptance=False,goalStatus='active',publicPlayableChanged=False,
               rawImageAudioVRAMCopiesWritten=0,inputHashes=pins)
    count=len(images);failed_count=len(ram['post_failures'])
    ram['server'].shutdown();ram['server'].server_close()
    for key in ('images','post_images','review_images'):ram[key].clear()
    ram['post_failures'].clear();ram.clear()
    proof.update(originalNativeRasterBuffersReleased=count,retainedFailedTargetSetsReleased=failed_count,
                 reviewServerClosed=True,originalCaptureRAMDictionaryCleared=not ram)
    receipt.write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps(dict(passed=True,preservationOnly=True,rasterBuffersReleased=count,
                         nativeMovementJumpAndContactObserved=True,receipt=str(receipt)),indent=2),flush=True)
    return proof
