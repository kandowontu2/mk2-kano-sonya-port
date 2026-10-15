"""Current all-slot Pit negative controls and actual grounded boss campaign progress."""
import json
from collections import Counter
from pathlib import Path
import verify_current_boss_ground_evasion_campaign_v2132 as ground
import verify_current_boss_delayed_counter_campaign_v2142 as delayed

ROOT=ground.ROOT
PREVIOUS=ROOT/'audit_v2129_current_campaign_progress_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2147_current_pit_campaign_progress_checkpoint'
CASES=(
 ('audit_v2133_current_kano_p1_ground_stomp_campaign','audit_v2138_current_kano_p1_ground_stomp_checked',ground),
 ('audit_v2134_current_sonya_p1_ground_stomp_campaign','audit_v2138_current_sonya_p1_ground_stomp_checked',ground),
 ('audit_v2135_current_kano_p1_ground_uppercut_campaign','audit_v2138_current_kano_p1_ground_uppercut_checked',ground),
 ('audit_v2143_current_kano_p1_delayed_ground_counter_campaign','audit_v2146_current_kano_p1_delayed_ground_counter_checked',delayed),
 ('audit_v2144_current_sonya_p1_delayed_ground_counter_campaign','audit_v2146_current_sonya_p1_delayed_ground_counter_checked',delayed),
)

def save():
 prior=json.loads(PREVIOUS.read_text())
 assert prior['goalStatus']=='active'and not prior['fullPortAcceptance']
 pins=dict(prior['inputHashes'])
 def pin(path,wanted=None):
  path=str(Path(path).resolve());actual=ground.digest(Path(path))
  assert wanted is None or actual==wanted,'Changed accepted dependency '+path
  assert path not in pins or pins[path]==actual,'Conflicting accepted dependency '+path
  pins[path]=actual
 def proof(leaf):
  path=ROOT/leaf/'report.json';report=json.loads(path.read_text())
  assert report['passed']and report['fullPortAcceptance']is False
  for path_,wanted in report['inputHashes'].items():pin(path_,wanted)
  pin(path);return report,str(path)
 pin(PREVIOUS);pin(__file__);pin(ROOT/'tools/test_current_native_pit_matrix_v2136.py')
 campaigns={}
 for capture,leaf,verifier in CASES:
  report,path=proof(leaf);folder=ROOT/capture
  meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
  assert report['bounded_campaign_evidence_proven']and meta['exit_code']==0
  assert meta['assistance']=='none'and not meta['cheats_enabled']
  rows=verifier.parse((folder/'run.log').read_text(encoding='utf-8-sig'),meta['human_slot'],meta['player'])
  own=[row for row in rows if row['tag']=='WIN'and row['slot']==meta['human_slot']]
  assert len(own)==report['native_own_round_wins']
  actions=[row for row in rows if row['tag']=='BOSS_ACTION']
  values=Counter(row['after']for row in actions)
  assigned=sum(row['after']==0x106 for row in actions)
  if verifier is delayed:
   assert assigned==report['actualNativeUppercutAssignments']
   assert len(actions)==report['readOnlyOwnActionStores']
  campaigns[capture]=dict(report=path,player=meta['player'],side=meta['human_slot'],
   strategy=meta['strategy'],policy=report['bossPolicy'],stages=report['stages_reached'],
   ownRoundWins=len(own),bossRoundWins=[{k:row[k]for k in('frame','stage','id','entry','pc','health')}
                                      for row in own if row['stage']in(15,16)],
   actualSpecialEntries=report['native_owned_special_entries'],moves=report['native_special_moves'],
   observedBossFields=report['observedBossFields'],paidLosses=report['paid_continue_losses'],
   endingStarts=report['ending_starts'],endingCompletions=report['ending_completions'],
   fullCampaignClear=report['unassisted_clear_proven'],
   ownActionStoreTracePresent=verifier is delayed,
   native106UppercutAssignments=assigned if verifier is delayed else None,
   observedIncomingNativeActionWords={f'{word:04X}':count for word,count in sorted(values.items())},
   intendedCounterNeverAssumedAnActivatedUppercut=True)
 total=0
 for case in('kano_p1','kano_p2','sonya_p1','sonya_p2'):
  version=2108 if case in('kano_p1','sonya_p2')else 2137
  report,path=proof(f'audit_v{version}_current_{case}_pit_counterexamples')
  assert report['rejectedCounterexamples']==31
  assert report['unchangedInMemoryControlPassed']and report['unmodifiedFullSceneRechecked']
  assert report['unexpectedErrorsAcceptedAsRejection']is False
  assert len(report['tests'])==31 and all(test['rejected']and test['errorType']=='ValueError'for test in report['tests'])
  prior['currentPitScenes'][case].update(counterexampleReport=path,
   rejectedSpecificCounterexamples=31,counterexamplesExercisedOnThisSlot=True)
  total+=31
 assert total==124
 # Recheck all actual earlier/frozen dependencies; a manifest is not enough.
 for path,wanted in pins.items():assert ground.digest(Path(path))==wanted,'Changed checkpoint dependency '+path
 prior.update(previousCheckpoint=str(PREVIOUS),
  previousGoalTurnClassification='progress: seven independent current campaign proofs, including genuine native Kano Kintaro round wins and Sonya defensive-leg ordinary ladder progression',
  thisGoalTurnClassification='progress: all four current Pit corruption suites now positively controlled and specifically rejected; five further actual-input boss trajectories independently checked, with a read-only native action trace rather than assumed counter activation',
  currentGroundedBossCampaigns=campaigns,rejectedSpecificPitCounterexamples=total,
  allFourPitSlotCounterexampleSuitesAccepted=True,
  groundAndDelayedControllerGameplaySourceChanged=False,
  gameSourceAndPlayableBytesChangedThisTurn=False,
  nativeDifficultyHealthAIPositionStageRNGModified=False,
  counterTraceConclusion='Boss inputs and native incoming action assignments are retained. A planned counter, intended crouch, grounded move or airborne observation alone is not a successful uppercut or jump. Bot losses alone do not identify a native game defect.',
  allOldBuildFoldersRemoved=False,foldersDeletedThisTurn=[],
  nextAction='Isolate a clean physical Down/HP command with neutral input history and verify the exact native human attack path, then finish actual boss campaigns/endings. Continue remaining move-phase/arena/CPU/finisher/victim/morph/secret/audio fidelity; final combined regression, dependency-aware cleanup and refreshed release remain required.',
  inputHashes=pins,goalStatus='active',finishedRelease=False,fullPortAcceptance=False)
 prior['scopeCaveats']=[value for value in prior['scopeCaveats']
                       if not value.startswith('112correctedTomb corruptions')and not value.startswith('Bossattempts still')]
 prior['scopeCaveats']+= [
  'All four current Pit slots have31specific ValueError corruption rejections each, an unchanged in-memory full-scene control, and a final unmodified independent full-scene replay. Total124; no incidental parser or indexing errors accepted as success.',
  'Prior current captures include one earned Kano Kintaro round in each of two strategies. New grounded runs and read-only native action traces do not establish a full Kintaro match, ShaoKahn clear, own ending or attract return.',
  'All current Pit positive/negative fixtures still cover Kano/Sonya as victims only; other native victim/mirror/branch combinations and complete stage DCS/audio fidelity remain unfinished.',
  'Current playable exe, payload, CMD and playtest ZIP are unchanged. No old build folders were removed in this turn.']
 prior['actualFullLadderClearAccepted']=all(any(case['fullCampaignClear']for case in
  list(prior['currentBossAnticipationCampaigns'].values())+list(campaigns.values())if case['player']==name)for name in('kano','sonya'))
 prior['actualEndingsAccepted']=prior['actualFullLadderClearAccepted']and all(any(case['endingCompletions']>0 for case in
  list(prior['currentBossAnticipationCampaigns'].values())+list(campaigns.values())if case['player']==name)for name in('kano','sonya'))
 return prior

if __name__=='__main__':
 assert not OUT.exists(),'Immutable checkpoint only'
 report=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(goalStatus='active',newCampaignCases=len(report['currentGroundedBossCampaigns']),
  allFourPitSlotCounterexampleSuitesAccepted=True,rejectedSpecificPitCounterexamples=report['rejectedSpecificPitCounterexamples'],
  actualFullLadderClearAccepted=report['actualFullLadderClearAccepted'],actualEndingsAccepted=report['actualEndingsAccepted'],
  finishedRelease=False,fullPortAcceptance=False),indent=2))
