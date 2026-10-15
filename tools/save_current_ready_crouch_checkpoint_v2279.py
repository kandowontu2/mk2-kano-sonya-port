"""Preserve full scope while accepting actual ready-crouch controls and geometry."""
import json
from concurrent.futures import ThreadPoolExecutor
from itertools import zip_longest
from pathlib import Path
import verify_current_ready_crouch_boss_ledger_v2274 as ledger
launch=ledger.launch;ROOT=ledger.ROOT
PREVIOUS=ROOT/'audit_v2272_current_prepared_boss_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2280_current_ready_crouch_checkpoint'

def save():
 prior=json.loads(PREVIOUS.read_text());assert prior['goalStatus']=='active'and prior['fullPortAcceptance']is False
 pins=dict(prior['inputHashes'])
 # Rehash every carried dependency; parallel reads change no evidence contract.
 with ThreadPoolExecutor(max_workers=4)as pool:
  for(file,wanted),actual in zip(pins.items(),pool.map(launch.sha,pins)):
   assert actual==wanted,'Changed carried source/capture '+file
 def pin(path,wanted=None):
  path=str(Path(path).resolve());actual=launch.sha(path)
  assert wanted is None or actual==wanted,'Changed actual dependency '+path
  assert path not in pins or pins[path]==actual,'Conflicting dependency '+path
  pins[path]=actual
 def accept(path):
  path=Path(path);r=json.loads(path.read_text());assert r['passed']and r['fullPortAcceptance']is False
  for file,wanted in r['inputHashes'].items():
   if file in pins:assert pins[file]==wanted,'Conflicting accepted graph '+file
   else:pin(file,wanted)
  pin(path);return r
 pin(PREVIOUS);pin(__file__)
 height_path=ROOT/'audit_v2277_current_boss_height_windows/report.json';height=accept(height_path)
 geometry_path=ROOT/'audit_v2282_current_actual_boss_hp_geometry/report.json';geometry=accept(geometry_path)
 assert not height['gameOrCaptureModified']and not geometry['gameOrCaptureModified']
 assert sum(c['actualHuman107Assignments']for c in height['cases'].values())==929
 assert all(not c['unmappedNative107Frames']for c in height['cases'].values())
 new_cases={};reports={}
 for case,(fighter,side,capture,positive)in ledger.CASES.items():
  campaign_path=ROOT/positive/'report.json';proof=accept(campaign_path);reports[case]=proof
  ledger_path=ROOT/f'audit_v2276_current_{case}_boss_ledger_checked/report.json';actual=accept(ledger_path)
  negative_path=ROOT/f'audit_v2278_current_{case}_input_counterexamples/report.json';negative=accept(negative_path)
  assert proof['bounded_campaign_evidence_proven']and not proof['unassisted_clear_proven']
  assert actual['finalUnmodifiedControlPassed']and actual['rejectedSpecificCounterexamples']==8
  assert negative['finalUnmodifiedFullCampaignControlPassed']and negative['rejectedSpecificCounterexamples']==8
  assert actual['originalHuman107Assignments']==proof['actualNativeUppercutAssignments']
  assert actual['ownBossRoundWins']==proof['actualBossRoundWins']==0
  assert actual['ownBossUppercutDamage']==proof['actualBossUppercutDamage']
  assert (ROOT/capture/'guest_maincpu.bin').read_bytes()==ledger.native.current_source.expected()[0]
  new_cases[case]=dict(campaignReport=str(campaign_path),ledgerReport=str(ledger_path),capture=str(ROOT/capture),
   inputCounterexampleReport=str(negative_path),stagesReached=proof['stages_reached'],
   actualNativeHuman107Assignments=actual['originalHuman107Assignments'],ownBossRoundWins=0,
   ownBossUppercutDamage=actual['ownBossUppercutDamage'],adjacentNativeBossFieldPairs=actual['positiveHealthAdjacentBossFieldPairs'],
   physicalPlans=proof['physicalBossPlans'],nativeHPDispatches=proof['nativeBossHPDispatches'],
   nativeUppercutEntryFetches=proof['nativeHumanUppercutEntryFetches'],
   rejectedSpecificLedgerCounterexamples=8,rejectedSpecificInputCounterexamples=8,fullCampaignClear=False,endingAccepted=False)
 assert sum(r['actualNativeHuman107Assignments']for r in new_cases.values())==500
 assert sum(r['physicalPlans']for r in new_cases.values())==524
 assert sum(r['ownBossUppercutDamage']for r in new_cases.values())==3120
 equivalence={}
 def native_lines(path,policy):
  with path.open(encoding='utf-8-sig')as stream:
   for line in stream:
    if line.startswith('MK2_NAT_CAMPAIGN_'):yield line.replace('policy='+policy,'policy=ready_crouch').rstrip('\r\n')
 for fighter in('kano','sonya'):
  one=fighter+'_ready_crouch30';two=fighter+'_ready_crouch60'
  a=ROOT/ledger.CASES[one][2];b=ROOT/ledger.CASES[two][2];count=0
  for left,right in zip_longest(native_lines(a/'run.log','ready_crouch30'),native_lines(b/'run.log','ready_crouch60')):
   assert left is not None and left==right,'Different actual native chronology beyond declared cooldown '+fighter
   count+=1
  assert count>100000,'Non-vacuous full actual native record comparison'
  assert launch.sha(a/'native_mix.wav')==launch.sha(b/'native_mix.wav')
  equivalence[fighter]=dict(equalNativeRecords=count,normalization='Declared policy label only; no frames/buttons/state/register/health/win data removed',
   nativePCMSHA256=launch.sha(a/'native_mix.wav'),scope='Exact independent control equivalence, not universal audio approval')
 descending={case:c['groups'].get('cpu_0407_161_240_descending',{})for case,c in geometry['cases'].items()if case.endswith(('prep_stomp','prep_stance'))}
 assert sum(g.get('plans',0)for g in descending.values())==312
 assert sum(g.get('ownedHitPlans',0)for g in descending.values())==310
 for name in('tools/verify_current_boss_ready_crouch_campaign_v2263.py','tools/verify_current_boss_ready_crouch_campaign_v2266.py','tools/run_current_boss_ready_crouch_campaign_v2262.ps1'):
  pin(ROOT/name)
 expected={
  ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
  ROOT/'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata':'5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'}
 for path,wanted in expected.items():pin(path,wanted)
 launch.module_pins(pins)
 cases=dict(prior['currentSourceBoundBossCampaigns']);assert not set(cases)&set(new_cases);cases.update(new_cases)
 prior.update(previousCheckpoint=str(PREVIOUS),
  previousGoalTurnClassification='progress: prepared physical commands proved429native107assignments,7391bossdamage, one realSonyaKintaro round and64specific negative checks. Actual incoming damage analysis selected the ready-crouch control.',
  thisGoalTurnClassification='progress: four2640second current-build cold ready-crouch campaigns pass full source/true-ID/progression gates,500native107assignments,3120owned damage, complete adjacent ledgers and64specific counterexamples. Both cooldown controls have exact full native chronology andPCM. Actual physically pressed HP geometry narrows successful stomp counters to the descending161-240height window (310of312prepared attempts hit), not rising/held-height windows. No boss match orending yet.',
  currentSourceBoundBossCampaigns=cases,currentFreshReadyCrouchBossCampaigns=new_cases,
  currentActualBossHuman107Assignments=sum(r['actualNativeHuman107Assignments']for r in cases.values()),
  currentActualBossUppercutDamage=sum(r['ownBossUppercutDamage']for r in cases.values()),
  currentBossLedgerCounterexamples=sum(r['rejectedSpecificLedgerCounterexamples']for r in cases.values()),
  currentBossPhysicalInputCounterexamples=sum(r.get('rejectedSpecificInputCounterexamples',0)for r in cases.values()),
  currentReadyCrouchFullControlEquivalence=equivalence,currentBossRequestedHPHeightWindows=str(height_path),
  currentBossActualPressedHPGeometry=str(geometry_path),currentPreparedDescendingStompGroups=descending,
  diagnosticReadyHarnessCorrections=dict(
   sourceDispatch2263='Restoration helper alone was exercised; actual main dispatch had a duplicate ready branch and omitted the new input replay. Never used for an accepted campaign; corrected dispatch2266and runner binding2268.',
   runner2262='Wrong prepared_crouch_v2261filename rejected all four preflights before starting MAME. Empty audit_v2264leaves preserved, not accepted as played campaigns.2267uses the actualreadydriver.',
   acceptedVerifier='tools/verify_current_boss_ready_crouch_campaign_v2268.py',acceptedRunner='tools/run_current_boss_ready_crouch_campaign_v2267.ps1'),
  gameSourceAndPlayableBytesChangedThisTurn=False,nativeDifficultyHealthAIPositionStageRNGModified=False,
  obsoleteFoldersDeletedThisTurn=False,foldersDeletedThisTurn=[],newCaptureLeavesNTFSCompressed=True,
  actualFullLadderClearAccepted=False,actualEndingsAccepted=False,finishedRelease=False,fullPortAcceptance=False,
  nextAction='Use actual CPUheight direction, not merely CPU0407or own readiness, to request a fresh native HP edge while the boss descends through161-240height; the existing310of312hit geometry is evidence for timing, not a new test result. Combine physical spacing/jump defense against close grabs and prove actualKintaro/ShaoKahn matches, own endings/attract. Keep unchanged full move-phase grounding/shadow/art/audio arena/CPU/repeated/KO/overlap, other finishers/victims/morphs/secrets/cinematics, final combinedUI regression, dependency-aware obsolete-folder cleanup and refreshed release scope.',
  inputHashes=pins,goalStatus='active')
 assert len(prior['remaining'])>=5 and prior['currentRealKintaroRoundWins']==3 and prior['currentRealKintaroMatchClears']==0
 return prior

if __name__=='__main__':
 assert not OUT.exists(),'Immutable full-scope checkpoint'
 result=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(goalStatus='active',newReadyCrouchCampaigns=4,actualHuman107Assignments=500,
  newNativeBossDamage=3120,newBossRoundWins=0,actualFullBossMatchClears=0,specificNewCounterexamples=64,
  preparedDescendingStompHitPlans=310,preparedDescendingStompPlans=312,
  exactNativeControlEquivalence=result['currentReadyCrouchFullControlEquivalence'],gameBytesChanged=False,
  finishedRelease=False,fullPortAcceptance=False),indent=2),flush=True)
