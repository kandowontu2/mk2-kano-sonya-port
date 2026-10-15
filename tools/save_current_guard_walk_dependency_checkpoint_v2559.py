"""Carry the complete original port objective; correct cleanup dependency scope."""
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_current_shao_guard_walk_boss_ledger_v2551 as ledger
ROOT=ledger.ROOT;launch=ledger.launch
PREVIOUS=ROOT/'audit_v2535_current_duck_wait_cleanup_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2560_current_guard_walk_dependency_checkpoint'

def need(ok,label):
 if not ok:raise ValueError(label)

def save():
 prior=json.loads(PREVIOUS.read_text());need(prior['goalStatus']=='active'and not prior['fullPortAcceptance']and not prior['finishedRelease'],'Full original objective remains unfinished')
 pins=dict(prior['inputHashes']);pins[str(PREVIOUS)]=launch.sha(PREVIOUS)
 def accept(path):
  r=json.loads(path.read_text());need(r['passed']and not r['fullPortAcceptance'],'Actual accepted bounded evidence '+str(path))
  for file,wanted in r['inputHashes'].items():need(file not in pins or pins[file]==wanted,'Consistent old/new dependency '+file);pins[file]=wanted
  pins[str(path)]=launch.sha(path);return r
 timing_path=ROOT/'audit_v2539_current_uppercut_collision_timing/report.json';timing=accept(timing_path)
 need(sum(r['actual107Assignments']for r in timing['cases'].values())==55 and all(r['actualDamageTimingHistogram']=={'4':r['actual107Assignments']}for r in timing['cases'].values()),'Actual old same-owner attack/collision timing established, not planned activation')
 recovery_path=ROOT/'audit_v2548_dynamic_native_source_dependencies_recovered/report.json';recovery=accept(recovery_path)
 compressed_path=ROOT/'audit_v2554_restored_native_dependencies_compressed/report.json';compressed=accept(compressed_path)
 source_path=ROOT/'audit_v2550_guard_walk_source_boundary_checked/report.json';source=accept(source_path)
 archive_check_path=ROOT/'audit_v2562_restored_native_dependency_archive_checked/report.json';archive_check=accept(archive_check_path)
 need(recovery['restoredFiles']==14 and recovery['wholeCurrentGuestAndPayloadReconstructed']and recovery['currentGameSettingsAndLaunchersUnchanged'],'Only required archived files restored; whole game reconstructed')
 need(compressed['filesCompressed']==14 and compressed['originalCleanupUnreferencedClaimSuperseded'],'Exact lossless dependency compression; old unreferenced assertion corrected')
 need(source['fullSourceInverse']and source['wholeLauncherInverse']and len(source['rejectedSpecificSourceCounterexamples'])==5,'Complete physical-only source and launcher boundary with five negatives')
 need(archive_check['independentlyComparedFiles']==14 and archive_check['requiredPartialHistoricalFolders']==8 and archive_check['onlyRequiredFilesRestored']and len(archive_check['rejectedSpecificProtectionCounterexamples'])==2,'Every restored original byte independently compared to archive; complete required-file protection checked')
 new={}
 for case,(fighter,side,capture,positive)in ledger.CASES.items():
  proof_path=ROOT/positive/'report.json';proof=accept(proof_path)
  book_path=ROOT/f'audit_v2556_current_{fighter}_shao_guard_walk_boss_ledger_checked/report.json';book=accept(book_path)
  negatives_path=ROOT/f'audit_v2557_current_{fighter}_shao_guard_walk_input_counterexamples/report.json';negative=accept(negatives_path)
  progress_path=ROOT/f'audit_v2558_current_{fighter}_shao_guard_walk_progress/report.json';progress=accept(progress_path)
  need(book['rejectedSpecificCounterexamples']==8 and negative['rejectedSpecificCounterexamples']==29 and negative['finalUnmodifiedFullCampaignControlPassed'],'Independent ordered and complete physical-input corruptions passed')
  need(progress['exactPreShaoNativeRecords']==(92646 if fighter=='kano'else 136135)and len(progress['rejectedSpecificPrefixCounterexamples'])==3,'All earlier ordinary/Kintaro chronology exactly replayed')
  need(progress['actualKintaroMatchClear']and len(progress['actualKintaroMatchClear']['actualOwnedWinFrames'])==2,'Actual owned Kintaro clear in one successful attempt')
  new[case]=dict(progress,campaignReport=str(proof_path),ledgerReport=str(book_path),inputCounterexampleReport=str(negatives_path),progressReport=str(progress_path),
   capture=str(ROOT/capture),stagesReached=proof['stages_reached'],actualNativeHuman107Assignments=book['originalHuman107Assignments'],
   ownBossUppercutDamage=book['ownBossUppercutDamage'],ownBossRoundWins=book['ownBossRoundWins'],fullCampaignClear=proof['unassisted_clear_proven'],
   endingAccepted=False,repeatedKintaroControlNotIndependentStrategyCoverage=True)
  new[case].pop('inputHashes');new[case].pop('scope')
 failure_path=ROOT/'audit_v2546_guard_walk_source_boundary_failure/failure.json'
 need(not json.loads(failure_path.read_text())['passed'],'Original failed preflight never waived')
 for path in(failure_path,ROOT/'tools/verify_guard_walk_source_boundary_v2545.py',Path(__file__).resolve()):pins[str(path)]=launch.sha(path)
 launch.module_pins(pins)
 print('Revalidating full carried/current dependency graph:',len(pins),'actual files',flush=True)
 with ThreadPoolExecutor(max_workers=4)as pool:
  for index,((file,wanted),actual)in enumerate(zip(pins.items(),pool.map(launch.sha,pins)),1):
   need(actual==wanted,'Changed authoritative dependency '+file)
   if index%5000==0:print('Verified',index,'actual dependencies',flush=True)
 campaigns=dict(prior['currentSourceBoundBossCampaigns']);need(len(campaigns)==60 and not set(new)&set(campaigns),'Only two new source-bound physical contexts');campaigns.update(new)
 required=sorted({str(Path(r['path']).relative_to(ROOT).parts[0])for r in recovery['restoredRequiredFiles']})
 need(len(required)==8 and all((ROOT/name).is_dir()for name in required),'All eight actually required partial historical dependency folders present')
 prior.update(previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification='no progress: user-requested status only; latest existing checkpoint inspected, no gameplay or evidence changed',
  thisGoalTurnClassification='progress: original uppercut collision diagnosis accepted; cleanup omission found and corrected by restoring only fourteen dynamically required archived files. Whole current guest and payload reconstructed again, exact original source/launcher boundary and five source negatives passed. Both genuine physical guard/walk-counter campaigns completed and accepted with sixteen ordered-ledger, fifty-eight full-input and six exact-prefix negatives. All game bytes, character IDs, difficulty, health, AI, RNG, stage, positions, settings and public launchers unchanged; no Shao/ending acceptance claimed.',
  currentSourceBoundBossCampaigns=campaigns,currentFreshShaoGuardWalkCampaigns=new,currentUppercutCollisionTimingReport=str(timing_path),
  currentDynamicNativeDependencyRecoveryReport=str(recovery_path),currentRestoredNativeDependencyCompressionReport=str(compressed_path),
  currentRestoredNativeDependencyArchiveCheck=str(archive_check_path),
  currentPhysicalGuardWalkSourceBoundaryReport=str(source_path),preservedGuardWalkSourceBoundaryFailure=str(failure_path),
  currentRequiredRestoredNativeDependencyFiles=recovery['restoredRequiredFiles'],currentRequiredRestoredNativeDependencyFolders=required,
  original68BuildUnreferencedClaimSuperseded=True,original68BuildRemovalWasHistoricalNotCurrentAbsenceProof=True,
  all68PreviouslyUnreferencedBuildFoldersRemoved=False,allOldBuildFoldersRemoved=False,currentAndRequiredNativeDependencyBuildsRetained=True,
  currentRemainingOldBuildCleanupNetAllocatedSavings=compressed['remaining68BuildCleanupNetSavingsAfterRequiredRecovery'],
  currentRestoredNativeDependencyAllocatedBytes=compressed['afterAllocatedBytes'],
  currentActualBossHuman107Assignments=sum(c['actualNativeHuman107Assignments']for c in campaigns.values()),
  currentActualBossUppercutDamage=sum(c['ownBossUppercutDamage']for c in campaigns.values()),
  currentRealKintaroRoundWins=prior['currentRealKintaroRoundWins']+sum(c['actualKintaroRoundWins']for c in new.values()),
  currentRealKintaroMatchClears=prior['currentRealKintaroMatchClears']+len(new),
  currentRealShaoKahnMatchClears=prior['currentRealShaoKahnMatchClears']+sum(c['actualShaoMatchClear']is not None for c in new.values()),
  currentFreshActualShaoRoundWins=sum(c['actualShaoRoundWins']for c in new.values()),
  currentBossLedgerCounterexamples=sum(c['rejectedSpecificLedgerCounterexamples']for c in campaigns.values()),
  currentBossPhysicalInputCounterexamples=sum(c.get('rejectedSpecificInputCounterexamples',0)for c in campaigns.values()),
  gameSourceAndPlayableBytesChangedThisTurn=False,testAutomationSourceChangedThisTurn=True,nativeDifficultyHealthAIPositionStageRNGModified=False,
  actualFullLadderClearAccepted=False,actualEndingsAccepted=False,fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
  nextAction='Use actual ordered guard/counter outcomes to select the next ordinary physical boss strategy without changing game balance or assigning health/IDs/state. Earn actual Shao clears, own endings/art/audio and attract both characters/both slots. Continue all-arena move-phase art/grounding/floor shadows/cleanup/audio, CPU/repeat/KO/overlap, all finishers/victims/morphs/secrets/cinematics, integrated UI/names/ladder regression and refreshed finished release ZIP. Fourteen dynamically required historical files are retained and protected; do not remove them based only on the obsolete static cleanup manifest.',
  inputHashes=pins)
 need(len(campaigns)==62 and len(prior['remaining'])>=5 and prior['objective']=='Once again, the goal is clear: THey need to appear as a natural part of the game in all aspects.','Entire original objective and unfinished scope retained')
 return prior

if __name__=='__main__':
 need(not OUT.exists(),'Immutable full-scope checkpoint')
 r=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(dict(goalStatus='active',acceptedPhysicalContexts=62,actualHuman107Assignments=r['currentActualBossHuman107Assignments'],
  actualShaoClears=r['currentRealShaoKahnMatchClears'],remaining68BuildNetAllocatedSavings=r['currentRemainingOldBuildCleanupNetAllocatedSavings'],
  gameChanged=False,fullPortAcceptance=False,finishedRelease=False),indent=2),flush=True)
