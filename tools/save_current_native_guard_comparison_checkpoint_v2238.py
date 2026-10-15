"""Carry full scope while recording actual stock/custom guard timing progress."""
import json
from pathlib import Path
import verify_current_interrupt_v1870 as launch
import verify_current_boss_guard_edge_ledger_v2227 as ledger
ROOT=launch.ROOT
PREVIOUS=ROOT/'audit_v2211_current_boss_guard_transition_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2239_current_native_guard_comparison_checkpoint'

def save():
 prior=json.loads(PREVIOUS.read_text());assert prior['goalStatus']=='active'and prior['fullPortAcceptance']is False
 pins=dict(prior['inputHashes'])
 for file,wanted in pins.items():assert launch.sha(file)==wanted,'Changed carried source/capture evidence '+file
 def pin(path,wanted=None):
  path=str(Path(path).resolve());actual=launch.sha(path)
  assert wanted is None or actual==wanted,'Changed actual new dependency '+path
  assert path not in pins or pins[path]==actual,'Conflicting dependency '+path
  pins[path]=actual
 def accept(path):
  path=Path(path);r=json.loads(path.read_text());assert r['passed']and r['fullPortAcceptance']is False
  for file,wanted in r['inputHashes'].items():
   if file in pins:assert pins[file]==wanted,'Conflicting accepted actual graph '+file
   else:pin(file,wanted)
  pin(path);return r
 pin(PREVIOUS);pin(__file__)
 matrix_path=ROOT/'audit_v2230_current_native_guard_transition_matrix/report.json';matrix=accept(matrix_path)
 assert matrix['acceptedActualUppercuts']==24 and matrix['acceptedNativeNoActivationDiagnostics']==8
 assert matrix['specificCounterexamplesRejected']==12 and matrix['originalGuardCrouchHPRouteUnchanged']
 phase_path=ROOT/'audit_v2245_current_boss_guard_phase/report.json';phase=accept(phase_path)
 assert phase['gameOrCaptureModified']is False
 assert sum(r['actual107Assignments']for r in phase['cases'].values())==132
 assert all(not r['unmappedNative107Frames']for r in phase['cases'].values())
 pin(ROOT/'tools/analyze_current_boss_guard_phase_v2242.py')
 new_cases={}
 for case,(fighter,side,capture,positive)in ledger.CASES.items():
  path=ROOT/positive/'report.json';proof=accept(path)
  ledger_path=ROOT/f'audit_v2235_current_{case}_boss_ledger_checked/report.json';actual=accept(ledger_path)
  negative_path=ROOT/f'audit_v2237_current_{case}_input_counterexamples/report.json';negative=accept(negative_path)
  assert proof['bounded_campaign_evidence_proven']and not proof['unassisted_clear_proven']
  assert actual['finalUnmodifiedControlPassed']and actual['rejectedSpecificCounterexamples']==8
  assert negative['finalUnmodifiedFullCampaignControlPassed']and negative['rejectedSpecificCounterexamples']==4
  assert actual['originalHuman107Assignments']==proof['actualNativeUppercutAssignments']
  assert actual['ownBossRoundWins']==proof['actualBossRoundWins']==0
  assert actual['ownBossUppercutDamage']==proof['actualBossUppercutDamage']
  new_cases[case]=dict(campaignReport=str(path),ledgerReport=str(ledger_path),capture=str(ROOT/capture),
   inputCounterexampleReport=str(negative_path),stagesReached=proof['stages_reached'],
   actualNativeHuman107Assignments=actual['originalHuman107Assignments'],
   ownBossRoundWins=0,ownBossUppercutDamage=actual['ownBossUppercutDamage'],
   adjacentNativeBossFieldPairs=actual['positiveHealthAdjacentBossFieldPairs'],
   rejectedSpecificLedgerCounterexamples=8,rejectedSpecificInputCounterexamples=4,
   fullCampaignClear=False,endingAccepted=False)
 truncated_path=ROOT/'audit_v2226_current_kano_p1_guard_edge16_checked/report.json'
 truncated=json.loads(truncated_path.read_text());assert not truncated['passed']
 assert truncated['errors']==['Own true ID before native confirm']
 for file,wanted in truncated['inputHashes'].items():
  if file in pins:assert pins[file]==wanted
  else:pin(file,wanted)
 pin(truncated_path)
 # Never use this unexecuted defective prefix implementation as proof.
 pin(ROOT/'tools/verify_current_boss_guard_edge_extended_v2232.py')
 pin(ROOT/'tools/verify_current_boss_guard_edge_extended_v2240.py')
 expected={
  ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
  ROOT/'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata':'5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'}
 for path,wanted in expected.items():pin(path,wanted)
 launch.module_pins(pins)
 cases=dict(prior['currentSourceBoundBossCampaigns']);assert not set(cases)&set(new_cases);cases.update(new_cases)
 prior.update(previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification='progress: prior eight boss controls and complete native ledgers narrowed the unresolved post-guard activation question; saved2211source graph remains unchanged.',
  thisGoalTurnClassification='progress:32cold true-ID native/custom two-human guard comparisons,24actual40damage/recovery/follow-up uppercuts and8genuine early-command failures establish native ten-field guard transition; later freshHPworks forKano/Sonya andstockLiu/SubZero inbothslots. Fourbossedge campaigns tested corrected physical timing with complete native ledgers/48specific counterexamples; truncated selection capture replaced with an extended cold run under unchanged strict gates and a non-vacuous whole-trajectory prefix check.',
  currentGuardComparisonReport=str(matrix_path),currentGuardComparisonCases=matrix['cases'],
  currentGuardComparisonActualUppercuts=24,currentGuardComparisonNoActivationDiagnostics=8,
  currentGuardComparisonSpecificCounterexamples=12,
  currentGuardComparisonConclusion=matrix['conclusion'],
  currentActualBossGuardPhaseReport=str(phase_path),currentActualBossGuardPhaseGroups={case:r['groups']for case,r in phase['cases'].items()},
  currentSourceBoundBossCampaigns=cases,currentFreshGuardEdgeBossCampaigns=new_cases,
  currentActualBossHuman107Assignments=sum(r['actualNativeHuman107Assignments']for r in cases.values()),
  currentActualBossUppercutDamage=sum(r['ownBossUppercutDamage']for r in cases.values()),
  currentBossLedgerCounterexamples=sum(r['rejectedSpecificLedgerCounterexamples']for r in cases.values()),
  currentBossPhysicalInputCounterexamples=sum(r.get('rejectedSpecificInputCounterexamples',0)for r in cases.values()),
  diagnosticTruncatedGuardEdgeCapture=dict(report=str(truncated_path),accepted=False,
   reason='The2600second timer ended50fields after the final continue CSS started, before scheduled Left at56and required130/146preconfirm samples. Earlier37selections have both true-ID samples. This is incomplete terminal evidence, not a waived true-ID gate or proof of a game selection defect.',
   replacement=str(ROOT/'audit_v2234_current_kano_p1_guard_edge16_extended_checked/report.json')),
  supersededUnexecutedPrefixCheck=dict(source=str(ROOT/'tools/verify_current_boss_guard_edge_extended_v2232.py'),accepted=False,
   reason='Overescaped numeric prefix regex would have produced a vacuous empty comparison.2240requires correctly parsed inventories exceeding10000native rows and full identical prior trajectory. No verification report was accepted using2232.'),
  gameSourceAndPlayableBytesChangedThisTurn=False,nativeDifficultyHealthAIPositionStageRNGModified=False,
  obsoleteFoldersDeletedThisTurn=False,foldersDeletedThisTurn=[],newCaptureLeavesNTFSCompressed=True,
  actualFullLadderClearAccepted=False,actualEndingsAccepted=False,finishedRelease=False,fullPortAcceptance=False,
  nextAction='The32cold native comparisons resolve the early post-guard HP input-phase issue without a game patch.132boss107assignments map uniquely to real command windows; both standing700andcrouch701plans sometimes activate, so excluding either action is not supported. Compare actual incoming health/action transitions during the12/16field guard-release lead and native handler/HP-edge dispatch to identify interrupted versus phase-lost commands; improve physical defense/movement and prove fullKintaro/ShaoKahn campaigns and own endings/attract. Continue unchanged full move-phase grounding/shadow/art/audio arena/CPU/repeated/KO/overlap scope, other finishers/victims/morphs/secrets/cinematics, final combinedUI regression, dependency-aware cleanup and refreshed release. These bounded ordinary transitions do not complete the port.',
  inputHashes=pins,goalStatus='active')
 assert len(prior['remaining'])>=5 and prior['currentRealKintaroRoundWins']==2
 return prior

if __name__=='__main__':
 assert not OUT.exists(),'Immutable checkpoint'
 report=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(goalStatus='active',nativeGuardComparisonCases=32,acceptedActualUppercuts=24,
  observedEarlyCommandFailures=8,nativeComparisonCounterexamples=12,newBossCampaigns=4,
  newBossLedgerAndInputCounterexamples=48,actualFullBossMatchClears=0,
  gameBytesChanged=False,finishedRelease=False,fullPortAcceptance=False),indent=2),flush=True)
