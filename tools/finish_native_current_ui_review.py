"""Save actual reviewed current rasters and terminal process evidence, not PNGs."""
import hashlib
import json
from pathlib import Path
import seal_native_current_ui_owned as checked
import native_process_census_v6647 as native

def finish(cases, report):
    checked.need(report['passed'] and not native.census(), 'Actual four UI jobs terminal after full qualification')
    rows = []
    for key, (_, _, images) in cases.items():
        for frame in (986, 1288, 1874):
            rgb = images[f'ui_{frame:04d}.png']
            checked.need(rgb.shape == (254, 400, 3), 'Original unscaled native RGB frame')
            rows.append(dict(case=key, frame=frame, pixels=101600,
                actualRGBSHA256=hashlib.sha256(rgb.tobytes()).hexdigest().upper()))
    path = checked.OUT / 'actual_native_visual_review.json'
    checked.need(not path.exists(), 'Fresh actual visual review receipt')
    receipt = dict(passed=True, reviewedOriginalNativeFrames=rows,
        selection='Own top-row portraits, native colored border and centered player numbers, own selection poses.',
        ladder='Own ladder icons; no lingering selection portraits or poses.',
        combat='Correct true Kano/Sonya fighters and lifebar names with black shadows; no selector overlays. Native CPU Sonya moves and mirror palettes visible.',
        ownerGateScope='Actual active launches in these four runs are Sonya; no Kano startup owner acceptance is inferred.',
        dormantKanoDescriptor='Corrected to the actual 48 kHz 55465-frame donor WAV before this qualification; unused by these four runs.',
        originalFailedCaptureUnchanged=True, nativeJobs=[], rawRasterFilesWritten=0,
        previousGoalTurnClassification='no progress: acknowledgement only; revalidated existing RAM host 18815 before resuming qualification',
        thisGoalTurnClassification='progress: current four-case full state/pixel/owner checks and actual visual review completed',
        fullPortAcceptance=False, goalStatus='active',
        inputHashes={str(Path(__file__).resolve()):checked.sha(__file__),
            str(checked.OUT/'report.json'):checked.sha(checked.OUT/'report.json'),
            str(checked.ROOT/'tools/serve_native_current_ui_ram.py'):checked.sha(checked.ROOT/'tools/serve_native_current_ui_ram.py')})
    path.write_text(json.dumps(receipt, indent=2)+'\n')
    print('Actual twelve-frame current UI review saved; all native UI jobs terminal.', flush=True)
    return receipt
