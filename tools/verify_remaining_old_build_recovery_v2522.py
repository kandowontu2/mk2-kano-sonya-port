"""Independent entire68build recovery verification before/after exact native deletion."""
import argparse,ctypes,hashlib,json,ntpath,tarfile
from pathlib import Path
from collections import defaultdict
import verify_current_interrupt_v1870 as launch
ROOT=launch.ROOT
SOURCE=ROOT/'audit_v2504_remaining_obsolete_build_inventory/report.json'
PREP=ROOT/'audit_v2518_remaining_old_build_recovery/report.json'
FINAL=ROOT/'audit_v2523_remaining_old_build_cleanup/report.json'
def need(ok,label):
 if not ok:raise ValueError(label)
def norm(path):return ntpath.normcase(ntpath.normpath(str(path)))
kernel=ctypes.WinDLL('kernel32',use_last_error=True);size=kernel.GetCompressedFileSizeW
size.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32));size.restype=ctypes.c_uint32
def allocated(path):
 high=ctypes.c_uint32();ctypes.set_last_error(0);low=size(str(path),ctypes.byref(high));need(low!=0xffffffff or ctypes.get_last_error()==0,'Actual allocation');return(high.value<<32)|low
def verify(final):
 original=json.loads(SOURCE.read_text());prep=json.loads(PREP.read_text())
 need(original['passed']and prep['passed']and not prep['filesDeleted'],'Actual non-destructive inventory/complete archive preparation')
 names=[r['name']for r in original['remainingUnreferencedBuildFolders']]
 need(len(set(names))==68 and prep['targetDirectories']==[str(ROOT/n)for n in names],'Exact68 original old-build targets')
 need('diagnostic_v1836_ball_register_boundary'not in names and 'diagnostic_v1597_native_ground_throw'not in names and 'diagnostic_v1250_native_correct_rom_metadata'not in names,'Current build and required native source dependencies never targets')
 archive=ROOT/'audit_v2518_remaining_old_build_recovery/remaining_68_builds_complete_recovery.tar.xz'
 need(norm(prep['recoveryArchive'])==norm(archive)and archive.is_file()and not archive.stat().st_file_attributes&0x400,'Exact regular archive inside intended recovery directory')
 need(launch.sha(archive)==prep['recoveryArchiveSHA256'],'Complete archive unchanged')
 records={r['path']:r for r in prep['inventory']};directories=set(prep['preservedDirectories'])
 need(len(records)==465 and len(directories)==352 and sum(r['bytes']for r in records.values())==7456052181,'Exact original465files/352directories/lengths')
 seen=set();seen_dirs=set();total=0
 with tarfile.open(archive,mode='r|xz')as packed:
  for item in packed:
   name=item.name.rstrip('/')
   need(name and name.split('/')[0]in names and not name.startswith('/')and ':'not in name and '\\'not in name and all(p not in('..','.')for p in name.split('/')),'Canonical safe exact original member path')
   need(not item.issym()and not item.islnk(),'Recovery has no links')
   if item.isdir():need(name in directories and name not in seen_dirs,'Every directory exactly once');seen_dirs.add(name)
   else:
    need(item.isfile()and name in records and name not in seen,'Every regular file exactly once');record=records[name]
    need(item.size==record['bytes'],'Exact original length');digest=hashlib.sha256();count=0
    with packed.extractfile(item)as stream:
     for block in iter(lambda:stream.read(1024*1024),b''):digest.update(block);count+=len(block)
    need(count==record['bytes']and digest.hexdigest().upper()==record['sha256'],'Every old source/config/ROM/EXE/snapshot byte independently recovered')
    seen.add(name);total+=count
 need(seen==set(records)and seen_dirs==directories,'Entire original file and directory topology; no omissions/additions')
 pins=dict(prep['inputHashes']);pins[str(SOURCE)]=launch.sha(SOURCE);pins[str(PREP)]=launch.sha(PREP)
 frontiers=[Path(p)for p in original['dependencyFrontiers']]+[ROOT/'audit_v2474_current_shao_crouch_exit_checkpoint/checkpoint.json',ROOT/'audit_v2508_current_kano_p1_shao_duck_wait_checked/report.json',ROOT/'audit_v2508_current_sonya_p1_shao_duck_wait_checked/report.json']
 for name in('audit_v2511_current_kano_shao_duck_wait_input_counterexamples/report.json','audit_v2516_current_sonya_p1_shao_duck_wait_checked/report.json'):
  if(ROOT/name).is_file():frontiers.append(ROOT/name)
 prefix=norm(ROOT)+'\\';targets={n.casefold()for n in names}
 for path in frontiers:
  report=json.loads(path.read_text());need('inputHashes'in report,'Actual graph source present, including retained rejected controls')
  for file in report['inputHashes']:
   key=norm(file);need(not(key.startswith(prefix)and key[len(prefix):].split('\\')[0]in targets),'No active proof/launch dependency may be removed')
  pins[str(path)]=launch.sha(path)
 for file,wanted in pins.items():need(launch.sha(file)==wanted,'Retained current game/settings/sources/proofs/archive unchanged')
 if not final:
  actual_files=set();actual_dirs=set();groups=defaultdict(list)
  for name in names:
   folder=ROOT/name;need(folder.is_dir()and folder.resolve().parent==ROOT.resolve()and not folder.stat().st_file_attributes&0x400,'Exact existing non-reparse old folder inside workspace');actual_dirs.add(name)
   for path in folder.rglob('*'):
    meta=path.stat();need(not meta.st_file_attributes&0x400,'No reparse anywhere before removal');relative=path.relative_to(ROOT).as_posix()
    if path.is_dir():actual_dirs.add(relative)
    else:
     need(path.is_file()and relative in records,'No unexpected original file before removal');record=records[relative]
     need(meta.st_size==record['bytes']and launch.sha(path)==record['sha256'],'Every original file still byte-identical immediately before deletion')
     need(meta.st_dev==record['volumeID']and meta.st_ino==record['fileID']and meta.st_nlink==record['hardlinkCount']and allocated(path)==record['allocatedBytes'],'Real original identity/allocation/hardlink count unchanged')
     groups[meta.st_dev,meta.st_ino].append(record);actual_files.add(relative)
  need(actual_files==set(records)and actual_dirs==directories,'Entire exact current original tree, no additional file/directory to lose')
  reclaimable=sum(group[0]['allocatedBytes']for group in groups.values()if len(group)==group[0]['hardlinkCount'])
  need(reclaimable==prep['originalReclaimableUniqueAllocatedBytes'],'Only unique allocation with every hardlink inside targets counted')
 else:
  need(all(not(ROOT/n).exists()for n in names),'All exact68 obsolete targets absent after native removal')
  retirement=json.loads(FINAL.read_text(encoding='utf-8-sig'))
  need(retirement['passed']and retirement['filesDeleted']and retirement['removedDirectories']==prep['targetDirectories'],'Exact authoritative native deletion report')
  for file,wanted in retirement['inputHashes'].items():need(launch.sha(file)==wanted,'Final retained dependencies unchanged');pins[file]=wanted
  pins[str(FINAL)]=launch.sha(FINAL)
 cost=allocated(archive);need(cost==prep['recoveryArchiveAllocatedBytes'],'Recovery actual allocation unchanged')
 savings=prep['originalReclaimableUniqueAllocatedBytes']-cost;need(savings>0 and savings==prep['netAllocatedSavingsIfExactTargetsRemoved'],'Real allocated savings, not logical byte count or double-counted hardlinks')
 pins[str(Path(__file__).resolve())]=launch.sha(__file__);launch.module_pins(pins)
 return dict(passed=True,phase='final'if final else'pre-delete',filesDeleted=final,
  verifiedFiles=465,verifiedDirectories=352,verifiedLogicalBytes=total,targetDirectories=prep['targetDirectories'],
  recoveryArchive=str(archive),recoveryArchiveSHA256=launch.sha(archive),recoveryArchiveAllocatedBytes=cost,
  originalReclaimableUniqueAllocatedBytes=prep['originalReclaimableUniqueAllocatedBytes'],netAllocatedSavings=savings,
  all68PreviouslyUnreferencedBuildFoldersRemoved=final,allOldBuildFoldersRemoved=False,
  currentAndRequiredNativeDependencyBuildsRetained=True,inputHashes=pins,fullPortAcceptance=False,scope=__doc__)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--final',action='store_true');p.add_argument('--output',type=Path,required=True);a=p.parse_args();need(not a.output.exists(),'Immutable independent full recovery check')
 r=verify(a.final);a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items()if k not in('inputHashes','targetDirectories')},indent=2),flush=True)
