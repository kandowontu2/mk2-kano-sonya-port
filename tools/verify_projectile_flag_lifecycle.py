"""Check real native flag writes and the ready gate; never rewrite a log/state."""
import argparse
import json
import re
from pathlib import Path


def verify(log,target,side):
    errors=[]
    identity={'kano':17,'sonya':18}[target]
    match=re.findall(r'MK2_RESTART_MATCH frame=(\d+) target=(\w+) id=(\d+) actor=([0-9A-F]+) stage=(\d+)',log)
    initial=re.findall(r'MK2_PROJECTILE_INITIAL_STATE frame=(\d+) side=(\d+) id=(\d+) actor=([0-9A-F]+) process=([0-9A-F]+) flags=([0-9A-F]+) action=([0-9A-F]+) writes=(\d+)',log)
    writes=re.findall(r'MK2_PROJECTILE_NATIVE_FLAGS frame=(\d+) age=(\d+) side=(\d+) actor=([0-9A-F]+) process=([0-9A-F]+) pc=([0-9A-F]+) before=([0-9A-F]+) after=([0-9A-F]+) mask=([0-9A-F]+) action=([0-9A-F]+) writer=(\w+)',log)
    gates=re.findall(r'MK2_PROJECTILE_GATE frame=(\d+) age=(\d+) at=([0-9A-F]+) a0=([0-9A-F]+) a1=([0-9A-F]+) a4=([0-9A-F]+) a7=([0-9A-F]+) a13=([0-9A-F]+) pc=([0-9A-F]+) action=([0-9A-F]+) process_flags=([0-9A-F]+) vy=([0-9A-F]+)',log)
    actions=re.findall(r'MK2_RESTART_PROJECTILE_EVENT frame=(\d+) age=(\d+) kind=action side=(\d+) id=(\d+) actor=([0-9A-F]+) process=([0-9A-F]+) a13=([0-9A-F]+)',log)
    if len(match)!=1 or len(initial)!=1:
        return {'passed':False,'errors':['Missing actual match or initial native state']}
    start=int(match[0][0]);actor=match[0][3];process=initial[0][4]
    if match[0][1:3]!=(target,str(identity)) or match[0][4]!='0':errors.append('Wrong restarted character')
    init=initial[0]
    if init[:4]!=(str(start),str(side),str(identity),actor) or init[7]!='0' or not 0x01000000<=int(process,16)<0x01100000:
        errors.append('Initial state is not the actual restarted human')
    current=int(init[5],16)
    if current&0x1c:errors.append('Restarted actor begins with a non-ready flag')
    set_fields=[];clear_fields=[];previous=start
    for field,age,slot,owner,task,pc,before,after,mask,action,writer in writes:
        f=int(field);old,new=int(before,16),int(after,16)
        if (not start<=f<=start+600 or f<previous or int(age)!=f-start or slot!=str(side) or owner!=actor or task!=process or
            writer!='native_game' or not 0xff800000<=int(pc,16)<=0xffffffff or int(mask,16)==0):
            errors.append('Flag write ownership/chronology/native writer incorrect')
        if old!=current or old==new:errors.append('Native flag lifecycle does not reconcile')
        if not old&4 and new&4:set_fields.append(f)
        if old&4 and not new&4:
            clear_fields.append(f)
            if int(pc,16)!=0xff83efc0:errors.append('Bit 04 was not cleared by the original recovery store')
        current=new;previous=f
    if not set_fields or not clear_fields or not any(s<c for s in set_fields for c in clear_fields):
        errors.append('No complete native hit/recovery flag lifecycle')
    if not actions:errors.append('No actual projectile action')
    for field,age,slot,own,owner,task,a13 in actions:
        if (slot,own,owner,task,a13)!=(str(side),str(identity),actor,process,process) or int(age)!=int(field)-start:
            errors.append('Action is not executed by the restarted human main process')
        ready=[g for g in gates if g[0]==field and int(g[2],16)==0xff8772f0 and g[3]==process and
               int(g[5],16)==0 and int(g[8],16)==0xff877300 and int(g[10],16)&0x1c==0 and int(g[11],16)==0]
        if not ready:errors.append('Action lacks the actual original ready-gate acceptance')
    return {'passed':not errors,'errors':errors,'target':target,'side':side,
            'native_flag_sets':len(set_fields),'native_recovery_clears':len(clear_fields),'owned_actions':len(actions),
            'observer_memory_writes':0,'scope':'native_ready_gate_and_hit_recovery_after_restart_not_other_specials'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('log',type=Path)
    parser.add_argument('--target',choices=('kano','sonya'),required=True)
    parser.add_argument('--side',choices=(1,2),type=int,required=True)
    args=parser.parse_args();result=verify(args.log.read_text(encoding='utf-8-sig'),args.target,args.side)
    print(json.dumps(result,indent=2));raise SystemExit(0 if result['passed'] else 1)


if __name__=='__main__':main()
