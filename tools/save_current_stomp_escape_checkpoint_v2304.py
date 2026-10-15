"""Carry full port scope while recording current real-input stomp/escape evidence."""
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_current_stomp_window_boss_ledger_v2288 as old
import verify_current_escape_hold_boss_ledger_v2298 as held
launch=old.launch;ROOT=old.ROOT
PREVIOUS=ROOT/'audit_v2280_current_ready_crouch_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2305_current_stomp_escape_checkpoint'

def save():
 prior=json.loads(PREVIOUS.read_text())
 assert prior['goalStatus']=='active' and not prior['fullPortAcceptance']
 pins=dict(prior['inputHashes'])
 with ThreadPoolExecutor(max_workers=4) as pool:
  for (file,wanted),actual in zip(pins.items(),pool.map(launch.sha,pins)):
   assert wanted==actual,'Changed carried dependency '+file
 def pin(path,wanted=None):
  path=str(Path(path).resolve());actual=launch.sha(path)
  assert wanted is None or actual==wanted,'Changed actual dependency '+path
  assert path not in pins or pins[path]==actual,'Inconsistent evidence dependency '+path
  pins[path]=actual
 def accept(path):
  path=Path(path);result=json.loads(path.read_text())
  assert result['passed'] and result['fullPortAcceptance'] is False
  for file,wanted in result['inputHashes'].items():
   if file in pins:assert pins[file]==wanted,'Conflicting evidence graph '+file
   else:pin(file,wanted)
  pin(path);return result
 pin(PREVIOUS);pin(__file__)
 analysis_path=ROOT/'audit_v2303_current_native_boss_jump_windows/report.json'
 analysis=accept(analysis_path)
 assert not analysis['gameOrCaptureModified']
 guest=old.native.current_source.expected()[0]
 new_cases={}
 for module,version in ((old,2299),(held,2300)):
  for case,(fighter,side,capture,positive) in module.CASES.items():
   positive_path=ROOT/positive/'report.json';proof=accept(positive_path)
   ledger_path=ROOT/f'audit_v{version}_current_{case}_boss_ledger_checked/report.json';book=accept(ledger_path)
   negative_path=ROOT/f'audit_v2301_current_{case}_input_counterexamples/report.json';negative=accept(negative_path)
   assert proof['bounded_campaign_evidence_proven'] and not proof['unassisted_clear_proven']
   assert book['finalUnmodifiedControlPassed'] and book['rejectedSpecificCounterexamples']==8
   expected_neg=8 if case.endswith('window_guard') else 11 if module is old else 12
   assert negative['finalUnmodifiedFullCampaignControlPassed'] and negative['rejectedSpecificCounterexamples']==expected_neg
   assert book['originalHuman107Assignments']==proof['actualNativeUppercutAssignments']
   assert book['ownBossRoundWins']==proof['actualBossRoundWins']
   assert book['ownBossUppercutDamage']==proof['actualBossUppercutDamage']
   assert (ROOT/capture/'guest_maincpu.bin').read_bytes()==guest,'Whole actual guest equals current independently reconstructed source'
   native=analysis['cases'][case]
   new_cases[case]=dict(campaignReport=str(positive_path),ledgerReport=str(ledger_path),
    inputCounterexampleReport=str(negative_path),capture=str(ROOT/capture),stagesReached=proof['stages_reached'],
    actualNativeHuman107Assignments=book['originalHuman107Assignments'],ownBossRoundWins=book['ownBossRoundWins'],
    ownBossUppercutDamage=book['ownBossUppercutDamage'],adjacentNativeBossFieldPairs=book['positiveHealthAdjacentBossFieldPairs'],
    physicalStompPlans=proof['physicalStompPlans'],physicalJumpkickPlans=proof['physicalJumpkickPlans'],
    actualHuman308Jumps=native['actualHuman308Jumps'],actualHuman200AirKicks=native['actualHuman200AirKicks'],
    actualOwnedBossDamage=native['actualOwnedBossDamage'],actualQuietWindowIncomingDamage=native['actualQuietWindowIncomingDamage'],
    rejectedSpecificLedgerCounterexamples=8,rejectedSpecificInputCounterexamples=expected_neg,
    fullCampaignClear=False,endingAccepted=False)
 assert sum(c['actualNativeHuman107Assignments'] for c in new_cases.values())==656
 assert sum(c['ownBossUppercutDamage'] for c in new_cases.values())==13119
 assert sum(c['ownBossRoundWins'] for c in new_cases.values())==1
 assert sum(c['rejectedSpecificInputCounterexamples'] for c in new_cases.values())==86
 failures={}
 for fighter in ('kano','sonya'):
  path=ROOT/f'audit_v2287_current_{fighter}_p1_window_escape_checked/report.json'
  failed=json.loads(path.read_text())
  assert not failed['passed'] and failed['errors']==['Every actual stomp-window crouch/HP/jumpkick/guard input equals independently replayed native state and height policy']
  pin(path);failures[fighter]=str(path)
 for name in ('tools/verify_current_boss_stomp_window_campaign_v2285.py','tools/diagnose_current_stomp_input_replay_v2294.py'):
  pin(ROOT/name)
 for name in ('mk2ks_natural_campaign_boss_active_escape_v2306.lua','tools/run_current_boss_active_escape_campaign_v2307.ps1','tools/verify_current_boss_active_escape_campaign_v2308.py'):
  pin(ROOT/name)
 expected={
  ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
  ROOT/'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata':'5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'}
 for path,wanted in expected.items():pin(path,wanted)
 launch.module_pins(pins)
 cases=dict(prior['currentSourceBoundBossCampaigns'])
 assert not set(cases)&set(new_cases);cases.update(new_cases)
 prior.update(previousCheckpoint=str(PREVIOUS),
  previousGoalTurnClassification='no progress: status-only answer inspected current reports but changed no authoritative state or next action; pending handles revalidated on continuation',
  thisGoalTurnClassification='progress: eight current-build cold physical-input campaigns and full native ledgers accepted,656 actual human107 assignments,13119 uppercut damage,one additional true Kano Kintaro round,64 native ledger and86 physical-input counterexamples; actual jump/air-kick dispatch and opening guard damage independently inventoried',
  currentSourceBoundBossCampaigns=cases,currentFreshStompEscapeBossCampaigns=new_cases,
  currentActualBossHuman107Assignments=sum(c['actualNativeHuman107Assignments'] for c in cases.values()),
  currentActualBossUppercutDamage=sum(c['ownBossUppercutDamage'] for c in cases.values()),
  currentBossLedgerCounterexamples=sum(c['rejectedSpecificLedgerCounterexamples'] for c in cases.values()),
  currentBossPhysicalInputCounterexamples=sum(c.get('rejectedSpecificInputCounterexamples',0) for c in cases.values()),
  currentRealKintaroRoundWins=prior['currentRealKintaroRoundWins']+1,
  currentNativeBossJumpWindowsReport=str(analysis_path),
  currentEscapeHoldNativeJumps=sum(c['actualHuman308Jumps'] for name,c in new_cases.items() if 'escape_hold' in name),
  currentEscapeHoldNativeAirKicks=sum(c['actualHuman200AirKicks'] for name,c in new_cases.items() if 'escape_hold' in name),
  preservedStompEscapeVerifierFailures=failures,
  stompEscapeHarnessCorrection='Old escape inputs sent Down and Up together on the first field and held Up only four fields.2295 verifies what was actually sent without promoting intent to a jump.2289 removes conflicting Down and holds Up sixteen fields; native308jump and200airkick entry stores are separately counted by2302, never inferred from airborne hurt states. No game-code fix is claimed from this driver correction.',
  gameSourceAndPlayableBytesChangedThisTurn=False,nativeDifficultyHealthAIPositionStageRNGModified=False,
  obsoleteFoldersDeletedThisTurn=False,foldersDeletedThisTurn=[],newCaptureLeavesNTFSCompressed=True,
  actualFullLadderClearAccepted=False,actualEndingsAccepted=False,finishedRelease=False,fullPortAcceptance=False,
  pendingActiveEscapeCampaigns=[f'audit_v2309_current_{fighter}_p1_escape_active_{spacing}_campaign' for fighter in ('kano','sonya') for spacing in ('close','early')],
  pendingActiveEscapeAccepted=False,
  nextAction='Finish and independently verify the four already-dispatched2309cold campaigns on their existing handles.2306removes only the test driver opening guard-only delay, which2302measured at roughly30incoming HP per positive-health boss segment. Compare native actual jumps, uppercuts, owned damage, real wins and full source/progression/ending gates. No native health, difficulty, AI, stage, RNG or positions changed. Keep the complete original remaining scope, including every move/arena grounding-shadow-art-audio, finishers/victims/morphs/secrets/cinematics, actual boss matches/endings, final UI regression, dependency-aware cleanup and refreshed release.',
  inputHashes=pins,goalStatus='active')
 assert prior['currentRealKintaroMatchClears']==prior['currentRealShaoKahnMatchClears']==0
 assert len(prior['remaining'])>=5 and prior['currentRealKintaroRoundWins']==4
 return prior

if __name__=='__main__':
 assert not OUT.exists(),'Immutable full-scope checkpoint'
 result=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(goalStatus='active',newCampaigns=8,newHuman107Assignments=656,newUppercutDamage=13119,
  newKintaroRoundWins=1,newSpecificCounterexamples=150,fullBossMatchClears=0,gameBytesChanged=False,
  finishedRelease=False,fullPortAcceptance=False),indent=2),flush=True)
