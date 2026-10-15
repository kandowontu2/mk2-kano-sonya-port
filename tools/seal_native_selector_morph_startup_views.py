"""Bind six actually reviewed whole native images to original46572 proof."""
import hashlib
import json
import sys
from pathlib import Path
import capture_native_selector_morph_startup_return as capture
import qualify_native_selector_morph_startup_return as qualification

ROOT, need, sha = capture.ROOT, capture.need, capture.sha
OUT = ROOT/'audit_native_selector_morph_startup_review_checked'
VIEWS = ROOT/'audit_native_selector_morph_startup_actual_views.json'


def execute(c):
    need(not OUT.exists(), 'Immutable same-native morph visual checkpoint')
    report_path = qualification.OUT/'report.json'
    report = json.loads(report_path.read_text())
    views = json.loads(VIEWS.read_text())
    need(report['passed'] and views['passed'] and
         c['process'].poll() == c['terminal']['nativeExit'] == 0 and
         c['terminal']['actualWindowsIdentity'] == report['actualNativeIdentity'] == views['actualNativeIdentity'] and
         views['identityRevalidatedBeforeAndAfter'] and
         (views['actualHostIdentity']['ProcessId'], views['actualHostIdentity']['ParentProcessId'],
          views['actualHostIdentity']['createdUnix']) == (38752,40316,1791734919.6266766) and
         not capture.original.original.identity.census(), 'Same terminal native and exact original live host')
    need([r['index'] for r in views['actualViewedCallbacks']] == [4,12,13,21,23,42],
         'Six actually viewed independent original native frames')
    for record in views['actualViewedCallbacks']:
        image = c['rgbFrames'][record['index']]
        raw, header = image['pixels'], image['header']
        need(header == record['header'] and hashlib.sha256(raw).hexdigest().upper() ==
             header['sha256'] == record['SHA256'] and len(raw) == 406400 and
             raw[3::4] == bytes([255])*101600 and record['actualReconstructedAlpha'] == 255,
             'Every original whole native pixel/header/alpha digest matches reviewed callback')
        rgb = b''.join(raw[i:i+3][::-1] for i in range(0,len(raw),4))
        need(hashlib.sha256(rgb).hexdigest().upper() == record['nativeRGBSHA256'],
             'Independent full RGB reconstruction equals actual reviewed native image')
    need(len(c['rgbFrames']) == len(c['rgb']) == 43, 'All original native callback inventories retained')
    for actual, header in zip(c['rgbFrames'], c['rgb'], strict=True):
        need(actual['header'] == header and hashlib.sha256(actual['pixels']).hexdigest().upper() == header['sha256'],
             'Every full original captured native image retains its digest')
    pins = dict(report['inputHashes'])
    paths = {Path(__file__).resolve(), report_path.resolve(), VIEWS.resolve(),
        (ROOT/'tools/read_native_selector_morph_startup_frames.py').resolve(),
        (ROOT/'tools/read_native_selector_morph_startup_frames_remote.py').resolve()}
    for module in tuple(sys.modules.values()):
        name = getattr(module,'__file__',None)
        if name:
            path = Path(name).resolve()
            if path.is_relative_to(ROOT) and path.is_file(): paths.add(path)
    for path in paths:
        key = str(path); digest = sha(path)
        need(key not in pins or pins[key] == digest, 'No immutable actual source/evidence replaced')
        pins[key] = digest
    need(all(sha(p) == h for p,h in pins.items()), 'Complete current actual source/capture inventory')
    value = dict(passed=True, goalStatus='active', actualNativeIdentity=report['actualNativeIdentity'],
        originalQualification=str(report_path), originalQualificationSHA256=sha(report_path),
        actualViews=views, allOriginalWholeRGBCallbacks=43, inputHashes=pins,
        requirements=report['requirements'], remainingGroups=report['remainingGroups'],
        finiteActualP1KanoMorphLateSpecialReturnReviewed=True, allMorphContextsAccepted=False,
        sourceBoundFullSceneReplayAccepted=False, fullPortAcceptance=False, publicPlayableChanged=False,
        newNativeGames=0, newBuilds=0, newROMCopies=0, newRawMediaFiles=0, newZIPs=0)
    OUT.mkdir(); (OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print('PASS same46572 native morph proof/six actual views/all43 whole images; full scope remains active',flush=True)
    return value
