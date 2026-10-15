"""Full goal retained; finite guard coverage and actual failed trials separated."""
import datetime,json
from pathlib import Path
import native_ai_response_context as current
import native_process_census_v6647 as census
ROOT,need,sha=current.ROOT,current.need,current.sha

if __name__=='__main__':
    out=ROOT/'audit_native_guard_campaign_progress'
    need(not out.exists() and not census.census(),'Fresh journal after all actual games terminal')
    paths=[ROOT/'audit_native_block_freeze_both_slots_progress/report.json',
           ROOT/'audit_native_postending_kano_p2_sonya_cpu_ice/bounded_controller_result.json',
           ROOT/'audit_native_postending_kano_p2_sonya_cpu_ice_phase900/bounded_controller_result.json']
    guard,first,phase=[json.loads(p.read_text()) for p in paths]
    need(guard['passed'] and guard['finiteHumanFreezeBlockRecoveryBothSlotsAccepted'] and
         guard['combinedNativeGames']==13 and guard['combinedNativeFields']==9113 and
         guard['combinedReviewedNativeScreens']==52 and guard['combinedEffectiveFaults']==248,
         'Actual saved two-slot native guard/recovery comparison')
    need(all(sha(p)==h for p,h in guard['inputHashes'].items()),'Completed original guard/source receipts still frozen')
    for trial in (first,phase):
        need(not trial['passed'] and trial['transportPassed'] and trial['nativeExit']==0 and
             trial['failedCampaignPreserved'] and trial['actualPaidContinueLosses']==8 and
             not trial['endingAccepted'] and not trial['postEndingJoinAccepted'],
             'Both actual bounded campaigns remain unsuccessful, never relabeled green')
        need(all(sha(p)==h for p,h in trial['inputHashes'].items()),'Every originally executed trial input still intact')
    need(phase['actualStages']==list(range(6)) and phase['actualOpponentIDsByStage']['2']==['17:17'] and
         phase['actualObservedTrueKanoFields']==1035,'Real extended ordinary-input route and true CPU Kano mirror, not an anticipated route')
    need(first['realCPUFreezeLaunchesObserved']==6 and first['ordinaryNextFieldReactiveGuardObserved'] and
         phase['realCPUFreezeLaunchesObserved']==0,'Finite actual CPU events not transferred into another run')
    launcher=ROOT/'PLAY_MK2_KANO_SONYA.cmd'
    need(sha(launcher)=='90BD99EC729C956A1414D9A544DBA537597A828AE382D323579DF266FB053ACE','Public executable routing unchanged')
    report=dict(passed=True,goalStatus='active',fullGoalComplete=False,fullPortAcceptance=False,
                observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                previousGoalTurnClassification='progress: six-case P2 guard proof and 24 original native screens sealed before interruption',
                thisGoalTurnClassification='progress: opposite-slot guard proof completes 13 native cases, 9113 fields, 248 effective faults and 52 reviewed screens; two bounded current earned-campaign attempts preserved, with actual CPU ice events and six-stage true-Kano/CPU-Kano mirror route',
                originalNaturalIntegrationRequirements=guard['originalNaturalIntegrationRequirements'],
                originalRemainingWorkGroups=guard['originalRemainingWorkGroups'],acceptedPriorWorkNotReset=guard['acceptedPriorWorkNotReset'],
                finiteHumanFreezeBlockRecoveryBothSlotsAccepted=True,actualGuardGames=13,actualGuardFields=9113,
                actualGuardFaults=248,actualGuardScreensReviewed=52,
                realCPUFreezeLaunchesObserved=6,extendedTrueKanoRouteStages=list(range(6)),trueCPUKanoMirrorObserved=True,
                fullCurrentCampaignAccepted=False,postEndingFreshJoinAccepted=False,audibleNativeKanoAttractAccepted=False,
                unsuccessfulTestPlayerTrials=[dict(path=str(paths[i+1]),nativeExit=0,paidLosses=8,
                   stages=trial['actualStages'],softlockClaim=False,gameBugClaim=False) for i,trial in enumerate((first,phase))],
                nextAction='Inspect and reuse the already-qualified character-specific campaign input tactics, including the complete Sonya P1 tested-prime/Kitana/Jax/Subzero policy, to reach a genuine current ending and ordinary fresh join. Do not equate weak test-player performance with a game defect, and do not reset accepted four historical campaigns/endings to untouched work.',
                noNativeGamesStillRunning=True,publicBuildPromoted=False,newBuilds=0,newROMCopies=0,newZIPs=0,
                newEvidenceAllocatedBytes=guard['allocatedEvidenceBytes']+first['allocatedEvidenceBytes']+phase['allocatedEvidenceBytes'],
                inputHashes={str(p):sha(p) for p in (*paths,Path(__file__).resolve(),launcher)})
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,guardBothSlotsAccepted=True,currentEndingJoinAccepted=False,
                         nativeGamesStillRunning=0,newEvidenceAllocatedBytes=report['newEvidenceAllocatedBytes'])),flush=True)
