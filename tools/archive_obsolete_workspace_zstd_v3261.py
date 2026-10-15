"""Fast self-contained Zstandard recovery; exact inventory/content roundtrip, no deletion."""
import compression.zstd as zstd
import hashlib, json, ntpath, shutil, tarfile, time
from pathlib import Path
import archive_obsolete_workspace_v3243 as common
ROOT=common.ROOT; OUT=ROOT/'audit_v3262_obsolete_workspace_zstd_recovery'
def main():
    common.need(not OUT.exists(),'Immutable fast recovery')
    original_inventory=ROOT/'audit_v3254_obsolete_workspace_parallel_recovery/inventory.json'
    original_digest=common.sha(original_inventory)
    data=json.loads(original_inventory.read_text()); records=data['files']; directories=data['directories']; names=set(data['targets'])
    plan_path=ROOT/'audit_v3242_unreferenced_workspace_cleanup_plan/report.json'
    plan=json.loads(plan_path.read_text())
    common.need(len(names)==470 and names=={r['name'] for r in plan['targets']} and len(records)==221001,'Exact previously parallel-hashed plan and complete source inventory')
    prefix=ntpath.normcase(str(ROOT))+'\\'; normalized_names={n.casefold() for n in names}
    pins={str(original_inventory):original_digest,str(plan_path):common.sha(plan_path)}
    for path in plan['dependencyFrontiers']:
        report=json.loads(Path(path).read_text()); pins[path]=common.sha(path)
        for file in report['inputHashes']:
            normal=ntpath.normcase(ntpath.normpath(file))
            common.need(not(normal.startswith(prefix) and normal[len(prefix):].split('\\')[0] in normalized_names),'No current dependency in obsolete targets')
    keep=[ROOT/'PLAY_MK2_KANO_SONYA.cmd',ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd',
        ROOT/'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
        ROOT/'diagnostic_v3172_native_morph_shadow/mkport_candidate.exe',
        ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip']
    pins.update({str(p):common.sha(p) for p in keep})
    OUT.mkdir(); inventory=OUT/'inventory.json'; shutil.copyfile(original_inventory,inventory)
    common.need(common.sha(inventory)==original_digest,'Exact retained full source inventory, not regenerated or altered')
    archive=OUT/'obsolete_470_folders_complete_recovery.tar.zst'
    p=zstd.CompressionParameter; options={p.compression_level:3,p.window_log:26,p.checksum_flag:1,p.nb_workers:4}
    content={}; packed=0; linked=0; done=0; started=time.time()
    with zstd.ZstdFile(archive,'wb',options=options) as compressed:
        with tarfile.open(fileobj=compressed,mode='w|',format=tarfile.PAX_FORMAT) as target:
            for name in sorted(directories):
                info=tarfile.TarInfo(name); info.type=tarfile.DIRTYPE; info.mode=0o755; target.addfile(info)
            for row in sorted(records,key=lambda r:(Path(r['path']).suffix.lower(),r['sha256'],r['path'])):
                path=ROOT/row['path']; key=(row['bytes'],row['sha256'])
                info=tarfile.TarInfo(row['path']); info.mode=0o644; info.mtime=row['mtime']
                if key in content:
                    info.type=tarfile.LNKTYPE; info.linkname=content[key]; target.addfile(info); linked+=1
                else:
                    meta=path.stat(); common.need(meta.st_size==row['bytes'] and not meta.st_file_attributes&0x400,'Same exact regular source length')
                    info.size=row['bytes']
                    with path.open('rb') as stream: target.addfile(info,stream)
                    content[key]=row['path']; packed+=row['bytes']
                done+=1
                if time.time()-started>20:
                    print('Fast packed files:',done,'; unique GiB:',round(packed/2**30,2),'; duplicates:',linked,flush=True); started=time.time()
    wanted={r['path']:r for r in records}; wanted_dirs=set(directories); seen={}; seen_dirs=set(); verified=0
    with zstd.ZstdFile(archive,'rb') as compressed:
        with tarfile.open(fileobj=compressed,mode='r|') as recovery:
            for member in recovery:
                name=member.name.rstrip('/')
                common.need(not name.startswith('/') and ':' not in name and '\\' not in name and
                    all(p not in ('..','.') for p in name.split('/')) and name.split('/')[0] in names,'Safe original recovery path')
                if member.isdir():
                    common.need(name in wanted_dirs and name not in seen_dirs,'Exact unique directory topology'); seen_dirs.add(name); continue
                common.need(name in wanted and name not in seen and not member.issym(),'Exact unique original file entry')
                row=wanted[name]
                if member.islnk():
                    common.need(member.linkname in seen and seen[member.linkname]==(row['bytes'],row['sha256']),'Internal duplicate link to earlier independently byte-verified member')
                else:
                    common.need(member.isfile() and member.size==row['bytes'],'Exact recovered file length')
                    digest=hashlib.sha256(); count=0
                    with recovery.extractfile(member) as stream:
                        for block in iter(lambda:stream.read(1024*1024),b''): digest.update(block); count+=len(block)
                    common.need(count==row['bytes'] and digest.hexdigest().upper()==row['sha256'],'Every archived original byte independently SHA256-verified')
                seen[name]=(row['bytes'],row['sha256']); verified+=1
                if time.time()-started>20:
                    print('Fast archive roundtrip verified:',verified,'/',len(records),flush=True); started=time.time()
    common.need(set(seen)==set(wanted) and seen_dirs==wanted_dirs,'Complete exact recovery with no missing or added original files/directories')
    for path,digest in pins.items(): common.need(common.sha(path)==digest,'Kept original inventory/launcher/build/checkpoint changed')
    result=dict(passed=True,filesDeleted=0,targetDirectories=[str(ROOT/n) for n in sorted(names)],
        verifiedFiles=len(records),verifiedDirectories=len(directories),verifiedLogicalBytes=sum(r['bytes'] for r in records),
        uniquePackedLogicalBytes=packed,duplicateContentEntries=linked,
        recoveryArchive=str(archive),recoveryArchiveSHA256=common.sha(archive),
        recoveryArchiveAllocatedBytes=common.space.allocated(archive),inventorySHA256=common.sha(inventory),
        originalParallelHashedInventory=str(original_inventory),originalParallelHashedInventorySHA256=original_digest,
        preservedHashes=pins,fullPortAcceptance=False,
        recovery='Extract this self-contained tar.zst into mk2port (Python 3.14 tarfile or compatible Zstandard/tar extractor). Exact original file hashes and directory names are in inventory.json. Internal duplicate links refer only to earlier verified archive members.')
    (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('targetDirectories','preservedHashes')},indent=2),flush=True)
if __name__=='__main__': main()
