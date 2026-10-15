"""Actual native response counterexamples, not button-marker-only acceptance."""
import json,re
from pathlib import Path
import cross_continue_adaptive_contract as contract
ROOT,need,sha=contract.ROOT,contract.need,contract.sha


def check(folder,text,fighter,side,target):
    folder=Path(folder);out=ROOT/f'audit_cross_continue_adaptive_control_faults_{fighter}_p{side}_to_{target}'
    need(not out.exists(),'Fresh same-terminal control fault receipt')
    proof=ROOT/f'audit_cross_continue_adaptive_checked_{fighter}_p{side}_to_{target}/report.json';good=json.loads(proof.read_text())
    need(good['passed'],'Actual full qualified native route')
    positive=contract.gate(text,fighter,side,target);events=positive['events'];faults=[]
    def reject(label,changed):
        need(changed!=text,'Effective actual field mutation')
        try:contract.gate(changed,fighter,side,target)
        except(ValueError,KeyError,IndexError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Missing real control response admitted '+label)
    for tag in ('WALK','JUMP','PUNCH','RECOVER'):
        line=next(s for s in text.splitlines()if s.startswith('MK2_SC_'+tag+' '))
        reject('actual '+tag+' response absent',text.replace(line+'\n','',1))
    for event,key,value in (('walk','x',None),('jump','y',None),('jump','action','1283'),('punch','action','771'),('recover','flags','00000005')):
        at=events[event]-1
        line=next(s for s in text.splitlines()if s.startswith('MK2_SC_FIELD ')and f'frame={at} 'in s and f'slot={side} 'in s)
        row=dict(re.findall(r'(\w+)=([^\s]+)',line))
        wanted=contract.rows(text,'WALK')[0]['fromX']if event=='walk'else row['floor']if value is None else value
        changed=re.sub(r'\b'+key+r'=\S+',key+'='+wanted,line,count=1)
        reject('actual '+event+' '+key+' changed',text.replace(line,changed,1))
    need(contract.gate(text,fighter,side,target)==positive,'Complete native positives restored after actual response faults')
    pins=dict(good['inputHashes']);pins[str(proof)]=sha(proof);pins[str(Path(__file__))]=sha(__file__)
    need(all(sha(p)==h for p,h in pins.items()),'All actual proof/source bytes stable')
    report=dict(passed=True,nativeCapture=str(folder),actualControlFaultsRejected=faults,inputHashes=pins,fullPortAcceptance=False,newNativeBoots=0,newBuilds=0)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,actualResponseFaultsRejected=len(faults))),flush=True)
    return report
