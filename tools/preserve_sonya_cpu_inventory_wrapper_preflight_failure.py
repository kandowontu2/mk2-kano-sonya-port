"""Preserve transitive-controller positional lookup failure before wrapper repair."""
import gzip,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
    out=ROOT/'audit_native_sonya_cpu_inventory_wrapper_preflight_failure'
    if out.exists() or (ROOT/'audit_native_sonya_cpu_finisher_inventory_checked').exists():
        raise ValueError('Fresh wrapper failure; no native test boot')
    paths=[ROOT/'tools/capture_native_sonya_cpu_finisher_inventory_checked.py',
           ROOT/'mk2ks_native_sonya_cpu_finisher_inventory_checked.lua']
    out.mkdir()
    with gzip.open(out/'original_wrapper_preflight_sources.json.gz','wt',encoding='utf-8') as f:
        json.dump({str(p):dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest().upper(),text=p.read_text()) for p in paths},f)
    (out/'report.json').write_text(json.dumps(dict(passed=False,hostExit=1,nativeJobsStarted=0,
        observedError="KeyError: controller list index1 refers to original Sonya observer, not native UI source after wrapper prepend",
        nativeGameFailure=False,fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
    print('Original positional-controller preflight preserved; no native process started.')
