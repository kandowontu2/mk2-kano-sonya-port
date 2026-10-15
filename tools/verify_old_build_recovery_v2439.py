"""Independently verify six recoverable removals, not all-old-build cleanup."""
import json,hashlib,zipfile,argparse
from pathlib import Path
import verify_current_interrupt_v1870 as launch
ROOT=launch.ROOT

def verify():
 path=ROOT/'audit_v2430_unreferenced_old_build_recovery/report.json'
 report=json.loads(path.read_text(encoding='utf-8-sig'))
 assert report['passed'] and not report['fullPortAcceptance'] and not report['allOldBuildFoldersRemoved']
 assert report['currentCheckpointTargetReferences']==0 and report['archiveEveryEntryAndSourceHashVerified']
 assert report['currentBuildSettingsAndPlaytestZIPUnchanged']
 names=('diagnostic_v277_native_battle_photos','diagnostic_v1329_native_ring_startup_core',
  'diagnostic_v1340_native_ring_lookup','diagnostic_v1411_native_grab_audio',
  'diagnostic_v1473_sonya_launch_audio','diagnostic_v1517_active_launch_timer')
 assert report['removedDirectories']==[str(ROOT/n)for n in names]
 assert all(not(ROOT/n).exists()for n in names)
 pins={str(path):launch.sha(path)}
 for file,wanted in report['keptHashes'].items():
  assert launch.sha(file)==wanted,'Unchanged canonical build/settings/checkpoint/cleaner '+file
  pins[file]=wanted
 inventory=report['inventory'];archive=Path(report['recoveryZIP'])
 assert len(inventory)==report['archivedFiles']==99 and launch.sha(archive)==report['recoveryZipSHA256']
 assert sum(r['bytes']for r in inventory)==report['removedLogicalBytes']==661440530
 assert sum(r['allocatedBytes']for r in inventory)==report['removedAllocatedBytes']
 assert report['netBuildStorageReductionBytes']==report['removedAllocatedBytes']-report['recoveryArchiveAllocatedBytes']==90457245
 with zipfile.ZipFile(archive)as z:
  entries=z.infolist();assert len({r.filename for r in entries})==len(entries)
  assert sum(r.is_dir()for r in entries)==report['preservedDirectoryEntries']
  files={r.filename:r for r in entries if not r.is_dir()}
  assert set(files)=={r['path']for r in inventory}
  assert all(p.split('/')[0]in names and not p.startswith('/')and '..'not in p.split('/')and ':'not in p for p in z.namelist())
  for r in inventory:
   assert files[r['path']].file_size==r['bytes']
   digest=hashlib.sha256()
   with z.open(r['path'])as stream:
    for block in iter(lambda:stream.read(1024*1024),b''):digest.update(block)
   assert digest.hexdigest().upper()==r['sha256'],'Every archived source/config/ROM/EXE/snapshot exact'
 checkpoint=json.loads((ROOT/'audit_v2407_current_shao_opening_guard_checkpoint/checkpoint.json').read_text())
 for file in checkpoint['inputHashes']:
  assert not any(Path(file).resolve().is_relative_to(ROOT/n)for n in names),'No active evidence lost'
 assert 'PLAY_CURRENT_V1836_CHECKED.cmd'in (ROOT/'PLAY_MK2_KANO_SONYA.cmd').read_text()
 pins[str(archive)]=report['recoveryZipSHA256'];pins[str(Path(__file__).resolve())]=launch.sha(__file__)
 launch.module_pins(pins)
 return dict(passed=True,removedOldBuildFolders=6,archivedExactFiles=99,
  reclaimedAllocatedBytes=90457245,recoveryZIP=str(archive),inputHashes=pins,
  currentBuildAndSettingsUnchanged=True,allOldBuildFoldersRemoved=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 assert not a.output.exists(),'Immutable recovery verification'
 r=verify();a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items()if k!='inputHashes'},indent=2),flush=True)
