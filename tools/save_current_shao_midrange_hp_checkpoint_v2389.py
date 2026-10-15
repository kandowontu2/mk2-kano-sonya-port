"""Freeze intermediate-distance Shao evidence and retain every unfinished full-port gate."""
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_current_shao_midrange_hp_boss_ledger_v2379 as ledger
ROOT=ledger.ROOT;launch=ledger.launch
PREVIOUS=ROOT/'audit_v2373_current_shao_grounded_hp_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2390_current_shao_midrange_hp_checkpoint'

def save():
 prior=json.loads(PREVIOUS.read_text());assert prior['goalStatus']=='active'and not prior['fullPortAcceptance']
 pins=dict(prior['inputHashes'])
 with ThreadPoolExecutor(max_workers=4)as pool:
  for(file,wanted),actual in zip(pins.items(),pool.map(launch.sha,pins)):assert actual==wanted,'Changed carried actual graph '+file
 def pin(path,wanted=None):
  path=str(Path(path).resolve())
  if path in pins:
   assert wanted is None or pins[path]==wanted,'Conflicting source graph '+path
   return
  actual=launch.sha(path);assert wanted is None or actual==wanted,'Changed actual dependency '+path;pins[path]=actual
 def accept(path):
  path=Path(path);r=json.loads(path.read_text());assert r['passed']and not r['fullPortAcceptance']
  for file,wanted in r['inputHashes'].items():pin(file,wanted)
  pin(path);return r
 pin(PREVIOUS);pin(__file__)
 analysis_path=ROOT/'audit_v2383_current_shao_midrange_hp_progress/report.json'
 analysis=accept(analysis_path);assert not analysis['gameOrCaptureModified']
 diagnostic_path=ROOT/'audit_v2386_current_boss_damage_action_order/report.json'
 diagnostic=accept(diagnostic_path);assert not diagnostic['gameOrCaptureModified']
 assert len(diagnostic['cases'])==4 and all(r['classificationDifferenceStores']==0 for r in diagnostic['cases'].values())
 contact_path=ROOT/'audit_v2388_current_shao_contact_outcomes/report.json'
 contact=accept(contact_path);assert not contact['gameOrCaptureModified']and len(contact['cases'])==8
 plan_contact_path=ROOT/'audit_v2394_current_shao_plan_contact_outcomes/report.json'
 plan_contact=accept(plan_contact_path);assert not plan_contact['gameOrCaptureModified']and len(plan_contact['cases'])==8
 for case,row in plan_contact['cases'].items():
  restored={k:v for k,v in row.items()if k!='planInputCPUStateGroups'}
  restored['episodes']=[{k:v for k,v in e.items()if k not in('planPreInputCPUPose','planPreInputCPUBody','planPreInputCPUAction')}for e in row['episodes']]
  assert restored==contact['cases'][case],'All original actual contact episodes retained exactly'
 assert plan_contact['source']==contact['source'],'Identical original source facts retained'
 failure_path=ROOT/'audit_v2392_current_shao_plan_contact_outcomes_failure/report.json'
 failure=json.loads(failure_path.read_text());assert not failure['passed']and failure['exit_code']==1 and not failure['gameOrCaptureModified']
 assert not (ROOT/'audit_v2392_current_shao_plan_contact_outcomes').exists(),'Failed checker never accepted as a contact report'
 pin(failure_path);pin(ROOT/'tools/analyze_current_shao_plan_contact_outcomes_v2391.py')
 new_cases={};delays=[]
 for case,(fighter,side,capture,positive)in ledger.CASES.items():
  positive_path=ROOT/positive/'report.json';proof=accept(positive_path)
  book_path=ROOT/f'audit_v2381_current_{case}_boss_ledger_checked/report.json';book=accept(book_path)
  negative_path=ROOT/f'audit_v2382_current_{case}_input_counterexamples/report.json';negative=accept(negative_path)
  native=analysis['cases'][case];outcomes=contact['cases'][case]
  assert book['finalUnmodifiedControlPassed']and book['rejectedSpecificCounterexamples']==8
  assert negative['finalUnmodifiedFullCampaignControlPassed']and negative['rejectedSpecificCounterexamples']==21
  assert proof['bounded_campaign_evidence_proven']and not proof['unassisted_clear_proven']
  assert book['originalHuman107Assignments']==proof['actualNativeUppercutAssignments']
  assert book['ownBossUppercutDamage']==proof['actualBossUppercutDamage']
  assert len(native['rejectedSpecificPrefixCounterexamples'])==3
  assert native['actualKintaroMatchClear']['stage']==15 and len(native['actualKintaroMatchClear']['actualOwnedWinFrames'])==2
  assert native['actualShaoRoundWins']==0 and native['actualShaoMatchClear']is None
  assert native['actualEndingStarts']==native['actualEndingCompletions']==0
  assert all(r['planTo107Fields']==4 for r in native['measuredShaoUppercutSpacing'])and native['nativeStartupSleepCalls']==2
  assert outcomes['actual107Assignments']==native['actualShaoHuman107Assignments']
  assert outcomes['actualOwned107Damage']==native['actualShaoUppercutDamage']
  delays.extend(r['planTo107Fields']for r in native['measuredShaoUppercutSpacing'])
  new_cases[case]=dict(campaignReport=str(positive_path),ledgerReport=str(book_path),inputCounterexampleReport=str(negative_path),
   capture=str(ROOT/capture),stagesReached=proof['stages_reached'],actualNativeHuman107Assignments=book['originalHuman107Assignments'],
   ownBossUppercutDamage=book['ownBossUppercutDamage'],ownBossRoundWins=book['ownBossRoundWins'],
   actualKintaroRoundWins=native['actualKintaroRoundWins'],actualKintaroMatchClear=native['actualKintaroMatchClear'],
   actualShaoRoundWins=native['actualShaoRoundWins'],actualShaoUppercutPlans=native['actualShaoUppercutPlans'],
   actualShaoHuman107Assignments=native['actualShaoHuman107Assignments'],actualShaoOwnedDamageStores=native['actualShaoOwnedDamageStores'],
   actualShaoOwnedDamage=native['actualShaoOwnedDamage'],actualShaoUppercutDamage=native['actualShaoUppercutDamage'],
   actualShaoIncomingDamage=native['actualShaoIncomingDamage'],exactPreShaoNativeRecords=native['exactPreShaoNativeRecords'],
   stage15IsExactReplayOfAcceptedLateApexControl=True,onlyExplicitPolicyLabelsNormalized=True,
   adjacentNativeBossFieldPairs=book['positiveHealthAdjacentBossFieldPairs'],
   physicalStompPlans=proof['physicalStompPlans'],physicalJumpkickPlans=proof['physicalJumpkickPlans'],
   rejectedSpecificLedgerCounterexamples=8,rejectedSpecificInputCounterexamples=21,rejectedSpecificPrefixCounterexamples=3,
   actualShaoAssignmentsWithOwnedDamage=outcomes['assignmentsWithOwnedDamage'],
   fullCampaignClear=False,endingAccepted=False)
 assert len(delays)==1292 and set(delays)=={4}
 assert sum(c['actualNativeHuman107Assignments']for c in new_cases.values())==1456
 assert sum(c['ownBossUppercutDamage']for c in new_cases.values())==4954
 assert sum(c['actualShaoUppercutDamage']for c in new_cases.values())==1710
 assert sum(c['actualShaoOwnedDamageStores']for c in new_cases.values())==57
 assert sum(c['actualKintaroRoundWins']for c in new_cases.values())==14
 expected={
  ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
  ROOT/'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata':'5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'}
 for file,wanted in expected.items():
  assert launch.sha(file)==wanted,'Canonical playable/deliverable unchanged';pin(file,wanted)
 launch.module_pins(pins)
 cases=dict(prior['currentSourceBoundBossCampaigns']);assert len(cases)==46 and not set(cases)&set(new_cases);cases.update(new_cases)
 prior.update(previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification='progress: four verified grounded-Shao campaigns and source-exact startup evidence in checkpoint2373',
  interveningUserStatusResponse='status only, no implementation; checkpoint2373 re-read and no live MAME process observed before four fresh campaigns',
  thisGoalTurnClassification='progress: four fresh2400second input-only campaigns and full independent source/identity/input/health/win/progression checks. Four ordered action/health ledgers reject32specific corruptions; four whole-controller suites reject84specific corruptions. Entire pre-Shao chronology replays the accepted baseline exactly except declared policy labels,457562rows and12specific prefix corruptions. Actual Shao107 assignments1292 produce57owned30HP hits/1710damage but no owned Shao round, match or ending. Original two startup sleeps/4field activation delay retained. Actual-event damage-action diagnostic reproduces all four prior totals without misclassification. Eight source-bound contact contexts track actual own107 episodes, original strike/body/scaling code and dedicated true-ID descriptors; no game bytes changed, no balance/AI/HP/difficulty/RNG/state assistance, full scope retained.',
  currentSourceBoundBossCampaigns=cases,currentFreshMidrangeShaoCampaigns=new_cases,currentMidrangeShaoProgressReport=str(analysis_path),
  currentBossDamageActionOrderDiagnostic=str(diagnostic_path),priorGroundedBossDamageActionClassificationDifferences=0,
  currentShaoContactOutcomesReport=str(contact_path),
  currentShaoPlanTimeContactOutcomesReport=str(plan_contact_path),
  preservedShaoPlanRepresentationComparisonFailure=dict(report=str(failure_path),successor=str(ROOT/'tools/analyze_current_shao_plan_contact_outcomes_v2393.py'),correction='Exact JSON tuple/list representation only; every source fact and original episode/count comparison retained'),
  currentActualBossHuman107Assignments=sum(c['actualNativeHuman107Assignments']for c in cases.values()),
  currentActualBossUppercutDamage=sum(c['ownBossUppercutDamage']for c in cases.values()),
  currentRealKintaroRoundWins=prior['currentRealKintaroRoundWins']+14,currentRealKintaroMatchClears=prior['currentRealKintaroMatchClears']+4,
  currentRealShaoKahnMatchClears=0,currentBossLedgerCounterexamples=sum(c['rejectedSpecificLedgerCounterexamples']for c in cases.values()),
  currentBossPhysicalInputCounterexamples=sum(c.get('rejectedSpecificInputCounterexamples',0)for c in cases.values()),
  currentMidrangeShaoSpecificPrefixCounterexamples=12,currentMidrangeShaoHuman107Assignments=1292,currentMidrangeShaoUppercutOwnedDamage=1710,
  currentMidrangeShaoOriginalStartupDelayFields=4,currentMidrangeShaoOriginalStartupSleepCalls=2,
  repeatedKintaroPhaseNotClaimedAsIndependentStrategyCoverage=True,
  gameSourceAndPlayableBytesChangedThisTurn=False,nativeDifficultyHealthAIPositionStageRNGModified=False,
  obsoleteFoldersDeletedThisTurn=False,foldersDeletedThisTurn=[],newCaptureLeavesNTFSCompressed=True,
  actualFullLadderClearAccepted=False,actualEndingsAccepted=False,finishedRelease=False,fullPortAcceptance=False,
  nextAction='Stop blind distance-only tuning. Use source-bound actual plan-time CPU pose/body/action visible before pressing HP, actual107 episodes and owned-damage chronology to design fresh physical movement/defense/attack-window controls; never use future/post-input CPU state as if visible at the command. Preserve original startup, all exact pre-Shao controls and all source/ID/input/damage/win gates. No health, AI, difficulty, RNG, stage, actor or task writes. Earn actual Shao matches and complete own endings/pages/audio/attract for both characters/slots. Keep all-move/all-arena art/ground/floor-shadow/audio, broaderCPU/repeated/KO/overlap, all finishers/victims/morphs/secrets/cinematics, final integratedUI regression, dependency-aware obsolete-build cleanup and refreshed finished release as unchanged remaining full objective.',
  inputHashes=pins,goalStatus='active')
 assert len(cases)==50 and prior['currentActualBossHuman107Assignments']==4806
 assert prior['currentActualBossUppercutDamage']==49468 and prior['currentRealKintaroRoundWins']==46 and prior['currentRealKintaroMatchClears']==12
 assert len(prior['remaining'])>=5 and not prior['allOldBuildFoldersRemoved']
 return prior

if __name__=='__main__':
 assert not OUT.exists(),'Immutable full-scope intermediate-Shao checkpoint'
 r=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(dict(goalStatus='active',acceptedStrategyContexts=50,newActualShaoHuman107Assignments=1292,newOwnedShaoUppercutDamage=1710,newSpecificCounterexamples=128,actualShaoRoundWins=0,fullClear=False,endingAccepted=False,gameBytesChanged=False,finishedRelease=False),indent=2),flush=True)
