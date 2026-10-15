"""Bounded original MK3 reference: Liu/Sub-Zero, actual hit/block/duck paths."""
import json
import re
import struct
from pathlib import Path
from verify_native_candidate_v500 import ROOT
from verify_ko_round_floor_shadows import need,digest

HEX={'pc','actor','main','victim_min','victim_max','attack_min','attack_max','vx','vy','gravity','mask','action'}
def rows(log,tag):
    found=[]
    for line in log.splitlines():
        if not line.startswith('MK3_BALL_'+tag+' '):continue
        row=dict(re.findall(r'(\w+)=([^\s]+)',line))
        for k,v in row.items():
            if k in HEX:row[k]=int(v,16)
            elif re.fullmatch(r'-?\d+',v):row[k]=int(v)
        found.append(row)
    return found

def rect(n):return n&65535,(n>>16)&65535

def verify_log(log,victim,scenario):
    need(victim in ('liu_kang','sub_zero') and scenario in ('ground','block','duck'),'Reference scenario')
    need(not re.search(r'Lua error|LUA ERROR|Fatal error|access violation',log,re.I),'Original runtime error')
    entries=rows(log,'ENTRY');need(len(entries)==1,'One original own instruction entry')
    e=entries[0];need(e['pc']==0xff9e6360 and e['writes']==0,'Original native action PC')
    start=e['frame']
    states=rows(log,'STATE');by={(r['frame'],r['side']):r for r in states}
    defense=rows(log,'DEFENSE');db={(r['frame'],r['slot']):r for r in defense}
    need(all((f,s)in by and(f,s)in db for f in range(start-12,4231)for s in(1,2)),
         'Complete paired original fields through post-contact recovery')
    own,v=by[start,1],by[start,2]
    need(own['actor']==e['actor'] and v['actor']!=own['actor'],'Native acting participant')
    victim_id=13 if victim=='liu_kang'else 4
    need(all(r['actor']==(own if r['side']==1 else v)['actor'] and r['id']==(0 if r['side']==1 else victim_id)
             for r in states if start-12<=r['frame']<=4230),'Original selected IDs, no substitution')
    health=rows(log,'HEALTH');damage=24 if scenario=='ground'else 5 if scenario=='block'else 0
    need(len(health)==(0 if scenario=='duck'else 1),'Original exact contact count')
    for h in health:
        need(h['slot']==2 and h['pc']==0xffa5d5a0 and h['mask']==0xffff and h['writes']==0 and
             h['before']==166 and h['after']==166-damage,'Original native collision damage')
    for f in range(start-12,4231):
        expected=(166,166-damage if health and f>health[0]['frame']else 166)
        need(tuple(map(int,by[f,1]['health'].split(',')))==expected and
             by[f,2]['health']==by[f,1]['health'],'Original paired health ledger')
    geometry=rows(log,'GEOMETRY');need(bool(geometry),'Original actual collision bounds')
    for g in geometry:
        need(g['pc']==0xffa5cc40 and(g['actor'],g['main'])==(e['actor'],e['main']) and
             g['bounds']==1 and g['writes']==0,'Original owned rectangle instruction')
        x,y=rect(g['attack_min']);right,bottom=rect(g['attack_max'])
        field=by[g['frame'],1]
        need(right-x==72 and bottom-y==31 and y==field['y']+14,'Original typed descriptor geometry')
        need(db[g['frame'],1]['action']==0x20b and field['y']==db[g['frame'],1]['floor']+16 and
             field['vx']==0xa0000 and field['vy']==field['gravity']==0,'Original actual flight')
    if scenario=='duck':
        need([g['frame']for g in geometry]==list(range(start+7,start+27)),
             'Original twenty complete rectangle comparisons')
        flight=[by[f,1]for f in range(start+1,start+27)]
        need(all(f['vx']==0xa0000 and f['vy']==f['gravity']==0 and f['y']==db[f['frame'],1]['floor']+16
                 for f in flight),'Original twenty-six actual rolling fields')
        need(all(b['x']-a['x']==10 for a,b in zip(flight,flight[1:])), 'Original ten-pixel coordinates')
        for g in geometry:
            ax,ay=rect(g['attack_min']);bx,by_=rect(g['attack_max'])
            vx,vy=rect(g['victim_min']);wx,wy=rect(g['victim_max'])
            need(db[g['frame'],2]['action']==0x302 and (bx<vx or wx<ax or by_<vy or wy<ay),
                 'Original duck has no two-dimensional collision overlap')
    else:
        need(geometry[-1]['frame']==health[0]['frame'],'Original contact rectangle and native write agree')
        contact=health[0]['frame']
        need(db[contact,2]['action']==(0x700 if scenario=='block'else 0x303),'Original actual defense at contact')
        rebound=[by[f,1]for f in range(contact+1,4231)if db[f,1]['action']==0x602]
        need(bool(rebound) and rebound[0]['vy']==0xfff80000 and rebound[0]['gravity']==0x6000,
             'Original rebound begins with native upward velocity and gravity')
        airborne=[r for r in rebound if r['y']<db[r['frame'],1]['floor']]
        need(bool(airborne) and all(r['gravity']==0x6000 for r in airborne),
             'Original gravity throughout airborne rebound')
        # Later left-edge clamping stops horizontal motion in this real arena.
        # Verify the first twenty fields, before that boundary, not an invented
        # constant velocity through the wall.
        initial=[by[f,1]for f in range(contact+1,contact+21)]
        need(all(r['vx']==(0xffff0000 if scenario=='block'else 0xfffb0000) for r in initial) and
             all(b['vy']==(a['vy']+0x6000)&0xffffffff for a,b in zip(initial,initial[1:])),
             'Original twenty-field one/five-pixel rebound and native vertical integration')
    need(all(by[4230,s]['y']==db[4230,s]['floor'] and by[4230,s]['vx']==by[4230,s]['vy']==by[4230,s]['gravity']==0
             for s in(1,2)),'Original participants finish on their own floors')
    return dict(victim=victim,scenario=scenario,damage=damage,geometry=len(geometry),fields=(4231-(start-12))*2)

def verify(inputs):
    program=ROOT/'mk3/mk3-maincpu.bin'
    descriptor=struct.unpack_from('<7h',program.read_bytes(),(0xffa5b520-0xff800000)//8)
    need(descriptor==(57,14,72,31,0x1a00,0x1805,1),'Original ROM descriptor, not inferred from captured HP')
    inputs[str(program)]=digest(program);cases=[]
    for victim in ('liu_kang','sub_zero'):
        for scenario in ('ground','block','duck'):
            folder=ROOT/f'audit_v505_original_ball_{victim}_{scenario}'
            r=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
            before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
            need(r['exit_code']==0 and r['game']=='mk3'and r['cheats']is False and r['assistance']=='none'and
                 r['scenario']==scenario and r['victim']==victim and r['input_hashes']==before,'Original launch provenance')
            for path,sha in before.items():
                need(digest(Path(path))==sha,'Original reference input changed');inputs[path]=sha
            need('1 were OK' in(folder/'verifyroms.log').read_text(encoding='utf-8-sig'),'Actual original ROM verification')
            cases.append(verify_log((folder/'run.log').read_text(encoding='utf-8-sig'),victim,scenario))
            for name in ('run.log','result.json','input_hashes_before.json','verifyroms.log'):
                f=folder/name;inputs[str(f)]=digest(f)
    return cases

def verify_phases(inputs):
    cases=[]
    for first in(3980,3984,3988,3992,3996,4004,4008,4012):
        folder=ROOT/f'audit_v507_original_liu_duck_phase_{first}'
        r=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
        need(r['exit_code']==0 and r['game']=='mk3'and r['cheats']is False and r['assistance']=='none'and
             r['scenario']=='duck'and r['victim']=='liu_kang'and r['duck_start']==first and r['input_hashes']==before,
             'Original phase launch provenance')
        for path,sha in before.items():
            need(digest(Path(path))==sha,'Original phase input changed');inputs[path]=sha
        log=(folder/'run.log').read_text(encoding='utf-8-sig')
        need(f'MK3_BALL_INPUT frame={first} field=P2 Down value=1 writes=0' in log,
             'Actual original phase-shifted controller input')
        case=verify_log(log,'liu_kang','duck');case['duckStart']=first;cases.append(case)
        for name in('run.log','result.json','input_hashes_before.json','verifyroms.log'):
            file=folder/name;inputs[str(file)]=digest(file)
    return cases
