"""Preserve concrete launch-audio progress without narrowing the full goal."""
import json,hashlib,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'audit_v1497_sonya_launch_audio_checkpoint'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def verify():
 pins={}
 def pin(p,h=None):
  p=Path(p);key=str(p.resolve());got=pins.setdefault(key,sha(p));assert h is None or got==h,'Changed source/evidence: '+key
 previous=ROOT/'audit_v1467_playable_and_sonya_cpu_checkpoint/checkpoint.json';pin(previous,'107B31831D2960A173E9C6DC17E12E40203A42C89CE7B8D414BF471733362336');old=json.loads(previous.read_text());assert not old['fullPortAccepted']
 reports={}
 for name in('audit_v1489_sonya_launch_audio_checked','audit_v1493_launch_interruption_checked','audit_v1496_old_compiler_cache_cleanup_checked'):
  path=ROOT/name/'report.json';data=json.loads(path.read_text());assert data['passed'];pin(path)
  for p,h in data['inputHashes'].items():pin(p,h)
  reports[name]=dict(passed=True,sha256=sha(path))
 sound=json.loads((ROOT/'audit_v1489_sonya_launch_audio_checked/report.json').read_text());assert len(sound['cases'])==10 and len(sound['liveChannels'])==4 and sound['wholeGuestIndependentlyReconstructed']
 interrupt=json.loads((ROOT/'audit_v1493_launch_interruption_checked/report.json').read_text());assert interrupt['acceptedActualIncomingHitCases']==1 and len(interrupt['counterexamples'])==7 and not interrupt['bicycleInterruptionAccepted']
 cleanup=json.loads((ROOT/'audit_v1496_old_compiler_cache_cleanup_checked/report.json').read_text());assert cleanup['removedLogicalCacheBytes']==22678330 and cleanup['logAdditionalAllocatedBytesReclaimed']==0
 for folder in ROOT.iterdir():
  m=re.match(r'^audit_v(\d+)_',folder.name)
  if folder.is_dir()and m and 1468<=int(m[1])<=1496:
   for path in folder.rglob('*'):
    if path.is_file():pin(path)
 for folder in(ROOT,ROOT/'tools'):
  for path in folder.iterdir():
   m=re.search(r'_v(\d+)\.(?:py|ps1|lua)$',path.name)
   if path.is_file()and m and 1468<=int(m[1])<=1497:pin(path)
 for name,wanted in [('mame-mkp/src/mame/midway/midtunit_m.cpp','EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34'),('mame-mkp/src/mame/midway/midtunit.cpp','07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85'),('mame-mkp/src/mame/midway/midtunit.h','256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644'),('mame-mkp/mkport.exe','413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'),('PLAY_CURRENT_V1411_TEST_BUILD.cmd','478544235F65C147A0D88A34D2EDEB928FA13ED8B1B06EF8FA8D847282074C12')]:pin(ROOT/name,wanted)
 pin(ROOT/'STATUS_2026-10-03_V1473_LAUNCH_AUDIO_CANDIDATE.md')
 return dict(candidate='diagnostic_v1473_sonya_launch_audio',playableCandidate='diagnostic_v1411_native_grab_audio',currentTestLauncher='PLAY_CURRENT_V1411_TEST_BUILD.cmd',launcherPromoted=False,previousCheckpoint=str(previous),previousCheckpointSHA256=sha(previous),previousPinsBoundByManifest=len(old['inputHashes']),previousPinsIndividuallyRehashedThisCheckpoint=False,freshReports=reports,originalLaunchCuesExtracted=3,nativeChannelVariantsPerCue=5,humanNativeStateCasesAccepted=10,priorFullScreensByteMatched=30,fullFiniteLiveChannelCasesAccepted=4,actualIncomingHitCasesAccepted=1,incomingHitCorruptionsRejected=7,bothSlotsInterruptionAccepted=False,bicycleInterruptionAccepted=False,canonicalSourcesAndInstalledExeRestored=True,deletedObsoleteCompilerCacheDirectories=2,deletedLogicalCacheBytes=22678330,deletedCachesRegenerableFromRetainedSource=True,allOldBuildFoldersDeleted=False,logAdditionalAllocatedBytesReclaimed=0,releaseZIPUpdated=False,allMoveAudioAccepted=False,fullAIRepertoireAccepted=False,fullCampaignAccepted=False,fullPortAccepted=False,inputHashes=pins)
if __name__=='__main__':
 assert not OUT.exists()
 report=verify();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'freshPins':len(report['inputHashes']),'candidate':report['candidate'],'playable':report['playableCandidate'],'fullPortAccepted':False}),flush=True)
