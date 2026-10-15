"""Fresh opposite-slot native Freeze/guard comparisons, physical inputs only."""
import code,gzip,json,traceback
from pathlib import Path
import capture_native_block_freeze_observed as capture

ROOT,need=capture.ROOT,capture.need
JOBS=[('kano',1,'none'),('sonya',1,'none'),('liu_kang',1,'held'),
      ('kano',1,'held'),('sonya',1,'held'),('kano',1,'reactive'),('sonya',1,'reactive')]

if __name__=='__main__':
    previous=ROOT/'audit_native_block_freeze_progress/report.json'
    old=json.loads(previous.read_text())
    need(old['passed'] and old['finiteP2HumanFreezeBlockRecoveryAccepted'],'Actual prior completed P2 scope preserved')
    need(all(capture.prior.sha(p)==h for p,h in old['inputHashes'].items()),'Every prior completed source/receipt remains intact')
    pins={str(p):capture.prior.sha(p) for p in (Path(__file__).resolve(),previous,Path(capture.__file__).resolve())}
    captures={}
    for fighter,side,policy in JOBS:
        folder=ROOT/f'audit_native_block_freeze_observed_{policy}_{fighter}_p{side}'
        need(all(capture.prior.sha(p)==h for p,h in pins.items()),'Exact opposite-slot physical wrapper before cold boot')
        try:c=capture.run(fighter,side,policy)
        except Exception as e:
            if folder.exists():
                failure=folder/'p1_capture_failure.json';need(not failure.exists(),'Preserve immutable actual failure')
                failure.write_text(json.dumps(dict(passed=False,error=repr(e),traceback=traceback.format_exc()),indent=2)+'\n')
            raise
        need(all(capture.prior.sha(p)==h for p,h in pins.items()),'Exact opposite-slot physical wrapper after native terminal')
        c['meta']['inputHashes'].update(pins)
        with gzip.open(folder/'executed_p1_wrapper.json.gz','wt',encoding='utf-8') as stream:
            json.dump(dict(inputHashes=pins,source=Path(__file__).read_text()),stream)
        captures[f'{fighter}_p{side}_{policy}']=c
    code.interact(banner='Seven actual terminal P1 native comparisons; original native pixels retained in RAM.',local=dict(captures=captures))
