"""Keep full natural-port scope with earned physical301escape evidence, not a release claim."""
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_current_shao_crouch_exit_boss_ledger_v2466 as ledger
ROOT=ledger.ROOT;launch=ledger.launch
PREVIOUS=ROOT/'audit_v2460_current_native_crouch_jump_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2474_current_shao_crouch_exit_checkpoint'
def need(ok,message):
 if not ok:raise ValueError(message)
def save():
 prior=json.loads(PREVIOUS.read_text());need(prior['goalStatus']=='active'and not prior['fullPortAcceptance'],'Original full port goal active')
 pins=dict(prior['inputHashes']);pins[str(PREVIOUS)]=launch.sha(PREVIOUS)
 def accept(path):
  report=json.loads(path.read_text());need(report['passed']and not report['fullPortAcceptance'],'Accepted independent bounded report '+str(path))
  for file,digest in report['inputHashes'].items():
   need(file not in pins or pins[file]==digest,'Consistent previous/new dependency');pins[file]=digest
  pins[str(path)]=launch.sha(path);return report
 progress_path=ROOT/'audit_v2472_current_shao_crouch_exit_progress/report.json';progress=accept(progress_path)
 boundary_path=ROOT/'audit_v2481_current_sonya_crouch_exit_extended_boundary/report.json';boundary=accept(boundary_path)
 cleanup_path=ROOT/'audit_v2490_next_old_build_solid_recovery_checked/report.json';cleanup=accept(cleanup_path)
 exposure_path=ROOT/'audit_v2493_current_shao_crouch_exit_exposure/report.json';exposure=accept(exposure_path)
 need(cleanup['oldZIPDeleted']and cleanup['verifiedFiles']==61 and cleanup['verifiedDirectories']==37 and
  cleanup['netOriginalBuildAllocationSavings']==170898990 and cleanup['allCurrentPlayableAndSettingsUnchanged']and
  not cleanup['allOldBuildFoldersRemoved'],'Ten original build folders fully recoverable, exact redundant ZIP retired, actual disk savings; not all cleanup complete')
 need(not exposure['gameOrCaptureModified'],'Read-only ordered exposure diagnosis')
 for name in('tools/verify_solid_old_build_recovery_v2488.py','audit_v2488_next_old_build_solid_recovery_syntax_failure/failure.json',
  'mk2ks_natural_campaign_boss_shao_duck_wait_v2494.lua','tools/run_current_boss_shao_duck_wait_v2495.ps1',
  'tools/verify_current_boss_shao_duck_wait_v2496.py','tools/verify_current_shao_duck_wait_boss_ledger_v2499.py',
  'tools/test_current_shao_duck_wait_inputs_v2500.py'):
  path=ROOT/name;pins[str(path)]=launch.sha(path)
 import verify_current_boss_shao_duck_wait_v2496 as pending
 pending.restore_shao_crouch_exit_policy((ROOT/'mk2ks_natural_campaign_boss_shao_duck_wait_v2494.lua').read_text())
 need(boundary['originalFailedCaptureNeverWaived']and boundary['originalFullCaptureRemainsRejected']and boundary['newSeconds']==3300,'Actual longer identical control completes original unfinished selection; original failure retained')
 need(not progress['gameOrCaptureModified']and not progress['fullEndingArtAudioAcceptance'],'Actual input-only evidence, not full ending-art/audio certification')
 new={}
 for case,(fighter,side,capture,positive)in ledger.CASES.items():
  proof_path=ROOT/positive/'report.json';proof=accept(proof_path)
  book_path=ROOT/f'audit_v2467_current_{case}_boss_ledger_checked/report.json';book=accept(book_path)
  negative_path=ROOT/f'audit_v2469_current_{case}_input_counterexamples/report.json';negative=accept(negative_path)
  row=progress['cases'][case]
  need(proof['bounded_campaign_evidence_proven']and book['finalUnmodifiedControlPassed'],'Whole actual campaign and ordered native ledger accepted')
  need(negative['rejectedSpecificCounterexamples']==34 and negative['finalUnmodifiedFullCampaignControlPassed'],'All prior controls plus non-vacuous native301/native-entry negatives')
  need(book['rejectedSpecificCounterexamples']==8,'Original independent action/health ledger negatives')
  need(row['actualShao301EscapePlans']>0 and row['actualOriginal301Assignments']>0 and row['actualOriginalHorizontalJumpEntries']>0,'Actual changed controller branch and original native entries exercised')
  need(book['originalHuman107Assignments']==proof['actualNativeUppercutAssignments'],'Actual human107 counts reconcile')
  need(book['ownBossUppercutDamage']==proof['actualBossUppercutDamage'],'Own native uppercut damage reconciles')
  need(len(row['actualKintaroMatchClear']['actualOwnedWinFrames'])==2,'Naturally earned Kintaro match, no accumulated failed rounds')
  new[case]=dict(campaignReport=str(proof_path),ledgerReport=str(book_path),inputCounterexampleReport=str(negative_path),
   capture=str(ROOT/capture),stagesReached=proof['stages_reached'],actualNativeHuman107Assignments=book['originalHuman107Assignments'],
   ownBossUppercutDamage=book['ownBossUppercutDamage'],ownBossRoundWins=book['ownBossRoundWins'],
   actualKintaroRoundWins=row['actualKintaroRoundWins'],actualKintaroMatchClear=row['actualKintaroMatchClear'],
   actualShaoRoundWins=row['actualShaoRoundWins'],actualShaoMatchClear=row['actualShaoMatchClear'],
   actualShao301EscapePlans=row['actualShao301EscapePlans'],actualShao301EscapePlansWithNativeJump=row['actualShao301EscapePlansWithNativeJump'],
   actualOriginal301Assignments=row['actualOriginal301Assignments'],actualOriginalHorizontalJumpEntries=row['actualOriginalHorizontalJumpEntries'],
   actualShaoOwnedDamage=row['actualShaoOwnedDamage'],actualShaoIncomingDamage=row['actualShaoIncomingDamage'],
   actualShaoOwnedDamageByActualAction=row['actualShaoOwnedDamageByActualAction'],actualShaoIncomingDamageByActualAction=row['actualShaoIncomingDamageByActualAction'],
   exactPreShaoNativeRecords=row['exactPreShaoNativeRecords'],onlyExplicitPolicyLabelsNormalized=True,
   stage15IsExactReplayOfAcceptedLateApexControl=True,rejectedSpecificLedgerCounterexamples=8,rejectedSpecificInputCounterexamples=34,
   rejectedSpecificPrefixCounterexamples=3,fullCampaignClear=proof['unassisted_clear_proven'],endingAccepted=False,
   actualEndingStarts=row['actualEndingStarts'],actualEndingCompletions=row['actualEndingCompletions'],fullEndingArtAudioAcceptance=False)
 source=(ROOT/'tools/run_current_boss_shao_crouch_exit_v2462.ps1').read_text().rstrip()+'\n'
 original=(ROOT/'tools/run_current_boss_shao_opening_escape_v2420.ps1').read_text().rstrip()+'\n'
 need(launch.sha(ROOT/'tools/run_current_boss_shao_opening_escape_v2420.ps1')=='29EB739A7227D3C039963BB8A2E9A45B01FDD62B1E0C12CE9FF9759D523DA759','Original executed launcher pinned')
 need(source.replace('shao_crouch_exit_escape','shao_walk_escape').replace('mk2ks_natural_campaign_boss_shao_crouch_exit_v2461','mk2ks_natural_campaign_boss_shao_opening_escape_v2419')==original,'Only declared physical driver and policy names differ in complete real launcher')
 pins[str(Path(__file__).resolve())]=launch.sha(__file__);pins[str(ROOT/'tools/run_current_boss_shao_opening_escape_v2420.ps1')]=launch.sha(ROOT/'tools/run_current_boss_shao_opening_escape_v2420.ps1')
 print('Revalidating full carried and new actual graph:',len(pins),'dependencies',flush=True)
 with ThreadPoolExecutor(max_workers=4)as pool:
  for index,((file,wanted),actual)in enumerate(zip(pins.items(),pool.map(launch.sha,pins)),1):
   need(actual==wanted,'Changed actual dependency '+file)
   if index%5000==0:print('Verified',index,'actual dependencies',flush=True)
 campaigns=dict(prior['currentSourceBoundBossCampaigns']);need(len(campaigns)==56 and not set(campaigns)&set(new),'Two new physical contexts, not duplicate accepted contexts');campaigns.update(new)
 prior.update(previousCheckpoint=str(PREVIOUS),
  previousGoalTurnClassification='no progress: status-only response; latest terminal authoritative reports re-read',
  thisGoalTurnClassification='progress: physical301escape cold Kano3000second and Sonya3300second campaigns completed and whole guest/source/input/progression/ordered action/health/owned wins checked,68specific input and16ledger invalid controls. Original Sonya3000second cutoff remains rejected; longer identical control completes pending selection with222750native rows exact. Entire pre-Shao trajectory exact. Ordered301damage diagnosis directs a new stage16physical crouch-wait test with exact driver inverse through originalv850; new campaigns not accepted yet. Ten obsolete build folders recoverably removed,61original files/37directories independently recovered; redundant ZIP replaced with21.6MBsolid archive,170898990actual allocated bytes saved. No ROM/source/AI/HP/RNG/stage/balance changes.',
  currentSourceBoundBossCampaigns=campaigns,currentFreshShaoCrouchExitCampaigns=new,currentShaoCrouchExitProgressReport=str(progress_path),
  preservedSonyaIncompleteCrouchExitCaptureBoundary=str(boundary_path),
  currentActualBossHuman107Assignments=sum(c['actualNativeHuman107Assignments']for c in campaigns.values()),
  currentActualBossUppercutDamage=sum(c['ownBossUppercutDamage']for c in campaigns.values()),
  currentRealKintaroRoundWins=prior['currentRealKintaroRoundWins']+sum(c['actualKintaroRoundWins']for c in new.values()),
  currentRealKintaroMatchClears=prior['currentRealKintaroMatchClears']+len(new),
  currentRealShaoKahnMatchClears=prior['currentRealShaoKahnMatchClears']+sum(c['actualShaoMatchClear']is not None for c in new.values()),
  currentFreshActualShaoRoundWins=sum(c['actualShaoRoundWins']for c in new.values()),
  currentBossLedgerCounterexamples=sum(c['rejectedSpecificLedgerCounterexamples']for c in campaigns.values()),
  currentBossPhysicalInputCounterexamples=sum(c.get('rejectedSpecificInputCounterexamples',0)for c in campaigns.values()),
  repeatedKintaroPhaseNotClaimedAsIndependentStrategyCoverage=True,
  gameSourceAndPlayableBytesChangedThisTurn=False,nativeDifficultyHealthAIPositionStageRNGModified=False,
  obsoleteFoldersDeletedThisTurn=True,foldersDeletedThisTurn=cleanup['removedDirectories'],
  currentAdditionalOldBuildCleanupReport=str(cleanup_path),currentAdditionalOldBuildRecoveryArchive=cleanup['recoveryArchive'],
  currentAdditionalOldBuildRecoveryNetAllocatedSavings=cleanup['netOriginalBuildAllocationSavings'],allOldBuildFoldersRemoved=False,
  currentShaoCrouchExitExposureReport=str(exposure_path),
  pendingPhysicalOnlyCrouchWaitCampaigns=['audit_v2497_current_kano_p1_shao_duck_wait_campaign','audit_v2497_current_sonya_p1_shao_duck_wait_campaign'],
  pendingCrouchWaitWholeSourceInversePassed=True,pendingCrouchWaitCampaignsAccepted=False,
  goalStatus='active',finishedRelease=False,fullPortAcceptance=False,
  actualFullLadderClearAccepted=False,actualEndingsAccepted=False,
  nextAction='Use actual original301escape/jump entries and ordered owned/incoming attack episodes to evaluate controller failures, never interpret attempted Up as activation or modify original game balance to make tests win. Earn full Kintaro/Shao campaigns and own endings/attract bothcharacters/bothslots; current controller contexts alone do not prove all-slot campaign or ending-art/audio acceptance. Continue broader all-arena/move phase art/grounding/floor shadows/cleanup/audio, CPU/repeat/KO/overlap cases, all finishers/victims/morphs/secrets/cinematics, integrated UI regression, dependency-aware remaining old-build cleanup and refreshed finishedreleaseZIP. Full original natural-in-all-aspects scope retained.',
  inputHashes=pins)
 need(len(prior['remaining'])>=5 and len(campaigns)==58,'All original unfinished gates preserved')
 return prior
if __name__=='__main__':
 need(not OUT.exists(),'Immutable full-scope physical301escape checkpoint')
 report=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(goalStatus='active',acceptedStrategyContexts=58,
  actualShaoRoundWins=report['currentFreshActualShaoRoundWins'],actualShaoMatchClears=report['currentRealShaoKahnMatchClears'],
  gameChanged=False,fullPortAcceptance=False,finishedRelease=False),indent=2),flush=True)
