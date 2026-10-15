"""Carry full port scope with source-bound prepared boss progress, never a release."""
import json
from pathlib import Path
import verify_current_prepared_boss_ledger_v2255 as ledger
launch=ledger.launch;ROOT=ledger.ROOT
PREVIOUS=ROOT/'audit_v2239_current_native_guard_comparison_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2272_current_prepared_boss_checkpoint'

def save():
 prior=json.loads(PREVIOUS.read_text());assert prior['goalStatus']=='active'and prior['fullPortAcceptance']is False
 pins=dict(prior['inputHashes'])
 for file,wanted in pins.items():assert launch.sha(file)==wanted,'Changed carried full-scope source/capture '+file
 def pin(path,wanted=None):
  path=str(Path(path).resolve());actual=launch.sha(path)
  assert wanted is None or actual==wanted,'Changed actual dependency '+path
  assert path not in pins or pins[path]==actual,'Conflicting dependency '+path
  pins[path]=actual
 def accept(path):
  path=Path(path);r=json.loads(path.read_text());assert r['passed']and r['fullPortAcceptance']is False
  for file,wanted in r['inputHashes'].items():
   if file in pins:assert pins[file]==wanted,'Conflicting accepted actual graph '+file
   else:pin(file,wanted)
  pin(path);return r
 pin(PREVIOUS);pin(__file__)
 interrupted_path=ROOT/'audit_v2247_current_boss_release_interrupts/report.json';interrupted=accept(interrupted_path)
 incoming_path=ROOT/'audit_v2258_current_prepared_boss_damage/report.json';incoming=accept(incoming_path)
 assert not interrupted['gameOrCaptureModified']and not incoming['gameOrCaptureModified']
 new_cases={};wins=[]
 for case,(fighter,side,capture,positive)in ledger.CASES.items():
  campaign_path=ROOT/positive/'report.json';proof=accept(campaign_path)
  ledger_path=ROOT/f'audit_v2256_current_{case}_boss_ledger_checked/report.json';actual=accept(ledger_path)
  negative_path=ROOT/f'audit_v2260_current_{case}_input_counterexamples/report.json';negative=accept(negative_path)
  assert proof['bounded_campaign_evidence_proven']and not proof['unassisted_clear_proven']
  assert actual['finalUnmodifiedControlPassed']and actual['rejectedSpecificCounterexamples']==8
  assert negative['finalUnmodifiedFullCampaignControlPassed']and negative['rejectedSpecificCounterexamples']==8
  assert actual['originalHuman107Assignments']==proof['actualNativeUppercutAssignments']
  assert actual['ownBossRoundWins']==proof['actualBossRoundWins']
  assert actual['ownBossUppercutDamage']==proof['actualBossUppercutDamage']
  assert (ROOT/capture/'guest_maincpu.bin').read_bytes()==ledger.native.current_source.expected()[0]
  rows=ledger.native.parse((ROOT/capture/'run.log').read_text(encoding='utf-8-sig'),side,fighter)
  earned=[r for r in rows if r['tag']=='WIN'and r['slot']==side and r['stage']in(15,16)]
  assert len(earned)==proof['actualBossRoundWins']
  wins.extend(dict(case=case,**r)for r in earned)
  new_cases[case]=dict(campaignReport=str(campaign_path),ledgerReport=str(ledger_path),capture=str(ROOT/capture),
   inputCounterexampleReport=str(negative_path),stagesReached=proof['stages_reached'],
   actualNativeHuman107Assignments=actual['originalHuman107Assignments'],ownBossRoundWins=actual['ownBossRoundWins'],
   ownBossUppercutDamage=actual['ownBossUppercutDamage'],adjacentNativeBossFieldPairs=actual['positiveHealthAdjacentBossFieldPairs'],
   physicalPlans=proof['physicalBossPlans'],nativeHPDispatches=proof['nativeBossHPDispatches'],
   nativeUppercutEntryFetches=proof['nativeHumanUppercutEntryFetches'],
   rejectedSpecificLedgerCounterexamples=8,rejectedSpecificInputCounterexamples=8,
   fullCampaignClear=False,endingAccepted=False)
 assert sum(r['actualNativeHuman107Assignments']for r in new_cases.values())==429
 assert sum(r['physicalPlans']for r in new_cases.values())==439
 assert sum(r['ownBossUppercutDamage']for r in new_cases.values())==7391
 assert len(wins)==1 and wins[0]['frame']==117181 and wins[0]['id']==18 and wins[0]['stage']==15
 assert wins[0]['entry']==0xfffefa40 and wins[0]['pc']==0xff8296b0 and wins[0]['health']=='2,0'
 expected={
  ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
  ROOT/'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata':'5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'}
 for path,wanted in expected.items():pin(path,wanted)
 launch.module_pins(pins)
 cases=dict(prior['currentSourceBoundBossCampaigns']);assert not set(cases)&set(new_cases);cases.update(new_cases)
 prior.update(previousCheckpoint=str(PREVIOUS),
  previousGoalTurnClassification='no progress: the status-only response restated unfinished scope; current source and completed campaign reports revalidated before this goal continuation.',
  thisGoalTurnClassification='progress: all four actual prepared boss campaigns pass full current-source/selection/progression/native handler gates, with429real human107assignments from439plans,7391owned boss damage and one newly earnedSonyaKintaro round. Complete adjacent action/health ledgers and64specific negative controls pass. Actual damage chronology now directs follow-up input testing at close-range grab opportunities rather than patching native HP activation.',
  currentSourceBoundBossCampaigns=cases,currentFreshPreparedBossCampaigns=new_cases,
  currentActualBossHuman107Assignments=sum(r['actualNativeHuman107Assignments']for r in cases.values()),
  currentActualBossUppercutDamage=sum(r['ownBossUppercutDamage']for r in cases.values()),
  currentBossLedgerCounterexamples=sum(r['rejectedSpecificLedgerCounterexamples']for r in cases.values()),
  currentBossPhysicalInputCounterexamples=sum(r.get('rejectedSpecificInputCounterexamples',0)for r in cases.values()),
  currentRealKintaroRoundWins=prior['currentRealKintaroRoundWins']+1,currentRealKintaroMatchClears=0,
  currentPreparedBossNativeRoundWins=wins,
  currentBossReleaseInterruptAnalysis=str(interrupted_path),currentPreparedBossIncomingDamageAnalysis=str(incoming_path),
  currentPreparedBossConclusion='Preparation fixes almost all requested HP dispatches in these test runs without a game patch. Native incoming damage concentrates at ownaction0000/CPU0507 close sequences and guard chip; native107activation alone is not a full boss match clear. Test fresh ready-crouch follow-ups through real recovery with the unchanged native boss.',
  gameSourceAndPlayableBytesChangedThisTurn=False,nativeDifficultyHealthAIPositionStageRNGModified=False,
  obsoleteFoldersDeletedThisTurn=False,foldersDeletedThisTurn=[],newCaptureLeavesNTFSCompressed=True,
  actualFullLadderClearAccepted=False,actualEndingsAccepted=False,finishedRelease=False,fullPortAcceptance=False,
  nextAction='Complete the live ready-crouch30/60 cold input-only campaigns and strict native gate checks; do not assume a full boss match/ending from any round. Continue full move-phase art/grounding/floor-shadow/audio arena/CPU/repeated/KO/overlap scope, all remaining finishers/victims/morphs/secrets/cinematics, final combinedUI regression, dependency-aware obsolete-folder cleanup and refreshed release. No proxy or weakened acceptance.',
  inputHashes=pins,goalStatus='active')
 assert len(prior['remaining'])>=5 and prior['currentRealKintaroRoundWins']==3
 return prior

if __name__=='__main__':
 assert not OUT.exists(),'Immutable full-scope checkpoint'
 result=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(goalStatus='active',newBossCampaigns=4,actualHuman107Assignments=429,newNativeBossDamage=7391,
  newKintaroRoundWins=1,actualFullBossMatchClears=0,specificNewCounterexamples=64,gameBytesChanged=False,
  finishedRelease=False,fullPortAcceptance=False),indent=2),flush=True)
