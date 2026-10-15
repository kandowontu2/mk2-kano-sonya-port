"""Independent parallel source rehash and exact current recovery/space verification; no deletion."""
import json, os, time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import archive_obsolete_workspace_v3243 as common
ROOT=common.ROOT; OUT=ROOT/'audit_v3256_obsolete_workspace_parallel_removal_checked'
def main():
    common.need(not OUT.exists(),'Immutable source verification')
    source=ROOT/'audit_v3262_obsolete_workspace_zstd_recovery/report.json'
    report=json.loads(source.read_text()); common.need(report['passed'] and report['filesDeleted']==0,'Actual completed recovery required')
    inventory_path=source.parent/'inventory.json'
    common.need(common.sha(inventory_path)==report['inventorySHA256'],'Same exact archive inventory')
    data=json.loads(inventory_path.read_text()); wanted={r['path']:r for r in data['files']}
    seen=set(); seen_dirs=set(); groups=defaultdict(list); physical={}; started=time.time()
    for name in data['targets']:
        folder=ROOT/name; common.need(folder.resolve().parent==ROOT.resolve(),'Exact workspace child')
        for base, dirs, files in os.walk(folder,followlinks=False):
            path=Path(base); common.need(not path.stat().st_file_attributes&0x400,'No directory links'); seen_dirs.add(path.relative_to(ROOT).as_posix())
            for filename in files:
                path=Path(base)/filename; rel=path.relative_to(ROOT).as_posix(); meta=path.stat(follow_symlinks=False)
                common.need(rel in wanted and not meta.st_file_attributes&0x400 and path.is_file(),'Exact safe old file')
                row=wanted[rel]; key=(meta.st_dev,meta.st_ino)
                common.need(meta.st_size==row['bytes'] and key==(row['volumeID'],row['fileID']) and meta.st_nlink==row['hardlinkCount'],'Exact source lengths/physical identities/hardlink topology')
                if key not in physical:
                    physical[key]=dict(path=str(path),sha256=row['sha256'],links=meta.st_nlink,allocated=common.space.allocated(path))
                else: common.need(physical[key]['sha256']==row['sha256'],'Shared identity must have identical expected bytes')
                groups[key].append(rel); seen.add(rel)
            if time.time()-started>20:
                print('Exact source paths rechecked:',len(seen),flush=True); started=time.time()
    common.need(seen==set(wanted) and seen_dirs==set(data['directories']),'Whole original tree unchanged')
    done=0
    with ThreadPoolExecutor(max_workers=16) as pool:
        tasks={pool.submit(common.sha,row['path']):row for row in physical.values()}
        for future in as_completed(tasks):
            common.need(future.result()==tasks[future]['sha256'],'Independent actual source SHA256 matches byte-verified archive')
            done+=1
            if time.time()-started>20:
                print('Independent physical source hashes:',done,'/',len(physical),flush=True); started=time.time()
    archive=Path(report['recoveryArchive']); common.need(common.sha(archive)==report['recoveryArchiveSHA256'],'Same fully roundtrip-verified archive bytes')
    reclaimable=sum(row['allocated'] for key,row in physical.items() if len(groups[key])==row['links'])
    cost=common.space.allocated(archive); common.need(reclaimable>cost,'Net real allocated savings required')
    for path,digest in report['preservedHashes'].items(): common.need(common.sha(path)==digest,'Kept playable/launcher/checkpoint unchanged')
    OUT.mkdir(); manifest=OUT/'exact_source_paths_and_lengths.tsv'
    with manifest.open('x',encoding='utf-8',newline='\n') as stream:
        for name in sorted(seen_dirs):
            common.need(not any(c in name for c in '\t\r\n'),'Unambiguous original directory path')
            stream.write('d\t'+name+'\n')
        for name in sorted(seen):
            common.need(not any(c in name for c in '\t\r\n'),'Unambiguous original file path')
            stream.write('f\t'+str(wanted[name]['bytes'])+'\t'+name+'\n')
    result=dict(passed=True,filesDeleted=0,targetDirectories=report['targetDirectories'],
        verifiedFiles=len(seen),verifiedDirectories=len(seen_dirs),independentlyRehashedPhysicalFiles=len(physical),
        reclaimableAllocatedBytes=reclaimable,recoveryArchiveAllocatedBytes=cost,netAllocatedSavings=reclaimable-cost,
        externalHardlinkGroups=sum(len(groups[k])<v['links'] for k,v in physical.items()),
        recoveryArchive=str(archive),recoveryArchiveSHA256=report['recoveryArchiveSHA256'],
        recoveryReport=str(source),recoveryReportSHA256=common.sha(source),
        inventoryPath=str(inventory_path),inventorySHA256=common.sha(inventory_path),
        sourceManifestPath=str(manifest),sourceManifestSHA256=common.sha(manifest),
        preservedHashes=report['preservedHashes'],fullPortAcceptance=False)
    (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('targetDirectories','preservedHashes')},indent=2),flush=True)
if __name__=='__main__': main()
