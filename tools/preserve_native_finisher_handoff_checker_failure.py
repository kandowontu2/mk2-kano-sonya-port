"""Freeze the failed LIVE-only continuation criterion before correcting it."""
import gzip,json,subprocess
from pathlib import Path
import native_cpu_finisher_dispatch_context as native
ROOT,need,sha=native.ROOT,native.need,native.sha
if __name__=='__main__':
    source=ROOT/'tools/qualify_native_cpu_finisher_repair_regression.py'
    run=ROOT/'audit_native_cpu_finisher_repair_regression_current_oracle'
    out=ROOT/'audit_native_cpu_finisher_handoff_checker_failure'
    need(not out.exists(),'Fresh immutable failed-checker record')
    meta=json.loads((run/'result.json').read_text())
    log=gzip.open(run/'run.log.gz','rt',encoding='utf-8').read()
    need(meta['nativeExit']==0 and not meta['nativeCacheOverrunObserved'] and
         'MK2_FINISH_DISPATCH_REGRESSION_WINNER_HANDOFF frame=36401 ' in log and
         'MK2_NAT_CAMPAIGN_LOSS frame=36709 ' in log and
         'MK2_FINISH_DISPATCH_REGRESSION_STOP frame=37070 ' in log,
         'Actual native earned finish, later loss transition and ordinary zero exit')
    need("need(tail,'Actual native scheduler continues after own winner handoff')" in source.read_text(),
         'Exact originally executed failing criterion still intact')
    out.mkdir()
    with gzip.open(out/'failed_executed_checker.json.gz','wt',encoding='utf-8') as f:
        json.dump(dict(path=str(source),sha256=sha(source),text=source.read_text()),f)
    report=dict(passed=False,checkerFailure=True,hostSession=47827,hostExit=1,
        observedError='ValueError: Actual native scheduler continues after own winner handoff',
        cause='LIVE only samples active gameplay; winner/loss/selection states are not LIVE rows.',
        nativeExit=0,nativeGameFailure=False,noCacheOverrunObserved=True,
        originalCheckerSHA256=sha(source),
        actualRunInputHashes={str(p):sha(p) for p in run.iterdir() if p.is_file()},
        fullPortAcceptance=False,goalStatus='active')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    for p in out.iterdir():
        subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],check=True,capture_output=True)
    print(json.dumps(dict(preserved=True,nativeExit=0,checkerFailure=True)))
