"""Bounded continuation of lossless compaction, excluding slow audio files."""
import json, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import compact_workspace_large_files_v3239 as common
ROOT=common.ROOT; OUT=ROOT/'audit_v3246_workspace_fast_file_compaction'
def main():
    if OUT.exists(): raise ValueError('Immutable run already exists')
    plan=ROOT/'audit_v3240_workspace_large_file_compaction/plan.json'
    targets=[r for r in json.loads(plan.read_text())['targets'] if Path(r['path']).suffix.lower()!='.wav']
    OUT.mkdir(); (OUT/'plan.json').write_text(json.dumps(dict(sourcePlanSHA256=common.sha(plan),targets=targets),indent=2)+'\n')
    done=[]; errors=[]; started=time.time()
    print('Fast non-audio files:',len(targets),'; allocated GiB:',round(sum(r['allocatedBytes'] for r in targets)/2**30,2),flush=True)
    with (OUT/'files.jsonl').open('x',encoding='utf-8') as log:
        with ThreadPoolExecutor(max_workers=3) as pool:
            tasks={pool.submit(common.compact,row):row for row in targets}
            for future in as_completed(tasks):
                try: row=future.result(); done.append(row)
                except Exception as exc:
                    row=dict(path=tasks[future]['path'],error=str(exc)); errors.append(row)
                log.write(json.dumps(row)+'\n'); log.flush()
                if time.time()-started>20:
                    print('Verified fast files:',len(done),'; saved GiB:',round(sum(r.get('reclaimedBytes',0) for r in done)/2**30,2),flush=True); started=time.time()
    result=dict(passed=not errors,filesCompressed=sum('skipped' not in r for r in done),
        reclaimedAllocatedBytes=sum(r.get('reclaimedBytes',0) for r in done),
        allContentHashesUnchanged=all(r.get('unchanged',True) for r in done),errors=errors,deletedFiles=0,
        recovery='Lossless NTFS compression; original files remain readable at identical paths. compact /U /EXE reverses compression.',fullPortAcceptance=False)
    (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2),flush=True)
    if errors: raise SystemExit(1)
if __name__=='__main__': main()
