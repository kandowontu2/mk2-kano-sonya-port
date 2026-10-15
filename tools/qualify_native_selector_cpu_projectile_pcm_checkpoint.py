"""Bind completed finite audio delivery and six actual visual inspections."""
import hashlib, json, os
from pathlib import Path
import numpy as np
import qualify_native_selector_cpu_projectile_pcm_delivery_effective as delivery

ROOT = delivery.original.ROOT
OUT = ROOT / 'audit_native_selector_cpu_projectile_pcm_checkpoint_checked'
sha = delivery.original.sha
need = delivery.original.need

def execute(state):
    need(not OUT.exists() and os.getpid() == 38752, 'Original retained host; immutable new receipt')
    receipt_path = delivery.OUT / 'report.json'
    report = json.loads(receipt_path.read_text())
    need(report['passed'] and len(report['actualRecordSourceFaultsRejected']) == 20,
         'Whole actual source/packet/clock gate and twenty effective faults')
    need(all(sha(p) == h for p, h in report['inputHashes'].items()), 'Every executed input remains pinned')
    capture = delivery.original.capture
    held = capture.NATIVE_HANDLES[capture.KEY]
    need(held['process'].poll() == 0 and held['identity'] == report['actualNativeIdentity'], 'Same original terminal game')
    folder, text, images = capture.RAM_CASES[capture.KEY]
    frames = json.loads((folder / 'result.json').read_text())['actualScenes']
    need(len(frames) == len(images) == 66, 'Entire original callback inventory, not a selected subset')
    for row in frames:
        rgb = images[row['imageKey']]
        need(rgb.shape == (254,400,3) and rgb.dtype == np.uint8, 'Whole native RGB dimensions/type')
        raw = np.empty((254,400,4),np.uint8)
        raw[:,:,:3] = rgb[:,:,::-1]
        raw[:,:,3] = 255
        need(hashlib.sha256(raw.tobytes()).hexdigest().upper() == row['sha256'], 'Every original captured BGRX digest')
    visual_path = ROOT / 'audit_native_selector_cpu_projectile_pcm_visual_review.json'
    visual = json.loads(visual_path.read_text())
    need(visual['passed'] and visual['actualNativeIdentity'] == held['identity'], 'Actual read-only viewed case')
    need([r['index'] for r in visual['actuallyViewedCallbacks']] == [1,2,10,17,24,59], 'Only six actual inspected callbacks claimed')
    for viewed in visual['actuallyViewedCallbacks']:
        need(viewed['header'] == frames[viewed['index']] and viewed['SHA256'] == viewed['header']['sha256'], 'Each inspected callback binds original full pixel digest')
    fixed = {
        ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
        ROOT/'mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
        ROOT/'mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644',
        ROOT/'diagnostic_native_selector_layers_long/mkport_candidate.exe':'EBDFEB6CCA3617308F1448A4A0F6778E3E787420CACF3D11E9B4F40358C87F6A',
        ROOT/'PLAY_LATEST_KANO_SONYA.cmd':'D6BABF8CBC1F4CB020F3D7F3A2C8C5A3A762B946E83D56FC1E5BA3B398129DE5',
        ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip':'4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C'}
    need(all(sha(p) == h for p,h in fixed.items()), 'Game sources/private executable/public CMD and ZIP unchanged')
    pins = dict(report['inputHashes'])
    pins.update({str(p):h for p,h in fixed.items()})
    for p in (Path(__file__).resolve(),receipt_path,visual_path,
        ROOT/'tools/read_native_selector_cpu_projectile_pcm_frames.py',
        ROOT/'tools/read_native_selector_cpu_projectile_pcm_frames_remote.py',
        ROOT/'tools/read_native_selector_cpu_projectile_pcm_frames_bound.py',
        ROOT/'tools/read_native_selector_cpu_projectile_pcm_frames_bound_remote.py',
        ROOT/'audit_native_selector_cpu_projectile_pcm_view_failure.json'):
        pins[str(p)] = sha(p)
    OUT.mkdir()
    result = dict(passed=True,goalStatus='active',thisGoalTurnClassification='progress',
        actualNativeIdentity=held['identity'],completeStereoFrames=report['completeStereoFrames'],
        completeMixedPCMSourceAndDeliveryAccepted=True,effectiveDeliveryFaults=20,
        all66OriginalRGBDigestsVerified=True,actuallyViewedCallbacks=visual['actuallyViewedCallbacks'],
        transitionBackdropStockComparisonRequired=True,allVisualsAccepted=False,
        allStartupReleaseAudioAccepted=False,allArenasSlotsVictimsAudioAccepted=False,
        heardAudioQualityAccepted=False,fullPortAcceptance=False,
        requirements=report['requirements'],remainingGroups=report['remainingGroups'],inputHashes=pins,
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0,publicPlayableChanged=False)
    capture.prior.current.prior.save(OUT/'report.json', result)
    print('PASS finite full audio delivery and six viewed callbacks; stock exit backdrop comparison remains open',flush=True)
    return result
