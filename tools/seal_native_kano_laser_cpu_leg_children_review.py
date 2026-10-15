"""Seal this actual mixed trace and 21 individually inspected native RAM frames.

No proxy identity, projectile/fighter alias, replay, disk raster or whole-port
claim. Original failed repeated acceptance and schema-binding failure retained.
"""
import hashlib
import json
from pathlib import Path
import verify_native_kano_laser_cpu_leg_children_faults as faults

ROOT,need,sha,base=faults.ROOT,faults.need,faults.sha,faults.base
OUT=ROOT/'audit_native_kano_laser_cpu_leg_children_review'
VIEWED=[998,1174,1288,1816,1850,1880,1884,1888,1892,1944,1963,1993,1997,2001,2005,2019,2541,2571,2575,2579,2583]


def run(actual):
    need(not OUT.exists() and not base.identity.census(),'Actual native is terminal; no gameplay replay')
    qualification_path=faults.health.OUT/'report.json'
    faults_path=faults.OUT/'report.json'
    qualification=json.loads(qualification_path.read_text())
    counterexamples=json.loads(faults_path.read_text())
    need(qualification['passed'] and counterexamples['passed'] and
         len(counterexamples['actualNativeOwnershipPhaseGuardHealthFaultsRejected'])==35 and
         len(qualification['actualOriginalBodyShadowFaultsRejected'])==11,
         'Whole actual mixed health/body/shadow plus all 46 native counterexamples accepted')
    for report in (qualification,counterexamples):
        need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Every actual executed input and evidence conserved')
    folder,text,images=actual.RAM_CASES[actual.KEY]
    metadata=json.loads((folder/'result.json').read_text())
    terminal=json.loads((folder/'native_terminal.json').read_text())
    need(not metadata['passed'] and terminal['nativeExit']==0 and not terminal['hostDecodeErrors'] and
         not (folder/'stderr.log').read_text() and len(metadata['proofs'])==2 and
         not base.re.search(r'LUA ERROR|stack traceback|fatal error|access violation|WRONG CHECKSUMS|might not run correctly',text,base.re.I),
         'Preserve failed original repeated/KO observer gate; actual native transport was warning-free and terminal0')
    failed=[s for s in text.splitlines()if s.startswith('MK2_HSPECIAL_FAILED ')]
    need(len(failed)==1 and 'reason=lost_owned_pair_at_field_done'in failed[0] and
         qualification['case']['state']['wholeNativeHealthHistory']['lastPreHPZero'],
         'The sole original observer failure is the actual witnessed KO boundary, not an unexplained freeze')
    need([s['frame']for s in metadata['actualScenes']]==VIEWED and len(images)==len(VIEWED),
         'Exactly all 21 individually viewed original native scenes, no reconstruction or substituted art')
    reviews=[]
    for scene in metadata['actualScenes']:
        frame=scene['frame'];rgb=images[f'ui_{frame:04d}.png']
        need(rgb.shape==(254,400,3),'Complete original unscaled native RAM raster')
        reviews.append(dict(frame=frame,stage=scene['stage'],sourceRawBGRXSHA256=scene['sha256'],
            nativeRGBSHA256=hashlib.sha256(rgb.tobytes()).hexdigest().upper(),individuallyViewed=True))
    need(not any(p.is_file()and p.suffix.lower()in('.png','.wav','.bin','.exe','.zip')for p in actual.BASE.rglob('*')),
         'No raw media, ROM or build copies created by this actual trial')
    pins=dict(counterexamples['inputHashes'])
    for p in (Path(__file__),qualification_path,faults_path,actual.OUT/'failure.json',
              faults.health.prior.OUT/'failure.json'):
        pins[str(p.resolve())]=sha(p)
    need(sha(ROOT/'PLAY_LATEST_KANO_SONYA.cmd')=='D6BABF8CBC1F4CB020F3D7F3A2C8C5A3A762B946E83D56FC1E5BA3B398129DE5',
         'Public CMD remains unchanged; finite private acceptance is not public promotion')
    state=qualification['case']['state']
    OUT.mkdir();base.save(OUT/'report.json',dict(passed=True,candidate=actual.native.NAME,key=actual.KEY,
        selectedOriginalLeg=state['selectedOriginalLeg'],selectedOriginalRing=state['selectedOriginalRing'],
        wholeNativeHealthHistory=state['wholeNativeHealthHistory'],nativeFlagStores=state['wholeNativeFlagStores'],
        actualSourceBoundShadowCopies=qualification['case']['actualSourceBoundShadowCopies'],
        actualOriginalBodyShadowFaults=11,actualPhaseOwnershipGuardHealthFaults=35,
        individuallyReviewedOriginalRasters=reviews,actualWholeGuestComparedInRAM=True,
        actualWholeGuestSHA256=hashlib.sha256(actual.guest).hexdigest().upper(),
        repeatedTwoUninterruptedPairGateStillRejected=True,earlierFailuresPreserved=True,
        finiteMixedRingOwnershipVerified=True,allNativeHPContextsInThisTraceVerified=True,
        allNativeFighterBodyShadowFieldsInThisTraceVerified=True,
        projectileFullRasterAcceptance=False,fullKOTransitionAccepted=False,
        fullCPUOrArenaAcceptance=False,fullAudioAcceptance=False,fullPortAcceptance=False,
        publicPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        inputHashes=pins,goalStatus='active',scope=__doc__,
        nextAction='Test the other native CPU slots/moves, blocked and unblocked contacts, arenas, projectile rasters/audio and actual post-KO round/ladder continuation; do not promote until combined acceptance.'))
    print(json.dumps(dict(passed=True,actualMixedRingDamage=6,nativeHPStores=25,
                         fighterShadowCopies=qualification['case']['actualSourceBoundShadowCopies'],
                         actualFaultsRejected=46,reviewedNativeRasters=len(reviews),fullPortAcceptance=False)),flush=True)
