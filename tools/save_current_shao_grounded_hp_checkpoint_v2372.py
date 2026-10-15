"""Freeze grounded Shao input/activation evidence, never substitute it for full acceptance."""
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_current_shao_grounded_hp_boss_ledger_v2366 as ledger
ROOT=ledger.ROOT;launch=ledger.launch
PREVIOUS=ROOT/'audit_v2356_current_late_airkick_observed_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2373_current_shao_grounded_hp_checkpoint'

def save():
 prior=json.loads(PREVIOUS.read_text())
 assert prior['goalStatus']=='active'and not prior['fullPortAcceptance']
 pins=dict(prior['inputHashes'])
 with ThreadPoolExecutor(max_workers=4)as pool:
  for (file,wanted),actual in zip(pins.items(),pool.map(launch.sha,pins)):
   assert actual==wanted,'Changed carried actual graph '+file
 def pin(path,wanted=None):
  path=str(Path(path).resolve());actual=launch.sha(path)
  assert wanted is None or actual==wanted,'Changed actual dependency '+path
  assert path not in pins or pins[path]==actual,'Conflicting actual graph '+path
  pins[path]=actual
 def accept(path):
  path=Path(path);r=json.loads(path.read_text())
  assert r['passed']and not r['fullPortAcceptance']
  for file,wanted in r['inputHashes'].items():
   if file in pins:assert pins[file]==wanted,'Conflicting graph '+file
   else:pin(file,wanted)
  pin(path);return r
 pin(PREVIOUS);pin(__file__)
 analysis_path=ROOT/'audit_v2371_current_shao_grounded_hp_progress/report.json'
 analysis=accept(analysis_path);assert not analysis['gameOrCaptureModified']
 new_cases={};native_sleeps=[];delays=[]
 for case,(fighter,side,capture,positive)in ledger.CASES.items():
  positive_path=ROOT/positive/'report.json';proof=accept(positive_path)
  book_path=ROOT/f'audit_v2368_current_{case}_boss_ledger_checked/report.json';book=accept(book_path)
  negative_path=ROOT/f'audit_v2369_current_{case}_input_counterexamples/report.json';negative=accept(negative_path)
  native=analysis['cases'][case]
  assert book['finalUnmodifiedControlPassed']and book['rejectedSpecificCounterexamples']==8
  assert negative['finalUnmodifiedFullCampaignControlPassed']and negative['rejectedSpecificCounterexamples']==21
  assert proof['bounded_campaign_evidence_proven']and not proof['unassisted_clear_proven']
  assert book['originalHuman107Assignments']==proof['actualNativeUppercutAssignments']
  assert book['ownBossUppercutDamage']==proof['actualBossUppercutDamage']
  assert len(native['rejectedSpecificPrefixCounterexamples'])==3
  assert native['actualKintaroMatchClear']['stage']==15 and len(native['actualKintaroMatchClear']['actualOwnedWinFrames'])==2
  assert native['actualShaoRoundWins']==0 and native['actualShaoMatchClear']is None
  assert native['actualEndingStarts']==native['actualEndingCompletions']==0
  assert all(r['planTo107Fields']==4 for r in native['measuredShaoUppercutSpacing'])
  delays.extend(r['planTo107Fields']for r in native['measuredShaoUppercutSpacing']);native_sleeps.append(native['nativeStartupSleepCalls'])
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
   rejectedSpecificLedgerCounterexamples=8,rejectedSpecificInputCounterexamples=21,rejectedSpecificPrefixCounterexamples=3,
   fullCampaignClear=False,endingAccepted=False)
 assert len(delays)==667 and set(delays)=={4}and set(native_sleeps)=={2}
 assert sum(c['actualNativeHuman107Assignments']for c in new_cases.values())==831
 assert sum(c['ownBossUppercutDamage']for c in new_cases.values())==7144
 assert sum(c['actualShaoUppercutDamage']for c in new_cases.values())==3900
 assert sum(c['actualShaoOwnedDamageStores']for c in new_cases.values())==130
 assert sum(c['actualKintaroRoundWins']for c in new_cases.values())==14
 expected={
  ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
  ROOT/'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata':'5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'}
 for file,wanted in expected.items():pin(file,wanted)
 views=[
  ROOT/'audit_v2364_current_kano_p1_shao_hp_early_campaign/snap/campaign_fight_selection10_stage16.png',
  ROOT/'audit_v2364_current_sonya_p1_shao_hp_early_campaign/snap/campaign_fight_selection14_stage16.png']
 for path in views:pin(path)
 launch.module_pins(pins)
 cases=dict(prior['currentSourceBoundBossCampaigns']);assert len(cases)==42 and not set(cases)&set(new_cases);cases.update(new_cases)
 prior.update(previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification='progress: observer-only correction, four fully verified Kintaro clears and exact native chronology;1.42GiB duplicate audio reclaimed with all evidence paths/hashes retained',
  thisGoalTurnClassification='progress: four fresh2400second natural grounded-Shao campaigns completed. Entire pre-Shao selection/ordinary/Kintaro native chronology reproduces accepted late-apex baseline with only declared policy labels normalized;457562total exact prior rows,12specific prefix counterexamples. Four full source/ID/input/health/win/progression controls, four ordered native ledgers32counterexamples and84physical input counterexamples pass. Native Shao uppercuts genuinely activate667times and land130owned30HP stores (3900damage); early125spacing activates almost every request while close95requests are commonly interrupted. All667activations follow request by exactly4fields, with unchanged original two1tick startup sleeps. No owned Shao round, full clear or ending. Two actual stage16 entry frames visually inspected for own sprites/names/shadows/no stale portraits; bounded only. No playable byte changed and original full scope preserved.',
  currentSourceBoundBossCampaigns=cases,currentFreshGroundedShaoCampaigns=new_cases,currentGroundedShaoProgressReport=str(analysis_path),
  currentActualBossHuman107Assignments=sum(c['actualNativeHuman107Assignments']for c in cases.values()),
  currentActualBossUppercutDamage=sum(c['ownBossUppercutDamage']for c in cases.values()),
  currentRealKintaroRoundWins=prior['currentRealKintaroRoundWins']+14,currentRealKintaroMatchClears=prior['currentRealKintaroMatchClears']+4,
  currentRealShaoKahnMatchClears=0,currentBossLedgerCounterexamples=sum(c['rejectedSpecificLedgerCounterexamples']for c in cases.values()),
  currentBossPhysicalInputCounterexamples=sum(c.get('rejectedSpecificInputCounterexamples',0)for c in cases.values()),
  currentGroundedShaoSpecificPrefixCounterexamples=12,currentGroundedShaoHuman107Assignments=667,currentGroundedShaoUppercutOwnedDamage=3900,
  currentGroundedShaoOriginalStartupDelayFields=4,currentGroundedShaoOriginalStartupSleepCalls=2,
  repeatedKintaroPhaseNotClaimedAsIndependentStrategyCoverage=True,
  boundedCurrentShaoEntryVisualInspection=dict(images=[str(path)for path in views],
   observation='Own Kano/Sonya sprites, shaded MK2 lifebar names, visible floor shadows and no lingering selection portraits in these two native stage16 fight-entry frames. Not all-move/all-arena art/ground/shadow certification.'),
  gameSourceAndPlayableBytesChangedThisTurn=False,nativeDifficultyHealthAIPositionStageRNGModified=False,
  obsoleteFoldersDeletedThisTurn=False,foldersDeletedThisTurn=[],newCaptureLeavesNTFSCompressed=True,
  actualFullLadderClearAccepted=False,actualEndingsAccepted=False,finishedRelease=False,fullPortAcceptance=False,
  nextAction='Test intermediate grounded-Shao HP spacing (for example110/115) while preserving measured4field original startup and all exact pre-Shao controls/gates. Use native CPU pose/field geometry and actual owned damage windows to avoid attributing every whiff solely to distance or calling it a character defect. Close95requests are often interrupted; early125almost always activates but often misses while boss spacing holds94/101/102. No guest health/AI/difficulty/RNG/stage/actor/task writes. Obtain actual Shao matches and own endings/pages/audio/attract for both characters/slots; retain full every-move/arena grounding-shadow-art-audio, broaderCPU/repeated/KO/overlap, all finishers/victims/morphs/secrets/cinematics, final combinedUI regression, dependency-aware old-build cleanup and refreshed release as the unchanged objective.',
  inputHashes=pins,goalStatus='active')
 assert len(cases)==46 and prior['currentActualBossHuman107Assignments']==3350
 assert prior['currentActualBossUppercutDamage']==44514 and prior['currentRealKintaroRoundWins']==32 and prior['currentRealKintaroMatchClears']==8
 assert len(prior['remaining'])>=5 and not prior['allOldBuildFoldersRemoved']
 return prior

if __name__=='__main__':
 assert not OUT.exists(),'Immutable full-scope Shao checkpoint'
 result=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(goalStatus='active',acceptedStrategyContexts=46,newActualShaoHuman107Assignments=667,
  newOwnedShaoUppercutDamage=3900,newSpecificCounterexamples=128,actualShaoRoundWins=0,
  fullClear=False,endingAccepted=False,gameBytesChanged=False,finishedRelease=False),indent=2),flush=True)
