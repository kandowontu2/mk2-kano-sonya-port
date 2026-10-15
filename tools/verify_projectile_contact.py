"""Read-only evidence for projectile geometry/contact; not full move fidelity.

Cold joins cannot prove endings, CPU play, audio or authentic impact choreography.
"""
import argparse
import json
import re
from pathlib import Path

HEX=set('actor main action pose xraw yraw vx vy gravity flags body trail entry pc a0 a1 a2 a3 a6 a8 a9 a10 a11 a13 child process actor_owner main_owner victim victim_main velocity_parameter parent_child palette descriptor damage parser animation first mask opcode root value address reaction group component victim_min victim_max attack_min attack_max start finish checksum'.split())
TEXT={'target','move','scenario','kind','button','pass'}
IDS={'kano':17,'sonya':18}
POSES={
    'kano':[0xff011de0,0xff011e20,0xff011e60,0xff011ea0,0,0xff011ee0,0xff011f20,0xff011ee0,0xff011f20,0xff011ee0],
    'sonya':[0xff031f40,0xff031f80,0xff031fc0,0xff032000,0,0xff032040,0xff032080,0xff032040,0xff032080,0xff032040],
}
# Independently decoded converted-component records, not asserted result flags.
COMPONENTS={
    'kano':[(34,40,-93,-44),(43,23,-89,-68),(24,46,-90,-60),(34,40,-73,-62),(43,25,-68,-52),(24,45,-87,-39)],
    'sonya':[(35,29,-73,-35),(36,29,-73,-35),(36,29,-73,-35),(37,29,-72,-35),(37,29,-72,-35),(36,29,-73,-35)],
}
ENTRIES={'child':0xff8b6530,'spawn':0xff8b5fb0,'flight':0xff8afc10,'release':0xff8afe00,
         'collision':0xff8b6ac0,'contact':0xff8b6a70,'cleanup':0xff8b6820,'reaction':0xff80f6b0,
         'recovery':0xff861350,'sound':0xffa12530}


def rows(log,tag):
    result=[]
    for line in log.splitlines():
        if not line.startswith('MK2_PROJ_CONTACT_'+tag+' '):continue
        result.append({k:v if k in TEXT else int(v,16 if k in HEX else 10)
                       for k,v in re.findall(r'(\w+)=([^\s]+)',line)})
    return result


def signed(x):return x-65536 if x>=32768 else x
def xy(x):return signed(x&65535),signed(x>>16)


def _verify(log,target,side,impact=False):
    errors=[]
    def check(ok,label):
        if not ok and label not in errors:errors.append(label)
    begin,result,rom=[rows(log,t) for t in ('BEGIN','RESULT','ROM')]
    check(len(begin)==len(result)==len(rom)==1,'Actual complete projectile anchors')
    if not (len(begin)==len(result)==len(rom)==1):return {'passed':False,'errors':errors}
    b,r,guard=begin[0],result[0],rom[0];mf=b['frame'];scenario=b['scenario'];move='knife' if target=='kano' else 'ring';victim=3-side
    check(b==dict(frame=mf,target=target,side=side,move=move,scenario=scenario,writes=0) and scenario in ('hit','block','miss'),'Actual target/controller/scenario')
    check(r==dict(frame=mf+600,**{'pass':'true'},target=target,side=side,move=move,scenario=scenario,cycles=2,fields=601,errors=0,writes=0),'601-field original observer result')
    parser,action,animation,root=(0xffffac00,0xffffb000,0xff0004e0,0xff009c50) if target=='kano' else (0xffffae00,0xffffb400,0xff0204e0,0xff029c50)
    check(guard==dict(parser=parser,action=action,animation=animation,first=0x09c0,mask=0x63 if target=='kano' else 0x72,opcode=0x574a,root=root,writes=0),'Own parser/action/animation guards')
    check(rows(log,'POSE')==[dict(index=i,value=v,writes=0) for i,v in enumerate(POSES[target])],'Own projectile ROM pose list')
    comps=rows(log,'COMPONENT');indices=(0,1,2,3,5,6)
    check(len(comps)==6 and [c['index'] for c in comps]==list(indices),'All actual geometry source components')
    for c,idx,spec in zip(comps,indices,COMPONENTS[target]):
        check(c['group']==POSES[target][idx] and tuple(c[k] for k in ('width','height','dx','dy'))==spec and
              0xff602000<=c['address']<0xff6028c0 and c['writes']==0,'Own converted component geometry')
    desc=rows(log,'DESCRIPTOR');check(len(desc)==4 and [d['phase'] for d in desc]==list(range(4)),'Four actual dedicated descriptors')
    for i,d in enumerate(desc):
        # Original MK3 read taps prove knife index 21 and ring index 18.
        # Apply the converter's +100,+72 knife pivot to its native core.
        right,top,width,height=(135,48,51,50) if target=='kano' else (108,35,36,11)
        base=0xfffe73e0 if target=='kano' else 0xfffe8be0
        check(d==dict(phase=i,address=base+i*0x90,edge=right,top=top,width=width,height=height,
                      reaction=0x1110,damage=0x1605 if i<3 else 0x1606,writes=0),'Donor collision core and converter pivot; native damage/reaction preserved')
    original=(Path(__file__).resolve().parents[1]/'mk2/mk2-maincpu.bin').read_bytes()
    checksum=0x811c9dc5
    for at in range((0xff8eba90-0xff800000)//8,(0xff8f3be0-0xff800000)//8,2):
        checksum=((checksum^int.from_bytes(original[at:at+2],'little'))*0x01000193)&0xffffffff
    check(rows(log,'STOCK')==[dict(start=0xff8eba90,finish=0xff8f3be0,checksum=checksum,writes=0)],'Entire original roster attack table/descriptor region stays unchanged')
    fields=rows(log,'FIELD');by={(f['age'],f['slot']):f for f in fields}
    check(len(fields)==len(by)==1202 and set(by)=={(age,s) for age in range(601) for s in (1,2)},'All 601 fields for both real fighters')
    owners={s:by[0,s]['actor'] for s in (1,2)};mains={s:by[0,s]['main'] for s in (1,2)}
    for f in fields:
        s=f['slot'];check(f['frame']==mf+f['age'] and f['actor']==owners[s] and f['main']==mains[s] and
                         0x01000000<=f['actor']<0x01100000 and 0x01000000<=f['main']<0x01100000 and
                         f['id']==f['roster']==(IDS[target] if s==side else 35-IDS[target]) and f['state']==1 and f['writes']==0,'Canonical actors/controllers and no guest writes')
    expected=[]
    for first in (180,380):
        forward='right' if by[first,side]['x']<by[first,victim]['x'] else 'left'
        direction=forward if target=='sonya' else ('left' if forward=='right' else 'right')
        for key,start,hold in [('down',first,3),(direction,first+5,3),('hp' if target=='kano' else 'lp',first+6,3)]:
            expected.extend((mf+age,age,side,key) for age in range(start,start+hold))
        if scenario!='hit':expected.extend((mf+age,age,victim,'block' if scenario=='block' else 'down') for age in range(first-20,first+140))
    controls=rows(log,'CONTROL')
    check([(c['frame'],c['age'],c['slot'],c['button']) for c in controls]==sorted(expected,key=lambda c:(c[1],0 if c[2]==side else 1)) and
          all(c['value']==1 and c['writes']==0 for c in controls),'Only actual ordinary command/guard/duck input pulses')
    events=rows(log,'EVENT');effects=rows(log,'EFFECT');health=rows(log,'HEALTH');geometry=rows(log,'GEOMETRY');owners_log=rows(log,'OWNER')
    expected_health=[]
    for cycle in (1,2):
        ev=[e for e in events if e['cycle']==cycle];ef=[f for f in effects if f['cycle']==cycle];geo=[g for g in geometry if g['cycle']==cycle]
        def group(kind):return [e for e in ev if e['kind']==kind]
        actions,child,spawn,flight,release,contact,cleanup,reaction=[group(k) for k in ('action','child','spawn','flight','release','contact','cleanup','reaction')]
        check(len(actions)==len(child)==len(spawn)==len(flight)==len(release)==len(cleanup)==1,'Two complete native projectile creations/flights/retirements')
        if not all(len(x)==1 for x in (actions,child,spawn,flight,release,cleanup)):continue
        act,ch,sp,fl,rel,end=[x[0] for x in (actions,child,spawn,flight,release,cleanup)]
        start=196+(cycle-1)*200;obj=ch['child'];proc=sp['process']
        check(act['age']==start-8 and ch['age']==sp['age']==fl['age']==start and rel['age']==start+12 and
              act['a8']==ch['a8']==sp['a8']==owners[side] and act['a13']==ch['a13']==sp['a13']==mains[side] and
              ch['a10']==obj and sp['a0']==proc and 0x01000000<=obj<0x01100000 and 0x01000000<=proc<0x01100000,'Actual owned native scheduling and child/process allocation')
        own=[o for o in owners_log if o['cycle']==cycle]
        check(own==[dict(frame=mf+start,age=start,cycle=cycle,child=obj,process=proc,actor_owner=owners[side],main_owner=mains[side],victim=owners[victim],victim_main=mains[victim],writes=0)],'Native creation binds both actual human owners and victim')
        for e in ev:
            kind=e['kind'];entry=parser if kind=='parser' else action if kind=='action' else animation if kind=='animation' else ENTRIES.get(kind)
            check(e['entry']==entry and e['frame']==mf+e['age'] and e['writes']==0,'Only actual native read-tap entries')
            if kind not in ('parser','animation'):check(e['pc']==entry+16,'Actual native instruction PC, not observer self-read')
            if kind in ('flight','release','collision','contact','cleanup','reaction'):check(e['a8']==obj and e['a13']==proc,'Actual detached child process owns collision/contact/cleanup')
        check(len(ef)==end['age']-start and [f['age'] for f in ef]==list(range(start+1,end['age']+1)),'Every live effect field until native retirement')
        effect_by={f['age']:f for f in ef}
        first=effect_by.get(start+1);body=by[start,side]
        direction=1 if body['x']<by[start,victim]['x'] else -1
        check(first is not None and first['x']==body['x']+direction*(-12 if target=='kano' else 0) and
              first['y']==body['y']+(-40 if target=='kano' else 0),'Donor body-relative flight origin, compensated for converted pivot')
        for f in ef:
            check(f['frame']==mf+f['age'] and f['child']==obj and f['process']==proc and f['id']==IDS[target] and f['type']==81 and
                  f['actor_owner']==owners[side] and f['velocity_parameter']==0x000c0000 and f['vy']==0 and f['writes']==0,'Own projectile ID, detached physics process and velocity parameter')
        check(len(geo)==len(group('collision')) and bool(geo),'Every collision has native rectangle evidence')
        for g in geo:
            d=desc[min((g['age']-start)//3,3)];f=effect_by.get(g['age'],effect_by.get(start+1))
            # Frame observers precede this field's native physics/collision.
            # The detached object moves by its signed 16.16 velocity first.
            velocity=f['vx']-(1<<32) if f['vx']&(1<<31) else f['vx']
            x=f['x']+velocity//65536
            left=x-d['edge'] if f['flags']&16 else x+d['edge']-d['width']
            check(g['child']==obj and g['process']==proc and xy(g['attack_min'])==(left,f['y']+d['top']) and
                  xy(g['attack_max'])==(left+d['width'],f['y']+d['top']+d['height']) and g['writes']==0,'Native rectangle matches donor collision core in actual facing direction')
        if scenario=='miss':
            check(not contact and not reaction,'Ducking produces no false contact/reaction')
        else:
            check(len(contact)==len(reaction)==1,'One real contact/reaction per projectile')
            if contact:
                at=contact[0]['age'];duration=28 if impact and target=='sonya' else 24
                check(end['age']==at+duration,'Native complete contact-effect retirement')
                g=next((g for g in geo if g['age']==at),None)
                if g:
                    amin,amax,vmin,vmax=[xy(g[k]) for k in ('attack_min','attack_max','victim_min','victim_max')]
                    check(all(amin[i]<vmax[i] and amax[i]>vmin[i] for i in (0,1)),'Actual contact overlaps actual victim bounds')
                else:check(False,'Contact has matching actual geometry')
                delta=22 if scenario=='hit' else 6
                expected_health.append(dict(frame=mf+at,age=at,cycle=cycle,slot=victim,before=161-(cycle-1)*delta,after=161-cycle*delta,pc=0xff836700,a8=obj,a13=proc,writes=0))
        sounds=group('sound');check([e['a0'] for e in sounds]==([5] if scenario=='miss' else [5,0x62 if scenario=='hit' else 0x63]),'Native launch/contact sound requests')
        check(any(e['kind']=='recovery' and e['a8']==owners[side] and e['a13']==mains[side] for e in ev),'Actual thrower recovery')
    check(health==expected_health,'Exact native damage/chip ledger; no damage for ducked projectiles')
    for s in (1,2):
        hp=161;writes=[h for h in health if h['slot']==s];index=0
        for age in range(601):
            while index<len(writes) and writes[index]['age']<age:hp=writes[index]['after'];index+=1
            check(by[age,s]['hp']==hp,'Every actual health field matches original damage stores')
        for age in range(560,601):
            f=by[age,s];check(f['action']==0x0303 and f['flags']==1 and f['body']==0x12 and f['trail']==0 and f['vx']==f['vy']==f['gravity']==0 and f['y']==f['floor'],'Both fighters stay cleanly grounded and ready')
    check('MK2_PROJ_CONTACT_ERROR' not in log and 'MK2_PROJ_COLD_ERROR' not in log,'No observer/start errors')
    return dict(passed=not errors,errors=errors,target=target,side=side,scenario=scenario,fields=601,
                scope='own_projectile_geometry_native_contact_damage_cleanup_not_full_impact_choreography_CPU_audio_or_endings')


def verify(log,target,side,impact=False):
    try:return _verify(log,target,side,impact)
    except (KeyError,ValueError,TypeError,IndexError) as error:
        return dict(passed=False,errors=['Malformed/incomplete projectile evidence: '+str(error)])


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('log',type=Path);p.add_argument('--target',choices=IDS,required=True);p.add_argument('--side',type=int,choices=(1,2),required=True)
    a=p.parse_args();r=verify(a.log.read_text(encoding='utf-8-sig'),a.target,a.side);print(json.dumps(r,indent=2));raise SystemExit(0 if r['passed'] else 1)
