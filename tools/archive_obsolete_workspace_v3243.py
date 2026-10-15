"""Self-contained, byte-verified solid recovery for planned obsolete folders. No deletion."""
import hashlib, json, lzma, ntpath, os, tarfile, time
from collections import defaultdict
from pathlib import Path
import inventory_workspace_space_v3237 as space
ROOT=space.ROOT; OUT=ROOT/'audit_v3244_obsolete_workspace_recovery'
def need(ok,message):
    if not ok: raise ValueError(message)
def sha(path):
    result=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''): result.update(block)
    return result.hexdigest().upper()
def main():
    need(not OUT.exists(),'Immutable recovery already exists')
    source=ROOT/'audit_v3242_unreferenced_workspace_cleanup_plan/report.json'
    plan=json.loads(source.read_text()); names={r['name'] for r in plan['targets']}
    need(plan['readOnly'] and len(names)==470,'Exact inspected obsolete folder plan')
    prefix=ntpath.normcase(str(ROOT))+'\\'; normalized_names={n.casefold() for n in names}
    pins={str(source):sha(source)}
    for path in plan['dependencyFrontiers']:
        report=json.loads(Path(path).read_text()); pins[path]=sha(path)
        for file in report['inputHashes']:
            normal=ntpath.normcase(ntpath.normpath(file))
            need(not(normal.startswith(prefix) and normal[len(prefix):].split('\\')[0] in normalized_names),'Current dependency intersects obsolete target')
    keep=[ROOT/'PLAY_MK2_KANO_SONYA.cmd',ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd',
        ROOT/'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
        ROOT/'diagnostic_v3172_native_morph_shadow/mkport_candidate.exe',
        ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip']
    pins.update({str(p):sha(p) for p in keep})
    records=[]; directories=[]; identities={}; started=time.time()
    for name in sorted(names):
        folder=ROOT/name
        need(folder.resolve().parent==ROOT.resolve(),'Exact direct child target')
        for base, dirs, files in os.walk(folder,followlinks=False):
            path=Path(base); need(not path.stat().st_file_attributes&0x400,'No directory reparse')
            directories.append(path.relative_to(ROOT).as_posix())
            for filename in files:
                path=Path(base)/filename; meta=path.stat(follow_symlinks=False)
                need(not meta.st_file_attributes&0x400 and path.is_file(),'No file reparse or nonregular data')
                key=(meta.st_dev,meta.st_ino)
                if key not in identities: identities[key]=sha(path)
                records.append(dict(path=path.relative_to(ROOT).as_posix(),bytes=meta.st_size,
                    sha256=identities[key],volumeID=meta.st_dev,fileID=meta.st_ino,
                    hardlinkCount=meta.st_nlink,mtime=meta.st_mtime))
            if time.time()-started>20:
                print('Hashed exact old files:',len(records),flush=True); started=time.time()
    need(records and len(directories)>=len(names),'Nonempty exact recovery')
    OUT.mkdir(); archive=OUT/'obsolete_470_folders_complete_recovery.tar.xz'
    (OUT/'inventory.json').write_text(json.dumps(dict(targets=sorted(names),files=records,directories=directories),indent=2)+'\n')
    content={}; packed=0; linked=0; logical=sum(r['bytes'] for r in records)
    print('Recovery inventory:',len(records),'files;',round(logical/2**30,2),'logical GiB',flush=True)
    with lzma.LZMAFile(archive,'wb',format=lzma.FORMAT_XZ,check=lzma.CHECK_CRC64,
        filters=[dict(id=lzma.FILTER_LZMA2,preset=1,dict_size=64*1024*1024)]) as compressed:
        with tarfile.open(fileobj=compressed,mode='w|',format=tarfile.PAX_FORMAT) as target:
            for name in sorted(directories):
                info=tarfile.TarInfo(name); info.type=tarfile.DIRTYPE; info.mode=0o755; target.addfile(info)
            for row in sorted(records,key=lambda r:(Path(r['path']).suffix.lower(),r['sha256'],r['path'])):
                path=ROOT/row['path']; key=(row['bytes'],row['sha256'])
                info=tarfile.TarInfo(row['path']); info.mode=0o644; info.mtime=row['mtime']
                if key in content:
                    info.type=tarfile.LNKTYPE; info.linkname=content[key]; target.addfile(info); linked+=1
                else:
                    info.size=row['bytes']
                    with path.open('rb') as stream: target.addfile(info,stream)
                    content[key]=row['path']; packed+=row['bytes']
                if time.time()-started>20:
                    print('Packed unique GiB:',round(packed/2**30,2),'; duplicate entries:',linked,flush=True); started=time.time()
    wanted={r['path']:r for r in records}; seen={}; seen_dirs=set(); verified=0
    with tarfile.open(archive,mode='r|xz') as recovery:
        for member in recovery:
            name=member.name.rstrip('/')
            need(not name.startswith('/') and ':' not in name and '\\' not in name and
                all(p not in ('..','.') for p in name.split('/')) and name.split('/')[0] in names,'Safe original archive path')
            if member.isdir():
                need(name in directories and name not in seen_dirs,'Exact unique directory topology'); seen_dirs.add(name); continue
            need(name in wanted and name not in seen and not member.issym(),'Exact unique file entry')
            row=wanted[name]
            if member.islnk():
                need(member.linkname in seen and seen[member.linkname]==(row['bytes'],row['sha256']),'Internal duplicate link to previously byte-verified member')
            else:
                need(member.isfile() and member.size==row['bytes'],'Exact recovered file length')
                digest=hashlib.sha256(); count=0
                with recovery.extractfile(member) as stream:
                    for block in iter(lambda:stream.read(1024*1024),b''): digest.update(block); count+=len(block)
                need(count==row['bytes'] and digest.hexdigest().upper()==row['sha256'],'Every recovered byte independently SHA256-verified')
            seen[name]=(row['bytes'],row['sha256']); verified+=1
            if time.time()-started>20:
                print('Roundtrip verified files:',verified,flush=True); started=time.time()
    need(set(seen)==set(wanted) and seen_dirs==set(directories),'Complete file/directory roundtrip')
    for path,digest in pins.items(): need(sha(path)==digest,'Kept current input changed: '+path)
    result=dict(passed=True,filesDeleted=0,targetDirectories=[str(ROOT/n) for n in sorted(names)],
        verifiedFiles=len(records),verifiedDirectories=len(directories),verifiedLogicalBytes=logical,
        uniquePackedLogicalBytes=packed,duplicateContentEntries=linked,
        recoveryArchive=str(archive),recoveryArchiveSHA256=sha(archive),
        recoveryArchiveAllocatedBytes=space.allocated(archive),inventorySHA256=sha(OUT/'inventory.json'),
        preservedHashes=pins,fullPortAcceptance=False,
        recovery='Extract this self-contained tar.xz into mk2port to restore every original folder/file; inventory.json records exact SHA256 hashes. Internal duplicate links refer only to earlier archived members.')
    (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('targetDirectories','preservedHashes')},indent=2),flush=True)
if __name__=='__main__': main()
