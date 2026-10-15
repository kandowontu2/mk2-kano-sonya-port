"""Independent complete old-build TAR recovery check, before/after exact ZIP retirement."""
import argparse,ctypes,hashlib,json,tarfile
from pathlib import Path
import verify_current_interrupt_v1870 as launch
ROOT=launch.ROOT
ORIGINAL=ROOT/'audit_v2483_next_unreferenced_old_build_recovery/report.json'
PREP=ROOT/'audit_v2486_next_old_build_solid_recovery/report.json'
FINAL=ROOT/'audit_v2487_next_old_build_solid_recovery_final/report.json'
NAMES=('diagnostic_v249_battle_card_aligned_trial','diagnostic_v260_skeleton_winner_hold_trial',
 'diagnostic_v261_victim_pull_sync_trial','diagnostic_v262_native_jax_body_trial','diagnostic_v263_native_stock_body_trial',
 'diagnostic_v264_native_stock_body_trial','diagnostic_v265_skeleton_facing_trial','diagnostic_v267_sonya_native_arc_trial',
 'diagnostic_v268_sonya_arc_register_trial','diagnostic_v269_sonya_arc_contact_trial')
FRONTIERS=('audit_v2460_current_native_crouch_jump_checkpoint/checkpoint.json',
 'audit_v2465_current_kano_p1_shao_crouch_exit_checked/report.json',
 'audit_v2465_current_sonya_p1_shao_crouch_exit_checked/report.json',
 'audit_v2479_current_sonya_p1_shao_crouch_exit_checked/report.json',
 'audit_v2467_current_kano_shao_crouch_exit_escape_boss_ledger_checked/report.json',
 'audit_v2467_current_sonya_shao_crouch_exit_escape_boss_ledger_checked/report.json',
 'audit_v2469_current_kano_shao_crouch_exit_escape_input_counterexamples/report.json',
 'audit_v2469_current_sonya_shao_crouch_exit_escape_input_counterexamples/report.json',
 'audit_v2481_current_sonya_crouch_exit_extended_boundary/report.json')
def need(ok,label):
 if not ok:raise ValueError(label)
def allocated(path):
 kernel=ctypes.WinDLL('kernel32',use_last_error=True);fn=kernel.GetCompressedFileSizeW
 fn.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32));fn.restype=ctypes.c_uint32
 high=ctypes.c_uint32();ctypes.set_last_error(0);low=fn(str(path),ctypes.byref(high))
 need(low!=0xffffffff or ctypes.get_last_error()==0,'Actual allocated bytes available')
 return (high.value<<32)|low
def canonical(path):return str(Path(path).resolve()).casefold()
def verify(final):
 original=json.loads(ORIGINAL.read_text(encoding='utf-8-sig'));prep=json.loads(PREP.read_text())
 need(original['passed']and prep['passed']and not prep['oldZIPDeleted'],'Accepted original cleanup and non-destructive packing')
 need(original['removedDirectories']==[str(ROOT/n)for n in NAMES]and all(not(ROOT/n).exists()for n in NAMES),'Only exact ten retired original folders')
 old=ROOT/'audit_v2483_next_unreferenced_old_build_recovery/ten_unreferenced_builds_complete_recovery.zip'
 archive=ROOT/'audit_v2486_next_old_build_solid_recovery/ten_unreferenced_builds_complete_recovery.tar.xz'
 need(canonical(prep['oldZIP'])==canonical(old)and canonical(prep['newRecoveryArchive'])==canonical(archive),'Exact recovery containers inside named workspace folders')
 need(archive.is_file()and not archive.is_symlink()and launch.sha(archive)==prep['newRecoveryArchiveSHA256'],'Unchanged solid recovery archive')
 need(final==not old.exists(),'Exact expected ZIP retirement phase')
 if not final:need(old.is_file()and not old.is_symlink()and launch.sha(old)==prep['oldZipSHA256']==original['recoveryZipSHA256'],'Original ZIP retained unchanged until independent full roundtrip')
 records={r['path']:r for r in original['inventory']};need(len(records)==61,'Exact61 original file records')
 directories=set()
 for name in NAMES:directories.add(name)
 for name in records:
  parent=Path(name).parent
  while str(parent)!='.':directories.add(parent.as_posix());parent=parent.parent
 need(len(directories)==37,'Exact37 original directory topology')
 seen=set();seen_dirs=set();total=0
 with tarfile.open(archive,mode='r|xz')as packed:
  for member in packed:
   name=member.name.rstrip('/')
   need(name and name.split('/')[0]in NAMES and not name.startswith('/')and ':'not in name and '\\'not in name and all(p not in('.','..')for p in name.split('/')),'Safe canonical relative member')
   need(not member.issym()and not member.islnk(),'No recovery links')
   if member.isdir():need(name in directories and name not in seen_dirs,'Exact unique original directory');seen_dirs.add(name)
   else:
    need(member.isfile()and name in records and name not in seen,'Exact unique original regular file')
    item=records[name];need(member.size==item['bytes'],'Exact original file length')
    digest=hashlib.sha256();read=0
    with packed.extractfile(member)as stream:
     for data in iter(lambda:stream.read(1024*1024),b''):digest.update(data);read+=len(data)
    need(read==item['bytes']and digest.hexdigest().upper()==item['sha256'],'Every original recovery byte independently verified')
    seen.add(name);total+=read
 need(seen==set(records)and seen_dirs==directories and total==1086141247,'Entire original file/directory topology, no omissions or additions')
 pins=dict(prep['inputHashes'])
 for relative in FRONTIERS:
  path=ROOT/relative;report=json.loads(path.read_text());keys=report['inputHashes']
  need(all(canonical(file)!=canonical(old)for file in keys),'Redundant ZIP not an active dependency')
  need(all(not any(canonical(file)==canonical(ROOT/n)or canonical(file).startswith(canonical(ROOT/n)+'\\')for n in NAMES)for file in keys),'No active proof depends on retired builds')
  pins[str(path)]=launch.sha(path)
 for file,wanted in pins.items():need(launch.sha(file)==wanted,'All retained current artifacts/settings/proofs/source unchanged')
 allocation=allocated(archive);need(allocation==prep['newRecoveryArchiveAllocatedBytes'],'Solid archive allocation unchanged')
 net=original['removedAllocatedBytes']-allocation;need(net>0 and net==prep['netOriginalBuildAllocationSavingsIfOldZIPRemoved'],'Real allocated disk savings, not logical bytes')
 if final:
  retirement=json.loads(FINAL.read_text(encoding='utf-8-sig'))
  need(retirement['passed']and retirement['oldZIPDeleted']and retirement['netOriginalBuildAllocationSavings']==net,'Exact verified final ZIP retirement')
  for file,wanted in retirement['inputHashes'].items():need(launch.sha(file)==wanted,'Final retirement graph unchanged');pins[file]=wanted
  pins[str(FINAL)]=launch.sha(FINAL)
 pins[str(ORIGINAL)]=launch.sha(ORIGINAL);pins[str(PREP)]=launch.sha(PREP);pins[str(Path(__file__).resolve())]=launch.sha(__file__)
 launch.module_pins(pins)
 return dict(passed=True,phase='final'if final else 'pre-delete',verifiedFiles=61,verifiedDirectories=37,verifiedLogicalBytes=total,
  removedDirectories=original['removedDirectories'],oldZIP=str(old),oldZipSHA256=original['recoveryZipSHA256'],oldZIPDeleted=final,
  recoveryArchive=str(archive),recoveryArchiveSHA256=launch.sha(archive),recoveryArchiveAllocatedBytes=allocation,
  originalRemovedAllocatedBytes=original['removedAllocatedBytes'],netOriginalBuildAllocationSavings=net,
  allCurrentPlayableAndSettingsUnchanged=True,allOldBuildFoldersRemoved=False,
  inputHashes=pins,fullPortAcceptance=False,scope=__doc__)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--final',action='store_true');parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 need(not args.output.exists(),'Immutable independent recovery verification')
 result=verify(args.final);args.output.mkdir();(args.output/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items()if k!='inputHashes'},indent=2),flush=True)
