"""Verify every changed audio leaf from bounded, stopped-queue compaction."""
import json, ntpath
from pathlib import Path
import compact_workspace_large_files_v3239 as common
ROOT=common.ROOT; OUT=ROOT/'audit_v3248_bounded_audio_compaction_checked'
def main():
    if OUT.exists(): raise ValueError('Immutable verification already exists')
    source=ROOT/'audit_v3240_workspace_large_file_compaction/plan.json'
    plan=json.loads(source.read_text())
    pins=json.loads((ROOT/'audit_v3208_corrected_morph_shadow_full_scope_checkpoint/checkpoint.json').read_text())['inputHashes']
    pins={ntpath.normcase(ntpath.normpath(p)):h for p,h in pins.items()}
    completed={}
    for line in (ROOT/'audit_v3240_workspace_large_file_compaction/files.jsonl').read_text().splitlines():
        row=json.loads(line)
        if row.get('unchanged'): completed[ntpath.normcase(ntpath.normpath(row['path']))]=row['sha256']
    rows=[]
    for row in plan['targets']:
        path=Path(row['path'])
        if path.suffix.lower()!='.wav': continue
        after=common.inventory.allocated(path)
        if after==row['allocatedBytes']: continue
        common.safe(path); key=ntpath.normcase(ntpath.normpath(str(path)))
        wanted=completed.get(key,pins.get(key))
        if not wanted or common.sha(path)!=wanted or after>row['allocatedBytes']:
            raise ValueError('Changed audio must match original captured SHA256: '+str(path))
        rows.append(dict(path=str(path),sha256=wanted,allocatedBefore=row['allocatedBytes'],allocatedAfter=after,reclaimedBytes=row['allocatedBytes']-after))
    result=dict(passed=True,queueIntentionallyStopped=True,allChangedAudioHashesUnchanged=True,
        filesCompressed=len(rows),reclaimedAllocatedBytes=sum(r['reclaimedBytes'] for r in rows),
        files=rows,deletedFiles=0,fullPortAcceptance=False)
    OUT.mkdir(); (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='files'},indent=2))
if __name__=='__main__': main()
