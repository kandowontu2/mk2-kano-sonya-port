"""Bind whole state/HP evidence, its actual loaded source and retained rasters.

Keep Sonya-choice and incomplete-grab coverage gaps visible. No native replay,
new build/media, automatic promotion or rewritten historical report.
"""
import copy
import hashlib
import json
from pathlib import Path
import numpy as np
import verify_native_source_sync as migration
import capture_current_subzero_audio_v6213 as artifact

ROOT = migration.ROOT
OUT = ROOT / 'audit_native_selector_natural_state_health_checkpoint_checked'
PARENT = ROOT / 'audit_native_selector_natural_state_health_checked/report.json'
VISUAL = ROOT / 'audit_native_selector_startup_pcm_actual_visual_review.json'
FIXED = {
    PARENT: '8D9430237996F5EAB71565A9BAC238650A441A959D11BA7A86D2252B1AC30B21',
    VISUAL: '5299F3AE0C8D842C18C78E0819A9293D2648F3B865FC3908D476A484555E5799',
    ROOT / 'tools/qualify_native_selector_natural_state_health.py': '4CA718873FF38A397855091C1C86504A9975AE6A2E63823FCE1883D30893BD9B',
    ROOT / 'tools/qualify_native_selector_natural_state_health_bound.py': '87666D1295D28B9A2CE6DE2CAA6863ECFFC323AD14EFF6AF8BF613200B3DA80F',
    ROOT / 'audit_native_selector_natural_state_health_prelaunch.json': 'CFB0273FFFD2560B53803236CC316B7F87A515DA997A309D5E15E50674009931',
    ROOT / 'tools/read_native_selector_startup_pcm_frames.py': '6A20181B99B1AA1C2F61BB423B196102E2F20F6A45B35F15B526B43FE7832F5E',
    ROOT / 'tools/read_native_selector_startup_pcm_frames_remote.py': 'E84092209323C6BE6359522ECF2A6D188AFD8CFAF72CD848594CFF8B09B6958B',
}


def need(value, label):
    if not value:
        raise ValueError(label)


def rasters(images, frames):
    need(len(images) == len(frames) and set(images) == {r['imageKey'] for r in frames},
         'Every distinct original callback image, no omitted or added raster')
    answer = []
    for ordinal, row in enumerate(frames):
        rgb = images[row['imageKey']]
        need(row['callbackOrdinal'] == ordinal and rgb.shape == (254, 400, 3) and rgb.dtype == np.uint8,
             'Complete native dimensions/type/callback order')
        raw = np.empty((254, 400, 4), np.uint8)
        raw[:, :, :3] = rgb[:, :, ::-1]
        matched = []
        for alpha in (0, 255):
            raw[:, :, 3] = alpha
            if hashlib.sha256(raw.tobytes()).hexdigest().upper() == row['sha256']:
                matched.append(alpha)
        need(len(matched) == 1, 'Whole original BGRX digest, no scanout fitting or overpainting')
        answer.append(dict(index=ordinal, header=row, actualReconstructedAlpha=matched[0],
                           nativeRGBSHA256=hashlib.sha256(rgb.tobytes()).hexdigest().upper()))
    return answer


def execute(cases):
    need(not OUT.exists(), 'Fresh immutable source/raster checkpoint')
    pins = {str(path): digest for path, digest in FIXED.items()}
    need(all(migration.sha(path) == digest for path, digest in pins.items()),
         'Exact loaded original/successor source, failure and evidence preserved')
    parent = json.loads(PARENT.read_text())
    need(parent['passed'] and parent['wholeAllModePhysicalFields'] == 7204 and
         len(parent['actualFaultsRejected']) == 26 and not parent['fullPortAcceptance'] and
         not parent['fullNaturalCPUChoiceAcceptance'], 'Whole finite ledger pass, not full gameplay acceptance')
    pins.update(parent['inputHashes'])
    visuals = json.loads(VISUAL.read_text())
    need(visuals['passed'] and visuals['actualViewedCallbackCount'] == 6 and
         not visuals['fullParticlesCleanupAccepted'] and not visuals['fullPortAcceptance'],
         'Actual six-view review remains scoped, not a complete cleanup/port claim')
    qualifications, faults = [], []
    for capture, expected_pid in cases:
        folder, text, images = capture.RAM_CASES[capture.KEY]
        held = capture.NATIVE_HANDLES[capture.KEY]
        meta = json.loads((folder / 'result.json').read_text())
        proof = next(r for r in parent['qualifications'] if r['nativePID'] == expected_pid)
        need(held['process'].poll() == meta['nativeExit'] == 0 and
             held['identity'] == proof['actualNativeIdentity'] == meta['nativeTerminal']['actualWindowsIdentity'] and
             held['identity']['ProcessId'] == expected_pid and meta['passed'],
             'Same exact original terminal game and retained handle, no replay')
        positive = rasters(images, meta['actualScenes'])
        need(len(positive) == proof['originalRGBCallbacks'], 'Whole original capture inventory unchanged')
        first = meta['actualScenes'][0]['imageKey']
        bad = dict(images); bad[first] = images[first].copy(); bad[first][0, 0, 0] ^= 1
        missing = dict(images); del missing[first]
        extra = dict(images); extra['invented_callback.png'] = images[first]
        for label, sample in [('one_native_pixel', bad), ('missing_callback', missing), ('invented_callback', extra)]:
            try:
                rasters(sample, meta['actualScenes'])
            except ValueError as error:
                faults.append(dict(nativePID=expected_pid, fault=label, rejectedBy=str(error)))
            else:
                raise ValueError('Actual whole raster corruption admitted: ' + label)
        need(rasters(images, meta['actualScenes']) == positive, 'Every original raster restored after faults')
        viewed = []
        if expected_pid == 46264:
            need(visuals['actualNativeIdentity'] == held['identity'], 'Six actually viewed rasters belong to this game')
            for row in visuals['actualViewedCallbacks']:
                actual = positive[row['index']]
                need(row['header'] == actual['header'] and row['SHA256'] == actual['header']['sha256'] and
                     row['nativeRGBSHA256'] == actual['nativeRGBSHA256'] and
                     row['actualReconstructedAlpha'] == actual['actualReconstructedAlpha'],
                     'Every actual review callback/header/whole pixel digest bound to original RAM')
                viewed.append(row)
            need([r['index'] for r in viewed] == [1, 2, 10, 17, 49, 122], 'Exact actually inspected callbacks')
        qualifications.append(dict(nativePID=expected_pid, wholeOriginalRGBCallbacks=positive,
                                   actuallyViewedCallbacksThisTurn=viewed, wholeOriginalStateHealth=proof['qualification']))
    for path in (Path(__file__), ROOT / 'audit_native_selector_startup_pcm_visual_transport_rejection.json',
                 Path(artifact.__file__).resolve(), Path(migration.__file__).resolve()):
        pins[str(path.resolve())] = migration.sha(path)
    need(all(migration.sha(path) == digest for path, digest in pins.items()),
         'Complete fresh current source/runtime/evidence pin census')
    OUT.mkdir()
    report = dict(passed=True, goalStatus='active', qualifications=qualifications,
                  wholeOriginalRGBCallbacks=sum(len(r['wholeOriginalRGBCallbacks']) for r in qualifications),
                  actuallyViewedCallbacksThisTurn=6, completeAllModePhysicalFields=7204,
                  originalStateHealthCounterexamples=parent['actualFaultsRejected'],
                  actualRasterFaultsRejected=faults, inputHashes=pins,
                  originalLoadedSourceIndependentlyPinned=True,
                  requirements=parent['requirements'], remainingGroups=parent['remainingGroups'],
                  originalMirrorRejectionsPreserved=True, fullNaturalCPUChoiceAcceptance=False,
                  completedGrabAcceptance=False, fullParticlesCleanupAccepted=False,
                  wholeRasterAudioAcceptance=False, fullPortAcceptance=False,
                  publicPlayableChanged=False, newNativeGames=0, newBuilds=0, newROMCopies=0,
                  newRawMedia=0, newZIPs=0)
    artifact.save(OUT / 'report.json', report)
    print('PASS7204 native callbacks/408 health stores/889 state stores/189 original rasters/six actual views; wider goal active', flush=True)
    return report
