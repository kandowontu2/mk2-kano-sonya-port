"""Four actual current native morph/special/return routes, with24 seen images.

One late Cannonball/Square Wave per form/player slot, not universal morph,
other opponent/arena/adversity, whole scene replay or finished port acceptance.
Completed P1 Kano is retained, not replayed. No new native game in this seal.
"""
import hashlib
import json
import sys
from pathlib import Path
import capture_native_selector_morph_startup_return as capture
import qualify_native_selector_morph_startup_return as first
import qualify_native_selector_morph_remaining_slots as remaining

ROOT, need, sha = capture.ROOT, capture.need, capture.sha
OUT = ROOT/'audit_native_selector_morph_late_special_matrix_checked'


def execute():
    need(not OUT.exists() and not capture.original.original.identity.census(),
         'One immutable full finite matrix, every original native child terminal')
    pins = {}; cases = []; identities = []
    requirements = groups = None
    for move,side in (('ball',1),('square',1),('ball',2),('square',2)):
        c = capture.CASES[move,side]
        path = ROOT/f'audit_native_selector_morph_startup_return_{move}_p{side}_checked/report.json'
        views_path = ROOT/('audit_native_selector_morph_startup_actual_views.json' if (move,side)==('ball',1)
                         else f'audit_native_selector_morph_{move}_p{side}_actual_views.json')
        proof = json.loads(path.read_text()); views = json.loads(views_path.read_text())
        identity = c['terminal']['actualWindowsIdentity']
        process = json.loads((c['folder']/'process.json').read_text())
        need(proof['passed'] and views['passed'] and c['report']['passed'] and
             c['process'].poll() == c['terminal']['nativeExit'] == 0 and
             identity == proof['actualNativeIdentity'] == views['actualNativeIdentity'] == process['actualWindowsIdentity'] and
             identity['ProcessId'] == c['process'].pid and identity['ParentProcessId'] == 38752 and
             views['identityRevalidatedBeforeAndAfter'] and
             (views['actualHostIdentity']['ProcessId'],views['actualHostIdentity']['ParentProcessId'],
              views['actualHostIdentity']['createdUnix']) == (38752,40316,1791734919.6266766),
             'Every distinct native handle/first Win32 identity/proof and actual view host agree')
        need((c['move'],c['side']) == (move,side) and
             len(c['rgbFrames']) == len(c['rgb']) == 43 and
             all(bytes(c['coldBuffers'][k]) == v for k,v in capture.SCOPE['WINDOWS'].items()),
             'Actual correct route, complete current native windows and all43 captured rasters')
        selected = views['actualViewedCallbacks']
        need([r['index'] for r in selected] == ([4,12,13,21,23,42] if move=='ball' else [3,12,13,21,23,42]),
             'Six actually inspected form/special/return/ordinary/final native images per route')
        for image,header in zip(c['rgbFrames'],c['rgb'],strict=True):
            need(image['header'] == header and hashlib.sha256(image['pixels']).hexdigest().upper() == header['sha256'],
                 'Every complete original native image retains exact whole-byte digest')
        for r in selected:
            actual = c['rgbFrames'][r['index']]; raw = actual['pixels']
            need(r['header'] == actual['header'] and r['SHA256'] == actual['header']['sha256'] and
                 len(raw) == 406400 and raw[3::4] == bytes([255])*101600 and r['actualReconstructedAlpha'] == 255,
                 'Exact actual reviewed native buffer/header and all alpha bytes')
            rgb = b''.join(raw[i:i+3][::-1] for i in range(0,len(raw),4))
            need(hashlib.sha256(rgb).hexdigest().upper() == r['nativeRGBSHA256'],
                 'Independent full native RGB reconstruction equals actual viewed pixels')
        physical, audio = proof['completePhysicalAndHealthInventory'], proof['completeSourceWaveform']
        need(physical['passed'] and physical['continuousPhysicalFields'] == 4802 and
             physical['nativeRosterRemainsShang'] and physical['actualOrdinaryControlsAfterReturnAccepted'] and
             physical['nativeReturnSchedulingInstructionIntervalUnchanged'] and
             audio['passed'] and audio['differentChannelSamples'] == 0 and
             audio['actualSHA256'] == audio['predictedSHA256'] and
             len(proof['actualMorphFaultsRejected']) == 18 and
             len(audio['actualWaveformFaultsRejected']) == 5 and
             len(proof['sourceDAC']['faults']) == 4 and len(proof['wholeSoundROM']['faults']) == 8,
             'Every whole source-qualified physical/return/controls/audio and35 original actual faults')
        if requirements is None: requirements,groups = proof['requirements'],proof['remainingGroups']
        need(proof['requirements'] == requirements and proof['remainingGroups'] == groups,
             'Full original14 requirements and six remaining work groups conserved')
        for p,h in proof['inputHashes'].items():
            need(p not in pins or pins[p] == h, 'Never relabel conflicting historical/actual input')
            pins[p] = h
        for p in (path,views_path): pins[str(p.resolve())] = sha(p)
        identities.append((identity['ProcessId'],identity['createdUnix']))
        cases.append(dict(move=move,slot=side,actualNativeIdentity=identity,
            qualification=str(path),qualificationSHA256=sha(path),views=str(views_path),viewsSHA256=sha(views_path),
            nativeForwardStore=physical['originalForwardStoreFrame'],nativeReturnEntries=physical['originalReturnEntries'],
            nativeReturnStore=physical['originalReturnStoreFrame'],returnDeferredFields=physical['returnEntryDeferredFields'],
            actualPhysicalInputs=physical['physicalInputs'],nativeHealthStores=physical['allNativeHealthWrites'],
            physicalSlotFields=physical['continuousPhysicalFields'],wholeStereoFrames=audio['comparedStereoFrames'],
            wholePCMSHA256=audio['actualSHA256'],actualFaultsRejected=35,wholeRGBCallbacks=43,actualViewedCallbacks=6))
    need(len(set(identities)) == 4, 'Four genuinely distinct original native processes; no case relabelling')
    sources = {Path(__file__).resolve(),
        (ROOT/'tools/read_native_selector_morph_remaining_frames.py').resolve(),
        (ROOT/'tools/read_native_selector_morph_remaining_frames_remote.py').resolve()}
    for module in tuple(sys.modules.values()):
        name = getattr(module,'__file__',None)
        if name:
            path = Path(name).resolve()
            if path.is_relative_to(ROOT) and path.is_file(): sources.add(path)
    for path in sources:
        p = str(path); h = sha(path)
        need(p not in pins or pins[p] == h, 'Immutable executed source inventory')
        pins[p] = h
    need(all(sha(p) == h for p,h in pins.items()), 'Entire current source/evidence inventory after full matrix seal')
    value = dict(passed=True,goalStatus='active',cases=cases,inputHashes=pins,
        requirements=requirements,remainingGroups=groups,
        actualDistinctNativeRoutes=4,actualViewedNativeImages=24,wholeNativeRGBCallbacks=172,
        physicalSlotFields=sum(r['physicalSlotFields'] for r in cases),
        comparedStereoFrames=sum(r['wholeStereoFrames'] for r in cases),
        effectiveActualFaultsRejected=140,
        finiteBothFormsBothSlotsLateSpecialNativeReturnAccepted=True,allMorphContextsAccepted=False,
        sourceBoundWholeSceneReplayAccepted=False,fullPortAcceptance=False,publicPlayableChanged=False,
        newNativeGamesDuringSeal=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir(); (OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print('PASS four distinct current native form/late-special/return routes,24 actual views and140 faults',flush=True)
    return value
