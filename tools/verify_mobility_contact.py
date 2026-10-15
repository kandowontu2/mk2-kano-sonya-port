"""Native joined cannonball/square contact, trajectories, poses and follow-up.

These checks do not claim a cold run proves an ending, CPU tower or audio.
The separate joined/full-restart verifier keeps those scope anchors mandatory.
"""
import argparse
import json
import re
from pathlib import Path

HEX={'actor','main','action','pose','xraw','yraw','vx','vy','gravity','flags','body','trail',
     'entry','pc','a8','a13','a0','a1','a2','a3','a5','a6','a7','a9','a11','b4','request','table','root','value'}
TEXT={'move','target','scenario','kind','button','pass','values'}
IDS={'kano':17,'sonya':18}


def rows(log,tag):
    result=[]
    for line in log.splitlines():
        if not line.startswith('MK2_MOB_CONTACT_'+tag+' '):continue
        row={}
        for key,value in re.findall(r'(\w+)=([^\s]+)',line):
            if key in TEXT:row[key]=value
            else:row[key]=int(value,16 if key in HEX or tag=='VELOCITY' and key in ('before','after') else 10)
        result.append(row)
    return result


def _verify(log,target,side):
    errors=[]
    def check(ok,label):
        if not ok and label not in errors:errors.append(label)
    move='ball' if target=='kano' else 'square'
    begin,result,descriptor,root=[rows(log,t) for t in ('BEGIN','RESULT','DESCRIPTOR','ROOT')]
    check(len(begin)==len(result)==len(descriptor)==len(root)==1,'Actual contact anchors and ROM guards')
    if not (len(begin)==len(result)==len(descriptor)==len(root)==1):return {'passed':False,'errors':errors}
    b,r,d,rt=begin[0],result[0],descriptor[0],root[0]
    mf=b['frame'];scenario=b['scenario'];victim=3-side
    check(b==dict(frame=mf,move=move,target=target,side=side,scenario=scenario,writes=0) and scenario in ('hit','block','miss'),'Actual fighter/slot/contact scenario')
    check(r=={'frame':mf+600,'pass':'true','move':move,'target':target,'side':side,'scenario':scenario,'fields':601,'errors':0,'writes':0},'Actual 601-field contact result')
    expected_descriptor='57,14,72,31,1417,1805,0,0,1' if target=='kano' else '70,15,58,52,1417,1B08,0,0,1'
    check(d==dict(frame=mf,move=move,values=expected_descriptor,writes=0),'Original hitbox/reaction/damage descriptor')
    check(rt==dict(move=move,table=0xff0000e0 if target=='kano' else 0xff0203c0,root=0xff004010 if target=='kano' else 0xff0244b0,writes=0),'Actual own animation root')
    expected_poses=([0xff00eae0,*range(0xff00eb40,0xff00ecc1,0x40),1,0xff004030,0xff00ed00] if target=='kano' else
                    [0xff031340,0xff031380,0xff0313c0,0,0xff031380,0xff031340])
    check(rows(log,'POSE')==[dict(move=move,index=i,value=v,writes=0) for i,v in enumerate(expected_poses)],'Own ROM poses and original roll-loop token')
    fields=rows(log,'FIELD');by={(f['frame'],f['slot']):f for f in fields}
    check(len(fields)==len(by)==1202 and set(by)=={(f,s) for f in range(mf,mf+601) for s in (1,2)},'Every actual paired field without omissions/duplicates')
    ids={side:IDS[target],victim:35-IDS[target]}
    owners={s:by[mf,s]['actor'] for s in (1,2)};mains={s:by[mf,s]['main'] for s in (1,2)}
    for f in fields:
        s=f['slot']
        check(f['age']==f['frame']-mf and f['actor']==owners[s] and f['main']==mains[s] and
              0x01000000<=f['actor']<0x01100000 and 0x01000000<=f['main']<0x01100000 and
              f['id']==f['roster']==ids[s] and f['state']==1 and f['writes']==0,'All real identities/controllers/Main processes')
    control=rows(log,'CONTROL');expected=[]
    def pulse(s,key,start,hold=3):expected.extend((mf+age,age,s,key) for age in range(start,start+hold))
    initial=by[mf+180,side];other=by[mf+180,victim]
    forward='right' if initial['x']<other['x'] else 'left';back='left' if forward=='right' else 'right'
    direction=1 if forward=='right' else -1
    if target=='kano':
        pulse(side,'lk',180,81)
        if scenario=='block':pulse(victim,'block',220,180)
        if scenario=='miss':pulse(victim,'down',220,180)
    else:
        pulse(side,forward,180);pulse(side,back,185);pulse(side,'hp',186)
        if scenario=='hit':pulse(victim,'up',193)
        if scenario=='block':pulse(victim,'block',160,150)
        if scenario=='miss':pulse(victim,forward,140,40)
    # Facing for the actual follow-up can change after crossing a ducked target.
    for age,key in ((450,'down'),(455,'direction'),(456,'hp' if target=='kano' else 'lp')):
        for a in range(age,age+3):
            actual=by[mf+a,side];opposite=by[mf+a,victim]
            fwd='right' if actual['x']<opposite['x'] else 'left'
            btn=(('left' if fwd=='right' else 'right') if target=='kano' else fwd) if key=='direction' else key
            expected.append((mf+a,a,side,btn))
    check(sorted((c['frame'],c['age'],c['slot'],c['button']) for c in control)==sorted(expected) and
          all(c['writes']==0 and c['value']==1 for c in control),'Every real charge/direction/jump/block/duck/follow-up pulse')
    events=rows(log,'EVENT');entries={'parser':0xffffdb00 if target=='kano' else 0xffffc800,
        'action':0xffffde00 if target=='kano' else 0xffffca00,'attack':0xffffec00 if target=='kano' else 0xffffda00,
        'animation':rt['table'],'fling':0xff876650,'recovery':0xff861350,'projectile':0xffffb000 if target=='kano' else 0xffffb400,
        'elapsed':0xffffdb60}
    for e in events:
        kind=e['kind'];slot=side if e['a8']==owners[side] else victim
        pc=0xff835480 if kind=='attack' else 0xff906140 if kind=='animation' else entries.get(kind,0)+16
        check(kind in entries and e['entry']==entries[kind] and e['pc']==pc and mf<=e['frame']<=mf+600 and
              e['age']==e['frame']-mf and e['a8']==owners[slot] and
              (0x01000000<=e['a13']<0x01100000 if kind in ('parser','elapsed') else e['a13']==mains[slot]) and e['writes']==0 and
              (kind in ('fling','recovery') or slot==side),'Actual native entry/owner/Main/callback chronology')
    actions=[e for e in events if e['kind']=='action'];projectiles=[e for e in events if e['kind']=='projectile']
    check(len(actions)==len(projectiles)==1,'Exactly one real special and subsequent own projectile action')
    if not actions:return {'passed':False,'errors':errors}
    sf=actions[0]['frame'];sa=sf-mf
    check(262<=sa<=265 if target=='kano' else 187<=sa<=190,'Action after actual native command')
    check(457<=projectiles[0]['age']<=460 if projectiles else False,'Actual later own projectile activation')
    check(any(e['kind']=='parser' and sf-3<=e['frame']<=sf for e in events),'Actual original parser before action')
    if target=='kano':check(any(e['kind']=='elapsed' and e['frame']==sf and e['a1']>80 for e in events),'Original strict LK charge threshold')
    own=[by[f,side] for f in range(sf+1,mf+440)]
    flight=[f for f in own if f['vx']==(0xa0000*direction)&0xffffffff and f['action']==(0x20b if target=='kano' else 0x207)]
    attacks=[e for e in events if e['kind']=='attack']
    check(bool(flight) and [f['frame'] for f in flight]==list(range(flight[0]['frame'],flight[-1]['frame']+1)),'Consecutive original horizontal strike fields')
    check([e['frame'] for e in attacks]==list(range(sf+(7 if target=='kano' else 9),flight[-1]['frame']+1)) if flight else False,'Original startup and exactly one collision per flight field')
    baseline=by[sf,side]
    for i,f in enumerate(flight):
        check(f['y']==baseline['floor']+(16 if target=='kano' else -96) and f['vy']==f['gravity']==0,'Exact original strike height/vertical motion')
        if i:
            prior=flight[i-1]
            check(f['xraw']==(prior['xraw']+direction*0xa0000)&0xffffffff and f['x']-prior['x']==direction*10,'Every actual ten-pixel horizontal strike step')
        if target=='kano':
            check(f['body']&8!=0,'Original compact roll body flag')
            if i:check(f['pose']==expected_poses[1+((i-1)//3)%7],'Every original three-field roll pose')
        elif i:check(f['pose']==expected_poses[min((i-1)//3,2)],'Every original square-flight pose hold')
    health=rows(log,'HEALTH');special=[h for h in health if h['age']<440]
    damage=(24 if scenario=='hit' else 5 if scenario=='block' else 0) if target=='kano' else (27 if scenario=='hit' else 0)
    check(len(special)==(1 if damage else 0),'Exact special hit/chip count or no miss damage')
    for h in special:check(h['slot']==victim and h['before']==161 and h['after']==161-damage and h['frame']==flight[-1]['frame'] and
                           h['pc']==0xff836700 and h['a8']==owners[side] and h['a13']==mains[side] and h['writes']==0,'Exact original native damage store and source ownership')
    # Follow-up damage is optional (the projectile may miss). It cannot be
    # miscounted as special damage or attributed to the fighter's strike code.
    follow=[h for h in health if h['age']>=440]
    check(len(follow)<=1 and all(h['slot']==victim and 460<=h['age']<530 and h['pc']==0xff836700 and
          h['before']-h['after']==22 and h['a8']!=owners[side] and 0x01000000<=h['a8']<0x01100000 and
          0x01000000<=h['a13']<0x01100000 and h['writes']==0 for h in follow),'Separate original subsequent projectile damage only')
    flings=[e for e in events if e['kind']=='fling' and sf<e['frame']<mf+440]
    if target=='kano':
        rebound=[f for f in own if f['gravity']==0x6000]
        check(len(rebound)==(42 if damage else 0) and (len(flight)<26 if damage else len(flight)==26),'Original hit/block rebound or full 26-field miss')
        if damage:
            of=[e for e in flings if e['a8']==owners[side]]
            check(len(of)==1 and (of[0]['a0'],of[0]['a1'],of[0]['a2'],of[0]['a3'])==
                  (0x50000 if scenario=='hit' else 0x10000,0xfff80000,0x6000,2),'Original five/one-pixel backward rebound parameters')
            for i,f in enumerate(rebound):
                wanted=(-direction*(0x50000 if scenario=='hit' else 0x10000))&0xffffffff
                bound=[v for v in rows(log,'VELOCITY') if v['slot']==side and v['frame']<f['frame'] and v['after']==0 and v['before']==wanted and
                       v['actor']==v['a2']==owners[side] and v['a13']==0xfffff010 and v['writes']==0 and
                       ((direction==1 and v['pc']==0xff805580 and v['x']==v['left']) or (direction==-1 and v['pc']==0xff805610 and v['x']==v['right']))]
                separation=[]
                def signed32(v):return v-0x100000000 if v&0x80000000 else v
                for v in rows(log,'VELOCITY'):
                    if not (v['slot']==side and v['frame']<f['frame'] and v['after']==0 and v['before']==wanted and
                            v['pc']==(0xff8285d0 if side==1 else 0xff8285b0) and v['a8']==owners[1] and v['a9']==owners[2] and
                            v.get('request')==wanted and v.get('b4')==0 and v.get('a6' if side==1 else 'a7')==0 and
                            abs(v['x']-v.get('tx',v['x']))==304 and v['writes']==0):continue
                    prev=by[v['frame'],side];opp=by[v['frame'],victim]
                    px=prev['x']+(signed32(wanted)>>16);tx=opp['x']+(signed32(opp['vx'])>>16)
                    correction=(abs(px-tx)-304)//2
                    if correction>=0 and abs(signed32(v['a5']))==correction and abs(v['x']-px)==correction and abs(v['tx']-tx)==correction:
                        separation.append(v)
                check((f['vx']==wanted or f['vx']==0 and bool(bound or separation)) and f['action']==0x602,'Every actual backward rebound field or proven native stage/separation limit')
                if i:check(f['pose']==expected_poses[1+((i-1)//2)%7],'Every original two-field rebound pose')
            groups=[rebound]
        else:groups=[]
    else:
        rise=[f for f in own if f['vy']==0xfff40000];fall=[f for f in own if f['gravity']==0x8000]
        check(len(rise)==8 and len(fall)==16 and (len(flight)<26 if damage else len(flight)==26),'Original eight-field rise, 96 height, 16-field fall and flight count')
        check(all(f['y']==baseline['floor']-12*i and f['vx']==f['gravity']==0 and f['pose']==0xfe835c80 for i,f in enumerate(rise)),'Exact own vertical launch and tuck pose')
        check(all(f['pose']==0xfe835c20 for f in fall),'Every own native fall pose')
        pause=[f for f in own if f['y']==baseline['floor']-96 and f['vx']==f['vy']==f['gravity']==0]
        check(len(pause)==(10 if damage else 0) and all(f['pose']==0xff031480 for f in pause),'Original ten-field own contact pose pause')
        of=[e for e in flings if e['a8']==owners[side]]
        check(len(of)==1 and (of[0]['a0'],of[0]['a1'],of[0]['a2'],of[0]['a3'])==(0,0x20000,0x8000,0xfff),'Original own downward landing continuation')
        groups=[fall]
    # Bind original victim fling to its own Main and verify every native
    # vertical integrator step through landing, not just one airborne image.
    vf=[e for e in flings if e['a8']==owners[victim]]
    hit=scenario=='hit'
    check(len(vf)==(1 if hit else 0),'Actual knockdown victim continuation only on unblocked contact')
    if hit and vf:
        v=vf[0];params=(0x60000,0xfffd0000,0x4000,5) if target=='kano' else (0x38000,0xfffa0000,0x8000,5)
        check((v['a0'],v['a1'],v['a2'],v['a3'])==params,'Original own victim reaction launch parameters')
        seq=[]
        for at in range(v['frame']+1,mf+440):
            f=by[at,victim]
            if f['gravity']!=params[2]:break
            seq.append(f)
        check(len(seq)>8 and seq[0]['vy']==params[1],'Complete real victim airborne continuation')
        groups.append(seq)
    for seq in groups:
        for prior,f in zip(seq,seq[1:]):
            check(f['frame']==prior['frame']+1 and f['yraw']==(prior['yraw']+f['vy'])&0xffffffff and
                  f['vy']==(prior['vy']+prior['gravity'])&0xffffffff,'Every full fixed-point native vertical physics step')
    for s in (1,2):
        recovery=[e for e in events if e['kind']=='recovery' and e['a8']==owners[s] and sf<e['frame']<mf+440]
        check(bool(recovery) if s==side or hit else True,'Both original contact recovery continuations')
        for age in (*range(420,450),*range(570,601)):
            f=by[mf+age,s]
            check(f['y']==f['floor'] and f['vx']==f['vy']==f['gravity']==0 and f['flags']&0x1c==0 and
                  f['body']&8==0 and f['trail']==0 and f['hp']>0 and f['action'] not in (0x20b,0x207,0x602),'Sustained grounded cleanup before and after subsequent control')
    check('MK2_MOB_CONTACT_ERROR' not in log,'No actual contact observer errors')
    return {'passed':not errors,'errors':errors,'target':target,'side':side,'move':move,'scenario':scenario,
            'fields':601,'damage':damage,'flight_fields':len(flight),'scope':'native_joined_mobility_contact_and_subsequent_controls_not_CPU_or_audio'}


def verify(log,target,side):
    try:return _verify(log,target,side)
    except (KeyError,ValueError,TypeError,IndexError) as error:
        return {'passed':False,'errors':['Malformed/incomplete native contact trace: '+str(error)]}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('log',type=Path)
    parser.add_argument('--target',choices=IDS,required=True);parser.add_argument('--side',type=int,choices=(1,2),required=True)
    args=parser.parse_args();result=verify(args.log.read_text(encoding='utf-8-sig'),args.target,args.side)
    print(json.dumps(result,indent=2));raise SystemExit(0 if result['passed'] else 1)
