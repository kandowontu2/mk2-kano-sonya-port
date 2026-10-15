"""Rehash exact obsolete sources, account external hardlinks and recovery cost; no deletion."""
import json, os, time
from collections import defaultdict
from pathlib import Path
import archive_obsolete_workspace_v3243 as common
ROOT=common.ROOT; OUT=ROOT/'audit_v3250_obsolete_workspace_removal_checked'
def main():
    common.need(not OUT.exists(),'Immutable removal verification')
    source=ROOT/'audit_v3244_obsolete_workspace_recovery/report.json'
    report=json.loads(source.read_text()); common.need(report['passed'] and report['filesDeleted']==0,'Completed exact recovery')
    inventory_path=source.parent/'inventory.json'
    common.need(common.sha(inventory_path)==report['inventorySHA256'],'Exact recovered inventory')
    data=json.loads(inventory_path.read_text()); wanted={r['path']:r for r in data['files']}
    names=set(data['targets']); seen=set(); seen_dirs=set(); identities={}; groups=defaultdict(list); started=time.time()
    for name in sorted(names):
        folder=ROOT/name
        common.need(folder.resolve().parent==ROOT.resolve(),'Exact obsolete folder inside workspace')
        for base, dirs, files in os.walk(folder,followlinks=False):
            path=Path(base); common.need(not path.stat().st_file_attributes&0x400,'No directory reparse'); seen_dirs.add(path.relative_to(ROOT).as_posix())
            for filename in files:
                path=Path(base)/filename; rel=path.relative_to(ROOT).as_posix(); meta=path.stat(follow_symlinks=False)
                common.need(rel in wanted and not meta.st_file_attributes&0x400 and path.is_file(),'Exact safe original file')
                row=wanted[rel]; key=(meta.st_dev,meta.st_ino)
                common.need(meta.st_size==row['bytes'] and key==(row['volumeID'],row['fileID']) and meta.st_nlink==row['hardlinkCount'],'Original bytes/identity/link topology stable')
                if key not in identities:
                    common.need(common.sha(path)==row['sha256'],'Every source SHA256 still matches independent recovery')
                    identities[key]=dict(allocated=common.space.allocated(path),links=meta.st_nlink)
                groups[key].append(rel); seen.add(rel)
            if time.time()-started>20:
                print('Reverified sources:',len(seen),flush=True); started=time.time()
    common.need(seen==set(wanted) and seen_dirs==set(data['directories']),'Complete unchanged original tree')
    archive=Path(report['recoveryArchive']); common.need(common.sha(archive)==report['recoveryArchiveSHA256'],'Same byte-verified recovery archive')
    reclaimable=sum(value['allocated'] for key,value in identities.items() if len(groups[key])==value['links'])
    archive_cost=common.space.allocated(archive)
    common.need(reclaimable>archive_cost,'Positive physical net savings; outside hardlinks excluded')
    for path,digest in report['preservedHashes'].items(): common.need(common.sha(path)==digest,'Kept current source/launcher/checkpoint unchanged')
    result=dict(passed=True,filesDeleted=0,targetDirectories=report['targetDirectories'],
        verifiedFiles=len(seen),verifiedDirectories=len(seen_dirs),reclaimableAllocatedBytes=reclaimable,
        recoveryArchiveAllocatedBytes=archive_cost,netAllocatedSavings=reclaimable-archive_cost,
        externalHardlinkGroups=sum(len(groups[k])<v['links'] for k,v in identities.items()),
        recoveryArchive=str(archive),recoveryArchiveSHA256=report['recoveryArchiveSHA256'],
        recoveryReport=str(source),recoveryReportSHA256=common.sha(source),
        inventoryPath=str(inventory_path),inventorySHA256=common.sha(inventory_path),
        preservedHashes=report['preservedHashes'],fullPortAcceptance=False)
    OUT.mkdir(); (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('targetDirectories','preservedHashes')},indent=2),flush=True)
if __name__=='__main__': main()
