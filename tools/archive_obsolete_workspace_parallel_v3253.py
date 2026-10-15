"""Parallel byte hashing for the unchanged exact 470-folder recovery contract."""
import json, os, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import archive_obsolete_workspace_v3243 as original
ROOT=original.ROOT
def main():
    out=ROOT/'audit_v3254_obsolete_workspace_parallel_recovery'
    original.need(not out.exists(),'Immutable parallel recovery')
    plan=json.loads((ROOT/'audit_v3242_unreferenced_workspace_cleanup_plan/report.json').read_text())
    paths={}; total=0; started=time.time()
    for row in plan['targets']:
        folder=ROOT/row['name']; original.need(folder.resolve().parent==ROOT.resolve(),'Exact old child folder')
        for base, dirs, files in os.walk(folder,followlinks=False):
            original.need(not Path(base).stat().st_file_attributes&0x400,'No directory reparse')
            for name in files:
                path=Path(base)/name; meta=path.stat(follow_symlinks=False)
                original.need(not meta.st_file_attributes&0x400 and path.is_file(),'No file reparse')
                key=(meta.st_dev,meta.st_ino,meta.st_size,meta.st_mtime_ns)
                paths.setdefault(key,path); total+=1
            if time.time()-started>20:
                print('Parallel pre-inventory files:',total,flush=True); started=time.time()
    digest=original.sha; cache={}; done=0
    print('Hashing unique physical files:',len(paths),'; paths:',total,flush=True)
    with ThreadPoolExecutor(max_workers=16) as pool:
        pending={pool.submit(digest,path):key for key,path in paths.items()}
        for future in as_completed(pending):
            key=pending[future]; cache[key]=future.result(); done+=1
            if time.time()-started>20:
                print('Parallel SHA256 verified:',done,'/',len(paths),flush=True); started=time.time()
    def exact_cached_sha(path):
        path=Path(path); meta=path.stat()
        key=(meta.st_dev,meta.st_ino,meta.st_size,meta.st_mtime_ns)
        return cache[key] if key in cache else digest(path)
    original.sha=exact_cached_sha
    original.OUT=out
    original.main()
if __name__=='__main__': main()
