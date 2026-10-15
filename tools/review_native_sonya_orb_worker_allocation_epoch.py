"""Successor checker: preserve failed pre-birth pointer-only review.

The same process slot held native tasks000F/0101 at ages0/10, before the
actual orb worker birth53. Require its real allocation epoch, not merely
a reused address. Frozen executed baseline is never edited in place.
"""
import gzip
import inspect
import json
from pathlib import Path
import review_native_sonya_orb_worker_lifetime_runtime as prior

ROOT=prior.ROOT
OUT=ROOT/'audit_native_sonya_orb_worker_allocation_epoch_review'
FAILURE=ROOT/'audit_native_sonya_orb_worker_lifetime_runtime_review_failure'
need,sha=prior.need,prior.sha

def main():
    need(not OUT.exists() and not FAILURE.exists() and not prior.OUT.exists(),
         'Fresh successor and original unsuccessful review has no acceptance output')
    text=gzip.open(ROOT/prior.RUNS[0]/'run.log.gz','rt').read()
    try:prior.worker_contract(text,256)
    except ValueError as error:
        need(str(error)=='Winner never prematurely mass-unlinks the original orb worker',
             'Exact actual baseline checker failure reproduced')
        failure=str(error)
    else:raise ValueError('Original pointer-only checker failure was not preserved')
    birth=next(r for r in prior.shared.rows(text,'TASK') if r['kind']=='worker')
    reused=[r for r in prior.shared.rows(text,'MASS') if r['pc']=='FF80E550' and r['target']==birth['job'] and int(r['age'])<int(birth['age'])]
    need([r['age'] for r in reused]==['0','10'] and [r['type'] for r in reused]==['000F','0101'] and
         all(r['known']=='unknown' for r in reused) and birth['age']=='53',
         'Actual earlier unrelated allocations at the same address, not deletion of the later worker')
    FAILURE.mkdir()
    (FAILURE/'report.json').write_text(json.dumps(dict(passed=False,checkerFailurePreserved=True,
        actualFailure=failure,originalOrbBirth=birth,actualEarlierUnrelatedAllocations=reused,
        gameplayFailureProven=False,originalCheckerSHA256=sha(Path(prior.__file__)),
        originalCheckerPath=str(Path(prior.__file__).resolve()),inputHashes={str(ROOT/prior.RUNS[0]/'run.log.gz'):sha(ROOT/prior.RUNS[0]/'run.log.gz')}),indent=2)+'\n')
    code=inspect.getsource(prior.worker_contract)
    old="int(r['age'])<=expected_age"
    need(code.count(old)==1,'One exact incorrect pointer-only lifetime boundary')
    code=code.replace(old,"int(birth['age'])<=int(r['age'])<=expected_age")
    scope=dict(vars(prior),OUT=OUT,__file__=__file__)
    exec(compile(code,__file__+'::actual_allocation_epoch','exec'),scope)
    code=inspect.getsource(prior.main)
    old='paths=[Path(__file__),Path(clouds.__file__),'
    need(code.count(old)==1,'Exact frozen review provenance boundary')
    code=code.replace(old,'paths=[Path(__file__),Path('+repr(str(Path(prior.__file__).resolve()))+'),ROOT/\'audit_native_sonya_orb_worker_lifetime_runtime_review_failure/report.json\',Path(clouds.__file__),')
    code=code.replace('result=dict(passed=True,nativeOrbWorkerCleanupAccepted=True,',
                      'result=dict(passed=True,actualAllocationEpochReviewed=True,nativeOrbWorkerCleanupAccepted=True,')
    exec(compile(code,__file__+'::review','exec'),scope)
    scope['main']()

if __name__=='__main__':main()
