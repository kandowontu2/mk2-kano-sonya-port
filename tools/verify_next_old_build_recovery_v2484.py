"""Independently verify ten recoverable removals, not all-old-build cleanup."""
import json,hashlib,zipfile,argparse
from pathlib import Path
import verify_current_interrupt_v1870 as launch
ROOT=launch.ROOT

def verify():
 path=ROOT/'audit_v2483_next_unreferenced_old_build_recovery/report.json'
 report=json.loads(path.read_text(encoding='utf-8-sig'))
 assert report['passed'] and not report['fullPortAcceptance'] and not report['allOldBuildFoldersRemoved']
 assert report['currentCheckpointTargetReferences']==0 and report['archiveEveryEntryAndSourceHashVerified']
 assert report['currentBuildSettingsAndPlaytestZIPUnchanged']
 names=["diagnostic_v249_battle_card_aligned_trial","diagnostic_v260_skeleton_winner_hold_trial","diagnostic_v261_victim_pull_sync_trial","diagnostic_v262_native_jax_body_trial","diagnostic_v263_native_stock_body_trial","diagnostic_v264_native_stock_body_trial","diagnostic_v265_skeleton_facing_trial","diagnostic_v267_sonya_native_arc_trial","diagnostic_v268_sonya_arc_register_trial","diagnostic_v269_sonya_arc_contact_trial"]
 assert report['removedDirectories']==[str(ROOT/n)for n in names]
 assert all(not(ROOT/n).exists()for n in names)
 pins={str(path):launch.sha(path)}
 for file,wanted in report['keptHashes'].items():
  assert launch.sha(file)==wanted,'Unchanged canonical build/settings/checkpoint/cleaner '+file
  pins[file]=wanted
 inventory=report['inventory'];archive=Path(report['recoveryZIP'])
 assert len(inventory)==report['archivedFiles']==61 and launch.sha(archive)==report['recoveryZipSHA256']
 assert sum(r['bytes']for r in inventory)==report['removedLogicalBytes']==1086141247
 assert sum(r['allocatedBytes']for r in inventory)==report['removedAllocatedBytes']
 assert report['netBuildStorageReductionBytes']==report['removedAllocatedBytes']-report['recoveryArchiveAllocatedBytes'] and report['netBuildStorageReductionBytes']>0
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
 expected_graphs=[ROOT/'audit_v2460_current_native_crouch_jump_checkpoint/checkpoint.json']+[ROOT/p for p in ["audit_v2465_current_kano_p1_shao_crouch_exit_checked/report.json","audit_v2465_current_sonya_p1_shao_crouch_exit_checked/report.json","audit_v2479_current_sonya_p1_shao_crouch_exit_checked/report.json","audit_v2467_current_kano_shao_crouch_exit_escape_boss_ledger_checked/report.json","audit_v2467_current_sonya_shao_crouch_exit_escape_boss_ledger_checked/report.json","audit_v2469_current_kano_shao_crouch_exit_escape_input_counterexamples/report.json","audit_v2481_current_sonya_crouch_exit_extended_boundary/report.json"]]
 assert report['dependencyFrontierGraphs']==[str(p)for p in expected_graphs],'Entire observed old/new accepted/rejected graph frontier checked'
 for graph in expected_graphs:
  checkpoint=json.loads(graph.read_text(encoding='utf-8-sig'))
  for file in checkpoint['inputHashes']:
   assert not any(Path(file).resolve().is_relative_to(ROOT/n)for n in names),'No active evidence lost'
 assert 'PLAY_CURRENT_V1836_CHECKED.cmd'in (ROOT/'PLAY_MK2_KANO_SONYA.cmd').read_text()
 pins[str(archive)]=report['recoveryZipSHA256'];pins[str(Path(__file__).resolve())]=launch.sha(__file__)
 launch.module_pins(pins)
 return dict(passed=True,removedOldBuildFolders=10,archivedExactFiles=61,
  reclaimedAllocatedBytes=report['netBuildStorageReductionBytes'],recoveryZIP=str(archive),inputHashes=pins,
  currentBuildAndSettingsUnchanged=True,allOldBuildFoldersRemoved=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 assert not a.output.exists(),'Immutable recovery verification'
 r=verify();a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items()if k!='inputHashes'},indent=2),flush=True)
