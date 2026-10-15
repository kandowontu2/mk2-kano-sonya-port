"""In-memory counterexamples for actual current CPU reset and choke/blade traces."""
import json
import re
import verify_current_cpu_round_trace_v1900 as rounds
import verify_current_cpu_signature_followup_v1902 as typed
from test_native_cpu_cycle_bookkeeping_v1426 import changed
from verify_human_special_phases_v1767 import sha

ROOT=rounds.ROOT
OUT=ROOT/'audit_v1903_current_cpu_round_and_kano_counterexamples'

def change_round(log,tag,frame,slot,key,value,predicate=lambda line:True):
    lines=log.splitlines();found=[i for i,line in enumerate(lines)if line.startswith('MK2_CPU_ROUND_'+tag+' ')and
        f'frame={frame} 'in line and f'slot={slot} 'in line and predicate(line)]
    assert len(found)==1,(tag,frame,slot,key,len(found))
    i=found[0];old=lines[i]
    assert len(re.findall(r'\b'+key+r'=\S+',old))==1
    lines[i]=re.sub(r'\b'+key+r'=\S+',key+'='+str(value),old)
    assert lines[i]!=old,'Counterexample actually changes observed data'
    return '\n'.join(lines)+'\n'

def verify():
    pins={}
    for leaf in ('audit_v1900_current_cpu_round_repeat_checked','audit_v1902_current_kano_cpu_floor_signature_checked'):
        path=ROOT/leaf/'report.json';proof=json.loads(path.read_text());assert proof['passed'] and proof['candidate']==rounds.launch.NAME
        pins.update(proof['inputHashes']);pins[str(path)]=sha(path)
    for file,wanted in pins.items():assert sha(file)==wanted
    log=(rounds.CASE/'run.log').read_text(encoding='utf-8-sig')
    base=rounds.verify(log);ko,reset=base['earnedKOFrame'],base['originalResetFrame']
    sentinel=reset+1
    mutations={
        'Missing callback in original round transition':'\n'.join(line for line in log.splitlines()if not(line.startswith('MK2_CPU_ROUND_FIELD ')and f'frame={reset} slot=2 'in line))+'\n',
        'Live actor is a Liu proxy':change_round(log,'FIELD',ko-1,1,'id',1),
        'Live Main is detached from actual actor':change_round(log,'FIELD',ko-1,1,'owner','00000000'),
        'Unlogged HP after earned KO':change_round(log,'FIELD',ko+1,2,'hp',1),
        'Reset assigned to wrong winner':change_round(log,'HEALTH',reset,2,'winner',2),
        'Native reset writer replaced':change_round(log,'HEALTH',reset,2,'pc','FF825950'),
        'Original reset instruction word corrupted':change_round(log,'HEALTH',reset,2,'op0','0000'),
        'Missing original P2 health reset':'\n'.join(line for line in log.splitlines()if not(line.startswith('MK2_CPU_ROUND_HEALTH ')and f'frame={reset} slot=2 'in line))+'\n',
        'Fill sentinel incorrectly accepted in live combat':change_round(log,'HEALTH',sentinel,2,'mode',2,lambda line:'pc=FF9DED10 'in line),
        'Sentinel value is not original FFFF':change_round(log,'HEALTH',sentinel,2,'after',65534,lambda line:'pc=FF9DED10 'in line),
        'Original fill begins with wrong value':change_round(log,'HEALTH',sentinel,2,'after',5,lambda line:'pc=FF9DEF70 'in line),
        'Fill store belongs to wrong health address':change_round(log,'HEALTH',sentinel+2,2,'at','010602F0'),
        'Fill skips its one-field cadence':change_round(log,'HEALTH',sentinel+2,2,'frame',sentinel+3),
        'Original fill stores wrong intermediate value':change_round(log,'HEALTH',sentinel+2,2,'after',9),
    }
    results=[]
    for label,mutant in mutations.items():
        assert mutant!=log
        try:rounds.verify(mutant)
        except (AssertionError,ValueError,KeyError,IndexError)as error:results.append(dict(counterexample=label,rejected=True,error=str(error)))
        else:raise AssertionError(label)
    raw=(ROOT/'audit_v1891_kano_cpu_choke_follow_human_kano/run.log').read_text(encoding='utf-8-sig')
    kano='\n'.join(line for line in raw.splitlines()if line.startswith(('MK2_CPU_PAIR_','MK2_P1CPU_')))+'\n'
    proof=typed.verify_log(kano,'kano','blade');assert proof['passed'],proof['errors']
    first=min(r['frame']for r in typed.rows(kano,'EVENT')if r['kind']=='step')+1
    follow,ready=proof['native_followup']['entry'],proof['native_followup']['ready']
    changes={
        'Kano CPU proxy ID':changed(kano,'FIELD',first,'id',1),
        'Mirror victim proxy ID':changed(kano,'FIELD',first,'vid',1),
        'Wrong choke-held pose':changed(kano,'FIELD',first,'pose','FE830000'),
        'Wrong choke grip position':changed(kano,'FIELD',first,'vxpos',999),
        'Wrong victim floor on native release':changed(kano,'FIELD',proof['release']+1,'vfloor',999),
        'Blade begins with wrong native pose':changed(kano,'FIELD',follow+1,'pose','FE830000'),
        'Blade detached during active follow-up':changed(kano,'FIELD',follow+1,'trail','00000000'),
        'Native blade ready retains Main busy flag':changed(kano,'FOLLOW_REGAIN',ready,'flags','00000010'),
        'Native blade ready retains trail':changed(kano,'FOLLOW_REGAIN',ready,'trail','01032D90'),
        'Subsequent follow-up relabelled ordinal':changed(kano,'FOLLOW_FIELD',ready+3,'cycle',999),
    }
    for label,mutant in changes.items():
        result=typed.verify_log(mutant,'kano','blade');assert not result['passed'],label
        results.append(dict(counterexample=label,rejected=True,errors=result['errors']))
    rounds.launch.module_pins(pins)
    for file,wanted in pins.items():assert sha(file)==wanted,'Real captures changed by counterexamples'
    return dict(passed=True,candidate=rounds.launch.NAME,pristineRoundAndKanoAccepted=True,counterexamples=results,
                actualCapturesModified=False,inputHashes=pins,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed evidence'
    try:proof=verify()
    except Exception as error:proof=dict(passed=False,error=repr(error),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps(dict(passed=proof['passed'],error=proof.get('error'),rejected=len(proof.get('counterexamples',[])))),flush=True)
    raise SystemExit(0 if proof['passed']else 1)
