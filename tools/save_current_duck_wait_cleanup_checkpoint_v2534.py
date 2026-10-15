"""Carry full port scope with completed natural input evidence and recoverable cleanup."""
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_current_shao_duck_wait_boss_ledger_v2526 as ledger
ROOT=ledger.ROOT;launch=ledger.launch
PREVIOUS=ROOT/'audit_v2474_current_shao_crouch_exit_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2535_current_duck_wait_cleanup_checkpoint'
def need(ok,label):
 if not ok:raise ValueError(label)
def save():
 prior=json.loads(PREVIOUS.read_text());need(prior['goalStatus']=='active'and not prior['fullPortAcceptance']and not prior['finishedRelease'],'Entire original objective still active')
 pins=dict(prior['inputHashes']);pins[str(PREVIOUS)]=launch.sha(PREVIOUS)
 def accept(path):
  r=json.loads(path.read_text());need(r['passed']and not r['fullPortAcceptance'],'Actual accepted bounded evidence '+str(path))
  for file,wanted in r['inputHashes'].items():need(file not in pins or pins[file]==wanted,'Consistent carried/current graph');pins[file]=wanted
  pins[str(path)]=launch.sha(path);return r
 progress_path=ROOT/'audit_v2533_current_shao_duck_wait_progress/report.json';progress=accept(progress_path)
 boundary_path=ROOT/'audit_v2529_current_sonya_duck_wait_extended_boundary/report.json';boundary=accept(boundary_path)
 cleanup_path=ROOT/'audit_v2525_remaining_old_build_cleanup_checked/report.json';cleanup=accept(cleanup_path)
 boot_path=ROOT/'audit_v2537_current_default_launcher_after_cleanup_checked/report.json';boot=accept(boot_path)
 need(boot['afterVerified68OldBuildRemoval']and boot['everyObservedPIDHasCompleteExpectedPath']and not boot['diagnosticAutobootUsed']and boot['userSettingsFilesPreserved']==4,'Actual public CMD chain starts unchanged current1836 after cleanup, four play settings retained, no scripted inputs')
 need(boundary['originalFullCaptureRemainsRejected']and boundary['exactOriginalNativeRows']==312603 and boundary['pendingSelectionNumber']==52,'Rejected3600selection cutoff never waived')
 need(cleanup['filesDeleted']and cleanup['verifiedFiles']==465 and cleanup['verifiedDirectories']==352 and cleanup['all68PreviouslyUnreferencedBuildFoldersRemoved'],'Entire original68build recovery and native cleanup verified')
 need(not progress['gameOrCaptureModified']and not progress['fullEndingArtAudioAcceptance'],'Actual input-only evidence, no game or ending acceptance substitution')
 checks={'kano_shao_duck_wait':('audit_v2510_current_kano_shao_duck_wait_boss_ledger_checked','audit_v2511_current_kano_shao_duck_wait_input_counterexamples'),
  'sonya_shao_duck_wait':('audit_v2530_current_sonya_shao_duck_wait_boss_ledger_checked','audit_v2531_current_sonya_shao_duck_wait_input_counterexamples')}
 new={}
 for case,(fighter,side,capture,positive)in ledger.CASES.items():
  proof_path=ROOT/positive/'report.json';proof=accept(proof_path);book_name,negative_name=checks[case]
  book_path=ROOT/book_name/'report.json';book=accept(book_path);negative_path=ROOT/negative_name/'report.json';negative=accept(negative_path)
  need(book['rejectedSpecificCounterexamples']==8 and negative['rejectedSpecificCounterexamples']==27 and negative['finalUnmodifiedFullCampaignControlPassed'],'Independent ordered8and physical27specific negatives per case with final unchanged controls')
  row=progress['cases'][case];need(len(row['actualKintaroMatchClear']['actualOwnedWinFrames'])==2,'Owned Kintaro match earned in one actual successful attempt')
  new[case]=dict(row,campaignReport=str(proof_path),ledgerReport=str(book_path),inputCounterexampleReport=str(negative_path),capture=str(ROOT/capture),
   stagesReached=proof['stages_reached'],actualNativeHuman107Assignments=book['originalHuman107Assignments'],ownBossUppercutDamage=book['ownBossUppercutDamage'],
   ownBossRoundWins=book['ownBossRoundWins'],fullCampaignClear=proof['unassisted_clear_proven'],endingAccepted=False,
   repeatedKintaroControlNotIndependentStrategyCoverage=True)
 failure_path=ROOT/'audit_v2498_current_duck_wait_launcher_comparison_failure/failure.json';pins[str(failure_path)]=launch.sha(failure_path)
 failed=ROOT/'audit_v2508_current_sonya_p1_shao_duck_wait_checked/report.json';need(not json.loads(failed.read_text())['passed'],'Original incomplete full capture still rejected');pins[str(failed)]=launch.sha(failed)
 pending_manifest=ROOT/'audit_v2519_current_duck_wait_cleanup_pending/pending.json';pins[str(pending_manifest)]=launch.sha(pending_manifest)
 pins[str(Path(__file__).resolve())]=launch.sha(__file__);launch.module_pins(pins)
 print('Revalidating complete carried/current graph:',len(pins),'actual dependencies',flush=True)
 with ThreadPoolExecutor(max_workers=4)as pool:
  for index,((file,wanted),actual)in enumerate(zip(pins.items(),pool.map(launch.sha,pins)),1):
   need(actual==wanted,'Changed actual carried/current dependency '+file)
   if index%5000==0:print('Verified',index,'actual dependencies',flush=True)
 campaigns=dict(prior['currentSourceBoundBossCampaigns']);need(len(campaigns)==58 and not set(campaigns)&set(new),'Two actual new physical contexts only; longer Sonya is not an independent context');campaigns.update(new)
 prior.update(previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification='progress and verified live wait: original301proof/cleanup completed, new physical crouch-wait cases and recovery running',
  thisGoalTurnClassification='progress: same live jobs resumed to terminal; whole Kano3300/Sonya3610 physical campaigns accepted with54specific full-input and16ordered-ledger corruptions plus6exact pre-Shao corruptions. Original Sonya3600last-selection cutoff stays rejected;312603old rows exact and same selection52 completes ownID18 then actual Shao13fight. Complete465file352directory recovery independently verified before/after exact68old-build native deletion, with real unique-allocation/hardlink accounting. No ROM, character state, source, AI, damage, difficulty, RNG, stage or playable-byte changes.',
  currentSourceBoundBossCampaigns=campaigns,currentFreshShaoDuckWaitCampaigns=new,currentShaoDuckWaitProgressReport=str(progress_path),
  currentActualBossHuman107Assignments=sum(c['actualNativeHuman107Assignments']for c in campaigns.values()),
  currentActualBossUppercutDamage=sum(c['ownBossUppercutDamage']for c in campaigns.values()),
  currentRealKintaroRoundWins=prior['currentRealKintaroRoundWins']+sum(c['actualKintaroRoundWins']for c in new.values()),
  currentRealKintaroMatchClears=prior['currentRealKintaroMatchClears']+len(new),
  currentRealShaoKahnMatchClears=prior['currentRealShaoKahnMatchClears']+sum(c['actualShaoMatchClear']is not None for c in new.values()),
  currentFreshActualShaoRoundWins=sum(c['actualShaoRoundWins']for c in new.values()),
  currentBossLedgerCounterexamples=sum(c['rejectedSpecificLedgerCounterexamples']for c in campaigns.values()),
  currentBossPhysicalInputCounterexamples=sum(c.get('rejectedSpecificInputCounterexamples',0)for c in campaigns.values()),
  preservedSonyaIncompleteDuckWaitCaptureBoundary=str(boundary_path),preservedDuckWaitLauncherComparisonFailure=str(failure_path),
  pendingCrouchWaitCampaignsAccepted=True,pendingPhysicalOnlyCrouchWaitCampaigns=[],
  currentRemainingUnreferencedOldBuildCleanupReport=str(cleanup_path),currentRemainingOldBuildRecoveryArchive=cleanup['recoveryArchive'],
  currentRemainingOldBuildCleanupNetAllocatedSavings=cleanup['netAllocatedSavings'],
  currentPublicLauncherAfterRemainingOldBuildCleanupReport=str(boot_path),
  obsoleteFoldersDeletedThisTurn=True,foldersDeletedThisTurn=cleanup['targetDirectories'],
  all68PreviouslyUnreferencedBuildFoldersRemoved=True,allOldBuildFoldersRemoved=False,currentAndRequiredNativeDependencyBuildsRetained=True,
  gameSourceAndPlayableBytesChangedThisTurn=False,nativeDifficultyHealthAIPositionStageRNGModified=False,
  actualFullLadderClearAccepted=False,actualEndingsAccepted=False,fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
  nextAction='Use actual ordered attack/guard/crouch-exit episodes to improve ordinary physical boss controls without changing game balance or assigning health/IDs/state. Earn actual Shao clears, own endings/art/audio and attract bothcharacters/bothslots. Continue all-arena move-phase art/grounding/floor shadows/cleanup/audio, CPU/repeat/KO/overlap, all finishers/victims/morphs/secrets/cinematics, integrated UI/names/ladder regression and refreshed finishedrelease ZIP. Required native dependency builds remain; obsolete unreferenced build cleanup is verified, not a whole-port completion claim.',
  inputHashes=pins)
 need(len(campaigns)==60 and len(prior['remaining'])>=5,'All original broad unfinished gates retained')
 return prior
if __name__=='__main__':
 need(not OUT.exists(),'Immutable entire full-scope checkpoint')
 r=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(dict(goalStatus='active',acceptedPhysicalContexts=60,actualHuman107Assignments=r['currentActualBossHuman107Assignments'],
  actualShaoClears=r['currentRealShaoKahnMatchClears'],netAllocatedBytesSaved=r['currentRemainingOldBuildCleanupNetAllocatedSavings'],
  gameChanged=False,fullPortAcceptance=False,finishedRelease=False),indent=2),flush=True)
