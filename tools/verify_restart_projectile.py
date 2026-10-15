"""Independently require input -> owned parser -> action -> animation after restart."""
import re

IDS={'kano':17,'sonya':18}


def verify(log,target,side):
    errors=[]
    own=IDS[target]
    parser,action,animation=(0xffffac00,0xffffb000,0xff0004e0) if target=='kano' else (0xffffae00,0xffffb400,0xff0204e0)
    mask=0x63 if target=='kano' else 0x72
    def single(pattern,label):
        matches=re.findall(pattern,log)
        if len(matches)!=1:errors.append(label+' must occur exactly once');return None
        return matches[0]
    guard=single(r'MK2_RESTART_PROJECTILE_ROM target=(\w+) side=(\d+) parser=([0-9A-F]+) first=([0-9A-F]+) mask=([0-9A-F]+) action=([0-9A-F]+) opcode=([0-9A-F]+) animation=([0-9A-F]+) writes=(\d+)','Native projectile code guard')
    if guard and (guard[:2]!=(target,str(side)) or tuple(int(v,16) for v in guard[2:8])!=(parser,0x09c0,mask,action,0x574a,animation) or guard[8]!='0'):
        errors.append('Wrong actual native parser/action/animation code guard')
    match=single(r'MK2_RESTART_MATCH frame=(\d+) target=(\w+) id=(\d+) actor=([0-9A-F]+) stage=(\d+)','Actual restarted match')
    done=single(r'MK2_RESTART_COMPLETE frame=(\d+)[^\r\n]* live=(\d+) errors=(\d+) restart_writes=(\d+)','Actual restart completion')
    result=single(r'MK2_RESTART_PROJECTILE_RESULT pass=(\w+) target=(\w+) side=(\d+) commands=(\d+) parsers=(\d+) actions=(\d+) animations=(\d+) errors=(\d+) writes=(\d+)','Owned projectile result')
    commands=re.findall(r'MK2_RESTART_PROJECTILE_COMMAND frame=(\d+) age=(\d+) side=(\d+) target=(\w+) direction=(\w+) button=(\w+) writes=(\d+)',log)
    plans=re.findall(r'MK2_RESTART_PROJECTILE_PLAN first=(\d+) interval=(\d+) commands=(\d+) writes=(\d+)',log)
    # The archived start-at-zero fixtures predate the explicit timing option.
    first_age=0
    if plans:
        if len(plans)!=1 or not 0<=int(plans[0][0])<=140 or plans[0][1:]!=('160','3','0'):
            errors.append('Invalid actual ordinary-input command plan')
        else:first_age=int(plans[0][0])
    events=re.findall(r'MK2_RESTART_PROJECTILE_EVENT frame=(\d+) age=(\d+) kind=(\w+) side=(\d+) id=(\d+) actor=([0-9A-F]+) process=([0-9A-F]+) a13=([0-9A-F]+) pc=([0-9A-F]+) entry=([0-9A-F]+) count=(\d+)',log)
    counts={'parser':0,'action':0,'animation':0}
    if match and done:
        mf,df=int(match[0]),int(done[0])
        if match[1:3]!=(target,str(own)) or match[4]!='0' or df-mf!=600 or done[1:]!=('601','0','0'):
            errors.append('Projectile coverage is not the correct full restarted match')
        expected_ages=[first_age+offset for offset in (0,160,320)]
        if len(commands)!=len(expected_ages) or [int(c[1]) for c in commands]!=expected_ages:
            errors.append('Missing actual ordinary projectile command pulses')
        for field,age,slot,fighter,direction,button,writes in commands:
            if int(field)!=mf+int(age) or (slot,fighter,button,writes)!=(str(side),target,'hp' if target=='kano' else 'lp','0') or direction not in ('left','right'):
                errors.append('Wrong actual command side/button/chronology/assistance')
        previous_parser,previous_action=None,None
        for field,age,kind,slot,identity,actor,process,a13,pc,entry,count in events:
            f=int(field)
            if kind not in counts:errors.append('Unknown native pipeline event');continue
            counts[kind]+=1
            if (int(count)!=counts[kind] or int(age)!=f-mf or not mf<=f<=df or slot!=str(side) or int(identity)!=own or
                actor!=match[3] or not all(0x01000000<=int(a,16)<0x01100000 for a in (actor,process,a13)) or
                not 0xff800000<=int(pc,16)<=0xffffffff or int(entry,16)!={'parser':parser,'action':action,'animation':animation}[kind]):
                errors.append('Native event ownership/code/chronology does not match restarted human')
            if kind=='parser':previous_parser=f
            elif kind=='action':
                prior=[int(c[0]) for c in commands if int(c[0])<=f]
                if not prior or not 6<=f-max(prior)<=36 or previous_parser is None or not 0<=f-previous_parser<=36:
                    errors.append('Actual action does not follow actual command/parser')
                previous_action=f
            elif previous_action is None or not 0<=f-previous_action<=40:
                errors.append('Animation is not preceded by the owned native action')
    if min(counts.values())<=0:errors.append('Actual complete native projectile pipeline not observed')
    if result and result!=('true',target,str(side),str(len(commands)),str(counts['parser']),str(counts['action']),str(counts['animation']),'0','0'):
        errors.append('Projectile result contradicts captured native events')
    if 'MK2_RESTART_PROJECTILE_ERROR' in log:errors.append('Runtime projectile observer error')
    return {'passed':not errors,'errors':errors,'target':target,'side':side,'native_pipeline_counts':counts,
            'commands':len(commands),'memory_writes':0,'scope':'owned_knife_or_ring_activation_after_restart_not_other_specials_or_damage_parity'}
