"""Preserve the current matched launcher and full preceding proof/failures."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'audit_v1248_current_launcher_checkpoint';assert not OUT.exists()
pins={}
def digest(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as stream:
  for block in iter(lambda:stream.read(4*1024*1024),b''):h.update(block)
 return h.hexdigest().upper()
def pin(path,wanted=None):
 path=Path(path);key=str(path);actual=pins[key] if key in pins else digest(path)
 assert wanted is None or wanted==actual,'Changed evidence '+key;pins[key]=actual
previous_path=ROOT/'audit_v1242_secondary_native_human_checkpoint/checkpoint.json';previous=json.loads(previous_path.read_text())
print('Revalidating',len(previous['inputHashes']),'native/human checkpoint pins',flush=True)
for file,wanted in previous['inputHashes'].items():pin(file,wanted)
pin(previous_path)
failed_path=ROOT/'audit_v1245_current_launcher_checked/report.json';failed=json.loads(failed_path.read_text(encoding='utf-8-sig'));pin(failed_path)
assert failed['passed'] is False and failed['exit_code']==1
for file,wanted in failed['input_hashes'].items():
 source=Path(file)
 if source.name=='PLAY_CURRENT_V1219_TEST_BUILD.cmd':source=ROOT/'audit_v1245_current_launcher_checked/input_sources'/source.name
 pin(source,wanted)
passed_path=ROOT/'audit_v1247_current_launcher_checked/report.json';passed=json.loads(passed_path.read_text(encoding='utf-8-sig'));pin(passed_path)
assert passed['passed'] and passed['exit_code']==0 and passed['candidate']==previous['candidate'] and passed['ordinary_boot_from_other_working_directory'] and passed['settings_isolated'] and not passed['diagnostic_autoboot_used'] and not passed['older_launchers_changed']
for file,wanted in passed['input_hashes'].items():pin(file,wanted)
for folder in ('audit_v1245_current_launcher_checked','audit_v1247_current_launcher_checked'):
 for path in (ROOT/folder).rglob('*'):
  if path.is_file():pin(path)
for file in ('PLAY_CURRENT_V1219_TEST_BUILD.cmd','tools/check_current_playtest_v1244.ps1','tools/check_current_playtest_v1246.ps1',
 'tools/test_current_launcher_v1245.ps1','tools/test_current_launcher_v1247.ps1','tools/save_current_launcher_checkpoint_v1248.py',
 'STATUS_2026-10-03_CURRENT_TEST_LAUNCHER.md'):
 pin(ROOT/file)
record={k:v for k,v in previous.items() if k not in ('inputHashes','historicalPinsRevalidated','launchersChanged')}
record.update(historicalPinsRevalidated=len(previous['inputHashes']),currentTestLauncher='PLAY_CURRENT_V1219_TEST_BUILD.cmd',
 currentTestLauncherMatchedSHA256BeforeStartup=True,currentCMDOrdinaryBootAccepted=True,currentCMDInteractiveVideoAudioAccepted=False,
 launchersChanged=True,olderLaunchersChanged=False,settingsIsolated=True,preservedInitialWindowsPowerShellBootFailure=True,
 materialDataDeleted=False,goalComplete=False,fullPortAccepted=False,inputHashes=pins)
OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(record,indent=2)+'\n')
print('Current matched CMD checkpoint saved; total pins',len(pins),'; full goal remains incomplete',flush=True)
