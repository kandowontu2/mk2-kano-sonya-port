"""Preserve native boss timing evidence without claiming a completed port."""
import json
from pathlib import Path
import verify_current_boss_action_health_ledger_v2184 as older
import verify_current_guarded_boss_ledger_v2196 as guarded
import verify_current_guarded_commit_ledger_v2204 as commit
import verify_current_interrupt_v1870 as launch
ROOT=launch.ROOT
PREVIOUS=ROOT/'audit_v2173_current_uppercut_render_shadow_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2211_current_boss_guard_transition_checkpoint'

def save():
 prior=json.loads(PREVIOUS.read_text());assert prior['goalStatus']=='active'and not prior['fullPortAcceptance']
 pins=dict(prior['inputHashes'])
 # Revalidate the whole carried source/capture graph, not the manifest alone.
 for file,wanted in pins.items():assert launch.sha(file)==wanted,'Changed carried evidence '+file
 def pin(path,wanted=None):
  path=str(Path(path).resolve());actual=launch.sha(path)
  assert wanted is None or actual==wanted,'Changed new dependency '+path
  assert path not in pins or pins[path]==actual,'Conflicting dependency '+path
  pins[path]=actual
 def accept(path):
  path=Path(path);r=json.loads(path.read_text());assert r['passed']and r['fullPortAcceptance']is False
  for file,wanted in r['inputHashes'].items():
   if file in pins:assert pins[file]==wanted,'Conflicting accepted evidence '+file
   else:pin(file,wanted)
  pin(path);return r
 pin(PREVIOUS);pin(__file__);cases={}
 sets=[(older,2185),(guarded,2198),(commit,2206)]
 for module,version in sets:
  for case,(fighter,side,capture,positive)in module.CASES.items():
   path=ROOT/positive/'report.json';proof=accept(path)
   ledger_path=ROOT/f'audit_v{version}_current_{case}_boss_ledger_checked/report.json';actual=accept(ledger_path)
   assert proof['bounded_campaign_evidence_proven']and not proof['unassisted_clear_proven']
   assert actual['finalUnmodifiedControlPassed']and not actual['fullLadderClearAccepted']
   assert proof['actualNativeUppercutAssignments']==actual['originalHuman107Assignments']
   assert proof['actualBossRoundWins']==actual['ownBossRoundWins']
   row=dict(campaignReport=str(path),ledgerReport=str(ledger_path),capture=str(ROOT/capture),
    stagesReached=proof['stages_reached'],actualNativeHuman107Assignments=actual['originalHuman107Assignments'],
    ownBossRoundWins=actual['ownBossRoundWins'],ownBossUppercutDamage=actual['ownBossUppercutDamage'],
    adjacentNativeBossFieldPairs=actual['positiveHealthAdjacentBossFieldPairs'],
    rejectedSpecificLedgerCounterexamples=actual['rejectedSpecificCounterexamples'],
    fullCampaignClear=False,endingAccepted=False)
   if version!=2185:
    negative_path=ROOT/f'audit_v2208_current_{case}_input_counterexamples/report.json';negative=accept(negative_path)
    assert negative['rejectedSpecificCounterexamples']==4 and negative['finalUnmodifiedFullCampaignControlPassed']
    assert negative['captureModified']is False
    row.update(inputCounterexampleReport=str(negative_path),rejectedSpecificInputCounterexamples=4)
   cases[case]=row
 windows_path=ROOT/'audit_v2187_current_boss_uppercut_windows/report.json';windows=accept(windows_path)
 incoming_path=ROOT/'audit_v2191_current_boss_incoming/report.json';incoming=accept(incoming_path)
 assert windows['gameOrCaptureModified']is False and incoming['gameOrCaptureModified']is False
 # These are observed hit windows, not CPU-height heuristics or intention labels.
 assert windows['cases']['kano_held']['hitWindows']==118 and windows['cases']['sonya_held']['hitWindows']==93
 assert windows['cases']['kano_native']['hitWindows']==24 and windows['cases']['sonya_native']['hitWindows']==33
 pin(ROOT/'tools/analyze_current_boss_incoming_v2188.py')
 expected={
  ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
  ROOT/'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata':'5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'}
 for path,wanted in expected.items():pin(path,wanted)
 launch.module_pins(pins)
 assert sum(r['ownBossRoundWins']for r in cases.values())==2
 assert sum(r['actualNativeHuman107Assignments']for r in cases.values())==499
 assert sum(r['ownBossUppercutDamage']for r in cases.values())==5672
 prior.update(previousCheckpoint=str(PREVIOUS),
  previousGoalTurnClassification='no progress: status-only response. Current saved reports/source graph and terminal runs were revalidated before continuing the next safe action.',
  thisGoalTurnClassification='progress: actual human107 hit/incoming timing analysis changed the next action; eight new real-input boss campaigns tested guard and unblocked-commit alternatives, complete native ledgers and specific physical-input corruptions independently checked. Both alternatives perform worse than the prior held-crouch controls and are not promoted as gameplay fixes.',
  currentSourceBoundBossCampaigns=cases,
  currentActualBossHuman107Assignments=499,currentActualBossUppercutDamage=5672,
  currentRealKintaroRoundWins=2,currentRealKintaroMatchClears=0,currentRealShaoKahnMatchClears=0,
  currentBossLedgerCounterexamples=sum(r['rejectedSpecificLedgerCounterexamples']for r in cases.values()),
  currentBossPhysicalInputCounterexamples=sum(r.get('rejectedSpecificInputCounterexamples',0)for r in cases.values()),
  currentBossUppercutWindowsReport=str(windows_path),currentBossIncomingTimingReport=str(incoming_path),
  bossTimingConclusion='Prior held-crouch delayed commands yielded118/120Kano and93/95Sonya hit windows; immediate crouch punches yielded24/97 and33/140. Much actual incoming damage occurs outside the own107window. New guarded/guarded-commit physical alternatives activate few107moves and win no boss rounds, so neither is accepted as an improvement. Action302/grounded/body masks alone do not establish that a post-guard attack command will be accepted. A longer unblocked commitment did not solve it. No missing portrait/shadow/gameplay defect is inferred from controller failure.',
  supersededIncomingOwnershipAssumption=dict(source=str(ROOT/'tools/analyze_current_boss_incoming_v2188.py'),
   accepted=False,reason='Requiring every incoming original collision writer to carry CPU actor/Main registers was false for other original damage contexts.2190/2191keeps exact physical health-slot/writer provenance and records actual A8/A13 without falsely identifying projectile/child registers as Main.'),
  gameSourceAndPlayableBytesChangedThisTurn=False,nativeDifficultyHealthAIPositionStageRNGModified=False,
  obsoleteFoldersDeletedThisTurn=False,foldersDeletedThisTurn=[],newCaptureLeavesNTFSCompressed=True,
  actualFullLadderClearAccepted=False,actualEndingsAccepted=False,finishedRelease=False,fullPortAcceptance=False,
  nextAction='Use cold real two-human selections to compare post-low-guard uppercut input acceptance/recovery against an original native fighter, with read-only native dispatch/continuation/actualHP-edge observers. Separate controller-state/phase errors from a genuine port defect before another boss policy or game patch. Then prove both actual fullKintaro/ShaoKahn campaigns, own endings/attract and the unchanged broader move-phase grounding/shadows across arenas, CPU/repeated/KO/overlap, all remaining finishers/victims/morphs/secrets/cinematics/audio; final combinedUI regression, dependency-aware cleanup and refreshed release.',
  inputHashes=pins,goalStatus='active')
 assert len(prior['remaining'])>=5
 return prior

if __name__=='__main__':
 assert not OUT.exists(),'Immutable checkpoint'
 report=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(goalStatus='active',campaigns=len(report['currentSourceBoundBossCampaigns']),
  actualHuman107Assignments=499,actualKintaroRoundWins=2,actualFullBossMatchClears=0,
  ledgerCounterexamples=report['currentBossLedgerCounterexamples'],
  physicalInputCounterexamples=report['currentBossPhysicalInputCounterexamples'],
  gameBytesChanged=False,finishedRelease=False,fullPortAcceptance=False),indent=2),flush=True)
