"""Actual human command/contact/recovery versus the selectable roster, not full acceptance."""
import json
import re
from pathlib import Path
import verify_native_candidate_v635 as build
import verify_human_special_negative_v5 as recoil
from verify_ko_round_floor_shadows import need, digest, rgb

ROOT=build.ROOT
VICTIMS={'kung_lao':0,'liu_kang':1,'cage':2,'baraka':3,'kitana':4,'mileena':5,
         'shang_tsung':6,'raiden':7,'sub_zero':8,'reptile':9,'scorpion':10,'jax':11,'kano':17,'sonya':18}
SPECS={'knife':(17,0xffffb000,22),'ball':(17,0xffffde00,24),
       'blade':(17,0xfff8cc00,26),'choke':(17,0xfff91400,32),
       'ring':(18,0xffffb400,22),'square':(18,0xffffca00,0),
       'bicycle':(18,0xfff9a400,22),'leg':(18,0xfff80800,35)}
HEX={'actor','main','owner','pose','vx','vy','gravity','flags','body','trail','bank',
     'entry','expectedEntry','pc','a8','a13','mask'}

def rows(log,tag):
    out=[]
    for line in log.splitlines():
        if not line.startswith('MK2_HSPECIAL_'+tag+' '):continue
        row=dict(re.findall(r'(\w+)=([^\s]+)',line))
        for key,value in row.items():
            if key in HEX and not(tag=='RESULT' and key=='entry'):row[key]=int(value,16)
            elif re.fullmatch(r'-?\d+',value):row[key]=int(value)
        out.append(row)
    return out

def clean(field):
    return (field['y']==field['floor'] and field['vx']==field['vy']==field['gravity']==field['trail']==0
            and field['flags']&0x1c==0 and field['body']&0x0c==0 and field['action']==0x303)

def verify_log(log,move,side,air=False,victim='sub_zero'):
    need(victim in VICTIMS,'Named actual victim')
    identity,entry_address,damage=SPECS[move]
    if air:
        need(move=='square','Only square has this airborne victim fixture')
        damage=27
    need(not re.search(r'Lua error|LUA ERROR|Fatal error|access violation',log,re.I),'Runtime error')
    need(not rows(log,'FAILED'),'Actual failed phase')
    results=rows(log,'RESULT');need(len(results)==1,'One complete terminal record')
    result=results[0]
    need(result['move']==move and result['side']==side and result.get('air')==int(air) and result['writes']==0 and
         result['assistance']=='none' and result['fullPortAcceptance']=='false' and result['victim']==victim,'Unassisted bounded result')
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
        need(field['move']==move and field['side']==side and field['victim']==victim and field['writes']==0 and
             field['assistance']=='none' and field['mode']==2 and field['state']==1 and
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
    if air:expected_command|={(result['command']+at,3-side,'Up')for at in range(3)}
    actual_command={key for key in keys if result['command']<=key[0]<result['followup']}
    need(actual_command==expected_command,'Exact real native command inputs, including LK release')
    follow=result['followup']
    expected_follow={(follow+at,side,button)for button,start,hold in
                     [(forward,0,8),('Up',40,3),('High_Punch',112,3)]for at in range(start,start+hold)}
    need({key for key in keys if key[0]>=follow}==expected_follow,'Actual ordinary follow-up inputs')
    walking=[by[f,side]for f in range(follow+1,follow+10)]
    # Square-wave crossings and the leg flip can leave the old command
    # direction pointing AWAY from the opponent. MKII walks backward at
    # two pixels, forward at 2.5; do not mistake a real backwalk for a stall.
    sign=1 if forward=='Right'else -1
    opponent=by[follow,3-side];walker=by[follow,side]
    toward=(opponent['x']-walker['x'])*sign>0
    speed=0x28000 if toward else 0x20000
    velocity=(speed*sign)&0xffffffff
    need(all(by[f,side]['vx']==velocity and by[f,side]['y']==by[f,side]['floor']
             for f in range(follow+3,follow+9)), 'Native forward/back walking responds after special')
    need(all((by[f,side]['x']-by[f-1,side]['x'])*sign in ((2,3)if toward else(2,))
             for f in range(follow+3,follow+9)), 'Actual walk coordinates agree with native velocity')
    need(any(by[f,side]['y']<by[f,side]['floor'] and by[f,side]['vy']!=0
             for f in range(follow+42,follow+65)),'Actual jump responds after special')
    need(any(by[f,side]['action']==0x101 for f in range(follow+114,follow+140)),
         'Original high-punch action responds after landing')
    need(all(clean(by[result['frame'],n])for n in (1,2)),'Both fighters finish follow-up cleanly')
    return dict(move=move,side=side,air=air,victim=victim,fields=len(fields),entry=result['entry'],
                recovered=result['recovered'],nativeContactDamage=actual_damage,
                fullPortAcceptance=False)

def case_folder(move,side,victim,air=False):
    suffix=move+'_air'if air else move
    return ROOT/f'audit_v656_positive_{suffix}_p{side}_{victim}'


def verify_case(move,side,victim,air=False):
    folder=case_folder(move,side,victim,air);inputs={}
    build.matched(folder,inputs)
    metadata=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    need((metadata['move'],metadata['side'],metadata['air'],metadata['victim'])==(move,side,air,victim),
         'Exact actual input fixture, no substitution')
    observer=(folder/'input_sources/mk2ks_human_special_matrix_v3.lua').read_text()
    need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|dofile\(',observer),
         'Standalone input-only observer, no guest-state assistance')
    for path in(folder/'snap').glob('*.png'):inputs[str(path)]=digest(path)
    # A failed gameplay contract stays failed; collecting the wider inventory
    # must not erase it or substitute a later passing fixture.
    try:
        log=(folder/'run.log').read_text(encoding='utf-8-sig')
        proof=verify_log(log,move,side,air,victim)
        if move=='ball':proof.update(recoil.verify_rebound(log,side,False))
        for name in('special_before.png','special_recovered.png','special_final.png'):
            path=folder/'snap'/name
            need(path.is_file() and rgb(path).shape==(254,400,3),'Three actual native snapshots')
        proof['passed']=True
    except ValueError as error:
        proof=dict(move=move,side=side,victim=victim,air=air,passed=False,error=str(error),fullPortAcceptance=False)
    proof['capture']=folder.name
    return proof,inputs


def verify():
    inputs={};cases=[]
    for move in SPECS:
        for side in(1,2):
            for victim in VICTIMS:
                for air in((False,True)if move=='square'else(False,)):
                    proof,checked=verify_case(move,side,victim,air);cases.append(proof);inputs.update(checked)
    need(len(cases)==252,'Every eight-move/slot/selectable-victim fixture, including square airborne cases')
    for file in('tools/verify_human_special_contacts_v635.py','tools/verify_native_candidate_v635.py',
                'tools/verify_human_special_negative_v5.py','tools/test_human_special_contacts_v635.py',
                'tools/verify_ko_round_floor_shadows.py','tools/inspect_ground_presentation.py'):
        inputs[str(ROOT/file)]=digest(ROOT/file)
    failures=[case for case in cases if not case['passed']]
    return dict(passed=not failures,fullPortAcceptance=False,candidate=build.NAME,cases=cases,
                cases_count=len(cases),failures=failures,
                pairedFields=sum(case.get('fields',0)for case in cases),
                scope='Actual human special commands and contact/ready/ordinary follow-up across all fourteen '
                      'selectable opponents in both slots, plus genuine airborne square-wave fixtures. '
                      'Standing square-wave is an expected anti-air miss. Failed fixtures remain failures. '
                      'Not all blocks/misses/interruptions/KO/CPU, complete choreography/pixels/audio, '
                      'all arenas, bosses, campaigns, finishers or release acceptance.',inputHashes=inputs)

if __name__=='__main__':print(json.dumps(verify(),indent=2))
