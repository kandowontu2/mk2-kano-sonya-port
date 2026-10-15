"""Retire exact native scene and later paid-rejoin rasters after individual review."""
import hashlib
import json
from pathlib import Path
import native_process_census_v6647 as census


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def retire(ram, viewed_frames, observations):
    folder, output = ram['folder'], ram['output']
    receipt = output/'native_visual_transition_review_and_ram_retirement.json'
    need(not receipt.exists(), 'Fresh actual transition review/retirement receipt')
    report_path, meta_path = output/'report.json', folder/'result.json'
    report = json.loads(report_path.read_text())
    meta = json.loads(meta_path.read_text())
    need(report == json.loads(json.dumps(ram['report'])) and report['passed'] and
         meta == json.loads(json.dumps(ram['terminal'])) and meta['captureCompleted'] and
         meta['exit_code'] == 0 and not meta['modelErrors'] and not census.census(),
         'Same actual complete positive scene and normal retired native process')
    scene, images, later = ram['scene'], ram['review_images'], ram['post_records']
    need(not scene.raw and not scene.rgb and not scene.events and not ram['post_raw'] and
         len(viewed_frames) == len(images) and set(viewed_frames) == set(images),
         'All actual bounded native rasters viewed, both original and later targets consumed')
    need(json.loads((folder/'continuous_scene_records.json').read_text()) == scene.records and
         json.loads((folder/'post_scene_records.json').read_text()) == later and
         json.loads((folder/'post_state_records.json').read_text()) == ram['post_states'] and
         json.loads((folder/'post_buffer_digests.json').read_text()) == ram['post_transport'].records,
         'Entire original model and later exact state/display/buffer chronology unchanged')
    need(report['sampledFrames'] == meta['modelExactFields'] == meta['observedRGBFields'] == len(scene.records) and
         report['oneInitialBaseOnly'] and report['laterTargetsNeverUsedAsAnchors'] and
         report['laterNativeTransitionAndPhysicalRejoin']['laterConsecutiveNativeFields'] == len(later),
         'Whole original one-base model retained, separate later native scanout scope explicit')
    original_ledger = {r['frame']:r for r in scene.records}
    post_ledger = {r['frame']:r for r in later}
    viewed = []
    for frame, rgb in sorted(images.items()):
        digest = hashlib.sha256(rgb.tobytes()).hexdigest().upper()
        need(rgb.shape == (254,400,3), 'Original native review raster size')
        if frame in original_ledger:
            row = original_ledger[frame]
            need(digest == row['rgbSHA256'] and row['exactVRAMWords'] == 512*512 and
                 row['exactRGBPixels'] == 101600, 'Original viewed raster is exact independent source model')
            kind = 'independent_original_scene_model'
        else:
            row = post_ledger[frame]
            need(row['passed'] and row['pixels'] == 101600 and digest == row['rgbSHA256'],
                 'Later viewed raster is exact native latch/VRAM/palette binding')
            kind = 'later_native_display_binding_not_independent_renderer_model'
        viewed.append(dict(frame=frame, rgbSHA256=digest, individuallyViewed=True, evidenceKind=kind))
    need(set(observations) == {'transitionClears', 'selectionNoPersistentFightOverlay', 'resumedActualBodies'},
         'Explicit individual-review observations without silent whole-port acceptance')
    need(all(isinstance(v, str) and v for v in observations.values()), 'Real observations, not automatic pointer-based claims')
    pins = dict(report['inputHashes'])
    pins.update(report['extensionSourceHashes'])
    for p in (Path(__file__),report_path,meta_path,folder/'native_identity.json',
              folder/'post_scene_records.json',folder/'post_state_records.json',folder/'post_buffer_digests.json'):
        pins[str(p.resolve())] = sha(p)
    need(all(sha(p)==h for p,h in pins.items()), 'Whole executed source and actual evidence hashes unchanged')
    identity = json.loads((folder/'native_identity.json').read_text())
    need(identity == ram['identity'] and identity['ProcessId'] ==
         json.loads((folder/'process.json').read_text())['pid'], 'Exact native birth/path/parent/command retained')
    need(not list(folder.rglob('*.png')) and not list(folder.rglob('*.wav')) and
         not list(folder.rglob('*.bin')), 'No raw native raster/audio/guest copies')
    proof = dict(passed=True, exactTerminalNativeIdentity=identity, individuallyViewedFields=viewed,
                 originalIndependentSceneFields=len(scene.records), laterNativeDisplayFields=len(later),
                 ordinaryPaidRejoin=report['laterNativeTransitionAndPhysicalRejoin'], observations=observations,
                 finiteActualTransitionOnly=True, allCharactersSlotsBranchesAccepted=False,
                 fullPortAcceptance=False, goalStatus='active', publicPlayableChanged=False,
                 rawImageAudioVRAMCopiesWritten=0, inputHashes=pins)
    server = ram['server']
    server.shutdown()
    server.server_close()
    count = len(images)
    images.clear()
    ram['images'].clear()
    ram['post_images'].clear()
    ram.clear()
    proof.update(originalNativeRasterBuffersReleased=count, reviewServerClosed=True,
                 originalCaptureRAMDictionaryCleared=not ram)
    receipt.write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps(dict(passed=True, nativeRastersReleased=count, receipt=str(receipt)),indent=2),flush=True)
    return proof
