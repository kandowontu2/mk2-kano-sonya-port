"""In-memory rejection tests for actual native ball callback causal evidence."""
import json,re
from pathlib import Path
import verify_ball_register_runtime_v1840 as runtime
from verify_human_special_phases_v1767 import sha
ROOT=runtime.current.ROOT;OUT=ROOT/'audit_v1847_ball_register_runtime_units_checked'

def mutate_row(log,tag,key):
    line=next(line for line in log.splitlines()if line.startswith('MK2_BALL_BOUND_'+tag+' '))
    token=re.search(r'\b'+key+r'=([^\s]+)',line)
    assert token is not None
    value=int(token[1],16 if key in runtime.HEX else 10)^1
    changed=line[:token.start(1)]+(format(value,'08X')if key in runtime.HEX else str(value))+line[token.end(1):]
    return log.replace(line,changed,1)

def verify():
    pins={};cases=[];exact_scenes=0
    for side in(1,2):
        folder=ROOT/f'audit_v1841_human_ball_p{side}_boundary';path=folder/'run.log'
        log=path.read_text(encoding='utf-8-sig');assert runtime.verify(log,side)['passed']
        pins[str(path)]=sha(path)
        for tag,key in [('EXIT',key)for key in('id','a0','a1','a2','a3','a4','a5','a8','a9','sp','callback')]+[('GATE','status'),('TIMER','value')]:
            altered=mutate_row(log,tag,key)
            try:runtime.verify(altered,side)
            except (ValueError,StopIteration,KeyError):cases.append(dict(side=side,tag=tag,key=key,rejected=True))
            else:raise ValueError('Corruption escaped '+tag+' '+key)
        altered='\n'.join(line for line in log.splitlines()if not line.startswith('MK2_BALL_BOUND_EXIT '))
        try:runtime.verify(altered,side)
        except ValueError:cases.append(dict(side=side,tag='EXIT',key='missing_all_returns',rejected=True))
        else:raise ValueError('Missing restored callback returns escaped')
        old=ROOT/f'audit_v1824_human_ball_p{side}_boundary'
        for picture in sorted((folder/'snap').glob('display_*.png')):
            baseline=old/'snap'/picture.name
            assert picture.read_bytes()==baseline.read_bytes(),'Caller preservation changes physical scene'
            pins[str(picture)]=sha(picture);pins[str(baseline)]=sha(baseline);exact_scenes+=1
    for path in(Path(__file__),Path(runtime.__file__),ROOT/'tools/verify_ball_register_source_v1837.py'):
        pins[str(path)]=sha(path)
    return dict(passed=True,negativeCases=len(cases),cases=cases,allMutationsInMemory=True,
                sameFixedBoundaryScenesBeforeAndAfterCallerPreservation=exact_scenes,
                actualGuestOrCaptureWrites=False,inputHashes=pins,fullPortAcceptance=False)

if __name__=='__main__':
    assert not OUT.exists(),'Never overwrite evidence'
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
