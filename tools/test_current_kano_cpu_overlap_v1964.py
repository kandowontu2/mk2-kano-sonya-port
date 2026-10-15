"""Corrupt copies of the real CPU mirror trace; never captured evidence."""
import json,re
from pathlib import Path
import verify_current_kano_cpu_overlap_v1963 as model

ROOT=model.ROOT;OUT=ROOT/'audit_v1964_current_kano_cpu_overlap_counterexamples'

def corrupt(log,tag,where,key,value,delete=False,extra=False):
    prefix=tag+' ';lines=log.splitlines();selected=[]
    for i,line in enumerate(lines):
        if not line.startswith(prefix):continue
        values=dict(re.findall(r'(\w+)=([^\s]+)',line))
        if all(values.get(k)==str(v)for k,v in where.items()):selected.append(i)
    assert len(selected)==1,(tag,where,len(selected))
    i=selected[0]
    if delete:del lines[i]
    else:
        changed,count=re.subn(r'(?<!\w)'+key+r'=[^\s]+',key+'='+value,lines[i])
        assert count==1 and changed!=lines[i]
        if extra:lines.insert(i+1,changed)
        else:lines[i]=changed
    return '\n'.join(lines)+'\n'

def run():
    checked=model.OUT/'report.json';proof=json.loads(checked.read_text());assert proof['passed']and not proof['fullPortAcceptance']
    pins=dict(proof['inputHashes'])
    for file,wanted in pins.items():assert model.launch.sha(file)==wanted
    pins[str(checked)]=model.launch.sha(checked)
    log=(model.CASE/'run.log').read_text(encoding='utf-8-sig');guest,_,_=model.launch.launch.current.expected()
    baseline=model.verify(log,guest);tests=[]
    def bad(label,tag,where,key='',value='',delete=False,extra=False):
        mutated=corrupt(log,tag,where,key,value,delete,extra)
        try:model.verify(mutated,guest)
        except(AssertionError,ValueError,KeyError,IndexError)as error:
            tests.append(dict(name=label,rejected=True,errorType=type(error).__name__))
        else:raise AssertionError('Accepted corrupted trace '+label)
        if len(tests)%10==0:print('Rejected '+str(len(tests))+' counterexamples',flush=True)
    pair='MK2_CPU_PAIR_FIELD'
    for label,key,value in(('cpu_proxy','id','1'),('victim_proxy','vid','1'),('detached_cpu_main','owner','01034E90'),
        ('wrong_choke_pose','pose','FE82F400'),('wrong_grip','vxpos','100'),('wrong_cpu_floor','floor','83'),
        ('wrong_victim_floor','vfloor','83'),('stale_victim_health','vhp','55')):
        bad(label,pair,{'frame':2490},key,value)
    bad('missing_held_callback',pair,{'frame':2490},delete=True)
    bad('wrong_squeeze_amount','MK2_CPU_PAIR_EVENT',{'frame':2484,'kind':'damage'},'a10','00000007')
    bad('wrong_squeeze_writer','MK2_CPU_PAIR_HEALTH',{'frame':2484,'slot':1},'a8','010350A0')
    bad('wrong_fling_gravity','MK2_CPU_PAIR_EVENT',{'frame':2526,'kind':'fling'},'a2','00004000')
    bad('stale_first_victim_cleanup','MK2_CPU_OVERLAP_EVENT',{'frame':2555,'kind':'cleanup'},'trail','01034E90')
    bad('wrong_original_cleanup_opcode','MK2_CPU_PAIR_FLAG',{'frame':2555,'kind':'flags','pc':'FF83EFC0'},'op0','B08C')
    bad('wrong_foreign_stun_operand','MK2_CPU_PAIR_FLAG',{'frame':2567,'kind':'flags','pc':'FF836030'},'a0','0106BF30')
    bad('wrong_earned_ko_writer','MK2_CPU_ROUND_HEALTH',{'frame':2662,'slot':1},'pc','FF836710')
    bad('wrong_round_winner','MK2_CPU_ROUND_HEALTH',{'frame':2850,'slot':1},'winner','1')
    bad('invented_health_refill','MK2_CPU_ROUND_FIELD',{'frame':2852,'slot':1},'hp','161')
    bad('invalid_fill_sentinel','MK2_CPU_ROUND_HEALTH',{'frame':2851,'slot':1,'after':65535},'after','65534')
    bad('missing_allmode_callback','MK2_CPU_ROUND_FIELD',{'frame':2900,'slot':2},delete=True)
    for serial,birth,hit,last in((1,2544,2567,2591),(2,2950,2976,3000)):
        stem='knife'+str(serial)+'_'
        bad(stem+'wrong_parent','MK2_CPU_OVERLAP_CHILD',{'frame':birth},'shot_owner','01034E90')
        bad(stem+'wrong_main_owner','MK2_CPU_OVERLAP_CHILD',{'frame':birth},'main_owner','010350A0')
        bad(stem+'wrong_child_type','MK2_CPU_OVERLAP_CHILD_FIELD',{'frame':birth+1},'type','1')
        bad(stem+'wrong_intro_origin','MK2_CPU_OVERLAP_CHILD_FIELD',{'frame':birth+1},'xraw','00000000')
        bad(stem+'wrong_travel_velocity','MK2_CPU_OVERLAP_CHILD_FIELD',{'frame':birth+20},'vx','00080000')
        bad(stem+'wrong_impact_pose','MK2_CPU_OVERLAP_CHILD_FIELD',{'frame':hit+2},'pose','FF60C040')
        bad(stem+'wrong_damage_slot','MK2_CPU_OVERLAP_HEALTH',{'frame':hit,'slot':1},'slot','2')
        bad(stem+'wrong_damage_amount','MK2_CPU_OVERLAP_HEALTH',{'frame':hit,'slot':1},'a10','00000007')
        bad(stem+'wrong_loaded_guard_main','MK2_KNIFE_PAIR_TESTED',{'frame':hit},'loaded_main','0106BF30')
        bad(stem+'false_physical_block','MK2_KNIFE_PAIR_BLOCK',{'frame':hit,'decision':2},'controls','FFFFFFDF'if serial==1 else'FFFFFFFF')
        bad(stem+'false_native_block_decision','MK2_KNIFE_PAIR_BLOCK',{'frame':hit,'decision':0 if serial==1 else 1},'decision','1'if serial==1 else'0')
        bad(stem+'late_retirement','MK2_CPU_OVERLAP_RETIRE',{'frame':last},'frame',str(last+1))
        bad(stem+'child_after_retirement','MK2_CPU_OVERLAP_CHILD_FIELD',{'frame':last},'frame',str(last+1),extra=True)
    bad('wrong_release_recovery_body','MK2_KNIFE_PAIR_FIELD',{'frame':2990,'slot':2},'body','0052')
    bad('shifted_knife_body_floor','MK2_KNIFE_PAIR_FIELD',{'frame':2990,'slot':2},'yraw','00530000')
    bad('stale_knife_native_handoff','MK2_CPU_OVERLAP_EVENT',{'frame':2996,'kind':'regain'},'flags','0010')
    bad('wrong_child_instruction_window','MK2_CPU_OVERLAP_CODE',{'start':'FFFC6000'},'words','0000')
    assert model.verify(log,guest)==baseline
    for file,wanted in pins.items():assert model.launch.sha(file)==wanted,'Original evidence changed'
    model.launch.launch.module_pins(pins)
    return dict(passed=True,candidate=model.launch.launch.NAME,counterexamples=tests,inputHashes=pins,
        originalCapturesUnchanged=True,gameBytesChanged=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed evidence'
    try:result=run()
    except Exception as error:
        import traceback
        result=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=result['passed'],counterexamples=len(result.get('counterexamples',[])),error=result.get('error'))),flush=True)
    raise SystemExit(0 if result['passed']else 1)
