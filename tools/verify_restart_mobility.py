"""Owned mobility command, flight/collision and recovery after a real restart."""
import re

SPECS={'kano':('ball',17,0xffffdb00,0xffffde00,0xffffec00,0xff0000e0,0x20b),
       'sonya':('square',18,0xffffc800,0xffffca00,0xffffda00,0xff0203c0,0x207)}


def verify(log,target,side):
    errors=[]
    name,identity,parser,action,attack,animation,state=SPECS[target]
    def one(pattern,label):
        rows=re.findall(pattern,log)
        if len(rows)!=1:errors.append(label+' must occur exactly once');return None
        return rows[0]
    guard=one(r'MK2_RESTART_MOBILITY_ROM target=(\w+) side=(\d+) move=(\w+) parser=([0-9A-F]+) action=([0-9A-F]+) attack=([0-9A-F]+) animation=([0-9A-F]+) state=([0-9A-F]+) writes=(\d+)','Native mobility guards')
    if guard and (guard[:3]!=(target,str(side),name) or tuple(int(v,16) for v in guard[3:8])!=(parser,action,attack,animation,state) or guard[8]!='0'):
        errors.append('Wrong native code/descriptor/animation guard')
    match=one(r'MK2_RESTART_MATCH frame=(\d+) target=(\w+) id=(\d+) actor=([0-9A-F]+) stage=(\d+)','Actual restarted match')
    done=one(r'MK2_RESTART_COMPLETE frame=(\d+)[^\r\n]* live=(\d+) errors=(\d+) restart_writes=(\d+)','Completed restarted match')
    result=one(r'MK2_RESTART_MOBILITY_RESULT pass=(\w+) target=(\w+) side=(\d+) move=(\w+) commands=(\d+) parsers=(\d+) actions=(\d+) animations=(\d+) attacks=(\d+) recoveries=(\d+) ready=(\d+) errors=(\d+) writes=(\d+)','Mobility result')
    counts={kind:0 for kind in ('parser','action','animation','attack','recovery','ready')}
    if not match or not done:return {'passed':False,'errors':errors,'scope':'owned_mobility_after_restart'}
    mf,df=int(match[0]),int(done[0]);actor=match[3]
    if match[1:3]!=(target,str(identity)) or match[4]!='0' or df-mf!=600 or done[1:]!=('601','0','0'):
        errors.append('Incorrect actual match/601-field completion')
    def ownership(field,age,slot,own,owner,process=None):
        if not mf<=int(field)<=df or int(age)!=int(field)-mf or slot!=str(side) or own!=str(identity) or owner!=actor:
            errors.append('Wrong event actor/identity/slot/chronology')
        if process and not 0x01000000<=int(process,16)<0x01100000:errors.append('Invalid owned process')
    commands=[]
    if target=='sonya':
        rows=re.findall(r'MK2_RESTART_MOBILITY_COMMAND frame=(\d+) age=(\d+) side=(\d+) target=(\w+) first=(\w+) second=(\w+) button=(\w+) writes=(\d+)',log)
        if len(rows)!=3 or [int(r[1]) for r in rows]!=[0,160,320]:errors.append('Missing actual square command pulses')
        for field,age,slot,fighter,first,second,button,writes in rows:
            if int(field)!=mf+int(age) or (slot,fighter,button,writes)!=(str(side),target,'hp','0') or {first,second}!={'left','right'}:
                errors.append('Wrong square input command')
            commands.append(int(field))
    else:
        press=one(r'MK2_RESTART_MOBILITY_PRESS frame=(\d+) age=(\d+) side=(\d+) target=(\w+) button=(\w+) writes=(\d+)','Actual LK press')
        release=one(r'MK2_RESTART_MOBILITY_RELEASE frame=(\d+) age=(\d+) side=(\d+) target=(\w+) button=(\w+) hold=(\d+) writes=(\d+)','Actual LK release')
        if press and release:
            if press!=(str(mf),'0',str(side),target,'lk','0') or release[2:5]!=(str(side),target,'lk') or release[6]!='0' or int(release[0])!=mf+int(release[1]) or int(release[5])!=int(release[1]) or not 81<=int(release[5])<=450:
                errors.append('Invalid real LK hold/release')
            commands=[int(release[0])]
            elapsed=re.findall(r'MK2_RESTART_MOBILITY_ELAPSED frame=(\d+) age=(\d+) side=(\d+) actor=([0-9A-F]+) ticks=(\d+) pc=([0-9A-F]+)',log)
            if not elapsed or any(int(f)<int(release[0]) or int(f)>int(release[0])+8 or int(a)!=int(f)-mf or s!=str(side) or own!=actor or int(ticks)<=80 or int(pc,16)!=0xffffdb70 for f,a,s,own,ticks,pc in elapsed):
                errors.append('Original native charge threshold not actually observed')
    events=re.findall(r'MK2_RESTART_MOBILITY_EVENT frame=(\d+) age=(\d+) kind=(\w+) cycle=(\d+) side=(\d+) id=(\d+) actor=([0-9A-F]+) process=([0-9A-F]+) a13=([0-9A-F]+) pc=([0-9A-F]+) entry=([0-9A-F]+) count=(\d+)',log)
    cycles={};latest_parser=None
    entries={'parser':parser,'action':action,'attack':attack,'animation':animation,'recovery':0xff861350}
    for field,age,kind,cycle,slot,own,owner,process,a13,pc,entry,count in events:
        f,c=int(field),int(cycle)
        ownership(field,age,slot,own,owner,process)
        if kind not in entries:errors.append('Unknown mobility event');continue
        counts[kind]+=1
        if int(count)!=counts[kind] or int(entry,16)!=entries[kind] or not 0xff800000<=int(pc,16)<=0xffffffff or not 0x01000000<=int(a13,16)<0x01100000:
            errors.append('Wrong actual code entry/process/count')
        if kind!='parser' and a13!=process:errors.append('Mobility did not execute in the human main process')
        if kind=='parser':latest_parser=f;continue
        if kind=='action':
            prior=[v for v in commands if v<=f]
            if not prior or not 1<=f-max(prior)<=36 or latest_parser is None or not 0<=f-latest_parser<=36 or c!=counts['action']:
                errors.append('Action is not preceded by the actual command/parser')
            cycles[c]={'start':f,'process':process,'animation':[],'attack':[],'recovery':[],'physics':[],'ready':[]}
        elif c not in cycles:errors.append('Mobility event has no actual owned action')
        else:
            current=cycles[c]
            if process!=current['process'] or not current['start']<=f<=df:errors.append('Wrong action-cycle ownership/chronology')
            if kind=='recovery' and (not current['attack'] or f<current['attack'][-1]):errors.append('Recovery precedes actual attack')
            current[kind].append(f)
    physics=re.findall(r'MK2_RESTART_MOBILITY_PHYSICS frame=(\d+) age=(\d+) cycle=(\d+) side=(\d+) id=(\d+) actor=([0-9A-F]+) action=([0-9A-F]+) y=(\d+) floor=(\d+) vx=([0-9A-F]+) vy=([0-9A-F]+) body=([0-9A-F]+)',log)
    for field,age,cycle,slot,own,owner,act,y,floor,vx,vy,body in physics:
        ownership(field,age,slot,own,owner)
        c=int(cycle)
        if c not in cycles or int(act,16) not in (state,0x602) or not cycles.get(c,{}).get('start',df+1)<=int(field)<=df:
            errors.append('Physics not owned by an actual mobility cycle');continue
        cycles[c]['physics'].append((int(floor)-int(y),int(vx,16),int(vy,16),int(body,16)))
    ready=re.findall(r'MK2_RESTART_MOBILITY_READY frame=(\d+) age=(\d+) cycle=(\d+) side=(\d+) id=(\d+) actor=([0-9A-F]+) process=([0-9A-F]+) y=(\d+) floor=(\d+) vx=([0-9A-F]+) vy=([0-9A-F]+) flags=([0-9A-F]+) body=([0-9A-F]+) trail=([0-9A-F]+) count=(\d+) writes=(\d+)',log)
    for field,age,cycle,slot,own,owner,process,y,floor,vx,vy,flags,body,trail,count,writes in ready:
        ownership(field,age,slot,own,owner,process);c=int(cycle);counts['ready']+=1
        if int(count)!=counts['ready'] or y!=floor or int(vx,16)!=0 or int(vy,16)!=0 or int(flags,16)&0x1c or int(body,16)&8 or int(trail,16)!=0 or writes!='0':
            errors.append('Incomplete grounded/native flag/attachment recovery')
        if c not in cycles or not cycles.get(c,{}).get('recovery') or process!=cycles[c]['process'] or not cycles[c]['recovery'][0]<=int(field)<=df:
            errors.append('Ready state has no actual native recovery')
        else:cycles[c]['ready'].append(int(field))
    complete=[]
    for c,data in cycles.items():
        flight=data['physics']
        if target=='sonya':moving=any(height>=80 for height,vx,vy,body in flight) and any(vx in (0xa0000,0xfff60000) for height,vx,vy,body in flight)
        else:moving=any(height==-16 and vx in (0xa0000,0xfff60000) and body&8 for height,vx,vy,body in flight)
        if moving and all(data[k] for k in ('animation','attack','recovery','ready')):complete.append(c)
    if not complete:errors.append('No complete owned native movement/collision/grounded recovery cycle')
    if min(counts.values())<=0:errors.append('Missing a native mobility pipeline stage')
    if result and result!=('true',target,str(side),name,str(len(commands)),*(str(counts[k]) for k in ('parser','action','animation','attack','recovery','ready')),'0','0'):
        errors.append('Mobility result contradicts actual captured events')
    if 'MK2_RESTART_MOBILITY_ERROR' in log:errors.append('Actual mobility observer errors')
    return {'passed':not errors,'errors':errors,'target':target,'side':side,'move':name,'native_counts':counts,
            'completed_owned_cycles':complete,'memory_writes':0,'scope':'owned_ball_or_square_flight_collision_and_recovery_after_restart_not_damage_parity_or_other_specials'}
