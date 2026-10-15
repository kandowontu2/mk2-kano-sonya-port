"""Preserve verified timer progress, current playtest and open full-goal work."""
import json,re
from pathlib import Path
import verify_active_launch_timer_v1520 as source
ROOT=source.ROOT;OUT=ROOT/'audit_v1541_active_launch_checkpoint'
def verify():
 pins={};mutable={}
 def pin(p,wanted=None):
  p=Path(p);key=str(p.resolve())
  if key not in pins and key not in mutable:
   got=source.sha(p)
   # User controls are runtime settings, not immutable compiled source. Verify
   # their captured hashes now, but do not require users to keep them unchanged.
   dest=mutable if 'diagnostic_v1411_native_grab_audio' in key and '/play/cfg/' in key.replace('\\','/')else pins
   dest[key]=got
  got=pins.get(key,mutable.get(key));assert wanted is None or got==wanted,'Changed current evidence '+key
 previous=ROOT/'audit_v1497_sonya_launch_audio_checkpoint/checkpoint.json'
 pin(previous,'E0CEA6A1E5640040AC57B8EBB7F1E2CD9EE6C6E4F547B34C9EC25C3476F60FA1')
 old=json.loads(previous.read_text());assert not old['fullPortAccepted']
 names=['audit_v1520_active_launch_timer_checked','audit_v1522_active_launch_ui_checked','audit_v1523_active_launch_ground_shadow_checked','audit_v1524_active_launch_human_matrix_checked','audit_v1525_active_launch_cpu_display_checked','audit_v1535_active_launch_interruption_checked','audit_v1537_active_launcher_checked','audit_v1538_discarded_timer_build_cleanup','audit_v1540_cpu_audio_divergence']
 reports={}
 for name in names:
  path=ROOT/name/'report.json';data=json.loads(path.read_text(encoding='utf-8-sig'));assert data['passed'];pin(path)
  for p,h in data.get('inputHashes',{}).items():pin(p,h)
  for key in ('keptHashes','retainedHashes'):
   for p,h in data.get(key,{}).items():pin(p,h)
  reports[name]=dict(passed=True,sha256=source.sha(path))
 matrix=json.loads((ROOT/'audit_v1524_active_launch_human_matrix_checked/report.json').read_text());assert matrix['current52CaseHumanStateMatrixAccepted']and matrix['exactPriorActualFullScreensMatched']==156
 interrupted=json.loads((ROOT/'audit_v1535_active_launch_interruption_checked/report.json').read_text());assert interrupted['acceptedActualIncomingHitCases']==3 and len(interrupted['counterexamples'])==24 and interrupted['bothSlotsBicycleInterruptionAccepted']and not interrupted['bothSlotsSquareInterruptionAccepted']
 failed=ROOT/'audit_v1526_active_launch_repeated_cpu_checked/report.json';data=json.loads(failed.read_text());assert not data['passed'];pin(failed)
 divergence=json.loads((ROOT/'audit_v1540_cpu_audio_divergence/report.json').read_text());assert divergence['oldRepeatReproduced']and divergence['firstActualStateDivergence']['frame']==2141 and divergence['activeOnlyAndAlwaysPollingSharedCPUStatesExact']
 cleanup=json.loads((ROOT/'audit_v1538_discarded_timer_build_cleanup/report.json').read_text());assert not Path(cleanup['removedDirectory']).exists();assert sum(q['bytes']for q in cleanup['inventory'])==cleanup['removedLogicalBytes']==110569233
 assert sum(q['allocatedBytes']for q in cleanup['inventory'])==cleanup['removedAllocatedBytes']==44445000
 for folder in ROOT.iterdir():
  match=re.match(r'^audit_v(\d+)_',folder.name)
  if folder.is_dir()and match and 1498<=int(match[1])<=1540:
   for p in folder.rglob('*'):
    if p.is_file():pin(p)
 for folder in (ROOT,ROOT/'tools'):
  for p in folder.iterdir():
   match=re.search(r'_v(\d+)\.(?:lua|ps1|py)$',p.name)
   if p.is_file()and match and 1498<=int(match[1])<=1541:pin(p)
 pin(ROOT/'PLAY_CURRENT_V1517_TEST_BUILD.cmd');pin(ROOT/'PLAY_CURRENT_V1411_TEST_BUILD.cmd','478544235F65C147A0D88A34D2EDEB928FA13ED8B1B06EF8FA8D847282074C12')
 pin(ROOT/'STATUS_2026-10-03_V1517_ACTIVE_LAUNCH_AUDIO.md');pin(__file__)
 return dict(candidate=source.NAME,playableCandidate=source.NAME,currentTestLauncher='PLAY_CURRENT_V1517_TEST_BUILD.cmd',previousPlayableRetained=True,launcherPromotedAsDevelopmentPlaytest=True,previousCheckpoint=str(previous),previousCheckpointSHA256=source.sha(previous),previousPinsBoundByManifest=len(old['inputHashes']),previousPinsIndividuallyRehashedThisCheckpoint=False,freshReports=reports,humanCasesAccepted=52,priorNativeHumanEventsExact=True,priorFullScreensMatched=156,bothSlotUICasesAccepted=4,boundedDeadPoolGroundShadowCasesAccepted=4,boundedCPUFixturesAccepted=3,exactCPUScanouts=263,finiteBothSlotLaunchAudioCasesAccepted=4,actualIncomingHitCasesAccepted=3,incomingHitCounterexamplesRejected=24,bothSlotsBicycleInterruptionAccepted=True,bothSlotsSquareInterruptionAccepted=False,repeatedCPUFixtureAccepted=False,previousRepeatReproduced=True,firstCPUStateDivergence=2141,idleTimerExplainsCPUDiscrepancy=False,canonicalSourcesAndInstalledExeRestored=True,discardedBuildLogicalBytesRemoved=110569233,discardedBuildAllocatedBytesRemoved=44445000,discardedBuildSourceAndLogsPreserved=True,allOldBuildFoldersDeleted=False,releaseZIPUpdated=False,fullAIRepertoireAccepted=False,allMoveAudioAndChoreographyAccepted=False,fullCampaignAccepted=False,fullPortAccepted=False,mutableSettingsAtCapture=mutable,mutableSettingsExcludedFromImmutablePins=True,inputHashes=pins)
if __name__=='__main__':
 assert not OUT.exists()
 report=verify();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(freshPins=len(report['inputHashes']),playable=report['playableCandidate'],actualHitCases=report['actualIncomingHitCasesAccepted'],fullPortAccepted=False)),flush=True)
