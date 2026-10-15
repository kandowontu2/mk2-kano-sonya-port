"""Save verified current active escape controls without narrowing port acceptance."""
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_current_active_escape_boss_ledger_v2318 as ledger
launch=ledger.launch;ROOT=ledger.ROOT
PREVIOUS=ROOT/'audit_v2305_current_stomp_escape_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2327_current_active_escape_checkpoint'

def save():
 prior=json.loads(PREVIOUS.read_text())
 assert prior['goalStatus']=='active' and not prior['fullPortAcceptance']
 pins=dict(prior['inputHashes'])
 with ThreadPoolExecutor(max_workers=4)as pool:
  for (file,wanted),actual in zip(pins.items(),pool.map(launch.sha,pins)):
   assert wanted==actual,'Changed carried dependency '+file
 def pin(path,wanted=None):
  path=str(Path(path).resolve());actual=launch.sha(path)
  assert wanted is None or actual==wanted,'Changed actual dependency '+path
  assert path not in pins or pins[path]==actual,'Conflicting evidence dependency '+path
  pins[path]=actual
 def accept(path):
  path=Path(path);result=json.loads(path.read_text())
  assert result['passed'] and result['fullPortAcceptance']is False
  for file,wanted in result['inputHashes'].items():
   if file in pins:assert pins[file]==wanted,'Inconsistent actual graph '+file
   else:pin(file,wanted)
  pin(path);return result
 pin(PREVIOUS);pin(__file__)
 prefix_path=ROOT/'audit_v2323_current_active_escape_extended_prefix/report.json';prefix=accept(prefix_path)
 analysis_path=ROOT/'audit_v2325_current_active_escape_windows/report.json';analysis=accept(analysis_path)
 assert prefix['completeNativePrefixWithoutNormalization'] and not prefix['identityGateWaived']
 assert prefix['exactOriginalNativeRecords']==163806 and prefix['originalTerminalSelectionAge']==79
 assert prefix['actualExtendedConfirmationFrames']==[98524,98540] and prefix['rejectedSpecificCounterexamples']==3
 assert not analysis['gameOrCaptureModified']
 guest=ledger.native.current_source.expected()[0];new_cases={}
 for case,(fighter,side,capture,positive)in ledger.CASES.items():
  positive_path=ROOT/positive/'report.json';proof=accept(positive_path)
  ledger_path=ROOT/f'audit_v2320_current_{case}_boss_ledger_checked/report.json';book=accept(ledger_path)
  negative_path=ROOT/f'audit_v2321_current_{case}_input_counterexamples/report.json';negative=accept(negative_path)
  assert proof['bounded_campaign_evidence_proven'] and not proof['unassisted_clear_proven']
  assert book['finalUnmodifiedControlPassed'] and book['rejectedSpecificCounterexamples']==8
  assert negative['finalUnmodifiedFullCampaignControlPassed'] and negative['rejectedSpecificCounterexamples']==12
  assert book['originalHuman107Assignments']==proof['actualNativeUppercutAssignments']
  assert book['ownBossUppercutDamage']==proof['actualBossUppercutDamage']
  assert book['ownBossRoundWins']==proof['actualBossRoundWins']==0
  assert (ROOT/capture/'guest_maincpu.bin').read_bytes()==guest,'Whole actual guest exactly matches independently reconstructed current source'
  native=analysis['cases'][case]
  new_cases[case]=dict(campaignReport=str(positive_path),ledgerReport=str(ledger_path),
   inputCounterexampleReport=str(negative_path),capture=str(ROOT/capture),stagesReached=proof['stages_reached'],
   actualNativeHuman107Assignments=book['originalHuman107Assignments'],ownBossUppercutDamage=book['ownBossUppercutDamage'],
   ownBossRoundWins=0,adjacentNativeBossFieldPairs=book['positiveHealthAdjacentBossFieldPairs'],
   physicalStompPlans=proof['physicalStompPlans'],physicalJumpkickPlans=proof['physicalJumpkickPlans'],
   actualHuman308Jumps=native['actualHuman308Jumps'],actualHuman200AirKicks=native['actualHuman200AirKicks'],
   actualOwnedBossDamage=native['actualOwnedBossDamage'],actualFirst120IncomingDamage=native['actualFirst120IncomingDamage'],
   rejectedSpecificLedgerCounterexamples=8,rejectedSpecificInputCounterexamples=12,
   fullCampaignClear=False,endingAccepted=False)
 assert sum(c['actualNativeHuman107Assignments']for c in new_cases.values())==148
 assert sum(c['ownBossUppercutDamage']for c in new_cases.values())==2960
 failed_path=ROOT/'audit_v2310_current_kano_p1_escape_active_early_checked/report.json'
 failed=json.loads(failed_path.read_text());assert not failed['passed'] and failed['errors']==['Own true ID before native confirm']
 pin(failed_path)
 for file in ('tools/verify_current_active_escape_boss_ledger_v2311.py','tools/test_current_active_escape_inputs_v2313.py'):
  pin(ROOT/file) # Preserved syntax-checked predecessors, never accepted for the failed recording.
 expected={
  ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
  ROOT/'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata':'5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'}
 for file,wanted in expected.items():pin(file,wanted)
 launch.module_pins(pins)
 cases=dict(prior['currentSourceBoundBossCampaigns']);assert not set(cases)&set(new_cases);cases.update(new_cases)
 prior.update(previousCheckpoint=str(PREVIOUS),
  previousGoalTurnClassification='no progress: previous user-facing turn was a status-only answer; this continuation revalidated the specific pending handles and completed new real-input evidence',
  thisGoalTurnClassification='progress: pending eight-campaign proof completed and checkpoint2305saved; four fresh active-escape controls completed,148actual native human107assignments and2960uppercut damage verified,80specific ledger/input checks plus3full-prefix counterexamples. Timer-truncated selection preserved; entire163806record native prefix reproduced without normalization and both missing true-ID confirmation fields recorded. No new boss round ormatch/endings.',
  currentSourceBoundBossCampaigns=cases,currentFreshActiveEscapeBossCampaigns=new_cases,
  currentActualBossHuman107Assignments=sum(c['actualNativeHuman107Assignments']for c in cases.values()),
  currentActualBossUppercutDamage=sum(c['ownBossUppercutDamage']for c in cases.values()),
  currentBossLedgerCounterexamples=sum(c['rejectedSpecificLedgerCounterexamples']for c in cases.values()),
  currentBossPhysicalInputCounterexamples=sum(c.get('rejectedSpecificInputCounterexamples',0)for c in cases.values()),
  currentActiveEscapeNativeWindowReport=str(analysis_path),currentActiveEscapeDelayComparisons=analysis['pairedDelayComparisons'],
  currentActiveEscapeNativeJumps=sum(c['actualHuman308Jumps']for c in new_cases.values()),
  currentActiveEscapeNativeAirKicks=sum(c['actualHuman200AirKicks']for c in new_cases.values()),
  currentActiveEscapeFullPrefixReport=str(prefix_path),
  diagnosticActiveEscapeTruncatedSelection=dict(failedReport=str(failed_path),originalFinalFrame=98473,
   selection=17,selectionAge=79,actualRequiredSampleAges=[130,146],actualExtendedFrames=[98524,98540],
   correctedRecording='audit_v2315_current_kano_p1_escape_active_early_extended_campaign',
   failedOriginalNotAccepted=True,identityGateWaived=False,completeNativePrefixRecords=163806),
  pendingActiveEscapeCampaigns=[],pendingActiveEscapeAccepted=True,
  gameSourceAndPlayableBytesChangedThisTurn=False,nativeDifficultyHealthAIPositionStageRNGModified=False,
  obsoleteFoldersDeletedThisTurn=False,foldersDeletedThisTurn=[],newCaptureLeavesNTFSCompressed=True,
  actualFullLadderClearAccepted=False,actualEndingsAccepted=False,finishedRelease=False,fullPortAcceptance=False,
  nextAction='Use actual native air-kick phase exits, CPUguard-owned contact stores and paired120-vs0opening-delay rates to select the next physical controller adjustment, not a game health/difficulty/AI patch. Test later descending/cross-up kick timing if supported by those records; keep native stomp counters and whole source/ID/selection/progression gates. Actual wholeKintaro/ShaoKahn matches, own ending pages/audio/return toattract remain unproven. Preserve all original move-phase grounding/shadow/art/audio arena/CPU/repeated/KO/overlap, finisher/victim/morph/secret/cinematic, final combinedUI regression, dependency-aware cleanup and refreshed release requirements.',
  inputHashes=pins,goalStatus='active')
 assert len(prior['remaining'])>=5 and prior['currentRealKintaroRoundWins']==4
 assert prior['currentRealKintaroMatchClears']==prior['currentRealShaoKahnMatchClears']==0
 assert len(cases)==38 and prior['currentActualBossHuman107Assignments']==2364
 return prior

if __name__=='__main__':
 assert not OUT.exists(),'Immutable full-scope checkpoint'
 result=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(goalStatus='active',newCampaignControls=4,actualNewHuman107Assignments=148,
  actualNewUppercutDamage=2960,newSpecificCounterexamples=83,newBossRoundWins=0,fullBossMatches=0,
  gameBytesChanged=False,finishedRelease=False,fullPortAcceptance=False),indent=2),flush=True)
