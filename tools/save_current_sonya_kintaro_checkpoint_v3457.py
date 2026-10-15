"""Current Sonya native Kintaro clear, failed Shao controller and measured exposure."""
import json,subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_current_campaign_shao_highkick_v3440 as native
ROOT=native.ROOT;need=native.need;sha=native.sha
PREVIOUS=ROOT/'audit_v3450_current_sonya_verification_pending_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3458_current_sonya_kintaro_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Immutable full objective checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=state['remaining'];fresh={}
    need(state['goalStatus']=='active' and len(remaining)==5 and not state['fullPortAcceptance']
         and not state['finishedRelease'] and not state['actualEndingsAccepted'],'Original full objective remains unachieved')
    def pin(path,digest=None):
        key=str(Path(path).resolve());digest=digest or sha(key)
        need(key not in fresh or fresh[key]==digest,'Consistent fresh proof pins')
        need(key not in state['inputHashes'] or state['inputHashes'][key]==digest,'Never relabel parent evidence')
        fresh[key]=digest
    def checked(relative):
        path=ROOT/relative;value=json.loads(path.read_text())
        need(value['passed'] and not value['fullPortAcceptance'],'Actual bounded proof, not full-port acceptance')
        pin(path)
        for file,digest in value['inputHashes'].items():pin(file,digest)
        return value
    campaign=checked('audit_v3446_current_sonya_defensive_leg_campaign_checked/report.json')
    outcome=checked('audit_v3448_current_sonya_highkick_campaign_outcomes/report.json')
    damage=checked('audit_v3452_current_highkick_damage_model_checked/report.json')
    exposure=checked('audit_v3456_current_highkick_incoming_exposure/report.json')
    need(campaign['current3172WholeGuestAndCampaignAccepted'] and campaign['bounded_campaign_evidence_proven']
         and not campaign['unassisted_clear_proven'] and campaign['native_own_round_wins']==36
         and campaign['paid_continue_losses']==59 and len(campaign['specificActualInputCounterexamples'])==2
         and campaign['ending_starts']==campaign['ending_completions']==0,'Full current source/native/input campaign and qualified physical faults')
    need(outcome['actualCurrentKintaroMatchClear']==dict(ownWinFrames=[98392,100403],nativeStage16Frame=100927)
         and outcome['actualShaoFields']==50390 and outcome['actualNative0113Assignments']==502
         and outcome['actualShao0113Damage']==830 and outcome['actualShaoRoundWins']==outcome['actualEndingEvents']==0,
         'Current true Sonya Kintaro match, actual activations/damage, no Shao clear or ending')
    model=damage['actualCurrentDamageModel']
    need(model['rawNormalDamage']==12 and model['rawBlockDamage']==3 and model['actualDamageHistogram']=={'9':92,'1':2}
         and model['totalDamage']==830 and model['branchClassificationIsSourceDerivedInferenceNotDirectBranchTrace']
         and len(damage['specificActualCounterexamples'])==4 and damage['samePathPositiveControlAccepted'],
         'Entire native dedicated highkick/scaler ABI and94actual stores, with qualified controls')
    need(exposure['actualIncomingStores']==366 and exposure['actualIncomingDamage']==14802
         and exposure['ownActualActionAtIncomingCollision']['0302']==dict(stores=330,damage=14387,guardIntentStores=0,guardIntentDamage=0)
         and exposure['incomingGuardIntentNotAssumedNativeBlock'] and exposure['cpuActionOnlyPreInputNotActualDamageWriterTrace'],
         'Original ordered incoming collision stores, raw own action and physical guard exposure only')
    for relative in (state['currentCMD'],state['currentPlaytestZIP'],
        'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
        'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata'):
        key=str((ROOT/relative).resolve());pin(key,state['inputHashes'][key])
    pin(PREVIOUS);pin(__file__)
    with ThreadPoolExecutor(max_workers=4)as pool:
        for (file,digest),actual in zip(fresh.items(),pool.map(sha,fresh)):
            need(actual==digest,'Every relevant current source/capture/public byte unchanged')
    state['inputHashes']=fresh
    state.update(inputHashInheritance=dict(schema=1,parentCheckpoint=str(PREVIOUS),
        parentCheckpointSHA256=fresh[str(PREVIOUS)],mergeRule='Resolve parent recursively, preserving retired/deleted exclusions. Fresh pins agree with inherited keys; never flatten/copy historical map.'),
        previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification=state['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: whole native current Sonya defensive_leg3426 campaign3446 terminal verifier73027 passes,2qualified actual highkick input faults. Ordered3448 proves genuine current Sonya Kintaro wins98392/100403 advance100927. Shao50390fields2471plans502native0113assignments94stores830damage0wins0endings; no controller improvement/character defect.3452 independently checks whole original highkick selector/strike/scaler/health path and dedicated17/18descriptors;92x9+2x1=830, inference not captured branch;4qualified faults/same-path positive.3456 incoming original collision stores366total14802damage;330atownactual0302crouch transition14387damagewithBlocknotpressed. Original source/build/public unchanged. All five groups remain.',
        pendingCurrentNaturalDefensiveLegHighkickCampaign={},currentSonyaDefensiveLegCampaignTerminal=True,
        currentSonyaDefensiveLegCampaignReport=str(ROOT/'audit_v3446_current_sonya_defensive_leg_campaign_checked/report.json'),
        currentSonyaHighkickOutcomeReport=str(ROOT/'audit_v3448_current_sonya_highkick_campaign_outcomes/report.json'),
        currentSonyaHighkickDamageModelReport=str(ROOT/'audit_v3452_current_highkick_damage_model_checked/report.json'),
        currentSonyaHighkickIncomingExposureReport=str(ROOT/'audit_v3456_current_highkick_incoming_exposure/report.json'),
        current3172SonyaNaturalKintaroMatchClearAccepted=True,current3172SonyaNaturalKintaroWinFrames=[98392,100403],
        current3172SonyaNaturalStage16TransitionFrame=100927,
        current3172NaturalShaoClearAccepted=False,currentRealShaoKahnMatchClears=0,actualEndingsAccepted=False,
        currentSonyaHighkickControllerImprovementAccepted=False,currentSonyaControllerFailureNotCharacterDefect=True,
        gameSourceAndPlayableBytesChangedThisTurn=False,nativeGuestProgramChangedThisTurn=False,
        publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,newExecutableROMOrRawAudioCopiesThisTurn=0,
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),historicalPinMapCopiedAgain=False,
        nextAction='No live capture/verification handles remain:73027/22019/82710/29323 terminal0. Do not restart completed3426 or rerun3446/3448/3452/3456 merely for continuity. Current both real Kano and Sonya Kintaro match clears now proven; Shao/own endings/return still unproven. A successor physical controller must address measured guard release atgap125 versus actual successful contacts76..108 (bulk98..104) and330incoming actual0302transition stores. Do not alter native power/difficulty/AI or infer exact CPU branch from pre-input action. Keep original whole arenas/victims/effects/audio, full move phase/ground/shadow/cleanup CPU/repeat/KO/overlap, finishers/morphs/secrets/cinematics, natural bosses/own-endings/attract, final integrated UI/audio/dependency-cleanup/refreshed-release groups. Use current builds and compressed bounded evidence; no raw audio/build copies, retired recovery or flattened historical pin maps.')
    need(state['remaining']==remaining,'Original full requirement groups intact')
    OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(state,indent=2)+'\n');digest=sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and sha(path)==digest,'Lossless checkpoint compression')
    print(json.dumps(dict(saved=str(path),goalStatus='active',remainingGroups=5,currentSonyaKintaroMatchClearAccepted=True,
        ShaoClearOrEndingAccepted=False,freshPins=len(fresh),fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
