"""Current native release/intro/full-flight/contact fields, not screenshot proof.

The actual real-join transition is checked independently by the shared lifecycle
verifier. This new contact verifier replaces only its superseded v291 timing
model; old verifiers/tests retain their original default behavior.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

import build_native_projectile_choreography as assets
from verify_projectile_contact import rows,xy,IDS
from verify_restart_lifecycle import verify_projectile_join

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_SHA = '51bd733de93015db71faa7e5172d68d90832622173d776d1725aeabf27e33e82'
HEX = set('actor process action pose group pc vx vy flags'.split())


def choreography_rows(log,kind):
    return [{k:int(v,16 if k in HEX else 10) for k,v in re.findall(r'(\w+)=([^ ]+)',line)}
            for line in log.splitlines() if line.startswith('MK2_CHOREO_'+kind+' ')]


def impact_rows(log):
    return [{k:v if k=='snapshot' else int(v,16 if k in {'child','process','action','pose','vx','vy','flags'} else 10)
             for k,v in re.findall(r'(\w+)=([^ ]+)',line)}
            for line in log.splitlines() if line.startswith('MK2_IMPACT_FIELD ')]


def _contact(log,target,side):
    errors=[]
    def check(ok,label):
        if not ok and label not in errors:errors.append(label)
    begin,result=rows(log,'BEGIN'),rows(log,'RESULT')
    check(len(begin)==len(result)==1,'Complete actual projectile anchors')
    if len(begin)!=1 or len(result)!=1:return dict(passed=False,errors=errors)
    b,r=begin[0],result[0];mf=b['frame'];scenario=b['scenario'];victim=3-side
    check(b==dict(frame=mf,target=target,side=side,move='knife' if target=='kano' else 'ring',scenario=scenario,writes=0)
          and scenario in ('hit','block','miss'),'Actual target, side and scenario')
    check(r==dict(frame=mf+600,**{'pass':'true'},target=target,side=side,move=b['move'],scenario=scenario,
                  cycles=2,fields=601,errors=0,writes=0),'Complete 601-field observer result')
    fields=rows(log,'FIELD');by={(f['age'],f['slot']):f for f in fields}
    check(len(fields)==len(by)==1202 and set(by)=={(age,s) for age in range(601) for s in (1,2)},'Every real fighter field')
    owners={s:by[0,s]['actor'] for s in (1,2)};mains={s:by[0,s]['main'] for s in (1,2)}
    for f in fields:
        s=f['slot']
        check(f['frame']==mf+f['age'] and (f['actor'],f['main'])==(owners[s],mains[s]) and
              0x01000000<=f['actor']<0x01100000 and 0x01000000<=f['main']<0x01100000 and
              f['id']==f['roster']==(IDS[target] if s==side else 35-IDS[target]) and f['state']==1 and f['writes']==0,
              'True canonical fighter identities, native owners and no observation writes')
    expected=[]
    for first in (180,380):
        forward='right' if by[first,side]['x']<by[first,victim]['x'] else 'left'
        direction=forward if target=='sonya' else ('left' if forward=='right' else 'right')
        for key,start,hold in [('down',first,3),(direction,first+5,3),('hp' if target=='kano' else 'lp',first+6,3)]:
            expected.extend((mf+age,age,side,key) for age in range(start,start+hold))
        if scenario!='hit':expected.extend((mf+age,age,victim,'down' if scenario=='miss' else 'block') for age in range(first-20,first+140))
    controls=rows(log,'CONTROL')
    check(sorted((c['frame'],c['age'],c['slot'],c['button']) for c in controls)==sorted(expected) and
          all(c['value']==1 and c['writes']==0 for c in controls),'Two complete ordinary input sequences and actual guard/duck controls')
    descriptors=rows(log,'DESCRIPTOR')
    core=(135,48,51,50) if target=='kano' else (108,35,36,11)
    check(len(descriptors)==4,'Four own native collision descriptors')
    for i,d in enumerate(descriptors):
        check(d==dict(phase=i,address=(0xfffe73e0 if target=='kano' else 0xfffe8be0)+i*0x90,
                      edge=core[0],top=core[1],width=core[2],height=core[3],reaction=0x1110,
                      damage=0x1605 if i<3 else 0x1606,writes=0),'Original observed collision core and MKII damage/reaction')
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();checksum=0x811c9dc5
    for at in range((0xff8eba90-0xff800000)//8,(0xff8f3be0-0xff800000)//8,2):
        checksum=((checksum^int.from_bytes(original[at:at+2],'little'))*0x01000193)&0xffffffff
    check(rows(log,'STOCK')==[dict(start=0xff8eba90,finish=0xff8f3be0,checksum=checksum,writes=0)],'Entire stock attack/descriptor table unchanged')
    events,effects,health,geometry=[rows(log,t) for t in ('EVENT','EFFECT','HEALTH','GEOMETRY')]
    groups=choreography_rows(log,'GROUP');human=choreography_rows(log,'HUMAN');native=impact_rows(log)
    report=json.loads((ROOT/'diagnostic_v298_projectile_choreography_payload/roms/mk2ks/mk2ks.choreography.json').read_text())
    timing=assets.TIMING[target];expected_health=[]
    for cycle in (1,2):
        ev=[e for e in events if e['cycle']==cycle]
        kinds=lambda k:[e for e in ev if e['kind']==k]
        action,child,spawn,cleanup=[kinds(k) for k in ('action','child','spawn','cleanup')]
        check(len(action)==len(child)==len(spawn)==len(cleanup)==1,'Two real owned child allocations and native retirements')
        if not all(len(x)==1 for x in (action,child,spawn,cleanup)):continue
        act,ch,sp,end=[x[0] for x in (action,child,spawn,cleanup)]
        start=188+(cycle-1)*200;obj=ch['child'];proc=sp['process'];birth=start+timing['child_spawn_age']
        check(act['age']==start and ch['age']==sp['age']==birth and
              act['a8']==ch['a8']==sp['a8']==owners[side] and act['a13']==ch['a13']==sp['a13']==mains[side] and
              ch['a10']==obj and sp['a0']==proc and 0x01000000<=obj<0x01100000 and 0x01000000<=proc<0x01100000,
              'Original complete body timing and actual native task allocation')
        own=[o for o in rows(log,'OWNER') if o['cycle']==cycle]
        check(own==[dict(frame=mf+birth,age=birth,cycle=cycle,child=obj,process=proc,actor_owner=owners[side],
                        main_owner=mains[side],victim=owners[victim],victim_main=mains[victim],writes=0)],'Actual native human and victim ownership')
        body=[g for g in groups if g['body'] and g['actor']==owners[side] and mf+start<=g['frame']<mf+start+60]
        bodyposes=[int(g['native'],16) for g in report[target]['body']]
        ages=[0]
        for hold in timing['body_holds'][:-1]:ages.append(ages[-1]+hold)
        check([g['group'] for g in body]==bodyposes and [g['frame']-mf-start for g in body]==ages,
              'Complete original body-release pose list and every pose execution age')
        for g in body:
            check(g['pc']==0xff8387a0 and g['process']==mains[side] and g['id']==IDS[target] and
                  g['writes']==0 and g['vx']==g['vy']==0,'Actual native release renderer and real body process')
        total=sum(timing['body_holds']);ready=mf+start+total+timing['recovery_fields']+1
        hr={h['frame']:h for h in human if h['side']==side and mf+start<h['frame']<=ready+1}
        check(len(hr)==ready+1-mf-start,'Every held release and recovery body field')
        for frame in range(mf+start+1,ready):
            h=hr[frame];pose=next(g['group'] for g in reversed(body) if g['frame']<frame)
            check(h['pose']==pose and h['action']==(4 if frame<=mf+start+total else 0x604) and
                  (h['actor'],h['process'],h['id'],h['x'],h['y'],h['vx'],h['vy'],h['writes'])==
                  (owners[side],mains[side],IDS[target],by[start,side]['x'],by[start,side]['y'],0,0,0),
                  'All original body holds/recovery, grounded own identity and zero velocity')
        check(hr[ready]['action']==0x303 and hr[ready]['flags']==1 and hr[ready]['pose']==bodyposes[-1] and
              hr[ready+1]['action']==0x303 and hr[ready+1]['pose']!=bodyposes[-1], 'Original recovery age, native readiness and resumed stance')
        life=[f for f in effects if f['cycle']==cycle]
        check([f['age'] for f in life]==list(range(birth+1,end['age']+1)), 'Every child field through native retirement')
        effect_by={f['age']:f for f in life}
        for f in life:
            check(f['child']==obj and f['process']==proc and f['id']==IDS[target] and f['type']==81 and
                  f['actor_owner']==owners[side] and f['velocity_parameter']==0x80000 and f['writes']==0,
                  'Actual native child ID, owner, task, type and eight-pixel speed')
        flight_age=start+timing['first_flight_age'];first=next(g for g in groups if not g['body'] and g['actor']==obj and g['frame']==mf+flight_age)
        sign=-1 if first['flags']&16 else 1;vx=(sign*0x80000)&0xffffffff
        if target=='kano':
            intro=[g for g in groups if not g['body'] and g['actor']==obj and g['process']==proc and mf+birth<=g['frame']<mf+flight_age]
            check([g['group'] for g in intro]==[int(g['native'],16) for g in report[target]['intro']] and
                  [g['frame']-mf-start for g in intro]==[3,6,9,12,15,18],'All original detached startup composites and three-field cadence')
            for j in range(18):
                f=effect_by[birth+1+j]
                check(f['pose']==int(report[target]['intro'][j//3]['native'],16) and
                      (f['x'],f['y'],f['vx'],f['vy'])==(by[start,side]['x']-sign*100,by[start,side]['y']-72,0,0),
                      'Every stationary original intro field and compensated pivot')
            f=effect_by[flight_age]
            check(f['pose']==int(report[target]['intro'][-1]['native'],16) and f['vx']==vx and
                  (f['x'],f['y'])==(by[start,side]['x']-sign*100,by[start,side]['y']-72), 'Exact one-field original knife velocity-before-pose handoff')
        travels=[int(g['native'],16) for g in report[target]['flight']]
        contacts=kinds('contact');last=contacts[0]['age'] if contacts else end['age']
        executed=[g for g in groups if not g['body'] and g['actor']==obj and mf+flight_age<=g['frame']<=mf+last]
        # Exclude impact groups on the contact field, which execute immediately.
        executed=[g for g in executed if g['group'] in travels]
        redraws=[g for g in executed if g['vx']!=vx]
        # Native victim alignment stops velocity and redraws the last travel
        # group twice while flipping to the victim then restoring travel facing.
        # Those are real contact redraws, not new travel-cycle advances.
        check(not redraws if not contacts else len(redraws)==2 and all(
              g['frame']==mf+last and g['vx']==0 and g['process']==proc and g['pc']==0xff8387a0 and g['writes']==0
              for g in redraws), 'Only actual native contact alignment redraws interrupt travel')
        executed=[g for g in executed if g['vx']==vx]
        check(bool(executed),'Actual travelling group executions')
        for j,g in enumerate(executed):
            check(g['group']==travels[j%len(travels)] and g['frame']==mf+flight_age+j*timing['flight_hold'] and
                  g['pc']==0xff8387a0 and g['process']==proc and g['id']==IDS[target] and g['vx']==vx and g['vy']==0 and g['writes']==0,
                  'Every native full-cycle travelling pose, one/three-field cadence and owned velocity')
        fx=by[start,side]['x']+sign*(-12 if target=='kano' else 8);fy=by[start,side]['y']+(-40 if target=='kano' else 0)
        check((first['x'],first['y'])==(fx,fy),'Original first-flight body-relative position in actual facing')
        for age in range(flight_age+1,last+1):
            f=effect_by[age];j=age-flight_age-1
            check(f['pose']==travels[(j//timing['flight_hold'])%len(travels)] and
                  (f['x'],f['y'],f['vx'],f['vy'])==(fx+sign*8*j,fy,vx,0), 'Every original travel pose hold and actual native position field')
        geo=[g for g in geometry if g['cycle']==cycle];collisions=kinds('collision')
        check(len(geo)==len(collisions) and bool(geo),'Every actual collision call has native rectangle evidence')
        for g,e in zip(geo,collisions):
            f=effect_by[g['age']];vel=f['vx']-(1<<32) if f['vx']&(1<<31) else f['vx'];x=f['x']+vel//65536;y=f['y']
            if target=='kano' and g['age']==flight_age:x+=sign*80;y+=32
            left=x-core[0] if f['flags']&16 else x+core[0]-core[2]
            check(e['a0']==19 and e['entry']==0xff8b6ac0 and e['pc']==0xff8b6ad0 and e['a8']==obj and e['a13']==proc and
                  g['child']==obj and g['process']==proc and xy(g['attack_min'])==(left,y+core[1]) and
                  xy(g['attack_max'])==(left+core[2],y+core[1]+core[3]) and g['writes']==0 and
                  g['age']>=start+(21 if target=='kano' else 16), 'Original active timing and actual native collision core, not an early proxy hit')
        if scenario=='miss':
            check(not contacts and not kinds('reaction'),'Duck produces no false contact')
        else:
            check(len(contacts)==len(kinds('reaction'))==1,'One actual native hit/block reaction')
            at=contacts[0]['age'];duration=24 if target=='kano' else 28
            check(end['age']==at+duration,'Complete native impact retirement duration')
            delta=22 if scenario=='hit' else 6
            expected_health.append(dict(frame=mf+at,age=at,cycle=cycle,slot=victim,before=161-(cycle-1)*delta,
                                        after=161-cycle*delta,pc=0xff836700,a8=obj,a13=proc,writes=0))
        for e in [end,*contacts,*kinds('reaction')]:
            check(e['a8']==obj and e['a13']==proc and e['pc']==e['entry']+16 and e['writes']==0,'Actual owned native contact and retirement instructions')
        for age in range(start+70,min(start+80,600)):
            f=by[age,side]
            check(f['action']==0x303 and f['flags']==1 and f['vx']==f['vy']==0 and f['y']==f['floor'], 'Thrower remains grounded and ready after recovery')
    check(health==expected_health,'Exact native hit/chip ledger or zero duck damage')
    for s in (1,2):
        value=161;ledger=[h for h in health if h['slot']==s];index=0
        for age in range(601):
            while index<len(ledger) and ledger[index]['age']<age:value=ledger[index]['after'];index+=1
            check(by[age,s]['hp']==value,'Every actual lifebar field matches native damage')
        for age in range(560,601):
            f=by[age,s];check(f['action']==0x303 and f['flags']==1 and f['body']==0x12 and f['trail']==0 and
                             f['vx']==f['vy']==f['gravity']==0 and f['y']==f['floor'],'Both actors recover, clear attachments and remain ready')
    check('MK2_PROJ_CONTACT_ERROR' not in log,'No native contact observer errors')
    return dict(passed=not errors,errors=errors,scope='native_choreography_fields_not_component_DMA_screenshot_endings_CPU_or_audio_proof')


def verify_contact(log,target,side):
    try:return _contact(log,target,side)
    except (KeyError,ValueError,TypeError,IndexError,StopIteration) as e:
        return dict(passed=False,errors=['Malformed/missing choreography evidence: '+str(e)])


def verify(folder,target,side,*,candidate_name='diagnostic_v300_native_projectile_choreography',exe_sha='b67d9fd07b285c5bd186086125b6568bbd2d8fb001e887bb73df353a216d6d20',payload_sha=PAYLOAD_SHA):
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    result=verify_projectile_join(log,target,side,False,contact_verifier=verify_contact)
    result['contact']=verify_contact(log,target,side)
    metadata=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    identity_errors=[]
    if (metadata.get('exit_code'),metadata.get('target'),metadata.get('side'),metadata.get('candidate')) != (
            0,target,side,candidate_name):
        identity_errors.append('Exact terminal current-candidate case identity')
    hashes=metadata.get('input_hashes',{})
    for path,expected in hashes.items():
        source=Path(path)
        if source.suffix.lower() in ('.lua','.ps1'):
            source=folder/'input_sources'/source.name
        if not source.exists() or hashlib.sha256(source.read_bytes()).hexdigest().upper()!=expected:
            identity_errors.append('Exact immutable case launch input: '+source.name)
    candidate=ROOT/candidate_name
    if hashlib.sha256((candidate/'roms/mk2ks/mk2ks.mdata').read_bytes()).hexdigest()!=payload_sha.lower():
        identity_errors.append('Exact matched full choreography payload')
    if hashlib.sha256((candidate/'mkport_candidate.exe').read_bytes()).hexdigest()!=\
            exe_sha.lower():
        identity_errors.append('Exact current choreography executable')
    result['errors']+=identity_errors
    result['passed']=not result['errors']
    result['scope']='cold_real_join_native_release_startup_full_flight_contact_fields_not_render_endings_CPU_or_audio'
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path)
    parser.add_argument('--target',choices=IDS,required=True);parser.add_argument('--side',choices=(1,2),type=int,required=True)
    args=parser.parse_args();result=verify(args.folder,args.target,args.side)
    print(json.dumps(result,indent=2));raise SystemExit(0 if result['passed'] else 1)
