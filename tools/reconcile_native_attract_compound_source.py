"""Keep the exact earlier executed qualifier before its sealing helpers.

Only an appended helper changed this file. Recover the original whole prefix
by its recorded SHA; never replace an old result or infer hash equivalence.
"""
import gzip
import hashlib
import json
from pathlib import Path
import qualify_native_attract_compound_audio as model

def record():
    out=model.ROOT/'audit_native_attract_kano_launch_v2'
    path=Path(model.__file__).resolve()
    result=json.loads((out/'native_compound_attract_mix.json').read_text())
    wanted=result['sourceHashes'][str(path)]
    raw=path.read_bytes();marker=b'\n\ndef contribution(c,event,full=False):'
    model.need(raw.count(marker)==1,'One exact appended helper boundary')
    prefix=raw.split(marker)[0]
    candidates=[prefix+b'\n'*n for n in range(4)]
    matches=[data for data in candidates if hashlib.sha256(data).hexdigest().upper()==wanted]
    model.need(len(matches)==1,'Exact prior entire source bytes match the actual first-execution SHA')
    archive=out/'qualification_source_at_first_execution.py.gz'
    model.need(not archive.exists(),'One exact prior source record, no result overwritten')
    with gzip.open(archive,'wb') as f:f.write(matches[0])
    with gzip.open(archive,'rb') as f:model.need(f.read()==matches[0],'Exact whole historical source preserved')
    note=dict(passed=True,originalQualifiedSource=str(path),originalSHA256=wanted,exactHistoricalSource=str(archive),
              currentSourceSHA256=model.sha(path),change='Sealing/contribution helpers appended after the original complete qualifier; first-execution source bytes recovered exactly by its pinned SHA. Existing PCM result unchanged.',
              fullPortAcceptance=False)
    (out/'source_append_receipt.json').write_text(json.dumps(note,indent=2)+'\n')
    print(json.dumps(note),flush=True)
    return note

if __name__=='__main__':record()
