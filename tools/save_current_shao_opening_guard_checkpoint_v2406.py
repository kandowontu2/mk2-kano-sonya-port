"""Preserve real-input opening evidence, the public launcher repair and full scope."""
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_current_shao_opening_guard_boss_ledger_v2400 as ledger
ROOT=ledger.ROOT;launch=ledger.launch
PREVIOUS=ROOT/'audit_v2390_current_shao_midrange_hp_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2407_current_shao_opening_guard_checkpoint'

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
   assert wanted is None or pins[path]==wanted,'Conflicting source graph '+path
   return
  actual=launch.sha(path)
  assert wanted is None or actual==wanted,'Changed actual dependency '+path
  pins[path]=actual
 def accept(path):
  path=Path(path);r=json.loads(path.read_text())
  assert r['passed'] and not r['fullPortAcceptance']
  for file,wanted in r['inputHashes'].items():pin(file,wanted)
  pin(path);return r
 pin(PREVIOUS);pin(__file__)
 progress_path=ROOT/'audit_v2405_current_shao_opening_guard_progress/report.json'
 damage_path=ROOT/'audit_v2409_current_shao_opening_damage_states/report.json'
 boundary_path=ROOT/'audit_v2413_current_sonya_opening_boundary/report.json'
 launcher_path=ROOT/'audit_v2418_current_default_launcher_checked/report.json'
 progress=accept(progress_path);damage=accept(damage_path);boundary=accept(boundary_path)
 launcher=accept(launcher_path)
 assert not progress['gameOrCaptureModified'] and not damage['gameOrCaptureModified']
 assert boundary['originalFullCampaignStillRejected'] and damage['shortRunStillRejected']
 assert damage['recaptureNotAnotherIndependentStrategy']
 assert len(damage['rejectedSpecificRecapturePrefixCounterexamples'])==3
 assert launcher['candidate']=='diagnostic_v1836_ball_register_boundary'
 assert launcher['defaultTargetChangedFromV277ToV1836']
 assert launcher['ordinaryBootFromOuterWorkingDirectory'] and not launcher['diagnosticAutobootUsed']
 assert launcher['everyObservedPIDHasCompleteExpectedPath'] and launcher['completeExecutablePathSnapshots']>0
 assert launcher['userSettingsFilesPreserved']==4 and not launcher['gameExecutableAndPayloadChanged']
 assert launcher['historicalV1852DefaultLauncherHashCheckSuperseded']
 failed_path=ROOT/'audit_v2416_current_default_launcher_checked/report.json'
 failed=json.loads(failed_path.read_text())
 assert not failed['passed'] and failed['exit_code']==0
 for file,wanted in failed['inputHashes'].items():pin(file,wanted)
 pin(failed_path);pin(ROOT/'tools/test_current_default_launcher_v2415.ps1')
 new_cases={};delays=[]
 for case,(fighter,side,capture,positive)in ledger.CASES.items():
  positive_path=ROOT/positive/'report.json';proof=accept(positive_path)
  book_path=ROOT/f'audit_v2402_current_{case}_boss_ledger_checked/report.json';book=accept(book_path)
  negative_path=ROOT/f'audit_v2403_current_{case}_input_counterexamples/report.json';negative=accept(negative_path)
  native=progress['cases'][case];outcomes=damage['cases'][case]
  assert book['finalUnmodifiedControlPassed'] and book['rejectedSpecificCounterexamples']==8
  assert negative['finalUnmodifiedFullCampaignControlPassed'] and negative['rejectedSpecificCounterexamples']==23
  assert proof['bounded_campaign_evidence_proven'] and not proof['unassisted_clear_proven']
  assert book['originalHuman107Assignments']==proof['actualNativeUppercutAssignments']
  assert book['ownBossUppercutDamage']==proof['actualBossUppercutDamage']
  assert len(native['rejectedSpecificPrefixCounterexamples'])==3
  assert native['actualKintaroMatchClear']['stage']==15 and len(native['actualKintaroMatchClear']['actualOwnedWinFrames'])==2
  assert native['actualShaoRoundWins']==0 and native['actualShaoMatchClear']is None
  assert native['actualEndingStarts']==native['actualEndingCompletions']==0
  assert native['nativeStartupSleepCalls']==2
  assert all(r['planTo107Fields']==4 for r in native['measuredShaoUppercutSpacing'])
  assert outcomes['actual107Assignments']==native['actualShaoHuman107Assignments']
  assert outcomes['actualOwned107Damage']==native['actualShaoUppercutDamage']
  assert outcomes['allActual107EpisodesHaveExactlyOneOwned30HPStore']
  delays.extend(r['planTo107Fields']for r in native['measuredShaoUppercutSpacing'])
  new_cases[case]=dict(campaignReport=str(positive_path),ledgerReport=str(book_path),inputCounterexampleReport=str(negative_path),
   capture=str(ROOT/capture),stagesReached=proof['stages_reached'],actualNativeHuman107Assignments=book['originalHuman107Assignments'],
   ownBossUppercutDamage=book['ownBossUppercutDamage'],ownBossRoundWins=book['ownBossRoundWins'],
   actualKintaroRoundWins=native['actualKintaroRoundWins'],actualKintaroMatchClear=native['actualKintaroMatchClear'],
   actualShaoRoundWins=0,actualShaoUppercutPlans=native['actualShaoUppercutPlans'],
   actualShaoHuman107Assignments=native['actualShaoHuman107Assignments'],actualShaoOwnedDamageStores=native['actualShaoOwnedDamageStores'],
   actualShaoOwnedDamage=native['actualShaoOwnedDamage'],actualShaoUppercutDamage=native['actualShaoUppercutDamage'],
   actualShaoIncomingDamage=native['actualShaoIncomingDamage'],exactPreShaoNativeRecords=native['exactPreShaoNativeRecords'],
   stage15IsExactReplayOfAcceptedLateApexControl=True,onlyExplicitPolicyLabelsNormalized=True,
   adjacentNativeBossFieldPairs=book['positiveHealthAdjacentBossFieldPairs'],
   physicalStompPlans=proof['physicalStompPlans'],physicalJumpkickPlans=proof['physicalJumpkickPlans'],
   rejectedSpecificLedgerCounterexamples=8,rejectedSpecificInputCounterexamples=23,rejectedSpecificPrefixCounterexamples=3,
   actualShaoAssignmentsWithOwnedDamage=outcomes['actual107EpisodesWithOwnedDamage'],
   fullCampaignClear=False,endingAccepted=False)
 assert len(delays)==101 and set(delays)=={4}
 assert sum(c['actualNativeHuman107Assignments']for c in new_cases.values())==265
 assert sum(c['ownBossUppercutDamage']for c in new_cases.values())==6274
 assert sum(c['actualShaoUppercutDamage']for c in new_cases.values())==3030
 assert sum(c['actualKintaroRoundWins']for c in new_cases.values())==14
 expected={
  ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'PLAY_MK2_KANO_SONYA.cmd':'631DDB18A2F740F102E5D4167B18269DE848A1E9936FE54DD8D8DD54C55ACAE7',
  ROOT/'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
  ROOT/'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata':'5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'}
 for file,wanted in expected.items():
  assert launch.sha(file)==wanted,'Canonical playable/deliverable'
  pin(file,wanted)
 launch.module_pins(pins)
 cases=dict(prior['currentSourceBoundBossCampaigns'])
 assert len(cases)==50 and not set(cases)&set(new_cases)
 cases.update(new_cases)
 prior.update(previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification='no progress: user-requested status report only; authoritative completed jobs and available next analyses revalidated',
  thisGoalTurnClassification='progress: complete exact pre-Shao trajectory and real-input opening damage analyses;101 actual human107 attacks each deal one original owned30HP hit, but no Shao round/match/ending. Preserve shorter Sonya recording as rejected and prove longer same-policy recapture exact through all nonterminal rows. Public CMD repair independently boots guarded current1836 instead of old277, settings unchanged. Full objective and all unfinished acceptance gates retained.',
  currentSourceBoundBossCampaigns=cases,currentFreshOpeningGuardCampaigns=new_cases,
  currentOpeningGuardProgressReport=str(progress_path),currentOpeningGuardDamageStatesReport=str(damage_path),
  preservedIncompleteSonyaOpeningCaptureDiagnosis=str(boundary_path),
  currentDefaultLauncherBootProof=str(launcher_path),defaultTargetChangedFromV277ToV1836=True,
  originalPublicLauncherBackup=launcher['oldV277LauncherBackup'],
  preservedDefaultLauncherTransientCIMCheckFailure=dict(report=str(failed_path),successor=str(launcher_path),
   correction='Every observed PID/parent must later have a complete expected executable path; transient null paths remain unknown, never accepted as path proof'),
  historicalV1852DefaultLauncherHashCheckSuperseded=True,
  currentActualBossHuman107Assignments=sum(c['actualNativeHuman107Assignments']for c in cases.values()),
  currentActualBossUppercutDamage=sum(c['ownBossUppercutDamage']for c in cases.values()),
  currentRealKintaroRoundWins=prior['currentRealKintaroRoundWins']+14,currentRealKintaroMatchClears=prior['currentRealKintaroMatchClears']+4,
  currentRealShaoKahnMatchClears=0,currentBossLedgerCounterexamples=sum(c['rejectedSpecificLedgerCounterexamples']for c in cases.values()),
  currentBossPhysicalInputCounterexamples=sum(c.get('rejectedSpecificInputCounterexamples',0)for c in cases.values()),
  currentOpeningGuardSpecificPrefixCounterexamples=12,currentSonyaRecaptureSpecificPrefixCounterexamples=3,
  currentOpeningGuardHuman107Assignments=101,currentOpeningGuardShaoUppercutOwnedDamage=3030,
  currentOpeningGuardOriginalStartupDelayFields=4,currentOpeningGuardOriginalStartupSleepCalls=2,
  repeatedKintaroPhaseNotClaimedAsIndependentStrategyCoverage=True,sonyaRecaptureNotClaimedAsIndependentStrategyCoverage=True,
  gameSourceAndPlayableBytesChangedThisTurn=False,publicDefaultLauncherChanged=True,nativeDifficultyHealthAIPositionStageRNGModified=False,
  obsoleteFoldersDeletedThisTurn=False,foldersDeletedThisTurn=[],newCaptureLeavesNTFSCompressed=True,
  actualFullLadderClearAccepted=False,actualEndingsAccepted=False,finishedRelease=False,fullPortAcceptance=False,
  nextAction='Use actual incoming action/physical-Block chronology to select fresh defense/movement tests. Successful measured opening attacks do not prove match balance or universal character fidelity. Earn original-game boss wins/own endings without writes or balance changes. Preserve all-move/all-arena art/ground/shadow/audio, CPU/repeated/KO/overlap, finishers/victims/morphs/secrets/cinematics, integrated UI regression, safe obsolete-build cleanup and finished release scope.',
  inputHashes=pins,goalStatus='active')
 assert len(cases)==54 and prior['currentActualBossHuman107Assignments']==5071
 assert prior['currentActualBossUppercutDamage']==55742
 assert prior['currentRealKintaroRoundWins']==60 and prior['currentRealKintaroMatchClears']==16
 assert len(prior['remaining'])>=5 and not prior['allOldBuildFoldersRemoved']
 return prior

if __name__=='__main__':
 assert not OUT.exists(),'Immutable full-scope opening checkpoint'
 r=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(dict(goalStatus='active',acceptedStrategyContexts=54,newActualShaoHuman107Assignments=101,
  newOwnedShaoUppercutDamage=3030,newSpecificCounterexamples=139,actualShaoRoundWins=0,
  defaultLauncherNowCurrent=True,fullClear=False,endingAccepted=False,gameBytesChanged=False,finishedRelease=False),indent=2),flush=True)
