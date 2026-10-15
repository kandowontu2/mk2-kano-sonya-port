"""Current natural CPU leg/Square trace counterexamples, without capture writes."""
import json
from pathlib import Path
import verify_current_cpu_square_followup_v1883 as display
import verify_cpu_followup_v1423 as state
from test_native_cpu_cycle_bookkeeping_v1426 import changed
from verify_human_special_phases_v1767 import sha

ROOT=display.ROOT
CASE=ROOT/'audit_v1884_sonya_cpu_leg_square_human_kano'
OUT=ROOT/'audit_v1888_current_cpu_square_counterexamples'

def verify():
    accepted=ROOT/'audit_v1885_current_cpu_leg_square_checked/report.json'
    report=json.loads(accepted.read_text());assert report['passed'] and report['candidate']==display.NAME
    pins=dict(report['inputHashes']);pins[str(accepted)]=sha(accepted)
    for file,wanted in pins.items():assert sha(file)==wanted,'Changed accepted CPU proof '+file
    raw=(CASE/'run.log').read_text(encoding='utf-8-sig')
    log='\n'.join(line for line in raw.splitlines()if line.startswith(('MK2_CPU_PAIR_','MK2_P1CPU_')))+'\n'
    proof=state.verify_log(log,'kano','square');assert proof['passed'],proof['errors']
    assert proof==state.verify_log(raw,'kano','square'),'Rendering rows cannot replace state evidence'
    first=proof['start']+1;ready=proof['native_followup']['ready'];later=ready+3
    follow=proof['native_followup']['entry']
    held=min(row['frame']for row in state.rows(log,'EVENT')if row['kind']=='step')+1
    mutations={
        'CPU proxy ID':changed(log,'FIELD',first,'id',1),
        'Human proxy ID':changed(log,'FIELD',first,'vid',1),
        'Wrong CPU physical slot':changed(log,'FIELD',first,'cpu_slot',2),
        'Wrong Main owner':changed(log,'FIELD',first,'owner','01000000'),
        'Wrong leg pose':changed(log,'FIELD',held,'pose','FE830000'),
        'Unlogged victim health':changed(log,'FIELD',proof['release']+2,'vhp',1),
        'Wrong Square rising velocity':changed(log,'FIELD',follow+2,'vy','FFF50000'),
        'Wrong Square horizontal speed':changed(log,'FIELD',follow+10,'vx','00000000'),
        'Wrong Square flight height':changed(log,'FIELD',follow+10,'y',999),
        'Persistent body lock at actual ready':changed(log,'FOLLOW_REGAIN',ready,'body','00000016'),
        'Persistent Main lock at actual ready':changed(log,'FOLLOW_REGAIN',ready,'flags','00000010'),
        'Wrong subsequent CPU Main':changed(log,'FOLLOW_FIELD',later,'main','01000000'),
        'Wrong completed follow ordinal':changed(log,'FOLLOW_FIELD',later,'cycle',999),
        'Wrong actual grab ordinal':changed(log,'FIELD',later,'cycle',999),
        'Removed actual Square entry':'\n'.join(line for line in log.splitlines()if not(line.startswith('MK2_CPU_PAIR_FOLLOW_INSTRUCTION ')and'kind=action 'in line))+'\n',
        'Missing owning ready instruction':'\n'.join(line for line in log.splitlines()if not(line.startswith('MK2_CPU_PAIR_FOLLOW_READY_INSTRUCTION ')and'kind=regained 'in line))+'\n',
        'Wrong native health writer':log.replace('pc=FF836700','pc=00000000',1),
    }
    results=[]
    for label,mutant in mutations.items():
        assert mutant!=log,'No-op corruption'
        result=state.verify_log(mutant,'kano','square');assert not result['passed'],label
        results.append(dict(counterexample=label,rejected=True,errors=result['errors']))
    groups,*_=display.raster.data(CASE)
    guest,_,payload=display.active.expected()
    context={**proof,'log':raw}
    baseline=display.check_composites(groups,payload,guest,context)
    dispatch=groups['FLOOR_QUEUE_DISPATCH'][0]
    index=next(i for i,q in enumerate(groups['FLOOR_QUEUE'])if(q['frame'],q['cursor'])==(dispatch['queue_frame'],dispatch['cursor']))
    for label,key,value in (('Composite proxy ID','id',1),('Composite wrong owner','owner',0),('Composite wrong original cache cursor','row',0)):
        altered={**groups,'FLOOR_QUEUE':list(groups['FLOOR_QUEUE'])}
        altered['FLOOR_QUEUE'][index]={**altered['FLOOR_QUEUE'][index],key:value}
        assert altered['FLOOR_QUEUE'][index]!=groups['FLOOR_QUEUE'][index]
        try:display.check_composites(altered,payload,guest,context)
        except ValueError as error:results.append(dict(counterexample=label,rejected=True,error=str(error)))
        else:raise AssertionError(label)
    altered={**groups,'FLOOR_QUEUE_DISPATCH':groups['FLOOR_QUEUE_DISPATCH'][1:]}
    try:display.check_composites(altered,payload,guest,context)
    except ValueError as error:results.append(dict(counterexample='Missing actual owned DMA dispatch',rejected=True,error=str(error)))
    else:raise AssertionError('Missing actual owned DMA dispatch')
    display.active_launch.module_pins(pins)
    for file,wanted in pins.items():assert sha(file)==wanted,'Counterexamples altered real evidence '+file
    return dict(passed=True,candidate=display.NAME,statePristineAccepted=True,compositePristineAccepted=baseline,
                counterexamples=results,inputHashes=pins,actualCapturesModified=False,fullPortAcceptance=False,
                scope=__doc__)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed evidence'
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=report['passed'],error=report.get('error'),rejected=len(report.get('counterexamples',[])))),flush=True)
    raise SystemExit(0 if report['passed']else 1)
