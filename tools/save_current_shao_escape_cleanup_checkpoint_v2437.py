"""Retain failed-clear movement evidence and verified recoverable old-build cleanup."""
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_current_shao_opening_escape_boss_ledger_v2431 as ledger
ROOT=ledger.ROOT;launch=ledger.launch
PREVIOUS=ROOT/'audit_v2407_current_shao_opening_guard_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2438_current_shao_escape_cleanup_checkpoint'

def save():
 prior=json.loads(PREVIOUS.read_text())
 assert prior['goalStatus']=='active' and not prior['fullPortAcceptance']
 pins=dict(prior['inputHashes'])
 with ThreadPoolExecutor(max_workers=4)as pool:
  for(file,wanted),actual in zip(pins.items(),pool.map(launch.sha,pins)):
   assert actual==wanted,'Changed carried actual graph '+file
 def pin(path,wanted=None):
  path=str(Path(path).resolve())
  if path in pins:
   assert wanted is None or pins[path]==wanted,'Conflicting actual dependency '+path
   return
  actual=launch.sha(path);assert wanted is None or actual==wanted,'Changed dependency '+path;pins[path]=actual
 def accept(path):
  path=Path(path);r=json.loads(path.read_text())
  assert r['passed'] and not r['fullPortAcceptance']
  for file,wanted in r['inputHashes'].items():pin(file,wanted)
  pin(path);return r
 pin(PREVIOUS);pin(__file__)
 progress_path=ROOT/'audit_v2436_current_shao_opening_escape_progress/report.json'
 guard_path=ROOT/'audit_v2427_current_shao_native_guard_damage/report.json'
 recovery_path=ROOT/'audit_v2440_old_build_recovery_checked/report.json'
 progress=accept(progress_path);guard=accept(guard_path);recovery=accept(recovery_path)
 boot_path=ROOT/'audit_v2442_current_default_launcher_after_cleanup_checked/report.json'
 boot=accept(boot_path)
 assert boot['afterVerifiedSixOldBuildRemoval'] and boot['ordinaryBootFromOuterWorkingDirectory']
 assert boot['completeExecutablePathSnapshots']>0 and boot['everyObservedPIDHasCompleteExpectedPath']
 assert boot['userSettingsFilesPreserved']==4 and not boot['diagnosticAutobootUsed']
 assert not boot['gameExecutableAndPayloadChanged']
 assert not progress['gameOrCaptureModified'] and not guard['gameOrCaptureModified']
 assert guard['original17ReactionRowsRetainedExactly'] and guard['trueIDs17And18IncomingDamageCallbackNull']
 assert guard['originalGuardAndBlockedDamageRouteUnchangedExceptValidatedReactionTableRelocation']
 assert recovery['removedOldBuildFolders']==6 and recovery['archivedExactFiles']==99
 assert recovery['reclaimedAllocatedBytes']==90457245 and not recovery['allOldBuildFoldersRemoved']
 cleanup_path=ROOT/'audit_v2430_unreferenced_old_build_recovery/report.json'
 cleanup=json.loads(cleanup_path.read_text(encoding='utf-8-sig'));pin(cleanup_path)
 assert cleanup['passed'] and cleanup['archiveEveryEntryAndSourceHashVerified']
 assert cleanup['currentBuildSettingsAndPlaytestZIPUnchanged']
 for file,wanted in cleanup['keptHashes'].items():pin(file,wanted)
 assert all(not Path(folder).exists()for folder in cleanup['removedDirectories'])
 new={};delays=[]
 for case,(_,_,capture,positive)in ledger.CASES.items():
  positive_path=ROOT/positive/'report.json';proof=accept(positive_path)
  book_path=ROOT/f'audit_v2433_current_{case}_boss_ledger_checked/report.json';book=accept(book_path)
  negative_path=ROOT/f'audit_v2434_current_{case}_input_counterexamples/report.json';negative=accept(negative_path)
  row=progress['cases'][case]
  assert proof['bounded_campaign_evidence_proven'] and not proof['unassisted_clear_proven']
  assert book['finalUnmodifiedControlPassed'] and book['rejectedSpecificCounterexamples']==8
  assert negative['finalUnmodifiedFullCampaignControlPassed'] and negative['rejectedSpecificCounterexamples']==29
  assert book['originalHuman107Assignments']==proof['actualNativeUppercutAssignments']
  assert book['ownBossUppercutDamage']==proof['actualBossUppercutDamage']
  assert len(row['rejectedSpecificPrefixCounterexamples'])==3
  assert len(row['actualKintaroMatchClear']['actualOwnedWinFrames'])==2
  assert row['actualShaoRoundWins']==0 and row['actualShaoMatchClear']is None
  assert row['actualEndingStarts']==row['actualEndingCompletions']==0
  assert row['nativeStartupSleepCalls']==2
  assert all(r['planTo107Fields']==4 for r in row['measuredShaoUppercutSpacing'])
  delays.extend(r['planTo107Fields']for r in row['measuredShaoUppercutSpacing'])
  new[case]=dict(campaignReport=str(positive_path),ledgerReport=str(book_path),inputCounterexampleReport=str(negative_path),
   capture=str(ROOT/capture),stagesReached=proof['stages_reached'],actualNativeHuman107Assignments=book['originalHuman107Assignments'],
   ownBossUppercutDamage=book['ownBossUppercutDamage'],ownBossRoundWins=book['ownBossRoundWins'],
   actualKintaroRoundWins=row['actualKintaroRoundWins'],actualKintaroMatchClear=row['actualKintaroMatchClear'],
   actualShaoRoundWins=0,actualShaoUppercutPlans=row['actualShaoUppercutPlans'],
   actualShaoHuman107Assignments=row['actualShaoHuman107Assignments'],actualShaoOwnedDamageStores=row['actualShaoOwnedDamageStores'],
   actualShaoOwnedDamage=row['actualShaoOwnedDamage'],actualShaoUppercutDamage=row['actualShaoUppercutDamage'],
   actualShaoIncomingDamage=row['actualShaoIncomingDamage'],actualPositiveHealthShaoFields=row['actualPositiveHealthShaoFields'],
   actualShaoEscapeJumpkickPlans=row['actualShaoEscapeJumpkickPlans'],actualShaoHorizontalJumpAssignments=row['actualShaoHorizontalJumpAssignments'],
   actualShaoOwnedDamageByActualAction=row['actualShaoOwnedDamageByActualAction'],
   actualShaoIncomingDamageByActualAction=row['actualShaoIncomingDamageByActualAction'],
   exactPreShaoNativeRecords=row['exactPreShaoNativeRecords'],stage15IsExactReplayOfAcceptedLateApexControl=True,
   onlyExplicitPolicyLabelsNormalized=True,adjacentNativeBossFieldPairs=book['positiveHealthAdjacentBossFieldPairs'],
   physicalStompPlans=proof['physicalStompPlans'],physicalJumpkickPlans=proof['physicalJumpkickPlans'],
   rejectedSpecificLedgerCounterexamples=8,rejectedSpecificInputCounterexamples=29,rejectedSpecificPrefixCounterexamples=3,
   fullCampaignClear=False,endingAccepted=False)
 assert len(delays)==52 and set(delays)=={4}
 assert sum(c['actualNativeHuman107Assignments']for c in new.values())==134
 assert sum(c['ownBossUppercutDamage']for c in new.values())==3007
 assert sum(c['actualKintaroRoundWins']for c in new.values())==7
 cases=dict(prior['currentSourceBoundBossCampaigns']);assert len(cases)==54 and not set(cases)&set(new);cases.update(new)
 launch.module_pins(pins)
 prior.update(previousCheckpoint=str(PREVIOUS),
  thisGoalTurnClassification='progress: complete opening/damage/native guard route checks and two fresh3000second physical movement campaigns with independent source/ID/input/health/win/progression checks. All pre-Shao native chronology remains exact. Movement controls do not earn Shao wins or endings; no ROM/balance/AI/HP/RNG/stage changes. Six exact unreferenced old build folders removed only after99files and original directories archived and independently hash verified,90,457,245allocated bytes reclaimed. All broad full-port gates retained.',
  currentSourceBoundBossCampaigns=cases,currentFreshShaoEscapeCampaigns=new,
  currentShaoEscapeProgressReport=str(progress_path),currentShaoNativeGuardDamageReport=str(guard_path),
  currentOldBuildRecoveryProof=str(recovery_path),
  currentDefaultLauncherAfterCleanupBootProof=str(boot_path),
  currentActualBossHuman107Assignments=sum(c['actualNativeHuman107Assignments']for c in cases.values()),
  currentActualBossUppercutDamage=sum(c['ownBossUppercutDamage']for c in cases.values()),
  currentRealKintaroRoundWins=prior['currentRealKintaroRoundWins']+7,currentRealKintaroMatchClears=prior['currentRealKintaroMatchClears']+2,
  currentRealShaoKahnMatchClears=0,currentBossLedgerCounterexamples=sum(c['rejectedSpecificLedgerCounterexamples']for c in cases.values()),
  currentBossPhysicalInputCounterexamples=sum(c.get('rejectedSpecificInputCounterexamples',0)for c in cases.values()),
  currentShaoEscapeSpecificPrefixCounterexamples=6,currentShaoEscapeOriginalStartupDelayFields=4,currentShaoEscapeOriginalStartupSleepCalls=2,
  repeatedKintaroPhaseNotClaimedAsIndependentStrategyCoverage=True,
  gameSourceAndPlayableBytesChangedThisTurn=False,nativeDifficultyHealthAIPositionStageRNGModified=False,
  obsoleteFoldersDeletedThisTurn=True,foldersDeletedThisTurn=cleanup['removedDirectories'],
  currentOldBuildRecoveryZIP=cleanup['recoveryZIP'],currentOldBuildRecoveryZipSHA256=cleanup['recoveryZipSHA256'],
  currentOldBuildCleanupReclaimedAllocatedBytes=90457245,allOldBuildFoldersRemoved=False,
  actualFullLadderClearAccepted=False,actualEndingsAccepted=False,finishedRelease=False,fullPortAcceptance=False,
  nextAction='Do not mistake repeated automated-controller losses for a proved character/balance defect. Guard route/stock descriptors and true-ID incoming damage callbacks are verified; close jumping and backward retreat still do not earn Shao wins. Most new incoming damage occurs in actual0000/0301 states, and the physical jump predicate excludes0301; determine the original meaning and jump transition of that native state before another whole campaign. Use actual incoming action/attack episodes for a genuinely different physical control or stock-human comparison, without modifying original game balance. Continue all-arena/move phase art/ground/shadow/audio and CPU/repeated/KO/overlap verification, all finishers/victims/morphs/secrets/cinematics, earned both-slot endings/attract, integrated UI regression, remaining dependency-aware old-build cleanup and refreshed finished release. Full original objective stays active.',
  inputHashes=pins,goalStatus='active')
 assert len(cases)==56 and prior['currentActualBossHuman107Assignments']==5205
 assert prior['currentActualBossUppercutDamage']==58749 and prior['currentRealKintaroRoundWins']==67 and prior['currentRealKintaroMatchClears']==18
 assert len(prior['remaining'])>=5
 return prior

if __name__=='__main__':
 assert not OUT.exists(),'Immutable complete-scope escape/cleanup checkpoint'
 r=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(dict(goalStatus='active',acceptedStrategyContexts=56,actualShaoRoundWins=0,
  fullClear=False,endingAccepted=False,gameBytesChanged=False,removedOldBuildFolders=6,
  reclaimedAllocatedBytes=90457245,allOldBuildFoldersRemoved=False,finishedRelease=False),indent=2),flush=True)
