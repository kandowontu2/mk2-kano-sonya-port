"""Read-only dependency-aware plan for obsolete top-level build/test folders."""
import json, ntpath, re
from pathlib import Path
from collections import Counter
import inventory_workspace_space_v3237 as space
ROOT=space.ROOT; OUT=ROOT/'audit_v3242_unreferenced_workspace_cleanup_plan'
def main():
    if OUT.exists(): raise ValueError('Immutable plan already exists')
    frontiers=[ROOT/'audit_v3208_corrected_morph_shadow_full_scope_checkpoint/checkpoint.json',
        ROOT/'audit_v3236_morph_adversity_checked/report.json',
        ROOT/'audit_v3219_morph_adversity_dispatch/report.json',
        ROOT/'audit_v3230_morph_ko_dispatch/report.json']
    pins=set(str(p) for p in frontiers)
    for source in frontiers:
        report=json.loads(source.read_text())
        pins.update(report['inputHashes'])
    protected=set()
    prefix=ntpath.normcase(str(ROOT))+'\\'
    for path in pins:
        normal=ntpath.normcase(ntpath.normpath(path))
        if normal.startswith(prefix): protected.add(normal[len(prefix):].split('\\')[0])
    protected.update(p.name.casefold() for p in ROOT.iterdir() if p.is_dir() and
        (p.name.startswith('audit_v32') or p.name.startswith('release') or
         p.name.startswith('_archive') or p.name in ('mame-mkp','tools','assets','roms','play_settings')))
    inventory=json.loads((ROOT/'audit_v3238_workspace_space_inventory/report.json').read_text())
    targets=[]
    for row in inventory['groups']:
        name=row['name']
        if name.casefold() in protected: continue
        match=re.match(r'^(audit|diagnostic|regression|control|trace|pilot|reference)_v(\d+)_',name)
        if not match or int(match[2])>=3200 or row['uniqueAllocatedBytes']<16*1024*1024: continue
        targets.append(row)
    OUT.mkdir(); report=dict(readOnly=True,root=str(ROOT),dependencyFrontiers=[str(p) for p in frontiers],
        pinnedFiles=len(pins),protectedTopLevelFolders=len(protected),targets=targets,
        estimatedAllocatedBytes=sum(r['uniqueAllocatedBytes'] for r in targets),filesDeleted=0)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(targetFolders=len(targets),estimatedGiB=round(report['estimatedAllocatedBytes']/2**30,2),largestTargets=targets[:25]),indent=2))
if __name__=='__main__': main()
