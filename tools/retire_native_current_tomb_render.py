"""Bind individually viewed native RGB to the full scene before RAM release."""
import hashlib
import json
from pathlib import Path
import native_process_census_v6647 as census


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def retire(ram, viewed_frames):
    folder, output = ram['folder'], ram['output']
    receipt = output / 'native_visual_review_and_ram_retirement.json'
    need(not receipt.exists(), 'Never replace native review/retirement evidence')
    report_path = output / 'report.json'
    report = json.loads(report_path.read_text())
    meta_path = folder / 'result.json'
    meta = json.loads(meta_path.read_text())
    need(report == ram['report'] and report['passed'] and meta == ram['terminal'] and
         meta['captureCompleted'] and meta['exit_code'] == 0 and not meta['modelErrors'] and
         not census.census(), 'Same actually normal terminal and complete accepted native scene')
    need(report['sampledFrames'] == meta['modelExactFields'] == meta['observedRGBFields'] and
         report['oneInitialBaseOnly'] and report['laterTargetsNeverUsedAsAnchors'] and
         not report['fullPortAcceptance'], 'Full original one-base/continuous scene model retained')
    scene, images = ram['scene'], ram['images']
    need(not scene.raw and not scene.rgb and not scene.events and
         set(viewed_frames) == set(images) and len(viewed_frames) == len(images),
         'All held original native fields individually viewed; no omitted model targets')
    ledger = {r['frame']: r for r in scene.records}
    disk = json.loads((folder / 'continuous_scene_records.json').read_text())
    need(disk == scene.records, 'Entire exact scene chronology still bound to original RAM model')
    rows = []
    origin = report['nativeScene']['origin']
    for frame, rgb in sorted(images.items()):
        digest = hashlib.sha256(rgb.tobytes()).hexdigest().upper()
        row = ledger[frame]
        need(rgb.shape == (254, 400, 3) and digest == row['rgbSHA256'] and
             row['exactVRAMWords'] == 512 * 512 and row['exactRGBPixels'] == 400 * 254,
             'Every viewed original native raster is a full exact source-modeled field')
        rows.append(dict(frame=frame, age=frame-origin, rgbSHA256=digest,
                         nativeBodyCoverage=row['body'], nativeShadowPixels=row['shadowPixels'],
                         individuallyViewedOriginalRaster=True))
    pins = dict(report['inputHashes'])
    for path in (Path(__file__), report_path, meta_path, folder / 'native_identity.json',
                 folder / 'visible_digests.json', folder / 'continuous_scene_records.json'):
        pins[str(path.resolve())] = sha(path)
    need(all(sha(p) == h for p, h in pins.items()), 'All actual executed source and native scene evidence frozen')
    identity = json.loads((folder / 'native_identity.json').read_text())
    need(identity == ram['identity'] and identity['ProcessId'] == json.loads((folder / 'process.json').read_text())['pid'],
         'Original actual native birth/path/parent/command preserved')
    need(not list(folder.rglob('*.png')) and not list(folder.rglob('*.wav')) and
         not list(folder.rglob('*.bin')), 'No raw image/audio/VRAM/guest copies')
    proof = dict(passed=True, exactTerminalNativeIdentity=identity,
                 individuallyViewedFields=rows, completeSceneFrames=report['sampledFrames'],
                 completeSceneRGBPixels=report['exactRGBPixels'],
                 nativeShadowCopies=report['nativeScene']['nativeShadowCopies'],
                 finiteCrossTombSceneOnly=True, fullPortAcceptance=False,
                 allStageFinishersAccepted=False, publicPlayableChanged=False,
                 rawImageFilesWritten=0, inputHashes=pins)
    ram['server'].shutdown()
    ram['server'].server_close()
    images.clear()
    ram.clear()
    proof['originalNativeRasterBuffersReleased'] = len(rows)
    proof['reviewServerClosed'] = True
    proof['originalCaptureRAMDictionaryCleared'] = not ram
    receipt.write_text(json.dumps(proof, indent=2) + '\n')
    print(json.dumps(dict(passed=True, originalNativeRastersReleased=len(rows),
                         receipt=str(receipt), fullPortAcceptance=False)), flush=True)
    return proof
