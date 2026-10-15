"""Freeze verified native audio progress without declaring/promoting release."""
import json,re
from pathlib import Path
import verify_ring_native_lookup_v1342 as old
ROOT=old.ROOT;OUT=ROOT/'audit_v1428_native_grab_audio_checkpoint';NAME='diagnostic_v1411_native_grab_audio'

def verify():
 pins={};reports={}
 def pin(path,wanted=None):
  path=Path(path);key=str(path)
  if key not in pins:pins[key]=old.digest(path)
  assert wanted is None or pins[key]==wanted,'Changed evidence '+key
 previous=ROOT/'audit_v1394_current_playtest_checkpoint/checkpoint.json'
 pin(previous,'F85BAC1BC19D631FA21154F8939F54F7B8584AC11A1B979D5086D0D8244D146A')
 previous_data=json.loads(previous.read_text());assert previous_data['fullPortAccepted'] is False and previous_data['playableCandidate']==old.CANDIDATE
 checks={
  'audit_v1402_current_cpu_pair_checked':old.CANDIDATE,
  'audit_v1408_current_move_audio_checked':old.CANDIDATE,
  'audit_v1415_native_grab_audio_checked':NAME,
  'audit_v1421_grab_defense_checked':NAME,
  'audit_v1424_grab_audio_cpu_checked':NAME,
  'audit_v1426_cpu_cycle_counterexamples':None}
 for name,candidate in checks.items():
  path=ROOT/name/'report.json';data=json.loads(path.read_text());pin(path)
  assert data['passed'] and (candidate is None or data['candidate']==candidate)
  for p,h in data['inputHashes'].items():pin(p,h)
  reports[name]=dict(passed=True,sha256=old.digest(path))
 audio=json.loads((ROOT/'audit_v1408_current_move_audio_checked/report.json').read_text());assert len(audio['cases'])==16 and audio['allMoveAudioAccepted'] is False
 delta=json.loads((ROOT/'audit_v1415_native_grab_audio_checked/report.json').read_text());assert len(delta['cases'])==6 and delta['wholeGuestIndependentlyReconstructed'] and delta['exactPriorActualFullScreensMatched']==18
 defense=json.loads((ROOT/'audit_v1421_grab_defense_checked/report.json').read_text());assert len(defense['cases'])==10 and defense['exactPriorActualFullScreensMatched']==30
 counters=json.loads((ROOT/'audit_v1426_cpu_cycle_counterexamples/report.json').read_text());assert len(counters['counterexamples'])==9 and all(q['rejected']for q in counters['counterexamples'])
 for folder in ROOT.iterdir():
  match=re.match(r'^audit_v(\d+)_',folder.name)
  if folder.is_dir() and match and 1395<=int(match[1])<=1426:
   for path in folder.rglob('*'):
    if path.is_file():pin(path)
 for parent in (ROOT,ROOT/'tools'):
  for path in parent.iterdir():
   match=re.search(r'_v(\d+)\.(?:lua|py|ps1)$',path.name)
   if path.is_file() and match and 1395<=int(match[1])<=1428:pin(path)
 for path in (ROOT/NAME).rglob('*'):
  if path.is_file():pin(path)
 for name,h in (
  ('mame-mkp/src/mame/midway/midtunit_m.cpp','EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34'),
  ('mame-mkp/src/mame/midway/midtunit.cpp','07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85'),
  ('mame-mkp/mkport.exe','413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'),
  ('PLAY_CURRENT_V1340_TEST_BUILD.cmd','E250F5673C26A3F8A08565B6FEA40B1AD8BE41AD57813BB15C6293547CC4EBA2')):pin(ROOT/name,h)
 pin(ROOT/'STATUS_2026-10-03_NATIVE_GRAB_AUDIO_V1411.md')
 return dict(candidate=NAME,playableCandidate=old.CANDIDATE,currentTestLauncher='PLAY_CURRENT_V1340_TEST_BUILD.cmd',launcherPromoted=False,
  previousCheckpoint=str(previous),previousCheckpointSHA256=old.digest(previous),previousPinsBoundByManifest=len(previous_data['inputHashes']),previousPinsIndividuallyRehashedThisCheckpoint=False,
  freshReports=reports,oldCandidateHumanAudioCases=16,newCandidateHumanAudioCases=6,newCandidateDefensiveCases=10,
  newCandidateExactPriorFullScreensMatched=48,newCandidateCPUSampledScanouts=179,CPUContinuationCounterexamplesRejected=9,
  canonicalHistoricalSourcesAndInstalledExeRestored=True,currentPlayableLauncherUnchanged=True,
  newCandidateBroadRegressionAndPromotionPending=True,allMoveAudioAccepted=False,SonyaCPUAccepted=False,
  broaderFullGameIntegrationPending=True,releaseZIPUpdated=False,oldBuildFoldersDeleted=False,materialFilesDeleted=False,fullPortAccepted=False,inputHashes=pins)

if __name__=='__main__':
 assert not OUT.exists()
 try:
  report=verify();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
  print('Native grab audio checkpoint saved: '+str(len(report['inputHashes']))+' fresh pins; playable1340 unchanged; full goal active',flush=True)
 except Exception as error:
  OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(error=repr(error),fullPortAccepted=False),indent=2)+'\n');raise
