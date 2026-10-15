"""Current native Kintaro clear and failed Shao strategy; full objective retained."""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_current_campaign_shao_lowkick_v3409 as native

ROOT=native.ROOT;need=native.need;sha=native.sha
PREVIOUS=ROOT/'audit_v3411_current_campaign_pending_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3416_current_kintaro_campaign_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Immutable full-scope checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=state['remaining']
    need(state['goalStatus']=='active'and len(remaining)==5 and not state['fullPortAcceptance']and
         not state['actualEndingsAccepted']and not state['finishedRelease'],'Keep all full-port requirements')
    fresh={}
    def pin(path,digest=None):
        path=Path(path).resolve();key=str(path);digest=digest or sha(path)
        need(key not in fresh or fresh[key]==digest,'Consistent fresh relevant evidence')
        need(key not in state['inputHashes']or state['inputHashes'][key]==digest,'Never relabel parent evidence')
        fresh[key]=digest
    def proof(relative):
        path=ROOT/relative;value=json.loads(path.read_text())
        need(value['passed']and not value['fullPortAcceptance'],'Actual bounded proof only');pin(path)
        for file,digest in value['inputHashes'].items():pin(file,digest)
        return value
    campaign=proof('audit_v3412_current_kano_natural_lowkick_campaign_checked/report.json')
    outcomes=proof('audit_v3414_current_lowkick_campaign_outcomes/report.json')
    need(campaign['current3172WholeGuestAndCampaignAccepted']and campaign['bounded_campaign_evidence_proven']and
         not campaign['unassisted_clear_proven']and campaign['native_own_round_wins']==32 and
         campaign['paid_continue_losses']==64 and campaign['ending_starts']==campaign['ending_completions']==0 and
         len(campaign['specificActualInputCounterexamples'])==2,'Complete genuine terminal campaign and qualified replay faults, not an ending')
    need(outcomes['terminalFrame']==213357 and outcomes['actualCurrentKintaroMatchClear']==
         dict(ownWinFrames=[76520,78384],nativeStage16Frame=79020)and
         outcomes['actualShaoRoundWins']==outcomes['actualEndingEvents']==0 and
         outcomes['actualPhysicalLowKickPlans']==326 and outcomes['actualNative011AAssignments']==30 and
         outcomes['actualShao011ADamage']==108 and not outcomes['controllerImprovementAccepted']and
         not outcomes['characterGameplayDefectInferredFromControllerFailure'],
         'Current earned Kintaro match, actual blocked lowkick damage, failed controller not an invented gameplay bug')
    for relative in (state['currentCMD'],state['currentPlaytestZIP'],
                     'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
                     'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata'):
        key=str((ROOT/relative).resolve());need(key in state['inputHashes'],'Retained public playable guard')
        pin(key,state['inputHashes'][key])
    pin(PREVIOUS);pin(__file__)
    with ThreadPoolExecutor(max_workers=4)as pool:
        for (file,digest),actual in zip(fresh.items(),pool.map(sha,fresh)):
            need(actual==digest,'Every fresh capture/source/public relevant byte unchanged')
    state['inputHashes']=fresh
    state.update(inputHashInheritance=dict(schema=1,parentCheckpoint=str(PREVIOUS),
        parentCheckpointSHA256=fresh[str(PREVIOUS)],mergeRule='Resolve parent recursively, preserving retired/deleted exclusions. Fresh inputHashes must agree with inherited keys; do not flatten/copy the historical map.'),
        historicalPinMapCopiedAgain=False,previousCheckpoint=str(PREVIOUS),
        previousGoalTurnClassification=state['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: existing3172 full cold Kano campaign terminal0 at213357frames,107061livefields,32native round wins,64paid continues. Whole independently assembled guest/compiled inputs/native schedule/IDs/morphs/health/winner/progression plus exact physical boss replay accepted, two qualified actual input faults rejected with same-path positive. Genuine current Kintaro match wins76520/78384 advances79020. Shao crouch-lowkick controller fails:326plans only30native011Aassignments,108damage,0Shao wins,0endings. No gameplay defect inferred or difficulty changed. Source/build/public unchanged, no raw audio/build copies. Full five groups retained.',
        pendingCurrentNaturalLowkickCampaign={},pendingCampaignLogNotPinnedWhileMutable=False,
        currentNaturalLowkickCampaignTerminal=True,currentNaturalLowkickCampaignReport=str(ROOT/'audit_v3412_current_kano_natural_lowkick_campaign_checked/report.json'),
        currentNaturalLowkickCampaignOutcomesReport=str(ROOT/'audit_v3414_current_lowkick_campaign_outcomes/report.json'),
        current3172KanoNaturalKintaroMatchClearAccepted=True,
        current3172KanoNaturalKintaroWinFrames=[76520,78384],
        current3172KanoNaturalStage16TransitionFrame=79020,
        current3172NaturalShaoClearAccepted=False,actualEndingsAccepted=False,
        currentRealShaoKahnMatchClears=0,
        currentNaturalLowkickShaoStrategyImprovementAccepted=False,
        currentNaturalLowkickControllerFailureIsNotCharacterDefect=True,
        candidateUnderTestBroadCPUOrKOOrMorphCoverageAccepted=False,
        gameSourceAndPlayableBytesChangedThisTurn=False,nativeGuestProgramChangedThisTurn=False,
        newExecutableROMOrRawAudioCopiesThisTurn=0,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),
        goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
        nextAction='No live campaign/verification handles remain:41305,85569,29782 terminal0. Do not restart completed3408 or re-run completed3412/3414. Campaign objective remains open: current Kano natural Kintaro match proven, Shao and own endings/return unproven, current Sonya campaign still open. Plan a successor only from measured block/hurt exposure and30actual011Aactivations rather than326intentions; all30Shao hits total108damage, no improvement. Keep original full arenas/victims/effects/audio, move-phase/CPU/arena/repeat/KO/overlap/shadows, finishers/morphs/secrets/cinematics, bosses/own endings/attract, final integrated UI/audio/cleanup/refreshed release. Reuse builds and compressed evidence; no raw audio, broad historical pin-map copies or retired archive recreation.')
    need(state['remaining']==remaining,'Original objective not narrowed')
    OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(state,indent=2)+'\n');digest=sha(path)
    compact=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(compact.returncode==0 and sha(path)==digest,'Lossless checkpoint compression')
    print(json.dumps(dict(saved=str(path),goalStatus='active',originalRemainingGroups=5,
        currentKanoKintaroMatchClearAccepted=True,ShaoClearOrEndingAccepted=False,
        freshPinsRehashed=len(fresh),fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
