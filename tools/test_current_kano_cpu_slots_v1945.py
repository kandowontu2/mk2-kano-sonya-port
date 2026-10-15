"""Current Kano CPU on both physical sides: typed state and rendered ownership."""
import functools,json
from pathlib import Path
import verify_current_kano_sonya_cpu_display_v1934 as p1
import verify_current_kano_physical_p2_cpu_v1941 as p2
from test_current_cpu_overlap_v1912 import mutate

ROOT=p1.ROOT;OUT=ROOT/'audit_v1945_current_kano_cpu_slots_counterexamples'

def verify():
    pins={};reports=[]
    for model in(p1,p2):
        path=model.OUT/'report.json';report=json.loads(path.read_text());assert report['passed']
        for file,value in report['inputHashes'].items():
            assert file not in pins or pins[file]==value;pins[file]=value
        pins[str(path)]=p2.sha(path);reports.append(report)
    original_expected=p2.launch.current.expected
    p2.launch.current.expected=functools.lru_cache(maxsize=1)(original_expected)
    guest,_,payload=p2.launch.current.expected();rejected=[];raw_p1=None;proof_p1=None
    for cpu_slot,folder in ((1,p1.CASE),(2,ROOT/p2.CASES['sonya'])):
        raw=(folder/'run.log').read_text(encoding='utf-8-sig')
        log='\n'.join(line for line in raw.splitlines()if line.startswith(('MK2_CPU_PAIR_','MK2_P1CPU_','MK2_P2CPU_')))+'\n'
        def check(text):return p1.verify_log(text)if cpu_slot==1 else p2.verify_log(text,'sonya',guest)['originalContract']
        base=check(log);assert base==check(raw)
        parser=p1.ordinary if cpu_slot==1 else p2.original
        human_slot=3-cpu_slot;start=base['start'];ready=base['native_followup']['first_ready']
        held=min(r['frame']for r in parser.rows(log,'EVENT')if r['kind']=='step'and r['cycle']==base['cycle'])+1
        first=next(r for r in parser.rows(log,'HEALTH')if r['slot']==human_slot and start<=r['frame']<=base['complete']and r['before']>r['after'])
        own=base['own_handoff'];victim=base['victim_handoff']
        clear=[r for r in parser.flag_rows(log)if r['slot']==cpu_slot and r['frame']==own and r['kind']=='body'and r['before']!=r['after']]
        assert len(clear)==1
        P='MK2_CPU_PAIR_'
        tests=[
          ('CPU proxy',P+'FIELD',{'frame':str(held)},'id','1'),
          ('victim proxy',P+'FIELD',{'frame':str(held)},'vid','1'),
          ('wrong CPU physical role',P+'FIELD',{'frame':str(held)},'cpu_slot',str(human_slot)),
          ('detached victim Main',P+'FIELD',{'frame':str(held)},'vowner','01000000'),
          ('wrong choke body pose',P+'FIELD',{'frame':str(held)},'pose','FE820000'),
          ('wrong choke victim grip',P+'FIELD',{'frame':str(held)},'vxpos','999'),
          ('wrong Kano floor',P+'FIELD',{'frame':str(held)},'floor','83'),
          ('wrong Sonya floor',P+'FIELD',{'frame':str(held)},'vfloor','82'),
          ('wrong native damage request',P+'EVENT',{'frame':str(first['frame']),'kind':'damage'},'a10','00000009'),
          ('wrong native health writer',P+'HEALTH',{'frame':str(first['frame']),'slot':str(human_slot)},'pc','FF836710'),
          ('wrong physical victim health slot',P+'HEALTH',{'frame':str(first['frame']),'slot':str(human_slot)},'slot',str(cpu_slot)),
          ('wrong fling gravity',P+'FIELD',{'frame':str(base['release']+1)},'vgravity','00010000'),
          ('stale own ready lock',P+'OWN_REGAIN',{'frame':str(own)},'flags','00000010'),
          ('stale victim ready trail',P+'VICTIM_REGAIN',{'frame':str(victim)},'vtrail','01000000'),
          ('wrong native clear opcode',P+'FLAG',{'frame':str(own),'slot':str(cpu_slot),'kind':'body','before':f"{clear[0]['before']:04X}"},'op0','0000'),
          ('stale actual ordinary follow-up lock',P+'FOLLOW_REGAIN',{'frame':str(ready)},'flags','00000010'),
          ('missing actual subsequent ready',P+'FOLLOW_READY_INSTRUCTION',{'frame':str(ready),'kind':'regained'},None,None),
          ('missing paired callback',P+'FIELD',{'frame':str(held)},None,None),
        ]
        for label,tag,criteria,key,value in tests:
            damaged=mutate(log,tag,criteria,key,value)
            try:check(damaged)
            except (AssertionError,KeyError,IndexError,ValueError)as error:
                rejected.append(dict(cpuSlot=cpu_slot,name=label,error=repr(error)));print('Rejected P'+str(cpu_slot)+' '+label,flush=True)
            else:raise AssertionError('Accepted corruption: P'+str(cpu_slot)+' '+label)
        if cpu_slot==1:raw_p1,proof_p1=raw,base
    groups,*_=p1.display.raster.data(p1.CASE);context={**proof_p1,'log':raw_p1}
    pristine=p1.display.check_composites(groups,payload,guest,context)
    dispatch=groups['FLOOR_QUEUE_DISPATCH'][0]
    index=next(i for i,r in enumerate(groups['FLOOR_QUEUE'])if(r['frame'],r['cursor'])==(dispatch['queue_frame'],dispatch['cursor']))
    for label,key,value in(('rendered proxy ID','id',1),('rendered detached Main owner','owner',0),('wrong actual native cache row','row',0)):
        altered={**groups,'FLOOR_QUEUE':list(groups['FLOOR_QUEUE'])};altered['FLOOR_QUEUE'][index]={**altered['FLOOR_QUEUE'][index],key:value}
        try:p1.display.check_composites(altered,payload,guest,context)
        except ValueError as error:rejected.append(dict(cpuSlot=1,name=label,error=str(error)))
        else:raise AssertionError('Accepted corrupt rendering '+label)
    altered={**groups,'FLOOR_QUEUE_DISPATCH':groups['FLOOR_QUEUE_DISPATCH'][1:]}
    try:p1.display.check_composites(altered,payload,guest,context)
    except ValueError as error:rejected.append(dict(cpuSlot=1,name='missing actual owned DMA',error=str(error)))
    else:raise AssertionError('Accepted omitted owned DMA')
    p2.launch.module_pins(pins)
    for file,value in pins.items():assert p2.sha(file)==value,'Changed actual evidence '+file
    return dict(passed=True,candidate=p2.launch.NAME,counterexamples=rejected,inputHashes=pins,
        pristineComposite=pristine,originalCapturesUnchanged=True,gameBytesChanged=False,fullPortAcceptance=False)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed evidence'
    try:result=verify()
    except Exception as error:result=dict(passed=False,error=repr(error),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=result['passed'],rejected=len(result.get('counterexamples',[])),error=result.get('error'))),flush=True)
    raise SystemExit(0 if result['passed']else 1)
