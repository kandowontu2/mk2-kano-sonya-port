"""Keep the full natural-port scope; add the existing-capture release proof."""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_native_bicycle_release_push_v3337 as current

ROOT=current.ROOT
OUT=ROOT/'audit_v3344_current_bicycle_push_full_scope_checkpoint'
PREVIOUS=ROOT/'audit_v3334_current_bicycle_full_scope_checkpoint/checkpoint.json'
need=current.need

def main():
    need(not OUT.exists(),'Immutable full-scope checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=state['remaining']
    need(state['goalStatus']=='active' and len(remaining)==5 and not state['fullPortAcceptance'] and
         not state['finishedRelease'] and not state['actualEndingsAccepted'] and
         state['currentRealShaoKahnMatchClears']==0,'Original unfinished full-port scope')
    fresh={}
    def pin(path,digest=None):
        path=Path(path).resolve();key=str(path)
        digest=digest or current.prior.current.assembly.sha(path)
        need(key not in fresh or fresh[key]==digest,'Consistent executed input')
        need(key not in state['inputHashes']or state['inputHashes'][key]==digest,'No inherited evidence relabelled')
        fresh[key]=digest
    path=current.OUT/'report.json';positive=json.loads(path.read_text());pin(path)
    units_path=ROOT/'audit_v3342_native_bicycle_release_push_counterexamples/report.json'
    units=json.loads(units_path.read_text());pin(units_path)
    need(positive['passed'] and positive['capturedReleaseHorizontalAccepted'] and
         positive['ownHorizontalFields']==30 and positive['victimHorizontalFields']==55 and
         positive['completeSourceBoundCacheParts']==190 and positive['branches']==
         {'suppressed':2,'repel':2,'requested':25,'shared_p2':1},'Actual complete source-derived captured release')
    need(units['passed'] and units['actualCounterexamplesRejected']==16 and
         units['independentBranchBoundaryVectors']==12 and units['samePathPositiveControlsAccepted'] and
         units['unrelatedMissingEventExceptionsNeverAccepted'],'Specific actual and model negatives with untouched positive controls')
    for proof in (positive,units):
        need(not proof['fullPortAcceptance'],'Bounded proof never promotes full goal')
        for file,digest in proof['inputHashes'].items():pin(file,digest)
    failures=[]
    for relative,script,cause in (
        ('audit_v3336_native_bicycle_release_push_checked/report.json','tools/verify_native_bicycle_release_push_v3335.py',
         'Harness assumed16-bit MOVI3; actual source emits32-bit09E0/0003/0000. Corrected source binding and strict cache parser only; no game change.'),
        ('audit_v3340_native_bicycle_release_push_counterexamples/report.json','tools/test_native_bicycle_release_push_v3339.py',
         'Negative harness mutated hexadecimal20388 outside body code rather than computed bit-address byte offset20360decimal. Corrected targeted mutation; no assertion weakened.')):
        path=ROOT/relative;failure=json.loads(path.read_text());need(not failure['passed'],'Failed harness evidence retained')
        pin(path);pin(ROOT/script);failures.append(dict(report=str(path),error=failure['error'],cause=cause))
    pin(PREVIOUS);pin(__file__)
    with ThreadPoolExecutor(max_workers=4)as pool:
        for (file,digest),actual in zip(fresh.items(),pool.map(current.prior.current.assembly.sha,fresh)):
            need(actual==digest,'Fresh proof/source/capture bytes independently unchanged')
    state['inputHashes'].update(fresh)
    state.update(previousCheckpoint=str(PREVIOUS),
                 previousGoalTurnClassification='no progress: acknowledgement only; revalidated current source and existing bounded contact/render/erase evidence before advancing.',
                 thisGoalTurnClassification='progress: original native body-push/bounds/request/facing bytes unchanged; independent multipart cache bounds replay30own/55victimhorizontalfields/190parts; two suppressedfields/tworepulsions/onesharedhalf-speed branch;16specificactualcorruptions+12branchboundaryvectors. No game/build/ROM/capture/audio/promotion changes; full five-group objective retained.',
                 currentNativeBicycleFullHorizontalPushReplayAccepted=True,
                 currentNativeBicycleHorizontalProofScope='Only existing3172nativeCPUSonya18/humanKano17Bicyclecontact: original complete release horizontal integration/publication through own ready and victim landing/ready. Not all body-push branches, all moves, CPU, KO, arenas or audio.',
                 currentNativeBicycleHorizontalReport=str(current.OUT/'report.json'),
                 currentNativeBicycleHorizontalCounterexampleReport=str(units_path),
                 currentNativeBicycleHorizontalQualifiedCounterexamples=16,
                 currentNativeBicycleHorizontalBoundaryVectors=12,
                 candidateUnderTestCapturedNativeBicycleHitTrajectoryAccepted=True,
                 candidateUnderTestNativeBicycleHitOrBlockedAccepted=False,
                 currentNativeBicycleBlockedAllArenasAudioKOOverlapAccepted=False,
                 currentNativeBicycleNewHarnessFailuresPreserved=failures,
                 gameSourceAndPlayableBytesChangedThisTurn=False,nativeGuestProgramChangedThisTurn=False,
                 publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
                 inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),
                 goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
                 nextAction='Continue3172ordinary-inputblockedBicycle/contact/CPU/KO/overlap/morph contexts and remaining native art/arena/finisher/audio gates. Captured unblocked trajectory and109nativevisual/erase scenes are now bounded evidence, not all-move acceptance. Natural Kintaro/Shao match clears, own endings/attract, final combined selection/ladder/names/audio and refreshed release remain required. Reuse builds and bounded compressed captures; never recreate retired raw failed-campaign mixes/archive.')
    need(state['remaining']==remaining and len(remaining)==5 and not state['actualEndingsAccepted'] and
         not state['candidateUnderTestBroadCPUOrKOOrMorphCoverageAccepted'],'No original requirement reduced')
    OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(state,indent=2)+'\n')
    digest=current.prior.current.assembly.sha(path)
    compact=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(compact.returncode==0 and current.prior.current.assembly.sha(path)==digest,'Lossless checkpoint compression unchanged')
    print(json.dumps(dict(saved=str(path),goalStatus='active',originalRemainingGroups=5,
                         capturedHorizontalAccepted=True,actualCorruptionsRejected=16,
                         modelBoundaryVectors=12,freshPinsRehashed=len(fresh),fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
