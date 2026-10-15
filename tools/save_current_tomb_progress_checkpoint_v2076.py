"""Preserve current native Tomb scenes and bounded boss attempts.

All original full-goal requirements remain active. Neither partial campaign
progress nor two Tomb fixtures is promoted to a finished port/release.
"""
import json
from pathlib import Path
import verify_current_native_tomb_scene_v2067 as sonya
import verify_current_boss_timing_campaign_v2061 as campaign
ROOT=sonya.ROOT
PREVIOUS=ROOT/'audit_v2055_current_campaign_progress_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2076_current_tomb_progress_checkpoint'

def save():
 prior=json.loads(PREVIOUS.read_text());assert prior['goalStatus']=='active'and not prior['fullPortAcceptance']
 pins=dict(prior['inputHashes'])
 def pin(file,wanted=None):
  file=Path(file);key=str(file.resolve());value=sonya.launch.sha(file)
  assert wanted is None or value==wanted,'Changed authoritative input '+key
  assert key not in pins or pins[key]==value,'Conflicting source pin '+key
  pins[key]=value
 pin(PREVIOUS)
 def proof(leaf):
  path=ROOT/leaf/'report.json';r=json.loads(path.read_text())
  assert r['passed']and not r['fullPortAcceptance'],leaf
  for file,wanted in r['inputHashes'].items():pin(file,wanted)
  pin(path);return r,str(path)
 scenes={};counterexamples=0;reports={}
 for name,leaf,counter in(
  ('sonya_p2_original_random_drop','audit_v2067_current_sonya_p2_tomb_scene_checked','audit_v2068_current_sonya_p2_tomb_counterexamples'),
  ('kano_p1_original_ceiling_held','audit_v2073_current_kano_p1_tomb_scene_checked','audit_v2074_current_kano_p1_tomb_counterexamples')):
  r,path=proof(leaf);c,cpath=proof(counter)
  assert c['rejectedCounterexamples']==24 and c['unmodifiedFullSceneRechecked']and not c['gameOrCaptureBytesChanged']
  assert not r['fullTombArtAudioAcceptance']and not r['audioInventory']['audioAcceptance']
  scenes[name]={k:r[k]for k in('sampledFrames','exactReplayedFrames','exactHeldScanouts','exactScreenPixels','exactOwnedPixels',
   'sourceBoundProjections','fullPhysicalPaletteChecks','nativeShadowCopies','continuousErase','audioInventory')}
  scenes[name].update(sourceAndOriginalPhysicalTrajectoryUnchanged=True,rejectedCounterexamples=24,report=path,counterexampleReport=cpath)
  counterexamples+=c['rejectedCounterexamples'];reports[leaf]=path;reports[counter]=cpath
 announcements,path=proof('audit_v2075_current_tomb_announcements_checked')
 assert announcements['currentTombOwnedWinnerAnnouncementsAccepted']and not announcements['allStageAudioAccepted']
 reports['audit_v2075_current_tomb_announcements_checked']=path
 campaigns={}
 for policy in('projectile','air_counter'):
  leaf='audit_v2061_current_kano_boss_'+policy+'_timing_checked'
  r,path=proof(leaf)
  assert r['bounded_campaign_evidence_proven']and not r['unassisted_clear_proven']and not r['ending_starts']and not r['ending_completions']
  capture=ROOT/('audit_v2058_current_kano_p1_boss_projectile_timing'if policy=='projectile'else'audit_v2059_current_kano_p1_boss_air_counter_timing')
  rows=campaign.parse((capture/'run.log').read_text(encoding='utf-8-sig'),1,'kano')
  wins=[q for q in rows if q['tag']=='WIN'and q['stage']==15]
  assert wins and not any(q['slot']==1 for q in wins),'No earned Kintaro own round'
  terminal=[q for q in rows if q['tag']=='RESULT'];assert len(terminal)==1 and terminal[0]['ending']==terminal[0]['ending_completed']==-1
  campaigns[policy]={k:r[k]for k in('stages_reached','native_own_round_wins','native_combat_damage_stores',
   'paid_continue_losses','native_owned_special_entries','native_special_moves','physicalBossPlans','unassisted_clear_proven')}
  campaigns[policy].update(report=path,KintaroOwnRoundWins=0,minimumKintaroWinningHealth=min(int(q['health'].split(',')[1])for q in wins),
   nativeTerminalFrame=terminal[0]['frame'])
  reports[leaf]=path
 assert campaigns['projectile']['minimumKintaroWinningHealth']==7
 failures={}
 for number,leaf,why in(
  (2065,'audit_v2065_current_sonya_p2_tomb_scene_checked','New hex motion/input fields added to the parser alias rather than its actual globals; capture unchanged.'),
  (2066,'audit_v2066_current_sonya_p2_tomb_scene_checked','Incorrect post-fight player-state/Main-pointer assumption; corrected against native code and actual stores, capture unchanged.'),
  (2072,'audit_v2072_current_kano_p1_tomb_scene_checked','Tomb-only provenance observer stops on native next-arena installation, eight fields before actor clear; complete body observations cover the remainder.')):
  path=ROOT/leaf/'report.json';r=json.loads(path.read_text());assert not r['passed'];pin(path)
  failures[number]=dict(report=str(path),reason=why,gameOrCaptureChanged=False)
 # The v2070 indentation failure wrote no report; retain its immutable source.
 for file in('verify_current_native_tomb_scene_v2065.py','verify_current_native_tomb_scene_v2066.py','verify_current_native_tomb_scene_v2070.py','verify_current_native_tomb_scene_v2071.py','verify_current_native_tomb_scene_v2072.py',
  'verify_current_native_tomb_scene_v2073.py','test_current_native_tomb_scene_v2074.py','verify_current_tomb_announcements_v2075.py','verify_current_boss_timing_campaign_v2060.py','verify_current_boss_timing_campaign_v2061.py'):
  pin(ROOT/'tools'/file)
 pin(__file__)
 for file,wanted in pins.items():assert sonya.launch.sha(file)==wanted,'Changed saved proof dependency '+file
 return dict(goalStatus='active',objective=prior['objective'],previousCheckpoint=str(PREVIOUS),
  previousStatusOnlyTurnClassification='no progress; latest saved state was inspected before executing the next substantive action',
  thisGoalTurnClassification='progress: two current earned native Tomb branches now have complete source/FIFO/palette/projection/shadow/continuous-erase/scanout/retirement evidence and48rejected corruptions; own winner announcements proven audible; boss attempts remain incomplete',
  currentCandidate=prior['currentCandidate'],currentCMD=prior['currentCMD'],currentPlaytestZIP=prior['currentPlaytestZIP'],
  gameSourceAndPlayableBytesChangedThisTurn=False,currentTombScenes=scenes,currentTombWinnerAnnouncements=announcements['cases'],
  rejectedCurrentTombCounterexamples=counterexamples,currentBossTimingCampaigns=campaigns,acceptedReports=reports,
  preservedVerifierFailures=failures,preservedSyntaxFailure='tools/verify_current_native_tomb_scene_v2070.py; no report written; fresh2071successor used',
  scopeCaveats=[
   'Both fixtures use byte-unchanged806physicalcoin/start/true-IDselection/earned322damage/paidrematch/nativeTombcommand; no HP/RNG/stage/AI/difficulty/position/task/identity injection.',
   'SonyaP2random-drop:128fieldhold,112fieldslowdrop,nativefall/landing,thenretirement. KanoP1originalheld:unpressedcontrols,originalRNG658>=50,originalFF8EB400ceilingbranch,completeheldvictimcallbacks.',
   'Each537consecutivecompletedscanouts:507originaldrawingpasses and30directlyboundnaturallyheldpostteardownscreens. Heldscreens are not falsely called DMA-reconstructed or newly erased.',
   '48in-memorycorruptions rejected. Actualcapturedfiles, executable, payload, ROM, currentCMD andZIP areunchanged.',
   'Own winner source-announcements are audible at original native markers/routegain, and both complete PCM captures match prior native earned fixtures byte-for-byte. All DCS effects/victimvoices/stageaudio correctness remains unproven.',
   'Source/FIFO/art/palette/shadow/nativeerase checks are for these twoTombfixtures, not all Tomb branches, physicalslotcombinations, arenas, finishers, victims, morphs, secrets or cinematics.',
   'Kano current campaigns have29earnedroundwins throughShang toKintaro, but no Kintaroownround; projectilepolicybestKintarowinningHP7. No ShaoKahnclear, ownending orattractreturn accepted.',
   'Freshcaptures are NTFScompressed; no oldfolders deleted thisturn. No livegameplaycaptures remain after normal exits; existing release remains a playtest.'],
  remaining=prior['remaining'],
  nextAction='Verify remaining native Tomb/Pit performer/victim/slot combinations and stage effect/victim sound correctness; continue outstanding move/CPU/interrupt/arena audio and finisher/victim/morph/secret/cinematic fidelity; earn natural Kintaro/ShaoKahn campaign clears and own endings/attract; final combined regression, dependency-aware obsolete build cleanup and refreshed release.',
  inputHashes=pins,allCPUAccepted=False,allRepeatedCPUAccepted=False,allKOCasesAccepted=False,
  allMoveArtGroundShadowAudioAccepted=False,fullTombArtAudioAccepted=False,actualFullLadderClearAccepted=False,
  actualEndingsAccepted=False,allFinishersVictimsMorphsSecretsCinematicsAccepted=False,allOldBuildFoldersRemoved=False,
  finishedRelease=False,fullPortAcceptance=False)

if __name__=='__main__':
 assert not OUT.exists(),'Preserve immutable checkpoint'
 result=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(goalStatus=result['goalStatus'],TombCases=len(result['currentTombScenes']),
  consecutiveScreens=sum(r['sampledFrames']for r in result['currentTombScenes'].values()),
  nativeShadowCopies=sum(r['nativeShadowCopies']for r in result['currentTombScenes'].values()),
  rejectedCounterexamples=result['rejectedCurrentTombCounterexamples'],ownWinnerAnnouncements=2,
  fullPortAcceptance=False,finishedRelease=False)),flush=True)
