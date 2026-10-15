"""Two actual current jobs: full-damage ring and native KO/reset/live resume.

Seal 21 individually viewed guard rasters and independently byte-equal backing
from the second native job. No post-KO pixels, ordinary human responses, PCM,
all CPU/arena/ladder or complete port acceptance is inferred.
"""
import hashlib
import json
from pathlib import Path
import verify_native_kano_laser_cpu_leg_children_guard as guard
import verify_native_kano_laser_cpu_post_ko_ground as ko

ROOT,need,sha,base=guard.ROOT,guard.need,guard.sha,guard.base
OUT=ROOT/'audit_native_kano_laser_cpu_unblocked_round_progress'


def run(actual,post):
    need(not OUT.exists() and not base.identity.census(),'Both actual native jobs terminal; no replay')
    guard_path=guard.REVIEW/'report.json';ko_path=ko.OUT/'report.json'
    reviewed=json.loads(guard_path.read_text());resumed=json.loads(ko_path.read_text())
    need(reviewed['passed'] and resumed['passed'] and len(reviewed['individuallyReviewedOriginalRasters'])==21 and
         reviewed['actualPhaseOwnershipGuardHealthFaults']==35 and reviewed['actualOriginalBodyShadowFaults']==11 and
         len(resumed['actualSemanticFaultsRejected'])==16 and resumed['actualAllModeHealthFields']==2230,
         'Actual independent native ring/health/ground/shadow/KO/reset proof and all62 counterexamples')
    for report in (reviewed,resumed):
        need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Every actually executed immutable source/candidate/evidence pin')
    first_folder,first_text,first_images=actual.RAM_CASES[actual.KEY]
    last_folder,last_text,last_images=post.RAM_CASES[post.KEY]
    need(set(first_images)==set(last_images) and len(first_images)==len(last_images)==21,
         'Both actual native jobs retain exactly the same scene keys, no missing image aliases')
    backing=[]
    for image_review in reviewed['individuallyReviewedOriginalRasters']:
        frame=image_review['frame'];name=f'ui_{frame:04d}.png'
        a,b=first_images[name],last_images[name]
        need(a.shape==b.shape==(254,400,3) and a.tobytes()==b.tobytes() and
             hashlib.sha256(a.tobytes()).hexdigest().upper()==image_review['nativeRGBSHA256'],
             'Every second-job original native image is byte-equal to its individually viewed original native backing')
        backing.append(dict(frame=frame,nativeRGBSHA256=image_review['nativeRGBSHA256'],
                            allActualRGBBytesCompared=True,viewedNativeBackingVerified=True))
    pins={}
    for report in (reviewed,resumed):pins.update(report['inputHashes'])
    for p in (Path(__file__),Path(guard.__file__),Path(ko.__file__),guard_path,ko_path):
        pins[str(p.resolve())]=sha(p)
    for owner,key in ((actual,actual.KEY),(post,post.KEY)):
        folder=owner.RAM_CASES[key][0]
        terminal=json.loads((folder/'native_terminal.json').read_text())
        need(terminal['nativeExit']==0 and not terminal['hostDecodeErrors'],
             'Both exact native producer handles terminal0 with complete current RAM inventories')
        for p in folder.rglob('*'):
            if p.is_file():
                need(p.suffix.lower()not in('.png','.wav','.bin','.exe','.zip'),'No raw media/build/ROM/archive copies')
                pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All current immutable evidence stable before sealing')
    OUT.mkdir();base.save(OUT/'report.json',dict(passed=True,candidate=actual.native.NAME,
        actualNativeJobs=2,actualOriginalRastersIndividuallyReviewed=21,actualSecondJobRasterBackings=backing,
        originalRAMRastersToRelease=42,actualCounterexamplesRejected=62,
        fullDamageRing=reviewed['selectedOriginalRing'],nativeRoundResume=resumed['actualNativeKORoundResume'],
        trueSonyaIdentityMaintained=True,actualNativeModes=[2,5,6,7,2],
        actualNativeFullHealthResetAndSixtyLiveFieldsVerified=True,
        originalRepeatedGateAndGroundModelFailuresPreserved=True,
        postKONativeRasterAcceptance=False,postResetHumanControlResponseAcceptance=False,
        fullCPUOrArenaAcceptance=False,fullAudioAcceptance=False,fullPortAcceptance=False,
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False,
        inputHashes=pins,goalStatus='active',scope=__doc__,
        nextAction='Broaden actual CPU slots/moves/opponents, post-reset response/body/shadow/audio, arenas, remaining finishers and campaign/cinematic acceptance; keep public CMD/ZIP unchanged until combined acceptance.'))
    print(json.dumps(dict(passed=True,actualCounterexamplesRejected=62,actualNativeRoundResume=True,
                         originalRAMRastersToRelease=42,newBuilds=0,fullPortAcceptance=False)),flush=True)
