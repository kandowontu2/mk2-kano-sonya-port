"""Native Mileena round clear and stage12 progress; full original goal remains."""
import json,subprocess
from pathlib import Path
import verify_mileena_jump_retry_movement_v4292 as movement
ROOT,need,sha=movement.ROOT,movement.need,movement.sha
PARENT=ROOT/'audit_v4279_ring_spacing_observer_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4295_mileena_clear_jump_retry_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable complete-scope checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins=dict(state['inputHashes'])
    for p,h in pins.items():need(sha(p)==h,'All inherited logical source/native/public bytes unchanged')
    def pin(p,wanted=None):
        p=Path(p).resolve();key=str(p);h=sha(p)
        need(key not in pins or pins[key]==h,'Inherited/shared proof unchanged')
        need(wanted is None or wanted==h,'Exact executed/proof pin');pins[key]=h
    pin(PARENT);pin(__file__)
    names=('audit_v4282_mileena_jump_retry_source_preflight','audit_v4287_mileena_jump_retry_actual_prefix_checked',
           'audit_v4289_mileena_jump_retry_whole_campaign_checked','audit_v4293_mileena_jump_retry_movement_checked')
    reports={}
    for name in names:
        p=ROOT/name/'report.json';r=json.loads(p.read_text());need(r['passed'] and not r.get('fullPortAcceptance',False),'Actual completed bounded proof');pin(p);reports[name]=r
        for p,h in r.get('inputHashes',r.get('case',{}).get('inputHashes',{})).items():pin(p,h)
    campaign=reports[names[2]];c=campaign['case'];m=reports[names[3]]['actualMovementAndMileenaProgress']
    need(c['passed'] and c['actualWholeCampaignGrammarRetained'] and c['actual3836P2WholeCampaignAlgorithmRetained'] and
         not c['unassisted_clear_proven'] and not campaign['actualNaturalSonyaP2TowerClearAccepted'],
         'Full original campaign algorithm retained; not a tower clear')
    need(c['stages_reached']==list(range(13)) and c['native_own_round_wins']==30 and c['paid_continue_losses']==12 and
         c['ending_starts']==c['ending_completions']==0,'Actual stage12 terminal progress with no ending')
    r=c['actualWholeRingSpacingInputReplay']
    need(r['actualCompleteRangeFields']==1887 and r['actualNativeOwnRingTasks']==27 and
         r['actualNativeHuman308JumpStores']==r['actualNativeHuman200AirKickStores']==3 and
         r['actualNativeCpuGroundThrowStores']==r['actualOriginalHumanVictimCaptures']==0,
         'Actual own Ring/jump/air-kick actions, no logged native CPU throw in actual winning Mileena branch')
    need(len(m['actualOwnedMileenaRoundWins'])==2 and len(m['actualNativeMovementWindows'])==3 and
         [w['health'] for w in m['actualOwnedMileenaRoundWins']]==['0,21','0,3'] and
         not m['observerRepairSlotReuseRuntimeProven'],'Actual two earned native rounds; no unexercised observer reuse claim')
    failed_path=ROOT/'audit_v4291_mileena_jump_retry_observer_runtime_checked/report.json'
    f=json.loads(failed_path.read_text())
    need(not f['passed'] and 'both roles after Main address opposite-side reuse' in f['error'],
         'Strict reuse proof correctly remains failed/unexercised, not weakened to passing')
    pin(failed_path)
    for name in ('mk2ks_mileena_jump_retry_campaign_ram_v4280.lua','tools/qualify_mileena_jump_retry_source_v4281.py',
                 'tools/run_mileena_jump_retry_campaign_v4283.py','tools/verify_mileena_jump_retry_prefix_v4286.py',
                 'tools/verify_mileena_jump_retry_whole_campaign_v4288.py','tools/verify_mileena_jump_retry_observer_runtime_v4290.py',
                 'tools/verify_mileena_jump_retry_movement_v4292.py'):pin(ROOT/name)
    q=subprocess.run(['powershell.exe','-NoProfile','-Command',
      'Get-CimInstance Win32_Process -Filter "ProcessId=101448 OR ProcessId=37824 OR ProcessId=134612 OR ProcessId=70204" | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress'],capture_output=True,text=True)
    need(q.returncode==0 and not q.stdout.strip(),'Actual collector/native/prefix/whole jobs terminal, consumed same tool handles')
    state.update(previousCheckpoint=str(PARENT),inputHashes=pins,
      inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),mergeRule='All original full-goal requirements/exclusions and every inherited logical byte retained.'),
      previousGoalTurnClassification=state['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: physical Mileena-only complete Ring commands then earlierretreat plus groundedUp3on1offretry, no40fieldassumedjumpcooldown; originalselection/mirror/otheropponents/boss/ownending/attractcode unchanged, nativeAI/difficulty/RNG/health/identity/positions untouched. NewcoldSonyaP2 actual3836 run52530 collector101448/emulator37824 terminal0 consumed. Passed whole original native campaign/guest/selection/roster/schedule/morph/health/KO/paidcontinue/boss/ending grammar:30ownroundwins12paidlosses stages0..12, noending. Actual Mileena9 cleared with2nativeownwins, genuineHP0,21and0,3, noMileena paidloss; progressed10/11 and stalledrealShang10 at12. Actual1887Mileena fields27nativeRing3original HUMAN308jumps3HUMAN200airkicks, all3jumpstores followedownedairmotionandtheir actualnativekickdispatch.0loggedCPUthrow/capture inthiswinningbranch.64730prefix/90407whole/70259movementproof terminal0consumed;23actualprefix+9campaign+8guest+10mirror+8movementcounterexample executions reject, positives restored. Strict4290/4291observer opposite-role Mainreuse gate correctly failed because winningMileena pair never exercised bothrole reuse; source4275/4280keyfix remains source/model qualified, not native reuse complete. Preserve failedreport, do not shrinkthegate or rerunvalidcaptureforcheckerrepair. No game/playable/public/ZIP edits, new EXE/ROM/rawnative media. All5originalgroupsremain.',
      currentDevelopmentCampaignObservation=str(ROOT/'audit_v4285_mileena_jump_retry_campaign_observed/report.json'),
      currentDevelopmentCampaignReport=str(ROOT/'audit_v4289_mileena_jump_retry_whole_campaign_checked/report.json'),
      currentNativeMileenaMovementReport=str(ROOT/'audit_v4293_mileena_jump_retry_movement_checked/report.json'),
      currentTerminalMileenaJumpRetry=dict(capture=str(movement.FOLDER),execHandle=52530,terminalExitCode=0,
        collectorPID=101448,nativePID=37824,trueHumanID=18,trueMileenaID=5,actualCompleteMileenaFields=1887,
        actualOwnRingTasks=27,actualOriginalHuman308JumpStores=3,actualOriginalHuman200AirKickStores=3,
        actualOwnedMileenaRoundWins=2,actualMileenaWinningHealth=['0,21','0,3'],actualMileenaPaidLosses=0,
        actualLoggedCpuThrowStores=0,actualLoggedVictimCaptureStores=0,originalWholeCampaignGrammarRetained=True,
        actualOwnRoundWins=30,actualPaidLosses=12,stagesReached=list(range(13)),
        nextNativeOpponentRoster=10,nextNativeOpponentStage=12,naturalTowerClearAccepted=False,
        endingAccepted=False,completeCampaignAudioAccepted=False,fullPortAcceptance=False),
      currentNativeObserverSlotReuseRuntimeGate=dict(report=str(failed_path),passed=False,
        reason='Winning native Mileena pair did not exercise opposite-side Main reuse; no throw/capture pair occurred. Native reuse scope remains unverified.',
        correctedLuaSlotMainKeyRetained=True,sourceAndPredicateModelQualified=True,nativeBothRoleReuseProven=False,
        strictGateNotWeakened=True,oldMissingEventsNotRecreated=True),
      nextImplementationAction='Mileena9 now naturally cleared in2trueSonyaP2rounds withnative27Ring/3jump/3airkick events. Do notrepeat that solvedbranch. FullSonyaP2tower remainsopen atrealShangTsung roster10 stage12: next physicalcontroller can extend actualgrounded3on1offjump retry/completeRingearlierretreat toactualnativeShang roster10, correctly observing original legitimate morph IDs/Mainownership rather than requiringCPU currentID==roster or forcingCPU/roster/AI/health/difficulty/RNG/position. Preserve all current full campaign/native morph/boss/ownending/attract grammar. Retain repaired slot/Main observers; exercise actual native Main role reuse whereitoccurs, do notmark4291failedreusegatecompletefromnarrowwinningpair. Continueall5originalgroups: broaderPit/Tombvictim/mirror/branch/stageaudio, allmovephaseart/ground/floorshadows/cleanup/allarenas/CPU/repeat/KO/overlap, otherfinishers/victims/morphs/secrets/cinematics, naturalfulltowers/ownendings/attract, finalcombinedselection/ladder/names/audio/dependencycleanup/refreshedZIP. Public1836remainsunchangedplaytestnotfinal.',
      currentTurnReclaimedAllocatedBytes=0,currentTurnDeletedFiles=0,currentTurnNewBuilds=0,currentTurnNewNativeAudioRasterROMCopies=0,
      cleanupAccounting='No new deletion or reclaimed bytes; native diagnostics/text reports written into already compressed leaves, no raster/audio/guest/EXE/ROM copies. Historical4207savings3392749568B not counted again.',
      gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
      goalStatus='active',fullPortAcceptance=False,finishedRelease=False)
    need(state['remaining']==remaining and len(remaining)==5,'Every original goal group retained exactly')
    for p,h in pins.items():need(sha(p)==h,'All actual new/inherited logical bytes unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress checkpoint before writes')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),pins=len(pins),actualNativeMileenaRoundWins=2,
      actualHuman308Jumps=3,actualHuman200AirKicks=3,stagesReached=list(range(13)),wholeCampaignGrammarPassed=True,
      observerNativeReuseProven=False,naturalTowerClearAccepted=False,allOriginalRemainingGroups=len(remaining),fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
