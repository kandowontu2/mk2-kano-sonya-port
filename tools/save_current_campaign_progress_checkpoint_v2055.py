"""Preserve current build campaign evidence without accepting a boss clear."""
import json
from pathlib import Path
import verify_current_boss_evasion_campaign_v2052 as model
ROOT=model.ROOT
PREVIOUS=ROOT/'audit_v2049_current_sonya_cpu_square_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2055_current_campaign_progress_checkpoint'
def save():
 prior=json.loads(PREVIOUS.read_text());assert prior['goalStatus']=='active'and not prior['fullPortAcceptance']
 pins=dict(prior['inputHashes'])
 def pin(file,wanted=None):
  p=Path(file);value=model.digest(p)
  assert wanted is None or value==wanted,'Changed authoritative evidence '+str(p)
  assert str(p)not in pins or pins[str(p)]==value
  pins[str(p)]=value
 pin(PREVIOUS)
 reports={};summaries={}
 for leaf,report_leaf in(('audit_v2051_current_kano_p1_jumpkick_campaign','audit_v2052_current_kano_jumpkick_campaign_checked'),
  ('audit_v2053_current_kano_p1_zoning_campaign','audit_v2054_current_kano_zoning_campaign_checked')):
  path=ROOT/report_leaf/'report.json';proof=json.loads(path.read_text())
  assert proof['passed']and proof['bounded_campaign_evidence_proven']and not proof['unassisted_clear_proven']and not proof['fullPortAcceptance']
  for file,wanted in proof['inputHashes'].items():pin(file,wanted)
  pin(path)
  log=(ROOT/leaf/'run.log').read_text(encoding='utf-8-sig');rows=model.parse(log,1,'kano')
  assert not proof['ending_starts']and not proof['ending_completions']
  summaries[leaf]={k:proof[k]for k in('stages_reached','native_own_round_wins','native_combat_damage_stores',
   'paid_continue_losses','native_owned_special_entries','native_special_moves','unassisted_clear_proven','ending_starts','ending_completions')}
  live=[r for r in rows if r['tag']=='LIVE'and r['stage']==15]
  wins=[r for r in rows if r['tag']=='WIN'and r['stage']==15]
  if live:
   assert all(r['human']=='17:17'and r['cpu']=='12:12'for r in live),'Actual native Kano versus Kintaro'
   assert not any(r['slot']==1 for r in wins),'No earned Kintaro round was observed'
   summaries[leaf].update(nativeKintaroLiveSamples=len(live),
    minimumSampledKintaroHealth=min(int(r['health'].split(',')[1])for r in live),
    KintaroOwnRoundWins=0,
    minimumKintaroWinningHealth=min(int(r['health'].split(',')[1])for r in wins))
  terminal=[r for r in rows if r['tag']=='RESULT'];assert len(terminal)==1 and terminal[0]['ending']==terminal[0]['ending_completed']==-1
  summaries[leaf]['nativeTerminalFrame']=terminal[0]['frame']
  reports[report_leaf]=str(path)
 pin(ROOT/'tools/run_current_boss_evasion_campaign_v2050.ps1');pin(ROOT/'tools/verify_current_boss_evasion_campaign_v2052.py')
 pin(Path(__file__).resolve())
 for file,wanted in pins.items():assert model.digest(Path(file))==wanted
 return dict(goalStatus='active',objective=prior['objective'],previousCheckpoint=str(PREVIOUS),
  thisGoalTurnClassification='progress: current native P2 Sonya Square miss now has complete source/scene/shadow/erase/recovery and41counterexamples; genuine current-build Kano campaigns additionally validate29earned rounds and397knifeentries through native Shang then Kintaro, without claiming a boss clear',
  currentCandidate=prior['currentCandidate'],currentCMD=prior['currentCMD'],currentPlaytestZIP=prior['currentPlaytestZIP'],
  gameSourceAndPlayableBytesChangedThisTurn=False,currentP2SonyaSquareCheckpoint=str(PREVIOUS),
  acceptedCampaignReports=reports,currentCampaigns=summaries,
  scopeCaveats=[
   'Both current campaign attempts use actual physical coin/start/selection/attack controls, unchanged difficulty/CPU/HP/RNG/positions/schedule, isolated cfg/nvram and no cheats.',
   'Jump-kick route loses39paid-continue attempts at native first-stage Sonya with0own wins. It is not gameplay softlock evidence and is not treated as tower completion.',
   'Zoning route reaches0..12 then original endurance sentinel skips13, beats14Shang and reaches15Kintaro, with29earned native rounds,22paidcontinues,747original damage stores and397native knife entries. All live own IDs remain17.',
   'Kintaro remains unbeaten: no own round winner and no stage16/Shao Kahn or ending/attract. His lowest winning HP is retained only as discovery, not a clear.',
   'Source-bound native winner, damage, roster/morph/schedule, successful-match progression and paid-continue state checks pass; these campaigns do not accept all exact scene/art/audio or every contact.',
   'No current game executable, ROM/payload, CMD, ZIP or gameplay source changed. Dirty MAME12modified files and untracked native-picture header were inspected and preserved. Fresh captures are NTFScompressed; no deletion performed.',
   'All full-goal requirements remain intact. The existing ZIP remains a playtest, not a finished release.'],
  remaining=prior['remaining'],
  nextAction='Use actual Kintaro states/failed legitimate inputs to improve only the physical boss-play timing (do not force HP/AI/positions/difficulty/ladder), earn native Kintaro/Shao Kahn wins and observe own endings/attract. Continue remaining CPU/contact/interrupt/arena/audio and finishers/victims/morphs/secrets/cinematics; then combined regression, dependency-aware obsolete-folder cleanup and final release.',
  inputHashes=pins,allCPUAccepted=False,allRepeatedCPUAccepted=False,allKOCasesAccepted=False,
  allMoveArtGroundShadowAudioAccepted=False,actualFullLadderClearAccepted=False,actualEndingsAccepted=False,
  allFinishersVictimsMorphsSecretsCinematicsAccepted=False,allOldBuildFoldersRemoved=False,finishedRelease=False,fullPortAcceptance=False)
if __name__=='__main__':
 assert not OUT.exists(),'Preserve immutable checkpoint'
 result=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(goalStatus=result['goalStatus'],campaigns=result['currentCampaigns'],finishedRelease=False)),flush=True)

