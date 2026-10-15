"""Bind fresh playtest/CPU evidence; keep the full natural integration goal open."""
import json,re
from pathlib import Path
import verify_native_grab_audio_v1415 as source
ROOT=source.ROOT;NAME=source.NAME;OUT=ROOT/'audit_v1467_playable_and_sonya_cpu_checkpoint'

def verify():
 pins={};reports={}
 def pin(path,wanted=None):
  path=Path(path);key=str(path)
  if key not in pins:pins[key]=source.prior.digest(path)
  assert wanted is None or pins[key]==wanted,'Changed evidence '+key
 previous=ROOT/'audit_v1428_native_grab_audio_checkpoint/checkpoint.json'
 pin(previous,'E72A4825FDE7E8922B63C2CEF2D811C03E5DD90D06D39837B0E1E8B34FE4644B')
 prior=json.loads(previous.read_text());assert prior['candidate']==NAME and prior['fullPortAccepted']is False
 checks=('audit_v1435_grab_audio_human_matrix_checked','audit_v1433_grab_audio_ui_checked',
  'audit_v1434_grab_audio_ground_shadow_checked','audit_v1437_current_launcher_checked',
  'audit_v1454_sonya_cpu_display_checked','audit_v1458_physical_cpu_counterexamples',
  'audit_v1464_repeated_sonya_cpu_display_checked','audit_v1465_repeated_cpu_counterexamples')
 data={}
 for name in checks:
  path=ROOT/name/'report.json';result=json.loads(path.read_text(encoding='utf-8-sig'));pin(path)
  assert result['passed'] and result['candidate']==NAME
  for p,h in result['inputHashes'].items():pin(p,h)
  data[name]=result;reports[name]=dict(passed=True,sha256=pins[str(path)])
 matrix=data[checks[0]];assert len(matrix['cases'])==52 and matrix['positiveCases']==18 and matrix['negativeCases']==34 and matrix['exactPriorActualFullScreensMatched']==156
 assert len(data[checks[1]]['cases'])==len(data[checks[2]]['cases'])==4
 launcher=data[checks[3]];assert launcher['exit_code']==0 and launcher['ordinary_boot_from_other_working_directory']and launcher['diagnostic_autoboot_used']is False
 cpu=data[checks[4]];assert len(cpu['cases'])==3
 assert {(r['paired']['CPU_slot'],r['paired']['human_slot'],r['player'])for r in cpu['cases'].values()}=={(2,1,'kano'),(2,1,'sonya'),(1,2,'sonya')}
 assert sum(r['sampled_frames']for r in cpu['cases'].values())==264
 units=data[checks[5]];assert len(units['counterexamples'])==43 and all(r['rejected']for r in units['counterexamples'])
 repeated=data[checks[6]];assert len(repeated['cases'])==1
 case=next(iter(repeated['cases'].values()));assert case['sampled_frames']==121
 pairs=case['paired']['pairs'];assert len(pairs)==2 and sum(p['damage']for p in pairs)==70 and all(p['held_fields']==46 and p['passed']for p in pairs)
 repeat_units=data[checks[7]];assert len(repeat_units['counterexamples'])==10 and all(r['rejected']for r in repeat_units['counterexamples'])
 for folder in ROOT.iterdir():
  match=re.match(r'^audit_v(\d+)_',folder.name)
  if folder.is_dir()and match and 1429<=int(match[1])<=1465:
   for path in folder.rglob('*'):
    if path.is_file():pin(path)
 for parent in (ROOT,ROOT/'tools'):
  for path in parent.iterdir():
   match=re.search(r'_v(\d+)\.(?:lua|py|ps1)$',path.name)
   if path.is_file()and match and 1429<=int(match[1])<=1467:pin(path)
 for name,h in (
  ('mame-mkp/src/mame/midway/midtunit_m.cpp','EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34'),
  ('mame-mkp/src/mame/midway/midtunit.cpp','07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85'),
  ('mame-mkp/mkport.exe','413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'),
  ('PLAY_CURRENT_V1340_TEST_BUILD.cmd','E250F5673C26A3F8A08565B6FEA40B1AD8BE41AD57813BB15C6293547CC4EBA2'),
  ('PLAY_CURRENT_V1250_TEST_BUILD.cmd','8327B3DF7DCB577B38EAB82F922FE84C3564FC2C0259ADC63045701A94A45826'),
  ('PLAY_CURRENT_V1411_TEST_BUILD.cmd','478544235F65C147A0D88A34D2EDEB928FA13ED8B1B06EF8FA8D847282074C12')):pin(ROOT/name,h)
 pin(ROOT/'STATUS_2026-10-03_V1411_PLAYABLE_AND_SONYA_CPU.md')
 return dict(candidate=NAME,playableCandidate=NAME,currentTestLauncher='PLAY_CURRENT_V1411_TEST_BUILD.cmd',launcherPromoted=True,
  previousCheckpoint=str(previous),previousCheckpointSHA256=pins[str(previous)],previousPinsBoundByManifest=len(prior['inputHashes']),previousPinsIndividuallyRehashedThisCheckpoint=False,
  freshReports=reports,current52CaseHumanStateMatrixAccepted=True,exactPriorHumanFullScreensMatched=156,bothSlotsBoundedUIAccepted=True,
  boundedDeadPoolGroundShadowAccepted=True,ordinaryCMDColdBootAccepted=True,SonyaCPUBoundedPhysicalSlots=[1,2],
  SonyaCPUDistinctFixturesAccepted=4,SonyaCPUCompletedPairsChecked=5,SonyaCPURepeatedContactsAccepted=True,
  SonyaCPUFullRepertoireAccepted=False,SonyaCPUSampledScanoutsChecked=385,CPUCounterexamplesRejected=53,
  canonicalHistoricalSourcesAndInstalledExeRestored=True,olderPlaytestLaunchersUnchanged=True,gameSourceChangedThisTurn=False,
  interactivePlayCfgAndNvramIntentionallyNotPinned=True,allMoveAudioAccepted=False,allCPURepertoireAccepted=False,
  allArenasAccepted=False,broaderFullGameIntegrationPending=True,releaseZIPUpdated=False,oldBuildFoldersDeleted=False,
  materialFilesDeleted=False,fullPortAccepted=False,inputHashes=pins)

if __name__=='__main__':
 assert not OUT.exists()
 try:
  report=verify();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
  print('Saved checkpoint: '+str(len(report['inputHashes']))+' fresh pins; playable1411; actual Sonya CPU slots1/2; full goal remains active',flush=True)
 except Exception as error:
  OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(error=repr(error),fullPortAccepted=False),indent=2)+'\n');raise
