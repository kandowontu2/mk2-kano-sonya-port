"""Current physical P2 CPU contact and original continuation counterexamples."""
import json
from pathlib import Path
import verify_current_physical_p2_cpu_v1916 as model
from test_current_cpu_overlap_v1912 import mutate

ROOT=model.ROOT;OUT=ROOT/'audit_v1922_current_physical_p2_cpu_counterexamples'

def verify():
    proof=json.loads((model.OUT/'report.json').read_text());assert proof['passed']
    pins=dict(proof['inputHashes']);pins[str(model.OUT/'report.json')]=model.sha(model.OUT/'report.json')
    guest,_,_=model.launch.current.expected();rejected=[]
    for player,leaf in model.CASES.items():
        log=(ROOT/leaf/'run.log').read_text(encoding='utf-8-sig');base=model.verify_log(log,player,guest)['originalContract']
        start,release,own,victim=tuple(base[k]for k in('start','release','own_handoff','victim_handoff'))
        ready=base['native_followup']['first_ready']
        P='MK2_CPU_PAIR_'
        clear=[r for r in model.original.flag_rows(log)if r['frame']==own and r['slot']==2 and r['kind']=='body'and r['before']!=r['after']]
        assert len(clear)==1
        clear_before=f"{clear[0]['before']:04X}"
        tests=[
          ('wrong physical CPU slot',P+'FIELD',{'frame':str(start+20)},'cpu_slot','1'),
          ('CPU proxy identity',P+'FIELD',{'frame':str(start+20)},'id','1'),
          ('wrong victim Main owner',P+'FIELD',{'frame':str(start+20)},'vowner','010350A0'),
          ('wrong original held victim pose',P+'FIELD',{'frame':str(start+20)},'vpose','FE82AAA0'),
          ('wrong physical P1 floor',P+'FIELD',{'frame':str(start+20)},'vfloor','83'),
          ('wrong CPU floor',P+'FIELD',{'frame':str(start+20)},'floor','82'),
          ('wrong original fling vertical velocity',P+'FIELD',{'frame':str(release+1)},'vvy','00000000'),
          ('wrong physical health slot',P+'HEALTH',{'frame':str(release),'slot':'1'},'slot','2'),
          ('wrong leg damage request',P+'EVENT',{'frame':str(release),'kind':'damage'},'a10','00000024'),
          ('stale own lock at ready',P+'OWN_REGAIN',{'frame':str(own)},'flags','00000010'),
          ('stale victim child at ready',P+'VICTIM_REGAIN',{'frame':str(victim)},'vtrail','010350A0'),
          ('wrong native ready opcode',P+'FLAG',{'frame':str(own),'slot':'2','kind':'body','before':clear_before},'op0','0000'),
          ('stale follow-up lock',P+'FOLLOW_REGAIN',{'frame':str(ready)},'flags','00000010'),
          ('missing actual follow-up ready',P+'FOLLOW_READY_INSTRUCTION',{'frame':str(ready),'kind':'regained'},None,None),
          ('wrong terminal continuation',P+'RESULT',{},'frame',str(ready+31)),
          ('missing paired callback',P+'FIELD',{'frame':str(start+20)},None,None),
        ]
        for label,tag,criteria,key,value in tests:
            damaged=mutate(log,tag,criteria,key,value)
            try:model.verify_log(damaged,player,guest)
            except (AssertionError,KeyError,IndexError,ValueError)as error:
                rejected.append(dict(player=player,name=label,error=repr(error)));print('Rejected '+player+': '+label,flush=True)
            else:raise AssertionError('Accepted corruption '+player+': '+label)
    model.launch.module_pins(pins)
    for file,value in pins.items():assert model.sha(file)==value,'Changed original evidence '+file
    return dict(passed=True,candidate=model.launch.NAME,counterexamples=rejected,inputHashes=pins,originalCapturesUnchanged=True,gameBytesChanged=False,fullPortAcceptance=False)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed evidence'
    try:result=verify()
    except Exception as error:result=dict(passed=False,error=repr(error),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=result['passed'],rejected=len(result.get('counterexamples',[])),error=result.get('error'))),flush=True)
    raise SystemExit(0 if result['passed']else 1)
