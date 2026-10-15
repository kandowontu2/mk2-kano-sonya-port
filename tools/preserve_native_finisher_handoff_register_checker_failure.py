"""Preserve erroneous A13=zero expectation outside actor-owned gameplay."""
import gzip,json
from pathlib import Path
import native_cpu_finisher_dispatch_context as native
ROOT,need,sha=native.ROOT,native.need,native.sha
if __name__=='__main__':
    out=ROOT/'audit_native_cpu_finisher_handoff_register_checker_failure'
    source=ROOT/'tools/qualify_native_cpu_finisher_repair_regression.py'
    run=ROOT/'audit_native_cpu_finisher_repair_regression_current_oracle'
    need(not out.exists() and "stop['main']=='00000000'" in source.read_text(),'Fresh original failed checker')
    text=gzip.open(run/'run.log.gz','rt',encoding='utf-8').read()
    stop=next(s for s in text.splitlines() if s.startswith('MK2_FINISH_DISPATCH_REGRESSION_STOP '))
    need('actor=00000000 main=01068E30' in stop and 'mode=4' in stop,'Actual selection scheduler registers retained')
    out.mkdir()
    with gzip.open(out/'failed_executed_checker.json.gz','wt',encoding='utf-8') as f:
        json.dump(dict(path=str(source),sha256=sha(source),text=source.read_text()),f)
    (out/'report.json').write_text(json.dumps(dict(passed=False,checkerFailure=True,
        hostSession=27179,hostExit=1,nativeGameFailure=False,nativeExit=0,
        actualStopRow=stop,originalCheckerSHA256=sha(source),
        cause='A13 is the current native selection scheduler task, not a CPU gameplay owner in mode4.',
        actualRunInputHashes={str(p):sha(p) for p in run.iterdir() if p.is_file()},
        fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
    print(json.dumps(dict(preserved=True,nativeGameFailure=False)))
