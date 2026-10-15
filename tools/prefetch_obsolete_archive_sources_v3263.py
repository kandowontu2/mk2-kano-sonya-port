"""Read-only, bounded filesystem cache warming for the running recovery packer."""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
def main():
    first,last=map(int,sys.argv[1:3]); budget=512*1024*1024
    data=json.loads((ROOT/'audit_v3254_obsolete_workspace_parallel_recovery/inventory.json').read_text())
    rows=sorted(data['files'],key=lambda r:(Path(r['path']).suffix.lower(),r['sha256'],r['path']))
    if not 0<=first<last<=len(rows): raise ValueError('Exact bounded archive range')
    seen=set(); targets=[]; count=0; checked=set()
    for index,row in enumerate(rows[:last]):
        key=(row['bytes'],row['sha256'])
        if key in seen: continue
        seen.add(key)
        if index<first or not 0<row['bytes']<=8*1024*1024: continue
        if count+row['bytes']>budget: break
        path=ROOT/row['path']
        if not path.is_relative_to(ROOT): raise ValueError('No path escape')
        for item in (path,*path.parents):
            if item==ROOT: break
            if item not in checked:
                if item.stat(follow_symlinks=False).st_file_attributes&0x400: raise ValueError('No reparse paths')
                checked.add(item)
        if path.stat().st_size!=row['bytes']: raise ValueError('Original file changed')
        targets.append(path); count+=row['bytes']
    def read(path):
        total=0
        with path.open('rb') as stream:
            for block in iter(lambda:stream.read(1024*1024),b''): total+=len(block)
        return total
    with ThreadPoolExecutor(max_workers=16) as pool: actual=sum(pool.map(read,targets))
    print(json.dumps(dict(readOnly=True,warmedFiles=len(targets),readBytes=actual,budgetBytes=budget,filesWritten=0)))
if __name__=='__main__': main()
