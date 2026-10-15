"""Stream verified obsolete-build recovery into a solid XZ/TAR; no deletion here."""
import json,zipfile,tarfile,lzma,hashlib,calendar,ctypes
from pathlib import Path
import verify_current_interrupt_v1870 as launch
ROOT=launch.ROOT
SOURCE=ROOT/'audit_v2483_next_unreferenced_old_build_recovery/report.json'
OUT=ROOT/'audit_v2486_next_old_build_solid_recovery'
NAMES=('diagnostic_v249_battle_card_aligned_trial','diagnostic_v260_skeleton_winner_hold_trial',
 'diagnostic_v261_victim_pull_sync_trial','diagnostic_v262_native_jax_body_trial','diagnostic_v263_native_stock_body_trial',
 'diagnostic_v264_native_stock_body_trial','diagnostic_v265_skeleton_facing_trial','diagnostic_v267_sonya_native_arc_trial',
 'diagnostic_v268_sonya_arc_register_trial','diagnostic_v269_sonya_arc_contact_trial')
def need(ok,label):
 if not ok:raise ValueError(label)
def allocated(path):
 kernel=ctypes.WinDLL('kernel32',use_last_error=True);fn=kernel.GetCompressedFileSizeW
 fn.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32));fn.restype=ctypes.c_uint32
 high=ctypes.c_uint32();ctypes.set_last_error(0);low=fn(str(path),ctypes.byref(high))
 need(low!=0xffffffff or ctypes.get_last_error()==0,'Actual NTFS allocation available')
 return(high.value<<32)|low
def verify_tar(path,inventory,directories):
 records={r['path']:r for r in inventory};seen=set();seen_dirs=set();total=0
 with tarfile.open(path,mode='r|xz')as archive:
  for member in archive:
   name=member.name.rstrip('/')
   need(name.split('/')[0]in NAMES and not name.startswith('/')and ':'not in name and '..'not in name.split('/'),'Safe exact old-build recovery member')
   need(not member.issym()and not member.islnk(),'No archive links')
   if member.isdir():
    need(name+'/'in directories and name not in seen_dirs,'Exact original directory, no duplication');seen_dirs.add(name)
   else:
    need(member.isfile()and name in records and name not in seen,'Exact original regular file, no duplication')
    record=records[name];need(member.size==record['bytes'],'Original file length')
    digest=hashlib.sha256()
    with archive.extractfile(member)as stream:
     for block in iter(lambda:stream.read(1024*1024),b''):digest.update(block)
    need(digest.hexdigest().upper()==record['sha256'],'Every solid-recovered source/ROM/EXE/config/snapshot byte exact')
    seen.add(name);total+=member.size
 need(seen==set(records)and {d+'/'for d in seen_dirs}==set(directories),'Entire original61files and37directories retained')
 return dict(verifiedFiles=len(seen),verifiedDirectories=len(seen_dirs),verifiedLogicalBytes=total)
def pack():
 need(not OUT.exists(),'Immutable solid recovery evidence')
 report=json.loads(SOURCE.read_text(encoding='utf-8-sig'))
 need(report['passed']and report['archivedFiles']==61 and report['preservedDirectoryEntries']==37,'Original verified recoverable removal')
 need(report['removedDirectories']==[str(ROOT/n)for n in NAMES]and all(not(ROOT/n).exists()for n in NAMES),'Exact ten obsolete folders already recoverably removed')
 old=Path(report['recoveryZIP']);expected=ROOT/'audit_v2483_next_unreferenced_old_build_recovery/ten_unreferenced_builds_complete_recovery.zip'
 need(old.resolve()==expected.resolve()and launch.sha(old)==report['recoveryZipSHA256'],'Exact unchanged original ZIP')
 for file,wanted in report['keptHashes'].items():need(launch.sha(file)==wanted,'Current build/launcher/settings/ZIP/dependency graph unchanged')
 OUT.mkdir();archive_path=OUT/'ten_unreferenced_builds_complete_recovery.tar.xz'
 inventory=report['inventory'];directories=[]
 with zipfile.ZipFile(old)as source:
  entries=source.infolist();need(len({e.filename for e in entries})==len(entries),'No original ZIP duplicate members')
  directories=[e.filename for e in entries if e.is_dir()]
  need(len(directories)==37 and {e.filename for e in entries if not e.is_dir()}=={r['path']for r in inventory},'Original ZIP entire exact inventory')
  with lzma.LZMAFile(archive_path,'wb',format=lzma.FORMAT_XZ,check=lzma.CHECK_CRC64,
    filters=[dict(id=lzma.FILTER_LZMA2,preset=4,dict_size=128*1024*1024)])as compressed:
   with tarfile.open(fileobj=compressed,mode='w|',format=tarfile.PAX_FORMAT)as target:
    for name in directories:
     info=tarfile.TarInfo(name);info.type=tarfile.DIRTYPE;info.mode=0o755;target.addfile(info)
    for index,record in enumerate(inventory,1):
     entry=source.getinfo(record['path']);info=tarfile.TarInfo(record['path']);info.size=entry.file_size;info.mode=0o644;info.mtime=calendar.timegm(entry.date_time+(0,0,-1))
     need(info.size==record['bytes'],'Original ZIP file length')
     with source.open(entry)as stream:target.addfile(info,stream)
     if index%10==0:print('Solid packed',index,'of61 verified original files',flush=True)
 verified=verify_tar(archive_path,inventory,directories)
 need(verified['verifiedFiles']==61 and verified['verifiedDirectories']==37 and verified['verifiedLogicalBytes']==1086141247,'Whole byte-exact recovery roundtrip')
 need(launch.sha(old)==report['recoveryZipSHA256'],'Original ZIP unchanged through compression/recovery verification')
 old_allocation=allocated(old);new_allocation=allocated(archive_path)
 need(new_allocation<old_allocation,'Replacement must actually save allocated disk space')
 for file,wanted in report['keptHashes'].items():need(launch.sha(file)==wanted,'All current artifacts/settings/dependency graphs still unchanged')
 pins=dict(report['keptHashes']);pins[str(SOURCE)]=launch.sha(SOURCE);pins[str(Path(__file__).resolve())]=launch.sha(__file__);pins[str(archive_path)]=launch.sha(archive_path)
 result=dict(passed=True,verified=verified,originalRecoveryReport=str(SOURCE),
  oldZIP=str(old),oldZipSHA256=report['recoveryZipSHA256'],oldZipAllocatedBytes=old_allocation,
  newRecoveryArchive=str(archive_path),newRecoveryArchiveSHA256=launch.sha(archive_path),newRecoveryArchiveAllocatedBytes=new_allocation,
  additionalAllocatedSavingsIfOldZIPRemoved=old_allocation-new_allocation,
  netOriginalBuildAllocationSavingsIfOldZIPRemoved=report['removedAllocatedBytes']-new_allocation,
  oldZIPDeleted=False,allOriginalRecoveryBytesAndDirectoryNamesPreserved=True,
  inputHashes=pins,fullPortAcceptance=False,scope=__doc__)
 (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items()if k!='inputHashes'},indent=2),flush=True)
if __name__=='__main__':pack()
