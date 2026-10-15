"""Preserve the full natural-port objective; record both-slot real blocked tests."""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_current_bicycle_block_v3350 as current

ROOT=current.ROOT;OUT=ROOT/'audit_v3355_current_bicycle_block_full_scope_checkpoint'
PREVIOUS=ROOT/'audit_v3344_current_bicycle_push_full_scope_checkpoint/checkpoint.json'
need=current.need

def main():
    need(not OUT.exists(),'Immutable new full-scope checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=state['remaining']
    need(state['goalStatus']=='active' and len(remaining)==5 and not state['fullPortAcceptance'] and
         not state['finishedRelease'] and not state['actualEndingsAccepted'] and
         state['currentRealShaoKahnMatchClears']==0 and state['currentNativeBicycleFullHorizontalPushReplayAccepted'],
         'Keep original unfinished scope and completed bounded release proof')
    fresh={}
    def pin(path,digest=None):
        path=Path(path).resolve();key=str(path);digest=digest or current.current.assembly.sha(path)
        need(key not in fresh or fresh[key]==digest,'Consistent executed proof bytes')
        need(key not in state['inputHashes']or state['inputHashes'][key]==digest,'Existing immutable evidence never relabelled')
        fresh[key]=digest
    def proof(relative):
        path=ROOT/relative;result=json.loads(path.read_text());need(result['passed'] and not result['fullPortAcceptance'],'Actual bounded positive evidence')
        pin(path)
        for file,digest in result['inputHashes'].items():pin(file,digest)
        return result
    first=proof('audit_v3349_current_bicycle_block_checked/report.json')
    tested=proof('audit_v3351_current_bicycle_block_checked/report.json')
    units=proof('audit_v3353_current_bicycle_block_counterexamples/report.json')
    need(first['cases']==tested['cases'] and tested['physicalFixtures']==2 and tested['nativeFields']==720 and
         tested['sourceBoundStateStores']==24 and tested['actualBothPhysicalSlotsBlockedChipAndRecoveryAccepted'] and
         all(c['nativeChipDamage']==3 and c['start']==1593 and c['contact']==1601 and c['landing']==1624 and
             c['regain']==1630 and c['wholeContactStartupSeekAndVerticalReboundAccepted'] and
             c['ordinaryFollowup']['fields']==1050 and not c['defenderFullHorizontalPushAndRasterShadowAudioAccepted']
             for c in tested['cases']),'Whole actual both-slot blocked state/contact/vertical/recovery, no broader raster claim')
    need(units['actualCounterexamplesRejected']==46 and units['physicalSlots']==2 and
         units['samePathPositiveControlsAccepted'] and units['unrelatedMissingEventExceptionsNeverAccepted'],
         'Every actual negative qualified by intended invariant, original positive controls retained')
    # Public playable bytes remain guarded; these checks do not promote3172.
    for relative in (state['currentCMD'],
                     'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
                     'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata',
                     state['currentPlaytestZIP']):
        path=(ROOT/relative).resolve();key=str(path)
        need(key in state['inputHashes'],'Existing public playable evidence pin')
        pin(path,state['inputHashes'][key])
    pin(PREVIOUS);pin(__file__)
    with ThreadPoolExecutor(max_workers=4)as pool:
        for (file,digest),actual in zip(fresh.items(),pool.map(current.current.assembly.sha,fresh)):
            need(actual==digest,'Fresh actual source/input/capture/public bytes unchanged')
    state['inputHashes'].update(fresh)
    state.update(previousCheckpoint=str(PREVIOUS),
                 previousGoalTurnClassification='progress: existing native Bicycle release independently replayed30own/55victim horizontalfields,190cacheparts,16actualcorruptions+12branchboundaryvectors; no game/build/capture/audio changes.',
                 thisGoalTurnClassification='progress: two new bounded compressed current3172real-two-humanCSS fixtures, Sonya in both slots versus native Kano standingblock. Whole independently assembled guest/correctedpayload/compiledsnapshotinputs;720nativefields/24source-boundstate stores plus2100ordinaryinputfields. Actualcollisioncarry/B2blockedbranch/3chip/no214-215catch;originalstartup/seek/16-bitfraction-preservingfloorclamp/-6halfgravityrebound/6-fieldlanding/cleanready1630 and walk-jump-punch.46qualifiedactualcorruptions with same-path positives. No EXE/ROM/rawaudio copies, gameplay edits or public promotion; all five original groups remain.',
                 currentNativeBicycleBothHumanSlotsBlockedStateAccepted=True,
                 currentNativeBicycleBothHumanSlotsBlockedVerticalReboundAccepted=True,
                 currentNativeBicycleBlockedPhysicalCases=[c['case']for c in tested['cases']],
                 currentNativeBicycleBlockedStateReport=str(current.OUT/'report.json'),
                 currentNativeBicycleBlockedCounterexampleReport=str(ROOT/'audit_v3353_current_bicycle_block_counterexamples/report.json'),
                 currentNativeBicycleBlockedActualChipDamage=3,
                 currentNativeBicycleBlockedNativeFields=720,
                 currentNativeBicycleBlockedSourceBoundStateStores=24,
                 currentNativeBicycleBlockedOrdinaryInputFields=2100,
                 currentNativeBicycleBlockedQualifiedCorruptions=46,
                 currentNativeBicycleBlockedFullDefenderHorizontalRasterShadowAudioAccepted=False,
                 candidateUnderTestNativeBicycleHitOrBlockedAccepted=False,
                 candidateUnderTestBroadCPUOrKOOrMorphCoverageAccepted=False,
                 currentNativeBicycleBlockedAllArenasAudioKOOverlapAccepted=False,
                 currentNativeBicycleBlockedRecoveryScreensVisuallyInspected=True,
                 manualRecoveryScreenInspectionIsNotFullMoveRasterAcceptance=True,
                 gameSourceAndPlayableBytesChangedThisTurn=False,nativeGuestProgramChangedThisTurn=False,
                 newExecutableROMOrRawAudioCopiesThisTurn=0,
                 publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
                 inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),
                 goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
                 nextAction='Continue3172Bicycleblockeddefenderhorizontalpush/fullphaseart/shadow/erase/audio and ordinaryCPU/KO/overlap/morphcontexts. Both-slot standingblock contact/startup/vertical/ready/normalfollowup is now bounded evidence, not all-move/allCPU acceptance. All five original groups remain: full native arenas/effects/victims/audio, move phases/CPU/adversity, finishers/morphs/secrets/cinematics, natural Kintaro/Shao clears/own endings/attract, final combined UI/ladder/names/audio/cleanup/refreshedrelease. Reuse builds and bounded compressed captures; never recreate retired recordings/archive.')
    need(state['remaining']==remaining and len(remaining)==5 and not state['actualEndingsAccepted'] and
         state['currentRealShaoKahnMatchClears']==0,'Original full objective remains intact')
    OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(state,indent=2)+'\n')
    digest=current.current.assembly.sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and current.current.assembly.sha(path)==digest,'Lossless full checkpoint compression verified')
    print(json.dumps(dict(saved=str(path),goalStatus='active',originalRemainingGroups=5,blockedPhysicalSlots=2,
                         actualChipDamage=3,nativeFields=720,sourceBoundStateStores=24,qualifiedCorruptions=46,
                         freshPinsRehashed=len(fresh),fullBlockedRasterOrAudioAccepted=False,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
