"""Accept complete observer recaptures and earned Kintaro matches; preserve full port scope."""
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_current_late_airkick_observed_boss_ledger_v2349 as ledger
ROOT=ledger.ROOT;launch=ledger.launch
PREVIOUS=ROOT/'audit_v2331_current_active_escape_episode_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2356_current_late_airkick_observed_checkpoint'

def save():
 prior=json.loads(PREVIOUS.read_text())
 assert prior['goalStatus']=='active'and not prior['fullPortAcceptance']
 pins=dict(prior['inputHashes'])
 with ThreadPoolExecutor(max_workers=4)as pool:
  for (file,wanted),actual in zip(pins.items(),pool.map(launch.sha,pins)):
   assert wanted==actual,'Changed carried source/capture '+file
 def pin(path,wanted=None):
  path=str(Path(path).resolve());actual=launch.sha(path)
  assert wanted is None or actual==wanted,'Changed actual dependency '+path
  assert path not in pins or pins[path]==actual,'Conflicting source graph '+path
  pins[path]=actual
 def accept(path):
  path=Path(path);r=json.loads(path.read_text())
  assert r['passed']and r['fullPortAcceptance']is False
  for file,wanted in r['inputHashes'].items():
   if file in pins:assert pins[file]==wanted,'Conflicting graph '+file
   else:pin(file,wanted)
  pin(path);return r
 pin(PREVIOUS);pin(__file__)
 diagnostic_path=ROOT/'audit_v2343_current_late_airkick_action_tap_diagnostic/report.json'
 diagnostic=accept(diagnostic_path)
 equivalence_path=ROOT/'audit_v2358_current_late_airkick_boundary_observation_equivalence/report.json'
 equivalence=accept(equivalence_path)
 analysis_path=ROOT/'audit_v2342_current_late_airkick_boss_progress/report.json'
 analysis=accept(analysis_path)
 storage_path=ROOT/'audit_v2360_current_identical_late_audio_storage/report.json'
 storage=accept(storage_path)
 assert storage['duplicatesRemoved']==4 and storage['allocatedDuplicateBytesReclaimed']>0
 assert storage['allOriginalAndReplayPathsPreserved']and storage['allEvidenceBytesAndHashesUnchanged']and not storage['uniqueDataDeleted']
 failed_equivalence_path=ROOT/'audit_v2354_current_late_airkick_observation_equivalence_failure/report.json'
 failed_equivalence=json.loads(failed_equivalence_path.read_text())
 assert not failed_equivalence['passed']and failed_equivalence['exitCode']==1
 for file,wanted in failed_equivalence['inputHashes'].items():pin(file,wanted)
 pin(failed_equivalence_path)
 assert not analysis['gameOrCaptureModified']and not equivalence['nativeRowsNormalized']
 assert not diagnostic['originalLedgerGateWaived']and not equivalence['originalLedgerGateWaived']
 new_cases={};originals={}
 for case,(fighter,side,capture,positive)in ledger.CASES.items():
  positive_path=ROOT/positive/'report.json';proof=accept(positive_path)
  book_path=ROOT/f'audit_v2350_current_{case}_boss_ledger_checked/report.json';book=accept(book_path)
  negative_path=ROOT/f'audit_v2352_current_{case}_input_counterexamples/report.json';negative=accept(negative_path)
  assert proof['bounded_campaign_evidence_proven']and not proof['unassisted_clear_proven']
  assert book['finalUnmodifiedControlPassed']and book['rejectedSpecificCounterexamples']==8
  assert negative['finalUnmodifiedFullCampaignControlPassed']and negative['rejectedSpecificCounterexamples']==(15 if case.endswith('descend')else 14)
  assert book['originalHuman107Assignments']==proof['actualNativeUppercutAssignments']
  assert book['ownBossUppercutDamage']==proof['actualBossUppercutDamage']
  assert book['ownBossRoundWins']==proof['actualBossRoundWins']
  native=analysis['cases'][case];same=equivalence['cases'][case]
  assert len(native['actualKintaroMatchClears'])==1 and native['actualShaoRoundWins']==0
  assert native['actualEndingStarts']==native['actualEndingCompletions']==0
  assert same['everyOriginalActionRetainedInOrder']and same['allAddedActionsHaveProvenStaleBinding']
  assert same['strictOrderedActionHealthLedgerPassed']and len(same['specificCounterexamples'])==(3 if case=='sonya_late_descend'else 5)
  policy=case.split('_',1)[1]
  original_positive=ROOT/f'audit_v2336_current_{fighter}_p1_{policy}_checked/report.json';accept(original_positive)
  failed_path=ROOT/f'audit_v2338_current_{case}_boss_ledger_checked/report.json'
  failed=json.loads(failed_path.read_text());pin(failed_path)
  if case=='sonya_late_descend':assert failed['passed']
  else:assert not failed['passed']and 'Action stores explain actual adjacent native fields'in failed['error']
  originals[case]=dict(capture=str(ROOT/f'audit_v2335_current_{fighter}_p1_{policy}_campaign'),
   progressionProof=str(original_positive),orderedLedger=str(failed_path),
   originalOrderedLedgerPassed=failed['passed'],observationEquivalence=same,
   diagnosticMissingAdjacentPairs=diagnostic['cases'][case]['missingAdjacentActionObservations'],
   originalRecordingNotCountedAsIndependentStrategyContext=True)
  new_cases[case]=dict(campaignReport=str(positive_path),ledgerReport=str(book_path),
   inputCounterexampleReport=str(negative_path),capture=str(ROOT/capture),stagesReached=proof['stages_reached'],
   actualNativeHuman107Assignments=book['originalHuman107Assignments'],ownBossUppercutDamage=book['ownBossUppercutDamage'],
   ownBossRoundWins=book['ownBossRoundWins'],actualKintaroRoundWins=native['actualKintaroRoundWins'],
   actualKintaroMatchClears=native['actualKintaroMatchClears'],actualShaoRoundWins=0,
   adjacentNativeBossFieldPairs=book['positiveHealthAdjacentBossFieldPairs'],
   physicalStompPlans=proof['physicalStompPlans'],physicalJumpkickPlans=proof['physicalJumpkickPlans'],
   actualHuman308Jumps=native['actualHuman308Jumps'],actualHuman200AirKicks=native['actualHuman200AirKicks'],
   rejectedSpecificLedgerCounterexamples=8,rejectedSpecificInputCounterexamples=negative['rejectedSpecificCounterexamples'],
   fullCampaignClear=False,endingAccepted=False)
 expected={
  ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
  ROOT/'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata':'5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'}
 for file,wanted in expected.items():pin(file,wanted)
 launch.module_pins(pins)
 cases=dict(prior['currentSourceBoundBossCampaigns']);assert not set(cases)&set(new_cases);cases.update(new_cases)
 assert len(cases)==42
 assert sum(c['actualNativeHuman107Assignments']for c in new_cases.values())==155
 assert sum(c['ownBossUppercutDamage']for c in new_cases.values())==3048
 assert sum(c['actualKintaroRoundWins']for c in new_cases.values())==14
 prior.update(previousCheckpoint=str(PREVIOUS),
  previousGoalTurnClassification='no progress: previous user-facing turn inspected evidence and answered status only',
  thisGoalTurnClassification='progress: four late-phase physical controls completed; all naturally cleared Kintaro and reached Shao Kahn. Three strict action ledgers exposed an observer Main-address reuse bug; all386missing adjacent observations diagnosed without waiver. Read-only current-actor tap correction restores exactly to old driver and full850baseline. Four2400second recaptures preserve every native non-action record exactly and all original action records in order; only proven formerly suppressed records added. Complete source/identity/physical input/health/win/progression checks, four strict ordered ledgers,32ledger58input18equivalence12episode counterexamples accepted. Initial overly narrow equivalence assumption preserved as failed2353; corrected2357proves exactly32native mode6/7construction/refill records using unchanged original instructions, not combat activations. Four exact immutable replay-audio duplicates share storage while every evidence path and byte hash remains unchanged; allocated duplicate space reclaimed. No playable byte changed. Shao clears/endings and complete remaining scope unproven.',
  currentSourceBoundBossCampaigns=cases,currentFreshLateAirKickBossCampaigns=new_cases,
  currentActualBossHuman107Assignments=sum(c['actualNativeHuman107Assignments']for c in cases.values()),
  currentActualBossUppercutDamage=sum(c['ownBossUppercutDamage']for c in cases.values()),
  currentRealKintaroRoundWins=prior['currentRealKintaroRoundWins']+14,
  currentRealKintaroMatchClears=prior['currentRealKintaroMatchClears']+4,
  currentRealShaoKahnMatchClears=0,
  currentBossLedgerCounterexamples=sum(c['rejectedSpecificLedgerCounterexamples']for c in cases.values()),
  currentBossPhysicalInputCounterexamples=sum(c.get('rejectedSpecificInputCounterexamples',0)for c in cases.values()),
  currentLateAirKickBossProgressReport=str(analysis_path),currentLateAirKickObservationEquivalence=str(equivalence_path),
  currentLateAirKickActionTapDiagnosis=str(diagnostic_path),preservedOriginalLateAirKickRecordings=originals,
  currentLateAirKickEpisodeCounterexamples=12,currentLateAirKickObservationCounterexamples=18,
  preservedLateAirKickEquivalenceCheckerFailure=str(failed_equivalence_path),
  currentIdenticalLateAudioStorageCleanup=str(storage_path),
  duplicateAudioAllocatedBytesReclaimed=storage['allocatedDuplicateBytesReclaimed'],
  allReplayEvidencePathsAndBytesPreserved=True,
  gameSourceAndPlayableBytesChangedThisTurn=False,nativeDifficultyHealthAIPositionStageRNGModified=False,
  obsoleteFoldersDeletedThisTurn=False,foldersDeletedThisTurn=[],newCaptureLeavesNTFSCompressed=True,
  actualFullLadderClearAccepted=False,actualEndingsAccepted=False,finishedRelease=False,fullPortAcceptance=False,
  nextAction='Native Shao traces show heavy incoming damage during actual horizontal-jump startup and many guarded air-kicks. Test a boss13-only grounded fresh-HP/spacing or earlier/backward air-kick physical response; keep exact Kintaro and all ordinary controls, full source/ID/action/health/progression gates, no health/AI/difficulty/RNG/task writes. Verify actual Shao matches, own endings/pages/audio/attract; preserve every move/arena grounding-shadow-art-audio includingCPU/repeated/KO/overlap, all finishers/victims/morphs/secrets/cinematics, final combinedUI regression, dependency-aware cleanup and updated release as the unchanged full objective.',
  inputHashes=pins,goalStatus='active')
 assert prior['currentActualBossHuman107Assignments']==2519 and prior['currentActualBossUppercutDamage']==37370
 assert prior['currentRealKintaroRoundWins']==18 and prior['currentRealKintaroMatchClears']==4
 assert len(prior['remaining'])>=5
 return prior

if __name__=='__main__':
 assert not OUT.exists(),'Immutable full-scope boss checkpoint'
 result=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(goalStatus='active',acceptedStrategyContexts=len(result['currentSourceBoundBossCampaigns']),
  newActualKintaroMatchClears=4,newActualKintaroRoundWins=14,actualShaoMatchClears=0,
  actualOwnEndings=0,observerOnlyChange=True,gameBytesChanged=False,finishedRelease=False,fullPortAcceptance=False),indent=2),flush=True)
