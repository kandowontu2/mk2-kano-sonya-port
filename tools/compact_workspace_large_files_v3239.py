"""Lossless exact-leaf NTFS compaction; retain original paths and verify bytes."""
import hashlib, json, os, subprocess, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import inventory_workspace_space_v3237 as inventory
ROOT=inventory.ROOT
OUT=ROOT/'audit_v3240_workspace_large_file_compaction'
def sha(path):
    value=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''): value.update(block)
    return value.hexdigest().upper()
def safe(path):
    path=Path(path)
    if not path.is_absolute() or not path.is_relative_to(ROOT) or path==ROOT:
        raise ValueError('Exact workspace file required')
    for item in (path,*path.parents):
        if item==ROOT: break
        if item.stat(follow_symlinks=False).st_file_attributes & 0x400:
            raise ValueError('No reparse targets or ancestors')
    if not path.is_file(): raise ValueError('Regular file required')
    return path
def compact(row):
    path=safe(row['path']); meta=path.stat()
    before=inventory.allocated(path)
    if meta.st_nlink!=1: return dict(path=str(path),skipped='Hardlinked file preserved')
    if meta.st_size!=row['logicalBytes'] or before!=row['allocatedBytes']:
        raise ValueError('File changed since read-only inventory')
    digest=sha(path)
    result=subprocess.run([os.environ['SystemRoot']+'/System32/compact.exe','/C','/EXE:LZX','/F','/Q',str(path)],capture_output=True)
    after=inventory.allocated(path)
    unchanged=sha(path)==digest
    record=dict(path=str(path),logicalBytes=meta.st_size,allocatedBefore=before,
        allocatedAfter=after,reclaimedBytes=before-after,sha256=digest,
        unchanged=unchanged,exitCode=result.returncode)
    if result.returncode or not unchanged or after>before:
        record['output']=result.stdout.decode(errors='replace')+result.stderr.decode(errors='replace')
        raise ValueError(json.dumps(record))
    return record
def main():
    if OUT.exists(): raise ValueError('Immutable compaction run already exists')
    source=ROOT/'audit_v3238_workspace_space_inventory/report.json'
    report=json.loads(source.read_text())
    extensions={'.json','.jsonl','.txt','.log','.trace','.bin','.dat','.raw','.o','.a','.gch','.exe','.sym','.cpp','.h','.wav'}
    targets=[r for r in report['largestFiles'] if Path(r['path']).suffix.lower() in extensions
        and r['links']==1 and r['allocatedBytes']>r['logicalBytes']*.30]
    OUT.mkdir()
    (OUT/'plan.json').write_text(json.dumps(dict(inventorySHA256=sha(source),targets=targets),indent=2)+'\n')
    keep=[ROOT/'PLAY_MK2_KANO_SONYA.cmd',ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd',
        ROOT/'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
        ROOT/'diagnostic_v3172_native_morph_shadow/mkport_candidate.exe',
        ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip']
    pins={str(p):sha(p) for p in keep}
    done=[]; errors=[]; started=time.time()
    print('Exact large files selected:',len(targets),'; allocated GiB:',round(sum(r['allocatedBytes'] for r in targets)/2**30,2),flush=True)
    with (OUT/'files.jsonl').open('x',encoding='utf-8') as log:
        with ThreadPoolExecutor(max_workers=3) as pool:
            tasks={pool.submit(compact,row):row for row in targets}
            for future in as_completed(tasks):
                try: row=future.result(); done.append(row)
                except Exception as exc:
                    row=dict(path=tasks[future]['path'],error=str(exc)); errors.append(row)
                log.write(json.dumps(row)+'\n'); log.flush()
                if time.time()-started>20:
                    print('Verified',len(done),'files; recovered GiB:',round(sum(r.get('reclaimedBytes',0) for r in done)/2**30,2),flush=True); started=time.time()
    for path,digest in pins.items():
        if sha(path)!=digest: raise ValueError('Playable artifact changed: '+path)
    result=dict(passed=not errors,filesCompressed=sum('skipped' not in r for r in done),
        reclaimedAllocatedBytes=sum(r.get('reclaimedBytes',0) for r in done),
        allContentHashesUnchanged=all(r.get('unchanged',True) for r in done),
        errors=errors,deletedFiles=0,keptPlayableHashes=pins,
        recovery='Lossless filesystem compression; every file remains readable at its original path. compact /U /EXE reverses it.',
        fullPortAcceptance=False)
    (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)
    if errors: raise SystemExit(1)
if __name__=='__main__': main()
