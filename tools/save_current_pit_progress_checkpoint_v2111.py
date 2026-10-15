"""Save current Pit progress and corrected Tomb negative evidence.

Keep the full natural-character objective active; a playtest is not a release.
"""
import json
from pathlib import Path
import verify_current_native_pit_movie_v2100 as model
ROOT=model.ROOT
PREVIOUS=ROOT/'audit_v2076_current_tomb_progress_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2111_current_pit_progress_checkpoint'
def save():
 prior=json.loads(PREVIOUS.read_text());model.need(prior['goalStatus']=='active'and not prior['fullPortAcceptance'],'Full goal remains active')
 pins=dict(prior['inputHashes']);reports={}
 def pin(file,wanted=None):
  file=Path(file).resolve();key=str(file);value=model.launch.sha(file)
  model.need(wanted is None or value==wanted,'Changed authoritative input '+key)
  model.need(key not in pins or pins[key]==value,'Conflicting authoritative input '+key);pins[key]=value
 def proof(leaf):
  path=ROOT/leaf/'report.json';r=json.loads(path.read_text())
  model.need(r['passed']and not r['fullPortAcceptance'],'Incomplete scoped proof '+leaf)
  for file,wanted in r['inputHashes'].items():
   resolved=str(Path(file).resolve())
   model.need(resolved not in pins or pins[resolved]==wanted,'Conflicting report dependency '+resolved)
   pins[resolved]=wanted
  pin(path);reports[leaf]=str(path);return r,str(path)
 pin(PREVIOUS)
 tomb={};total_tomb=0
 for case in('kano_p1','kano_p2','sonya_p1','sonya_p2'):
  r,path=proof(f'audit_v2080_current_{case}_tomb_matrix_checked')
  c,cpath=proof(f'audit_v2096_current_{case}_tomb_counterexamples')
  model.need(c['rejectedCounterexamples']==28 and c['unchangedInMemoryControlPassed']and c['unmodifiedFullSceneRechecked']and c['unexpectedKeyOrIndexErrorsAcceptedAsRejection']is False,'Actual corrected Tomb controls')
  model.need(all(t['errorType']=='AssertionError'for t in c['tests']),'No unrelated parser failures count as rejections')
  tomb[case]={k:r[k]for k in('sampledFrames','exactReplayedFrames','exactHeldScanouts','exactScreenPixels','nativeTombBranch','nativeShadowCopies','continuousErase')}
  tomb[case].update(report=path,correctedCounterexampleReport=cpath,rejectedSpecificCounterexamples=28)
  total_tomb+=28
 tomb_audio,path=proof('audit_v2081_current_tomb_announcements_checked')
 model.need(tomb_audio['currentTombOwnedWinnerAnnouncementsAccepted']and len(tomb_audio['cases'])==4 and not tomb_audio['allStageAudioAccepted'],'Bounded all-slot Tomb winner cues')
 pit={};total_pit=0
 for case in('kano_p1','kano_p2','sonya_p1','sonya_p2'):
  original_pair=case in('kano_p1','sonya_p2')
  leaf=f'audit_v2100_current_{case}_pit_movie_checked'if original_pair else f'audit_v2107_current_{case}_pit_matrix_checked'
  r,path=proof(leaf)
  pit[case]={k:r[k]for k in('movie','sampledFrames','exactReplayedFrames','exactHeldScanouts','exactScreenPixels','sourceBoundProjections','fullOwnPaletteChecks','continuousErase','audioInventory')}
  pit[case].update(report=path,rejectedSpecificCounterexamples=0,counterexamplesExercisedOnThisSlot=False)
  if original_pair:
   c,cpath=proof(f'audit_v2108_current_{case}_pit_counterexamples')
   model.need(c['rejectedCounterexamples']==31 and c['unchangedInMemoryControlPassed']and c['unmodifiedFullSceneRechecked']and c['unexpectedErrorsAcceptedAsRejection']is False,'Actual controlled Pit corruption checks')
   model.need(all(t['errorType']=='ValueError'for t in c['tests']),'Specific Pit contract rejections only')
   pit[case].update(counterexampleReport=cpath,rejectedSpecificCounterexamples=31,counterexamplesExercisedOnThisSlot=True)
   total_pit+=31
 pit_audio,path=proof('audit_v2110_current_pit_announcements_checked')
 model.need(pit_audio['currentPitOwnedWinnerAnnouncementsAccepted']and len(pit_audio['cases'])==4 and not pit_audio['allStageAudioAccepted'],'Bounded current Pit winner cues')
 # Preserve failures, but do not promote discarded verifier assumptions.
 failures={}
 for version,reason in(
  (2089,'Included an already-declared source-bound composite-entry hook in an unchanged-original-code range.'),
  (2090,'New hexadecimal group field was absent from parser HEX metadata.'),
  (2091,'Address-only ownership confused pre-construction scenery reuse with a live cinematic body; initial observer also stopped at mode9 exit.'),
  (2095,'Mode3 begins before the original four-scheduler-tick/eight-render-field scene clear, not at the actual end of movie publications.'),
  (2097,'A real physical publication precedes native pointer clear within the same completed field.'),
  (2098,'First-only text replacement missed the physical-publication upper-bound predicate; corrected fresh2099successor.')):
  paths=[]
  for case in('kano_p1','sonya_p2'):
   path=ROOT/f'audit_v{version}_current_{case}_pit_movie_checked/report.json'
   report=json.loads(path.read_text());model.need(not report['passed'],'Expected preserved verifier failure')
   pin(path);paths.append(str(path))
  failures[version]=dict(reason=reason,reports=paths,gameOrCaptureBytesChanged=False)
 for case in('kano_p1','kano_p2','sonya_p1','sonya_p2'):
  path=ROOT/f'audit_v2082_current_{case}_tomb_counterexamples/report.json';old=json.loads(path.read_text())
  model.need(any(t['errorType']=='KeyError'for t in old['tests']),'Observed earlier negative-test weakness')
  pin(path)
 # Both earlier Pit observers are diagnostic-only, not accepted full scenes.
 diagnostics={}
 for version,stem,reason in(
  (2085,'pit_fullscene','Stopped at normal fighter-pointer retirement; movie had not begun.'),
  (2088,'pit_movie_fullscene','Stopped at native mode9 exit plus30; native impact remains legitimately during winner announcement.')):
  diagnostics[version]=dict(reason=reason,fullSceneAcceptance=False,captures=[])
  for case in('kano_p1','sonya_p2'):
   folder=ROOT/f'audit_v{version}_current_{case}_{stem}'
   meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
   model.need(meta['exit_code']==0 and meta['guest_writes']==0,'Preserved diagnostic terminal capture')
   pin(folder/'result.json');pin(folder/'run.log')
   diagnostics[version]['captures'].append(str(folder))
 for case in('kano_p1','sonya_p2'):
  path=ROOT/f'audit_v2101_current_{case}_pit_counterexamples/report.json'
  failed=json.loads(path.read_text());model.need(not failed['passed']and failed['error']=='StopIteration()','Preserved counter-fixture lookup failure')
  pin(path)
 failures['2101counter']=dict(reason='A counterexample assumed a freed movie address had a publication in the exact clear field. It does not; fresh2104adds a unique synthetic late publication in memory. Unexpected StopIteration correctly failed the suite.',gameOrCaptureBytesChanged=False)
 for case in('kano_p1','sonya_p2'):
  path=ROOT/f'audit_v2104_current_{case}_pit_counterexamples/report.json'
  failed=json.loads(path.read_text());model.need(not failed['passed']and 'max() iterable argument is empty'in failed['error'],'Preserved synthetic clear-field assumption failure')
  pin(path)
 failures['2104counter']=dict(reason='The exact native clear field has no FIFO publications at all; max(cursor) over that field is invalid. Fresh2108uses a unique copied original publication at the later field. This fixture error never counts as a rejection.',gameOrCaptureBytesChanged=False)
 pin(ROOT/'tools/verify_current_native_pit_matrix_v2107.py')
 pin(ROOT/'tools/verify_current_native_tomb_matrix_v2079.py')
 pin(__file__)
 for file,wanted in pins.items():model.need(model.launch.sha(file)==wanted,'Changed saved dependency '+file)
 return dict(goalStatus='active',objective=prior['objective'],previousCheckpoint=str(PREVIOUS),
  previousGoalTurnClassification='no progress: status-only turn; authoritative terminal Pit captures revalidated before new execution',
  thisGoalTurnClassification='progress: all four current earned native Pit character/slot scenes, native impact/voice routing and own announcements verified; all four Tomb negative suites corrected and positively controlled',
  currentCandidate=prior['currentCandidate'],currentCMD=prior['currentCMD'],currentPlaytestZIP=prior['currentPlaytestZIP'],
  gameSourceAndPlayableBytesChangedThisTurn=False,currentTombScenes=tomb,currentTombWinnerAnnouncements=tomb_audio['cases'],
  rejectedSpecificTombCounterexamples=total_tomb,currentPitScenes=pit,currentPitWinnerAnnouncements=pit_audio['cases'],
  rejectedSpecificPitCounterexamples=total_pit,currentBossTimingCampaigns=prior['currentBossTimingCampaigns'],
  acceptedReports=reports,preservedVerifierFailures=failures,diagnosticOnlyPitCaptures=diagnostics,
  supersededNegativeEvidence='Earlier2082count112 is not accepted because many failures were unrelated KeyErrors. New2096count112 uses unchanged-copy controls, specific AssertionErrors and final independent full positive rechecks.',
  scopeCaveats=[
   'All current captures use unchanged806 physical coin/start/selection/earned wins and paid challengers. No forced HP, RNG, stage, positions, difficulty, tasks or IDs.',
   'All four current Tomb slots retain537screens each:507exactdrawingpasses plus30source-bound heldscanouts; both original held and drop outcomes represented. Not all victims/branches or complete stage audio.',
   'Four Pit performer cases:KanoP1/P2 defeatsSonyaP2/P1;SonyaP1/P2 defeatsKanoP2/P1. Seven fullyearnedmatches each, twenty originalcadence fallgroups plusowninitialcache/impact, native constructedMain+140victim, allsixownmovieposes.',
   'Pit mode9exit is followed by native heldimpact/winnerannouncement; mode3precedes native fourtick/eightfield objectlistclear. Same-field physicalpublication can precede pointerclear. These intervals are captured, not cut out.',
   f'All four Pit fixtures: {sum(c["sampledFrames"]for c in pit.values())}completedscanouts, {sum(c["exactReplayedFrames"]for c in pit.values())}exact saved-pass replays, {sum(c["exactHeldScanouts"]for c in pit.values())}source-bound naturally heldscanouts; one initial base per run, never later buffer anchors.',
   'Constructed Pit body palettes and bothphysical palettes/sourceFIFO/queuedcamera/cache projections are exact. No blanketallarenaground/shadow, all-victim or artisticapproval claim.',
   'Original impacteffectcommand0254 and gendercorrect victimcommands0348/02E7 proven. Own wins announcements fit pinnedsourceaudio and fullnativePCM matches prior earnedfixtures. Correctness of all DCS waveforms/effects/victimvoices remains unproven.',
   '112correctedTomb corruptions across4cases;62Pitcopy-onlyspecificcorruptions inKanoP1/SonyaP2fixtures only, after unchanged-copy controls and finalfullpositive independentrechecks. RemainingtwoPitfixtures havefullpositives butno newcopy-onlynegative reruns. No mutatedcapture or guestfiles.',
   'Bossattempts still reachKintaro without an earnedKintarowin; no ShaoKahnclear, ownending orattractreturn accepted.',
   'CurrentCMD/ZIP/exe/payload and dirtyMAMEcheckout preserved. No oldfolders deleted thisturn; all freshcaptureleaves NTFScompressed. ExistingZIP remains a playtest.'],
  remaining=[
   'Broader native Pit/Tomb victim/mirror/branch combinations and complete stage effect/victim audio fidelity',
   'Full move-phase art, grounding, native floor shadows and cleanup across arenas; broader CPU, repeated, KO and overlap cases',
   'All other finishers, victims, morphs, secrets and cinematics',
   'Actual natural Kintaro/ShaoKahn campaign clears, own endings and return to attract',
   'Final combined selection/ladder/names/audio regression, dependency-aware obsolete-folder cleanup and refreshed release ZIP'],
  nextAction='Complete broader stage victim/mirror/branch and sound fidelity; continue full move/arena/CPU/finisher/victim/morph/secret fidelity and earn both complete campaigns/endings/attract. Then final combined regression, cleanup and release.',
  inputHashes=pins,allCPUAccepted=False,allRepeatedCPUAccepted=False,allKOCasesAccepted=False,
  allMoveArtGroundShadowAudioAccepted=False,fullTombArtAudioAccepted=False,fullPitArtAudioAccepted=False,
  actualFullLadderClearAccepted=False,actualEndingsAccepted=False,allFinishersVictimsMorphsSecretsCinematicsAccepted=False,
  allOldBuildFoldersRemoved=False,finishedRelease=False,fullPortAcceptance=False)
if __name__=='__main__':
 model.need(not OUT.exists(),'Immutable checkpoint only')
 report=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(goalStatus='active',TombCases=4,PitCases=4,
  PitScreens=sum(c['sampledFrames']for c in report['currentPitScenes'].values()),
  rejectedSpecificTombCounterexamples=report['rejectedSpecificTombCounterexamples'],
  rejectedSpecificPitCounterexamples=report['rejectedSpecificPitCounterexamples'],
  finishedRelease=False,fullPortAcceptance=False)),flush=True)
