"""Retain independently checked native campaign evidence without narrowing the goal."""
import json
from pathlib import Path
import verify_current_boss_anticipation_campaign_v2114 as old
import verify_current_boss_held_response_campaign_v2123 as held

ROOT=old.ROOT
PREVIOUS=ROOT/'audit_v2111_current_pit_progress_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2129_current_campaign_progress_checkpoint'
CASES=(
 ('audit_v2115_current_kano_p1_anticipation_campaign','audit_v2118_current_kano_p1_anticipation_checked',old),
 ('audit_v2116_current_kano_p1_range_guard_campaign','audit_v2118_current_kano_p1_range_guard_checked',old),
 ('audit_v2117_current_sonya_p1_anticipation_campaign','audit_v2118_current_sonya_p1_anticipation_checked',old),
 ('audit_v2119_current_sonya_p1_defensive_leg_anticipation_campaign','audit_v2125_current_sonya_p1_defensive_leg_anticipation_checked',old),
 ('audit_v2120_current_sonya_p1_defensive_leg_range_guard_campaign','audit_v2125_current_sonya_p1_defensive_leg_range_guard_checked',old),
 ('audit_v2124_current_kano_p1_held_range_guard_campaign','audit_v2128_current_kano_p1_held_range_guard_checked',held),
 ('audit_v2126_current_sonya_p1_held_anticipation_campaign','audit_v2128_current_sonya_p1_held_anticipation_checked',held),
)

def save():
 prior=json.loads(PREVIOUS.read_text())
 assert prior['goalStatus']=='active'and not prior['fullPortAcceptance']
 pins=dict(prior['inputHashes'])
 def pin(path,wanted=None):
  path=str(Path(path).resolve());actual=old.digest(Path(path))
  assert wanted is None or actual==wanted,'Changed accepted dependency '+path
  assert path not in pins or pins[path]==actual,'Conflicting dependency '+path
  pins[path]=actual
 pin(PREVIOUS);pin(__file__)
 campaigns={}
 for capture,leaf,verifier in CASES:
  folder=ROOT/capture;report_path=ROOT/leaf/'report.json'
  report=json.loads(report_path.read_text())
  assert report['passed']and report['bounded_campaign_evidence_proven']
  assert not report['fullPortAcceptance']
  for path,wanted in report['inputHashes'].items():pin(path,wanted)
  pin(report_path)
  result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
  assert result['exit_code']==0 and result['assistance']=='none'and not result['cheats_enabled']
  rows=verifier.parse((folder/'run.log').read_text(encoding='utf-8-sig'),result['human_slot'],result['player'])
  wins=[row for row in rows if row['tag']=='WIN'and row['slot']==result['human_slot']]
  boss=[row for row in wins if row['stage']in(15,16)]
  assert len(wins)==report['native_own_round_wins']
  fields=[row for row in rows if row['tag']=='BOSS_FIELD']
  plans=[row for row in rows if row['tag']=='BOSS_PLAN']
  # This is an observed controller predicate, not a claim about what a
  # native state flag means or proof that a physical input became a jump.
  blocked_crouch=[row for row in fields if row['human_action']in(4,1540)and
                  (row['flags']&0x0c or row['body']&0x0c)and row['height']<=8]
  bad_timing=[row for row in plans if row['move']in('early_stomp_escape','close_physical_escape')and
              row['human_action']!=0x303]
  campaigns[capture]=dict(report=str(report_path),player=result['player'],side=result['human_slot'],
   strategy=result['strategy'],policy=report['bossPolicy'],stages=report['stages_reached'],
   ownRoundWins=len(wins),bossRoundWins=[{k:row[k]for k in('frame','stage','id','entry','pc','health')}for row in boss],
   actualNativeSpecialEntries=report['native_owned_special_entries'],moves=report['native_special_moves'],
   observedBossFields=report['observedBossFields'],paidLosses=report['paid_continue_losses'],
   endingStarts=report['ending_starts'],endingCompletions=report['ending_completions'],
   fullCampaignClear=report['unassisted_clear_proven'],
   observedGroundedCrouchFieldsMatchingOldLockout=len(blocked_crouch),
   jumpAttemptsOutsideReadyAction=len(bad_timing),
   attemptDoesNotEstablishJumpActivation=True)
 # Old reports, playable binaries and release artifacts remain authoritative.
 for path,wanted in pins.items():assert old.digest(Path(path))==wanted,'Changed checkpoint dependency '+path
 prior.update(previousCheckpoint=str(PREVIOUS),
  previousGoalTurnClassification='progress: authoritative new terminal campaign results inspected; they changed the next strategy',
  thisGoalTurnClassification='progress: independently verified seven physical-input campaign trajectories; repaired the controller only and retested actual boss button holds',
  currentBossAnticipationCampaigns=campaigns,
  gameSourceAndPlayableBytesChangedThisTurn=False,
  nativeDifficultyHealthAIPositionStageRNGModified=False,
  controllerChange='Held-input2121 preserves entire ordinary2112 campaign and native observers byte-exact; defense no longer drops on old lockout predicate, escape holds eighteen fields, projectile begins only in actual ready action303.',
  obsoleteBossCaveatSuperseded='Earlier2111 had no accepted Kintaro round win. New checked captures distinguish earned rounds from a complete won boss match. No full campaign or ending is inferred from a round.',
  allOldBuildFoldersRemoved=False,
  nextAction='Use actual boss field/damage/input chronology to improve physical strategy; prove both full natural campaigns and own endings, and continue all remaining move/arena/CPU/finisher/victim/morph/secret/audio fidelity before final combined regression, cleanup and release.',
  inputHashes=pins)
 prior['actualFullLadderClearAccepted']=all(any(c['fullCampaignClear']for c in campaigns.values()if c['player']==name)for name in('kano','sonya'))
 prior['actualEndingsAccepted']=prior['actualFullLadderClearAccepted']and all(any(c['endingCompletions']>0 for c in campaigns.values()if c['player']==name)for name in('kano','sonya'))
 prior['finishedRelease']=False;prior['fullPortAcceptance']=False;prior['goalStatus']='active'
 return prior

if __name__=='__main__':
 assert not OUT.exists(),'Immutable checkpoint'
 report=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(goalStatus='active',campaignCases=len(report['currentBossAnticipationCampaigns']),
  actualFullLadderClearAccepted=report['actualFullLadderClearAccepted'],
  actualEndingsAccepted=report['actualEndingsAccepted'],finishedRelease=False,fullPortAcceptance=False),indent=2))
