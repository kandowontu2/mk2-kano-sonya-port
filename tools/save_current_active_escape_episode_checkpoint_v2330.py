"""Replace recycled-task kick residency inference; preserve all actual port scope."""
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_current_active_escape_boss_ledger_v2318 as ledger
ROOT=ledger.ROOT;launch=ledger.launch
PREVIOUS=ROOT/'audit_v2327_current_active_escape_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2331_current_active_escape_episode_checkpoint'

def save():
 prior=json.loads(PREVIOUS.read_text())
 assert prior['goalStatus']=='active' and not prior['fullPortAcceptance']
 pins=dict(prior['inputHashes'])
 with ThreadPoolExecutor(max_workers=4)as pool:
  for (file,wanted),actual in zip(pins.items(),pool.map(launch.sha,pins)):
   assert wanted==actual,'Changed carried source/capture '+file
 def pin(path,wanted=None):
  path=str(Path(path).resolve());actual=launch.sha(path)
  assert wanted is None or actual==wanted,'Changed actual dependency '+path
  assert path not in pins or pins[path]==actual,'Conflicting source graph '+path
  pins[path]=actual
 def accept(path):
  path=Path(path);r=json.loads(path.read_text())
  assert r['passed'] and r['fullPortAcceptance']is False
  for file,wanted in r['inputHashes'].items():
   if file in pins:assert pins[file]==wanted,'Conflicting graph '+file
   else:pin(file,wanted)
  pin(path);return r
 pin(PREVIOUS);pin(__file__)
 path=ROOT/'audit_v2329_current_active_escape_episodes/report.json';actual=accept(path)
 obsolete_path=ROOT/'audit_v2325_current_active_escape_windows/report.json';obsolete=json.loads(obsolete_path.read_text());pin(obsolete_path)
 assert not actual['gameOrCaptureModified']
 assert actual['rejectedSpecificEpisodeCounterexamples']==12
 rejected=sum(len(rows)for rows in actual['rejectedSupersededRecycledExits'].values())
 assert rejected>0,'Actual recycled-pointer inference rejected, not merely a speculative replacement'
 for case,current in actual['cases'].items():
  old=obsolete['cases'][case]
  for key in ('actualHuman308Jumps','actualHuman200AirKicks','physicalJumpkickPlans','actualOwnedBossDamage','ownedDamageGroups','jumpWindows','actualFirst120IncomingDamage','actualPositiveHealthBossSegments','rounds'):
   assert current[key]==old[key],'Actual campaign/dispatch/health/window evidence unchanged '+case+' '+key
  assert actual['pairedDelayComparisons'][case]==obsolete['pairedDelayComparisons'][case]
  assert len(actual['episodeCounterexamples'][case])==3
  assert len(current['nativeAirKickExits'])==current['actualHuman200AirKicks']
  for exit in current['nativeAirKickExits']:
   assert exit['exitFrame']is None or 0<=exit['durationFields']<100,'Actual kick exit remains in a short continuous owned episode, never a later match'
 assert len(prior['currentSourceBoundBossCampaigns'])==38
 assert prior['currentActualBossHuman107Assignments']==2364 and prior['currentRealKintaroRoundWins']==4
 assert prior['currentRealKintaroMatchClears']==prior['currentRealShaoKahnMatchClears']==0
 launch.module_pins(pins)
 prior.update(previousCheckpoint=str(PREVIOUS),
  thisGoalTurnClassification='progress: twelve current-build physical-input campaign controls accepted across completed2305/2327work, true jump/airkick dispatch and original HP ledgers verified, four new active-escape controls plus83counterexamples, exact163806record extended prefix. Recycled Main-pointer air-kick lifetime inference then rejected and replaced with first original action transition inside the same continuous positive-health owned actor/Main episode; twelve new episode counterexamples reject holes/recycling/unproven endpoints. No game byte changed, full boss matches/endings and complete remaining scope still unproven.',
  currentActiveEscapeNativeWindowReport=str(path),currentActiveEscapeEpisodeCounterexamples=12,
  currentActiveEscapeDelayComparisons=actual['pairedDelayComparisons'],
  supersededActiveEscapeAirKickResidency=dict(report=str(obsolete_path),source=str(ROOT/'tools/analyze_current_active_escape_windows_v2324.py'),
   reason='Searching ahead for any before200end with the same actor/Main could match recycled task pointers in later rounds.2328requires the first actual next non200transition and continuous positive-health fields with the same actor/Main. Unknown exits are not interpreted as game failures.',
   rejectedActualOldExitInferences=rejected,rejections=actual['rejectedSupersededRecycledExits'],
   replacement=str(path),oldResidencyNotAccepted=True,actualDispatchAndDamageEvidenceUnchanged=True),
  inputHashes=pins,goalStatus='active',gameSourceAndPlayableBytesChangedThisTurn=False,
  actualFullLadderClearAccepted=False,actualEndingsAccepted=False,finishedRelease=False,fullPortAcceptance=False,
  nextAction='Use the corrected continuous-episode native kick transitions and actual guarded/unblocked HP stores to test later descending/cross-up physical air-kick timing. Early spacing with no artificial opening delay lowered observed incoming HP per1000boss fields relative to its exact pre-boss paired baseline for both characters, but produced no actual full boss clear. Change only test controls unless a reproducible game defect is found. Keep fullKintaro/ShaoKahn matches and own endings/attract, every move/arena grounding-shadow-art-audio includingCPU/repeated/KO/overlap, finishers/victims/morphs/secrets/cinematics, final combinedUI regression, dependency-aware cleanup and updated release as the complete original remaining scope.')
 assert len(prior['remaining'])>=5
 return prior

if __name__=='__main__':
 assert not OUT.exists(),'Immutable full-scope corrected checkpoint'
 result=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(goalStatus='active',newSpecificEpisodeCounterexamples=12,
  rejectedActualRecycledPointerExits=result['supersededActiveEscapeAirKickResidency']['rejectedActualOldExitInferences'],
  campaignContexts=38,actualHuman107Assignments=2364,actualKintaroRoundWins=4,actualFullBossMatches=0,
  gameBytesChanged=False,finishedRelease=False,fullPortAcceptance=False),indent=2),flush=True)
