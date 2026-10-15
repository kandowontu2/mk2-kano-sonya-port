"""Retire fully checked native scanout transition and all reviewed original RGB."""
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

need,sha=previous.need,previous.sha


def retire(ram, newly_viewed_frames):
    folder,output=ram['folder'],ram['output']
    receipt=output/'native_effective_scanout_visual_review_and_ram_retirement.json'
    need(not receipt.exists() and not previous.census.census(),'Same terminal native process, fresh visual/retirement evidence')
    report=json.loads((output/'report.json').read_text())
    meta=json.loads((folder/'result.json').read_text())
    base_path=output.parent/(output.name+'_original_scene_report.json')
    base=json.loads(base_path.read_text())
    need(report==json.loads(json.dumps(ram['report'])) and report['passed'] and
         meta==json.loads(json.dumps(ram['terminal'])) and meta['captureCompleted'] and
         meta['exit_code']==0 and not meta['modelErrors'] and
         base==json.loads(json.dumps(ram['base_report'])) and base['passed'] and
         not ram['post_failures'] and not (folder/'stderr.log').read_text(),
         'Whole initial independent scene and full later native-display/rejoin gate genuinely pass')
    scene,records,states=ram['scene'],ram['post_records'],ram['post_states']
    need(not scene.raw and not scene.rgb and not scene.events and not ram['post_raw'] and
         json.loads((folder/'continuous_scene_records.json').read_text())==scene.records and
         json.loads((folder/'post_scene_records.json').read_text())==records and
         json.loads((folder/'post_state_records.json').read_text())==states and
         json.loads((folder/'post_buffer_digests.json').read_text())==ram['post_transport'].records,
         'All entire original/later native chronology and buffer transport still bound')
    need(report['sampledFrames']==meta['observedRGBFields']==meta['modelExactFields']==len(scene.records)==537 and
         report['oneInitialBaseOnly'] and report['laterTargetsNeverUsedAsAnchors'] and
         report['laterNativeTransitionAndPhysicalRejoin']['laterConsecutiveNativeFields']==len(records),
         'Original complete537-field independent model retained, separate later scope explicit')
    for s,r in zip(states,records):
        t=r['timing']
        effective=(t['dpyadr']+(t['vsblnk']-t['veblnk'])*(t['control']&0x03fc))&0xffff
        need(s=={k:r[k]for k in s} and r['passed'] and r['pixels']==101600 and
             r['nativeDPYADRSourceDefinedAddressOnly'] and r['currentVRAMNeverSelectedAsPassingTarget'] and
             r['effectiveNativeStart']==effective and r['queuedNativeStart']==s['start'] and
             t['vsblnk']-t['veblnk']==254 and t['control']==s['control'] and t['tap']==s['tap'] and
             t['vcount']==t['vsblnk']-1 and t['vtotal']>=t['vsblnk'] and
             t['control']&0x03fc==16 and t['dpystart']&3==t['dpyadr']&3==0,
             'Every later raster uses one native source-defined completed scanout, no target rescue')
    text=gzip.open(folder/'run.log.gz','rt').read()
    body=inspect.getsource(previous.retire)
    begin=body.index('    facts = state_facts(text,states)');end=body.index('    need(set(viewed_later_frames)',begin)
    code='def actual_states(text,states):\n'+body[begin:end]+'    return facts,rejected\n'
    scope=dict(vars(previous));exec(compile(code,__file__+'::entire_original_twelve_state_and_input_faults','exec'),scope)
    facts,rejected=scope['actual_states'](text,states)
    need(len(report['laterNativeTransitionAndPhysicalRejoin']['actualSemanticFaultsRejected'])==12 and len(rejected)==12,
         'Original full state/input/admission/terminal fault suites retained')
    prior_path=folder.parent/'audit_native_tomb_transition_timing_kano_p1_checked/actual_timing_diagnosis_visual_review_and_ram_retirement.json'
    prior=json.loads(prior_path.read_text())
    need(prior['passed'] and not prior['fullOriginalTransitionTrialAccepted'] and
         all(sha(p)==h for p,h in prior['inputHashes'].items()),'Whole original failed gate and actual diagnosis remain intact')
    known={r['frame']:r['rgbSHA256']for r in prior['individuallyReviewedFields']}
    images=ram['review_images'];ledger={r['frame']:r for r in scene.records}
    ledger.update({r['frame']:r for r in records})
    need(set(newly_viewed_frames)==set(images)-set(known) and len(newly_viewed_frames)==len(set(newly_viewed_frames)),
         'Every new actual held native raster individually inspected')
    views=[]
    for frame,rgb in sorted(images.items()):
        digest=hashlib.sha256(rgb.tobytes()).hexdigest().upper()
        need(rgb.shape==(254,400,3) and digest==ledger[frame]['rgbSHA256'],
             'Every reviewed actual native bitmap matches its entire recorded scanout')
        if frame in known:need(digest==known[frame],'Previously inspected bitmap is byte-identical at same actual native field')
        views.append(dict(frame=frame,rgbSHA256=digest,individuallyViewedNow=frame in newly_viewed_frames,
                          exactSamePreviouslyViewedRaster=frame in known))
    differences=[r for r in records if r['queuedStartDiffersFromEffective']]
    need(differences and all(r['effectiveNativeStart']!=r['queuedNativeStart'] for r in differences),
         'Actual queued/completed scanout difference measured, no forced equality')
    live=[r for r in records if facts['admitted']<=r['frame']<=facts['completed']]
    pos=[r['timing']for r in live]
    need(max(r['x1']for r in pos)>pos[0]['x1'] and min(r['x2']for r in pos)<pos[0]['x2'] and
         min(r['y1']for r in pos)<pos[0]['y1'] and pos[-1]['y1']==pos[0]['y1'],
         'Actual native forward movement, jump and landed recovery')
    pins=dict(report['inputHashes']);pins.update(report['extensionSourceHashes'])
    for p in (Path(__file__),Path(previous.__file__),prior_path,base_path,output/'report.json',
              folder/'result.json',folder/'post_scene_records.json',folder/'post_state_records.json'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Entire executed sources, old failures and actual complete positive result frozen')
    identity=json.loads((folder/'native_identity.json').read_text())
    need(identity==ram['identity'] and identity['ProcessId']==
         json.loads((folder/'process.json').read_text())['pid'],'Exact original native birth/path/parent/command preserved')
    need(not list(folder.rglob('*.png')) and not list(folder.rglob('*.wav')) and not list(folder.rglob('*.bin')),
         'No native raw RGB/VRAM/audio/guest files created')
    proof=dict(passed=True,finiteNativeTombTransitionAndPaidRejoinAccepted=True,
               exactTerminalNativeIdentity=identity,individuallyReviewedFields=views,
               originalIndependentSceneFields=len(scene.records),laterSourceDefinedNativeDisplayFields=len(records),
               laterSourceDefinedNativeRGBPixels=len(records)*101600,
               actualNativeScanoutPhase='Every field sampled at real VCOUNT273, last visible line before VSBLNK274 reload; VEBLNK20 gives254 visible lines, DUDATE16 and zero repeated-line bits.',
               actualQueuedCompletedAddressDifferences=[dict(frame=r['frame'],queued=r['queuedNativeStart'],
                   effective=r['effectiveNativeStart'],nativeVCOUNT=r['timing']['vcount'],nativeHCOUNT=r['timing']['hcount'])for r in differences],
               actualNativeGameplayFacts=facts,actualStateAndInputFaultsRejected=rejected,
               actualVisibleTransitionAndPlayabilityReviewed=True,
               actualVisualObservations='Native fatality shutters/continue, own numbered selection portraits and locked poses, correct native Battle3 portraits, clean Wasteland fight entry, actual Kano/Sonya walking/jump/landing/low-kick contact, both floor shadows and black-shadowed native lifebar names.',
               allCharactersSlotsBranchesAccepted=False,allStageFinishersAccepted=False,
               fullPortAcceptance=False,goalStatus='active',publicPlayableChanged=False,
               rawImageAudioVRAMCopiesWritten=0,inputHashes=pins)
    count=len(images)
    ram['server'].shutdown();ram['server'].server_close()
    for key in ('images','post_images','review_images'):ram[key].clear()
    ram.clear()
    proof.update(originalNativeRasterBuffersReleased=count,reviewServerClosed=True,
                 originalCaptureRAMDictionaryCleared=not ram)
    receipt.write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps(dict(passed=True,nativeRastersReleased=count,fullPortAcceptance=False,
                         receipt=str(receipt)),indent=2),flush=True)
    return proof
