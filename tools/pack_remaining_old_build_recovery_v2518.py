"""Complete solid recovery for exact68 unreferenced old builds. No deletion here."""
import ctypes,hashlib,json,lzma,ntpath,tarfile
from pathlib import Path
from collections import defaultdict
import verify_current_interrupt_v1870 as launch
ROOT=launch.ROOT
SOURCE=ROOT/'audit_v2504_remaining_obsolete_build_inventory/report.json'
OUT=ROOT/'audit_v2518_remaining_old_build_recovery'
def need(ok,label):
 if not ok:raise ValueError(label)
def normalized(path):return ntpath.normcase(ntpath.normpath(str(path)))
kernel=ctypes.WinDLL('kernel32',use_last_error=True);size=kernel.GetCompressedFileSizeW
size.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32));size.restype=ctypes.c_uint32
def allocated(path):
 high=ctypes.c_uint32();ctypes.set_last_error(0);low=size(str(path),ctypes.byref(high));need(low!=0xffffffff or ctypes.get_last_error()==0,'Actual NTFS allocation');return(high.value<<32)|low
def verify_archive(path,records,directories,names):
 wanted={r['path']:r for r in records};seen=set();seen_dirs=set();total=0
 with tarfile.open(path,mode='r|xz')as source:
  for member in source:
   name=member.name.rstrip('/')
   need(name.split('/')[0]in names and ':'not in name and '\\'not in name and not name.startswith('/')and all(p not in('..','.')for p in name.split('/')),'Exact safe archive member')
   need(not member.issym()and not member.islnk(),'No archive links')
   if member.isdir():need(name in directories and name not in seen_dirs,'Exact unique original directory');seen_dirs.add(name)
   else:
    need(member.isfile()and name in wanted and name not in seen,'Exact unique original file');record=wanted[name]
    need(member.size==record['bytes'],'Exact original length');digest=hashlib.sha256();count=0
    with source.extractfile(member)as stream:
     for block in iter(lambda:stream.read(1024*1024),b''):digest.update(block);count+=len(block)
    need(count==record['bytes']and digest.hexdigest().upper()==record['sha256'],'Every original file byte independently recovered')
    seen.add(name);total+=count
 need(seen==set(wanted)and seen_dirs==set(directories),'Complete file and directory topology, no additions or omissions')
 return dict(verifiedFiles=len(seen),verifiedDirectories=len(seen_dirs),verifiedLogicalBytes=total)
def pack():
 need(not OUT.exists(),'Immutable complete old-build recovery')
 inventory=json.loads(SOURCE.read_text());need(inventory['passed']and inventory['readOnly']and inventory['remainingUnreferencedCount']==68,'Exact current read-only68build inventory')
 names=[r['name']for r in inventory['remainingUnreferencedBuildFolders']]
 need(len(set(names))==68 and 'diagnostic_v1836_ball_register_boundary'not in names,'Exact old builds, never current candidate')
 frontiers=[Path(p)for p in inventory['dependencyFrontiers']]+[
  ROOT/'audit_v2474_current_shao_crouch_exit_checkpoint/checkpoint.json',
  ROOT/'audit_v2508_current_kano_p1_shao_duck_wait_checked/report.json',
  ROOT/'audit_v2508_current_sonya_p1_shao_duck_wait_checked/report.json']
 pins=dict(inventory['inputHashes']);pins[str(SOURCE)]=launch.sha(SOURCE)
 protected=normalized(ROOT)+'\\';target_names={n.casefold()for n in names}
 for path in frontiers:
  report=json.loads(path.read_text());need('inputHashes'in report,'Actual accepted/rejected frontier graph retained')
  for file in report['inputHashes']:
   key=normalized(file)
   need(not(key.startswith(protected)and key[len(protected):].split('\\')[0]in target_names),'No current whole evidence dependency may be archived')
  pins[str(path)]=launch.sha(path)
 keep=json.loads((ROOT/'audit_v2490_next_old_build_solid_recovery_checked/report.json').read_text())
 for file,wanted in keep['inputHashes'].items():need(launch.sha(file)==wanted,'All retained current artifacts/settings/previous recovery unchanged');pins[file]=wanted
 pending=ROOT/'audit_v2515_current_sonya_p1_shao_duck_wait_campaign/input_hashes_before.json'
 snapshot=json.loads(pending.read_text(encoding='utf-8-sig'));pins[str(pending)]=launch.sha(pending)
 for file,wanted in snapshot.items():
  key=normalized(file);need(not(key.startswith(protected)and key[len(protected):].split('\\')[0]in target_names),'Live extended campaign cannot depend on archive target')
  need(launch.sha(file)==wanted,'Exact running capture input unchanged');pins[file]=wanted
 records=[];directories=[];link_groups=defaultdict(list)
 for index,item in enumerate(inventory['remainingUnreferencedBuildFolders'],1):
  folder=ROOT/item['name'];need(folder.resolve().parent==ROOT.resolve()and not folder.stat().st_file_attributes&0x400,'Exact old folder inside intended workspace, no reparse')
  need(launch.sha(folder/'mkport_candidate.exe')==item['executableSHA256'],'Same observed old executable')
  if item['buildInfoSHA256']:need(launch.sha(folder/'build-info.json')==item['buildInfoSHA256'],'Same observed old build metadata')
  start=len(records);start_dirs=len(directories);directories.append(item['name'])
  for path in sorted(folder.rglob('*')):
   meta=path.stat();need(not meta.st_file_attributes&0x400,'No reparse anywhere in exact old tree')
   name=path.relative_to(ROOT).as_posix()
   if path.is_dir():directories.append(name)
   else:
    need(path.is_file()and meta.st_ino and meta.st_nlink>=1,'Regular original file with real NTFS identity')
    record=dict(path=name,bytes=meta.st_size,sha256=launch.sha(path),allocatedBytes=allocated(path),
     volumeID=meta.st_dev,fileID=meta.st_ino,hardlinkCount=meta.st_nlink,mtime=meta.st_mtime)
    records.append(record);link_groups[meta.st_dev,meta.st_ino].append(record)
  actual=records[start:];need(len(actual)==item['files']and len(directories)-start_dirs==item['directories']and sum(r['bytes']for r in actual)==item['logicalBytes'],'Entire observed original tree counts and lengths unchanged')
  if index%10==0:print('Inventoried/hash-verified',index,'of68 exact old builds',flush=True)
 need(len(records)==465 and len(directories)==352 and sum(r['bytes']for r in records)==7456052181,'Entire exact original465files/352directories')
 reclaimable=0;external=[]
 for group in link_groups.values():
  need(len({(r['hardlinkCount'],r['allocatedBytes'],r['sha256'])for r in group})==1,'Consistent actual hardlink group')
  if len(group)==group[0]['hardlinkCount']:reclaimable+=group[0]['allocatedBytes']
  else:need(len(group)<group[0]['hardlinkCount'],'Real complete link accounting');external.append([r['path']for r in group])
 OUT.mkdir();archive=OUT/'remaining_68_builds_complete_recovery.tar.xz'
 with lzma.LZMAFile(archive,'wb',format=lzma.FORMAT_XZ,check=lzma.CHECK_CRC64,
  filters=[dict(id=lzma.FILTER_LZMA2,preset=4,dict_size=128*1024*1024)])as compressed:
  with tarfile.open(fileobj=compressed,mode='w|',format=tarfile.PAX_FORMAT)as target:
   for name in directories:
    info=tarfile.TarInfo(name);info.type=tarfile.DIRTYPE;info.mode=0o755;target.addfile(info)
   for index,record in enumerate(records,1):
    path=ROOT/record['path'];need(launch.sha(path)==record['sha256'],'Original file stable immediately before archiving')
    info=tarfile.TarInfo(record['path']);info.size=record['bytes'];info.mode=0o644;info.mtime=record['mtime']
    with path.open('rb')as stream:target.addfile(info,stream)
    if index%50==0:print('Solid packed',index,'of465 original files',flush=True)
 verified=verify_archive(archive,records,directories,set(names))
 for record in records:need(launch.sha(ROOT/record['path'])==record['sha256'],'Every old source still unchanged after complete roundtrip')
 for file,wanted in pins.items():need(launch.sha(file)==wanted,'All kept dependencies/settings/source unchanged through archive verification')
 cost=allocated(archive);need(reclaimable>cost,'Exact potential allocated savings after archive, with external hardlinks excluded')
 pins[str(archive)]=launch.sha(archive);pins[str(Path(__file__).resolve())]=launch.sha(__file__)
 report=dict(passed=True,filesDeleted=False,removedDirectories=[],targetDirectories=[str(ROOT/n)for n in names],
  inventory=records,preservedDirectories=directories,verified=verified,recoveryArchive=str(archive),recoveryArchiveSHA256=launch.sha(archive),
  recoveryArchiveAllocatedBytes=cost,originalReclaimableUniqueAllocatedBytes=reclaimable,externallyRetainedHardlinkGroups=external,
  netAllocatedSavingsIfExactTargetsRemoved=reclaimable-cost,inputHashes=pins,allOldBuildFoldersRemoved=False,fullPortAcceptance=False,scope=__doc__)
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','inventory','preservedDirectories','targetDirectories')},indent=2),flush=True)
if __name__=='__main__':pack()
