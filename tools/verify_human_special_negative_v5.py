"""Current human blocks/duck/far misses and recovery, NOT complete fidelity.

Square versus ground block is deliberately NON-CONTACT, not a blocked hit.
Negative own-special damage is fixed from source descriptors/branches, not fitted
from the captured HP. Ordinary initial charged kicks are separate native actions.
"""
import json
import re
from pathlib import Path
import verify_native_candidate_v545 as build
from verify_ko_round_floor_shadows import need, digest, rgb

ROOT=build.ROOT
VICTIMS={'kung_lao':0,'liu_kang':1,'cage':2,'baraka':3,'kitana':4,'mileena':5,
         'shang_tsung':6,'raiden':7,'sub_zero':8,'reptile':9,'scorpion':10,'jax':11,'kano':17,'sonya':18}
SPECS={'knife':(17,0xffffb000,22),'ball':(17,0xffffde00,24),
       'blade':(17,0xfff8cc00,26),'choke':(17,0xfff91400,32),
       'ring':(18,0xffffb400,22),'square':(18,0xffffca00,0),
       'bicycle':(18,0xfff9a400,22),'leg':(18,0xfff80800,35)}
HEX={'actor','main','owner','pose','vx','vy','gravity','flags','body','trail','bank',
     'entry','expectedEntry','pc','a8','a13','mask','victim_min','victim_max','attack_min','attack_max','a0','a1','a2','a3','a6','b2','desired','address','data','victim_actor','victim_main','victim_action','victim_body'}

def rows(log,tag):
    out=[]
    for line in log.splitlines():
        if not line.startswith('MK2_HSPECIAL_'+tag+' '):continue
        row=dict(re.findall(r'(\w+)=([^\s]+)',line))
        for key,value in row.items():
            if (key in HEX and not(tag=='RESULT' and key=='entry')) or (tag=='PARAMETERS'and key=='action') or (tag=='VELOCITY'and key=='before'):row[key]=int(value,16)
            elif re.fullmatch(r'-?\d+',value):row[key]=int(value)
        out.append(row)
    return out

def clean(field):
    return (field['y']==field['floor'] and field['vx']==field['vy']==field['gravity']==field['trail']==0
            and field['flags']&0x1c==0 and field['body']&0x0c==0 and field['action']==0x303)

BLOCK_DAMAGE={'knife':6,'ball':5,'blade':3,'choke':0,'ring':6,'square':0,'bicycle':3,'leg':35}

def verify_log(log,move,side,scenario,victim='sub_zero'):
    need(victim in VICTIMS,'Named actual victim')
    need(scenario in ('block','miss')or(scenario=='duck_block'and move=='leg'),'Actual defensive/miss scenario')
    air=False
    identity,entry_address,_=SPECS[move]
    damage=BLOCK_DAMAGE[move]if scenario=='block'else 0
    need(not re.search(r'Lua error|LUA ERROR|Fatal error|access violation',log,re.I),'Runtime error')
    need(not rows(log,'FAILED'),'Actual failed phase')
    results=rows(log,'RESULT');need(len(results)==1,'One complete terminal record')
    result=results[0]
    need(result['move']==move and result['side']==side and result.get('air')==int(air) and result['writes']==0 and
         result['assistance']=='none' and result['fullPortAcceptance']=='false' and result['scenario']==scenario and result.get('victim')==victim,'Unassisted bounded result')
    for tag,key in [('CSS','css'),('LIVE','live'),('READY','ready'),('COMMAND','command'),
                    ('RECOVERED','recovered'),('FINAL','frame')]:
        events=rows(log,tag);need(len(events)==1 and events[0]['frame']==result[key], 'Actual '+tag+' event')
    need(700<=result['css']<result['live']<result['ready']<=result['command']<result['entry']<
         result['recovered']<result['followup']<result['frame'], 'Actual phase chronology')
    need(result['followup']==result['recovered']+16 and result['frame']==result['followup']+160,
         'Full ordinary follow-up interval')
    fields=rows(log,'FIELD');by={(f['frame'],f['slot']):f for f in fields}
    expected={(f,s)for f in range(result['ready'],result['frame']+1)for s in (1,2)}
    need(len(fields)==len(by)==len(expected) and set(by)==expected,'Every paired actual field')
    owners={n:(by[result['ready'],n]['actor'],by[result['ready'],n]['main'])for n in (1,2)}
    for field in fields:
        n=field['slot'];ident=identity if n==side else VICTIMS[victim]
        need(field['move']==move and field['side']==side and field['writes']==0 and
             field['assistance']=='none' and field['scenario']==scenario and field['victim']==victim and field['mode']==2 and field['state']==1 and
             field['id']==field['roster']==ident and field['owner']==field['actor'] and
             (field['actor'],field['main'])==owners[n] and
             0x01000000<=field['actor']<0x01100000 and 0x01000000<=field['main']<0x01100000 and
             0<=field['hp']<=161, 'Actual native character identity, human ownership and health')
    need(all(by[result['ready'],n]['hp']==161 and clean(by[result['ready'],n])for n in (1,2)),
         'Original full-health grounded match ready')
    events=rows(log,'EVENT');entries=[e for e in events if e['entry']==entry_address]
    need(len(entries)==1 and entries[0]['frame']==result['entry'],'Exactly one own native special entry')
    for event in events:
        need((event['actor'],event['main'])==owners[side] and event['a8']==event['actor'] and
             event['a13']==event['main'] and event['id']==identity and event['pc']==event['entry']+16 and
             event['entry'] in (entry_address,0xff861350,0xff861500) and event['writes']==0,
             'Native instruction and actual actor/Main provenance')
    returns=[e for e in events if e['entry']==0xff861350 and
             result['entry']<e['frame']<=result['recovered']]
    need(bool(returns),'Original individual ready handoff after own special')
    need(all(clean(by[result['recovered'],n])for n in (1,2)),'Both actual fighters recover on their own floors')
    released=rows(log,'DEFENSE_RELEASED')
    need(len(released)==1 and released[0]['frame']==result['command']+220 and
         result['recovered']>=result['command']+221,'Actual defense release precedes grounded recovery')
    defensive= scenario in ('block','duck_block')or move in ('knife','ring','ball','bicycle')
    if defensive:
        expected_action=0x700 if scenario=='block'else 0x701 if scenario=='duck_block'else 0x302
        need(all(by[f,3-side]['action'] in ((0x302,0x700,0x701) if scenario=='duck_block' else (expected_action,)) and
                 by[f,3-side]['y']==by[f,3-side]['floor']
                 for f in range(result['command']-4,result['entry']+1)),
             'Actual grounded native block/duck, not merely commanded input')
    if scenario=='miss'and move in ('blade','choke','leg'):
        need(rows(log,'COMMAND')[0]['gap']>=150,'Actual far separation for bounded close-move miss')
        need(all(abs(by[f,side]['x']-by[f,3-side]['x'])>=150
                 for f in range(result['entry'],result['entry']+10)),
             'Real miss geometry throughout original startup')
    if move=='bicycle':
        need(all(by[f,side]['action']!=0x214 and by[f,3-side]['action']!=0x215
                 for f in range(result['entry'],result['recovered']+1)),
             'No paired catch after a blocked or ducked bicycle')
    health=rows(log,'HEALTH')
    for event in health:
        need(event['slot']==3-side and event['writes']==0 and event['pc']==0xff836700 and
             event['mask']==0xffff and 0<=event['after']<=event['before']<=161,
             'Original collision damage, no health assistance')
    for n in (1,2):
        for frame in range(result['ready'],result['frame']):
            stores=[h for h in health if h['frame']==frame and h['slot']==n]
            before,after=by[frame,n]['hp'],by[frame+1,n]['hp']
            if stores:
                need(stores[0]['before']==before and stores[-1]['after']==after,
                     'Actual collision stores explain adjacent callback health')
                need(all(a['after']==b['before']for a,b in zip(stores,stores[1:])), 'Ordered damage ledger')
            else:need(before==after,'Unexplained health change')
    contacts=[h for h in health if result['entry']<=h['frame']<=result['recovered']]
    actual_damage=sum(h['before']-h['after']for h in contacts)
    need(actual_damage==damage,'Own special contact damage (excludes initial ordinary charged kick)')
    if scenario=='duck_block':
        need(bool(contacts) and all(by[h['frame'],3-side]['action']==0x701 for h in contacts),
             'Native crouch-block 0701 at the actual leg collision, including zero-damage store')
    if move=='ball':
        verify_ball(log,by,result,side,scenario,contacts)
    own_poses={by[f,side]['pose']for f in range(result['entry']+1,result['recovered']+1)}
    need(len(own_poses)>=3,'Actual special body animation advances')
    if air:
        need(contacts and all(by[h['frame'],3-side]['y']<by[h['frame'],3-side]['floor']
                             for h in contacts if h['before']!=h['after']),
             'Square-wave hit actually occurs against airborne victim')
    need(all(by[f,side]['hp']==161 for f in range(result['ready'],result['frame']+1)),
         'Passive opponent cannot injure attacker')
    inputs=rows(log,'INPUT');keys={(i['frame'],i['slot'],i['button'])for i in inputs}
    need(len(inputs)==len(keys) and all(i['writes']==0 and i['assistance']=='none'for i in inputs),
         'Actual input inventory without duplicates/assistance')
    command=rows(log,'COMMAND')[0];forward=command['forward'];back='Left'if forward=='Right'else'Right'
    need(command['expectedEntry']==entry_address and forward in ('Left','Right'),'Own command spec')
    plan=[]
    if move in ('knife','ring','blade','choke'):
        plan=[('Down',0,3),(back if move=='knife'else forward,5,3),
              ('High_Punch'if move in ('knife','blade')else'Low_Punch',6,3)]
    elif move=='square':plan=[(forward,0,3),(back,5,3),('High_Punch',6,3)]
    elif move=='ball':plan=[('Low_Kick',0,84)]
    elif move=='bicycle':plan=[(back,0,3),(back,6,3),('Down',12,3),('High_Kick',13,3)]
    else:plan=[('Down',0,7),('Low_Punch',3,4),('Block',3,4)]
    expected_command={(result['command']+at,side,button)for button,start,hold in plan
                      for at in range(start,start+hold)}
    if defensive:
        buttons=('Down','Block')if scenario=='duck_block'else('Block',)if scenario=='block'else('Down',)
        for button in buttons:
            expected_command|={(result['command']+at,3-side,button)for at in range(220)}
            need({(result['command']+at,3-side,button)for at in range(-20,0)}<=keys,
                 'Twenty actual preparation fields before the special command')
    actual_command={key for key in keys if result['command']<=key[0]<result['followup']}
    need(actual_command==expected_command,'Exact real native command inputs, including LK release')
    follow=result['followup']
    plans=rows(log,'FOLLOWUP_PLAN');need(len(plans)==1 and plans[0]['frame']==follow,'Actual follow-up plan')
    gap=abs(by[follow,side]['x']-by[follow,3-side]['x'])
    toward_direction='Right'if by[follow,side]['x']<by[follow,3-side]['x']else'Left'
    direction=('Left'if toward_direction=='Right'else'Right')if gap<100 else toward_direction
    hold=24 if gap<100 else 8
    need(plans[0]['gap']==gap and plans[0]['direction']==direction and plans[0]['hold']==hold,
         'Geometry-derived separation without a forced position or throw substitution')
    expected_follow={(follow+at,side,button)for button,start,hold in
                     [(direction,0,hold),('Up',40,3),('High_Punch',112,3)]for at in range(start,start+hold)}
    need({key for key in keys if key[0]>=follow}==expected_follow,'Actual ordinary follow-up inputs')
    walking=[by[f,side]for f in range(follow+1,follow+10)]
    # Square-wave crossings and the leg flip can leave the old command
    # direction pointing AWAY from the opponent. MKII walks backward at
    # two pixels, forward at 2.5; do not mistake a real backwalk for a stall.
    sign=1 if direction=='Right'else -1
    opponent=by[follow,3-side];walker=by[follow,side]
    toward=(opponent['x']-walker['x'])*sign>0
    speed=0x28000 if toward else 0x20000
    velocity=(speed*sign)&0xffffffff
    need(all(by[f,side]['vx']==velocity and by[f,side]['y']==by[f,side]['floor']
             for f in range(follow+3,follow+hold+1)), 'Native forward/back walking responds after special')
    need(all((by[f,side]['x']-by[f-1,side]['x'])*sign in ((2,3)if toward else(2,))
             for f in range(follow+3,follow+hold+1)), 'Actual walk coordinates agree with native velocity')
    need(any(by[f,side]['y']<by[f,side]['floor'] and by[f,side]['vy']!=0
             for f in range(follow+42,follow+65)),'Actual jump responds after special')
    need(any(by[f,side]['action']==0x101 for f in range(follow+114,follow+140)),
         'Original high-punch action responds after landing')
    need(all(clean(by[result['frame'],n])for n in (1,2)),'Both fighters finish follow-up cleanly')
    return dict(move=move,side=side,scenario=scenario,fields=len(fields),entry=result['entry'],
                recovered=result['recovered'],nativeContactDamage=actual_damage,
                fullPortAcceptance=False)


def coord(n):
    n &= 0xffff
    return n-0x10000 if n&0x8000 else n

def rect(n):
    return coord(n),coord(n>>16)

def verify_ball(log,by,result,side,scenario,contacts):
    geometry=rows(log,'GEOMETRY')
    need(bool(geometry),'Actual native rectangle comparisons')
    own=by[result['entry'],side]
    for g in geometry:
        need(g['move']=='ball' and g['side']==side and g['scenario']==scenario and
             g['pc']==0xff835b80 and g['actor']==own['actor'] and g['main']==own['main'] and
             g['writes']==0 and g['assistance']=='none' and g['bounds']==1,
             'Owned native cannonball rectangle instruction')
        field=by[g['frame'],side]
        victim=by[g['frame'],3-side]
        need(all(g[key]==field[key] for key in ('vx','vy','gravity','y','floor')) and
             g['victim_actor']==victim['actor'] and g['victim_main']==victim['main'] and
             g['victim_id']==victim['id'] and g['victim_action']==victim['action'],
             'Instruction-time motion and defender agree with actual owned callback fields')
        x,y=rect(g['attack_min']);right,bottom=rect(g['attack_max'])
        need(right-x==72 and bottom-y==31 and y==field['y']+8,
             'Translated native attack plane, unchanged 72-by-31 dimensions')
        need(field['action']==0x20b and field['y']==field['floor']+16 and
             field['vy']==field['gravity']==0 and abs(coord(field['vx']>>16))==10,
             'Unchanged actual cannonball height and native near-block/far-miss velocity')
    if scenario=='miss':
        need(rows(log,'COMMAND')[0]['gap']>=150,'Far charge excludes an ordinary low-kick hit')
        start=result['entry']+7
        need([g['frame']for g in geometry]==list(range(start,start+20)),
             'All twenty native checks following six non-contact flight fields')
        flight=[by[f,side]for f in range(result['entry']+1,result['entry']+27)]
        sign=1 if rows(log,'COMMAND')[0]['forward']=='Right'else -1
        need(all(f['action']==0x20b and f['y']==f['floor']+16 and
                 f['vx']==((sign*0xa0000)&0xffffffff) and f['vy']==f['gravity']==0 for f in flight),
             'All twenty-six original constant-speed flight fields')
        need(all((b['x']-a['x'])*sign==10 for a,b in zip(flight,flight[1:])),
             'Uninterrupted native cannonball coordinates')
        need(not contacts,'Duck miss must not invoke collision damage or rebound')
        for g in geometry:
            need(by[g['frame'],3-side]['action']==0x302,'Actual duck throughout native comparisons')
            x,y=rect(g['attack_min']);right,bottom=rect(g['attack_max'])
            vx,top=rect(g['victim_min']);vright,vbottom=rect(g['victim_max'])
            # Native CMPXY rejects equality at either edge: first comparison
            # uses JRNC/JRNV; second uses JRLT/JRLS with CMPXY's XY flags.
            # A shared edge has zero area and is not a native collision.
            need(right<=vx or vright<=x or bottom<=top or vbottom<=y,
                 'Actual two-dimensional duck-miss rectangles never overlap')
        need(all(by[f,3-side]['hp']==161 for f in range(result['ready'],result['frame']+1)),
             'Neither charged ordinary kick nor cannonball hits the ducking victim')
    else:
        need(len(geometry)==1 and len(contacts)==1 and contacts[0]['frame']==geometry[0]['frame'],
             'One actual blocked contact and native chip write')
        need(by[geometry[0]['frame'],3-side]['action']==0x700,'Actual standing block at contact')


def verify_repel(log,side):
    fields=rows(log,'FIELD');by={(f['frame'],f['slot']):f for f in fields}
    r=rows(log,'RESULT')[0]
    need(all(by[f,1]['repel']==by[f,2]['repel'] and 0<=by[f,1]['repel']<=4
             for f in range(r['ready'],r['frame']+1)),'Actual shared, bounded native repel counter')
    need(all(by[f,1]['repel']==0 for f in (r['ready'],r['recovered'],r['frame'])),
         'No persistent body-push suppression at ready/recovered/final')
    roll=[f for f in fields if f['slot']==side and f['action']==0x20b]
    need(bool(roll) and all(f['repel']==2 for f in roll),'Native refresh during owned rolling fields')
    end=max(f['frame']for f in fields if f['slot']==side and f['action']in(0x20b,0x602))
    need(all(by[f,1]['repel']==0 for f in range(end+3,r['recovered']+1)),
         'Short native counter expires after roll/rebound without observer assistance')

def verify_rebound(log,side,blocked):
    r=rows(log,'RESULT')[0];by={(f['frame'],f['slot']):f for f in rows(log,'FIELD')}
    contacts=[h for h in rows(log,'HEALTH')if r['entry']<=h['frame']<=r['recovered'] and h['before']!=h['after']]
    need(len(contacts)==1 and contacts[0]['before']-contacts[0]['after']==(5 if blocked else 24),'Native contact kind')
    hit=contacts[0]['frame'];magnitude=1 if blocked else 5
    own=by[hit,side]
    rebound=[by[f,side]for f in range(hit+1,r['recovered']+1)if by[f,side]['action']==0x602]
    need(len(rebound)>=20,'Actual complete rebound, not immediate fake ready')
    vx=rebound[0]['vx'];signed=vx if vx<0x80000000 else vx-0x100000000
    need(abs(signed)==magnitude*0x10000,'Actual one/five-pixel recoil, not old ten-pixel roll')
    initial=rebound[:20]
    need(all(f['vx']==vx and f['gravity']==0x6000 for f in initial) and initial[0]['vy']==0xfff80000,
         'Twenty native rebound fields preserve actual vector and original gravity')
    need(all(b['vy']==(a['vy']+0x6000)&0xffffffff for a,b in zip(initial,initial[1:])),
         'Native vertical rebound integration')
    need(all((b['x']-a['x'])*(1 if signed>0 else -1)==magnitude for a,b in zip(initial,initial[1:])),
         'Actual recoil coordinates, no velocity-only assertion')
    parameters=[p for p in rows(log,'PARAMETERS')if p['frame']==hit and p['action']==0x602]
    if blocked:
        flings=[p for p in parameters if p['entry']==0xff876660]
        velocity=[p for p in parameters if p['entry']==0xff831ac0]
        need(len(flings)==len(velocity)==1 and flings[0]['a0']==13 and flings[0]['a6']==0xffffdd00 and
             flings[0]['a1']==0xfff80000 and flings[0]['a2']==0x6000 and velocity[0]['a0']==vx,
             'Native away helper supplies signed actual/cache velocity; fling preserves it with D sentinel')
        need(all(p['actor']==own['actor'] and p['main']==own['main'] and p['pc']==p['entry']+16
                 for p in parameters),'Owned original helper instruction provenance')
        actual=[w for w in rows(log,'VELOCITY')if w['frame']==hit and
                w['actor']==own['actor'] and w['main']==own['main'] and 0xffffde00<=w['pc']<0xffffec00]
        need(len(actual)==2 and {w['address']for w in actual}=={own['actor']+0x40,own['actor']+0x50} and
             all(w['a8']==own['actor'] and w['a13']==own['main'] and w['mask']==0xffff and
                 w['data']==((vx>>16)&0xffff if w['address']==own['actor']+0x50 else vx&0xffff)
                 for w in actual),'Actual owned guest velocity stores, not merely cached/helper parameters')
    return dict(reboundFields=len(rebound),recoil=signed//0x10000)
