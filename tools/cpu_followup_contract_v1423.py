"""Full owned miss continuations after real grabs; never waive busy-state locks.

Profiles come from emitted v545 actions and their original native continuations.
Actual action-entry observations distinguish bicycle and square from generic
action-state labels. Not all contacts, victims, CPU slots, art/audio or campaigns.
"""
from build_native_blade import BODY_GROUPS, X_ADVANCES, POSE_FIELDS

PROFILES={
    'blade':(17,0xfff8cc00,0x117,0x618,0xfff8ce40),
    'bicycle':(18,0xfff9a400,0x204,0x611,0xfff9aaa0),
    'square':(18,0xffffca00,0x207,0x304,0xff876460),
}
BIKE_CYCLE=(0xfe83eb40,0xfe83eb80,0xfe83ebc0,0xfe83ec00,0xfe83ec40,
            0xfe83ec80,0xfe83ec40,0xfe83ec00,0xfe83ebc0,0xfe83eb80)


def verify(log,player,move,entry,own,victim,done,fields,flags,need,rows):
    identity,address,start_state,recovery_state,recovery_pc=PROFILES[move]
    terminal=rows(log,'RESULT')[0];end=terminal['frame'];cycle=done['cycle']
    instructions=rows(log,'FOLLOW_INSTRUCTION')
    actions=[r for r in instructions if r['kind']=='action']
    regains=rows(log,'FOLLOW_REGAIN');ready_events=rows(log,'FOLLOW_READY_INSTRUCTION')
    need(len(actions)==len(regains)==1,'Exactly one actual post-grab special entry and first owning regain')
    if len(actions)!=1 or len(regains)!=1:return {}
    action=actions[0];regain=regains[0];start,ready=action['frame'],regain['frame']
    need(action['move']==move and action['entry']==address and action['pc']==address+16 and
         action['cycle']==regain['cycle']==cycle and own['frame']<start<done['frame']<ready and
         terminal['follow_regain']==ready and end==ready+30,
         'Actual routine identity and complete first follow-up, not inferred from generic state')
    by={r['frame']:r for r in fields if entry['frame']<r['frame']<=end}
    need(len(by)==len([r for r in fields if entry['frame']<r['frame']<=end])==end-entry['frame'] and
         set(by)==set(range(entry['frame']+1,end+1)),
         'Every real paired callback through follow-up regain and terminal observation')
    follow_fields=rows(log,'FOLLOW_FIELD')
    # FOLLOW_FIELD remains explicitly owned by the first completed grab,
    # while FIELD labels the currently executing grab ordinal. A genuine new
    # CPU grab can enter during the post-follow-up observation tail. Validate
    # that bookkeeping against every observed real entry; all actual state,
    # ownership, instruction, health and motion fields remain exact.
    grab_entries=rows(log,'ENTRY')
    def same_state(r):
        current=by.get(r['frame'])
        if current is None:return False
        observed=max([entry['cycle']]+[q['cycle'] for q in grab_entries if q['frame']<r['frame']])
        return (r['cycle']==cycle and current['cycle']==observed and
                {k:v for k,v in r.items() if k!='cycle'}=={k:v for k,v in current.items() if k!='cycle'})
    need(len(follow_fields)==end-done['frame']+1 and
         {r['frame'] for r in follow_fields}==set(range(done['frame'],end+1)) and
         all(same_state(r) for r in follow_fields),
         'Independent full continuation records agree with original callback observations')
    for r in [*by.values(),regain]:
        need(all(r[k]==entry[k] for k in ('actor','main','vactor','vmain')) and
             r['owner']==r['actor'] and r['vowner']==r['vactor'] and
             r['id']==r['roster']==identity and r['vid']==r['vroster']==entry['vid'] and
             r['state']==0 and r['vstate']==1 and r['mode']==2 and
             r['stage']==entry['stage'] and r['schedule']==entry['schedule'] and
             r['hp']==entry['hp'] and r['vhp']>0,
             'Same living real CPU/human identities, owners and original campaign through continuation')
        need(r['writes']==0 and r['assistance']=='none' and r['cpu_slot']==1 and r['human_slot']==2,
             'Actual input-only continuation scope')
        def coordinate(value):
            value=(value>>16)&0xffff
            return value-0x10000 if value&0x8000 else value
        need(r['x']==coordinate(r['xraw']) and r['y']==coordinate(r['yraw']) and
             r['vxpos']==coordinate(r['vxraw']) and r['vypos']==coordinate(r['vyraw']),
             'Independent integer/raw coordinate records agree for both real actors')
    for r in [*instructions,*ready_events]:
        need(r['actor']==entry['actor'] and r['main']==entry['main'] and
             r['a8']==entry['actor'] and r['a13']==entry['main'] and
             r['cycle']==cycle and r['writes']==0 and r['assistance']=='none' and
             r['cpu_slot']==1 and r['human_slot']==2,
             'Every continuation instruction executes under the actual owning CPU Main')
    need([(r['kind'],r['entry'],r['pc'],r['frame'])for r in ready_events]==
         [('recovery',0xff861350,0xff861360,ready),('regained',0xff861500,0xff861510,ready)],
         'First actual original ready entry and post-cleanup regain share one field')
    need(regain['action']==0 and regain['y']==regain['floor'] and
         regain['vx']==regain['vy']==regain['gravity']==regain['trail']==0 and
         regain['flags']&0x1c==0 and regain['body']&0x0c==0,
         'Follow-up itself returns cleared, stopped, grounded and detached')
    selected=[n for n in flags if n['cycle']==cycle and n['slot']==1 and
              n['kind']=='action' and own['frame']<=n['frame']<ready]
    need(bool(selected) and selected[0]['frame']==own['frame'] and
         selected[0]['before']==(0x111 if identity==17 else 0x110) and selected[0]['after']==0,
         'Actual paired state clears at its original owning handoff')
    current=0x111 if identity==17 else 0x110;previous=own['frame']
    for n in selected:
        register='a1' if n['pc'] in (0xff877bc0,0xff876460) else 'a0'
        opcode=0xb02d if register=='a1' else 0xb00d
        allowed=(n['pc']==0xff83edd0 and n['after']==0 or
                 n['pc']==0xff9065d0 and n['after']==0x303 or
                 n['pc']==0xff877bc0 and n['frame']==start and n['after']==start_state or
                 n['pc']==recovery_pc and n['after']==recovery_state)
        need(allowed and n['actor']==entry['actor'] and n['main']==entry['main'] and
             n['a8']==entry['actor'] and n['a13']==entry['main'] and
             n['at']==entry['main']+0x1f0 and n['action']==n['before']==current and
             n[register]&0xffff==n['after'] and (n['op0'],n['op1'])==(opcode,0x1f0) and
             n['state']==0 and n['id']==identity and n['frame']>=previous,
             'Complete continuous native state-store ledger with live opcode, operands and registers')
        current=n['after'];previous=n['frame']
    cursor=0;current=0x111 if identity==17 else 0x110
    for at in range(own['frame']+1,ready+1):
        while cursor<len(selected) and selected[cursor]['frame']<at:
            current=selected[cursor]['after'];cursor+=1
        need(by[at]['action']==current,'Every post-grab callback matches actual original action stores')
    published=[n for n in selected if n['frame']==start and n['pc']==0xff877bc0]
    need(len(published)==1 and published[0]['before']==0x303,
         'Original setup publishes this special after genuine walking recovery')
    for field,pc,mask,offset in (('body',0xff838cf0,4,0x160),('flags',0xff877d50,0x10,0x210)):
        setters=[n for n in flags if n['cycle']==cycle and n['slot']==1 and n['frame']==start and
                 n['kind']==field and n['pc']==pc and n['actor']==entry['actor'] and
                 n['main']==entry['main'] and n['a8']==entry['actor'] and n['a13']==entry['main'] and
                 n['at']==(entry['actor'] if field=='body' else entry['main'])+offset and
                 n['action']==start_state and not n['before']&mask and n['after']==n['before']|mask]
        need(bool(setters) and bool(published) and flags.index(setters[0])>flags.index(published[0]),
             'NEW original special lock setup follows its own state publication, not residual grab locks')
    for field,pc,mask,offset in (('body',0xff83eeb0,0x0c,0x160),('flags',0xff83efc0,0x14,0x210)):
        need(any(n['cycle']==cycle and n['slot']==1 and n['frame']==ready and
                 n['kind']==field and n['pc']==pc and n['actor']==entry['actor'] and
                 n['main']==entry['main'] and n['a8']==entry['actor'] and n['a13']==entry['main'] and
                 n['at']==(entry['actor'] if field=='body' else entry['main'])+offset and
                 n['action']==0 and n['before']&mask and n['after']==n['before']&(~mask&0xffff)
                 for n in flags),'Exact original cleanup stores precede first follow-up owning regain')
    active=[by[at] for at in range(start+1,ready+1)]
    need(all(r['flags']&0x1c==0x10 and r['body']&0x0c==4 for r in active),
         'Every actual owned active field has only its NEW native action locks')
    health=rows(log,'HEALTH')
    stores=[r for r in health if entry['frame']<r['frame']<end]
    need(all(r['pc']==0xff836700 and r['slot']in(1,2) and 0<=r['after']<=r['before']<=161 and
             r['a8']in(entry['actor'],entry['vactor']) and r['a13']in(entry['main'],entry['vmain']) and
             r['writes']==0 and r['assistance']=='none' for r in stores),
         'Every continuing health store is owned original collision code, never observer assistance')
    for at in range(entry['frame']+1,end):
        for slot,key in ((1,'hp'),(2,'vhp')):
            changes=[r for r in stores if r['frame']==at and r['slot']==slot]
            if changes:
                need(changes[0]['before']==by[at][key] and changes[-1]['after']==by[at+1][key] and
                     all(a['after']==b['before']for a,b in zip(changes,changes[1:])),
                     'Complete native health ledger agrees with every adjacent continuation callback')
            else:need(by[at][key]==by[at+1][key],'No unlogged continuation health change')
    need(not any(start<=r['frame']<=ready and r['before']!=r['after'] for r in health) and
         all(r['vhp']==by[start]['vhp'] for r in active),
         'Actual three declared follow-up misses do not invent damage or catch a recovering victim')
    def calls(kind):return [r for r in instructions if r['kind']==kind and start<=r['frame']<=ready]
    def advance(a,b,gravity):
        need(b['vy']==(a['vy']+gravity)&0xffffffff and
             b['yraw']==(a['yraw']+b['vy'])&0xffffffff and
             b['xraw']==(a['xraw']+a['vx'])&0xffffffff,
             'Every exact fixed-point native gravity, Y and horizontal step')
    if move=='blade':
        need(ready==start+sum(POSE_FIELDS),'Complete original 38-field blade hold/recovery timing')
        origin=by[start+1];sign=-1 if origin['facing']&0x10 else 1
        at=start+1;advance_x=0
        trail=origin['trail']
        need(0x01000000<=trail<0x01100000,'Actual separately owned blade trail exists')
        for group,hold,delta in zip(BODY_GROUPS,POSE_FIELDS,X_ADVANCES):
            advance_x+=delta
            for field in range(at,at+hold):
                r=by[field]
                need(r['pose']==group and r['xraw']==(origin['xraw']+sign*(advance_x<<16))&0xffffffff and
                     r['y']==r['floor']==origin['floor'] and r['vx']==r['vy']==r['gravity']==0 and
                     r['trail']==trail,'Every original blade body pose, hold, advance and owned trail field')
            at+=hold
        cleanup=calls('trail_cleanup')
        need(any(r['frame']==ready and r['entry']==0xff83efd0 and r['pc']==0xff83efe0 and
                 r['trail']==trail for r in cleanup),
             'Original trail-removal routine consumes the actual effect before clean ready')
    elif move=='bicycle':
        intro=(0xfe83ea40,0xfe83ea80,0xfe83eae0);origin=by[start+1]
        sign=-1 if origin['facing']&0x10 else 1
        for elapsed in range(6):
            r=by[start+1+elapsed];phase=elapsed//2
            need(r['pose']==intro[phase] and r['xraw']==(origin['xraw']+sign*phase*5*0x10000)&0xffffffff and
                 r['yraw']==origin['yraw']+phase*10*0x10000 and r['vx']==r['vy']==r['gravity']==r['trail']==0,
                 'All three two-field original bicycle startup poses and five/ten-pixel advances')
        falling=calls('fall');need(len(falling)==1,'One original missed-bicycle fall continuation')
        if not falling:return {}
        fall=falling[0];split=fall['frame']
        need((fall['entry'],fall['pc'])==(0xff876660,0xff876670) and
             tuple(fall['a'+str(i)]for i in range(4))==(13,13,0xa000,4) and
             fall['a6']==0xfff9dc00,'Exact original bicycle fall arguments and own push callback')
        first=by[start+7]
        need(first['pose']==intro[-1] and first['vx']==(sign*0x40000)&0xffffffff and
             first['vy']==0xfffe0000 and first['gravity']==0xffff4000,
             'Actual bicycle acceleration starts after complete startup')
        for at in range(start+8,split+2):
            r=by[at];advance(by[at-1],r,0xffff4000)
            need(r['vx']==first['vx'] and r['gravity']==(0xa000 if at==split+1 else 0xffff4000) and
                 r['pose']==BIKE_CYCLE[((at-start-8)//4)%len(BIKE_CYCLE)] and r['trail']==0,
                 'Whole original negative-gravity seek and four-field body cycle through fall handoff')
        need(by[split]['stage_floor']-by[split]['y']<0xc0 and
             by[split+1]['stage_floor']-by[split+1]['y']>=0xc0,
             'First actual stage-ground-relative C0 ceiling crossing triggers missed-bicycle fall')
        base=(split-start-8)//4+2
        for at in range(split+2,ready+1):
            r=by[at];advance(by[at-1],r,0xa000)
            need(r['vx']==first['vx'] and r['gravity']==0xa000 and r['trail']==0 and
                 r['pose']==BIKE_CYCLE[(base+(at-split-2)//4)%len(BIKE_CYCLE)],
                 'Whole original bicycle falling gravity and looping body sequence')
        last=by[ready];next_y=(last['yraw']+last['vy']+last['gravity'])&0xffffffff
        need(last['y']<last['floor'] and (next_y>>16)>=last['floor'] and
             regain['yraw']==(last['floor']<<16)|(next_y&0xffff),
             'First landing crossing uses native integer-floor clamp while preserving fractional Y')
    else:
        origin=by[start+1];sign=-1 if origin['facing']&0x10 else 1
        for elapsed in range(8):
            r=by[start+1+elapsed]
            need(r['pose']==0xfe835c80 and r['xraw']==origin['xraw'] and
                 r['yraw']==(origin['yraw']-elapsed*12*0x10000)&0xffffffff and
                 r['vx']==r['gravity']==r['trail']==0 and r['vy']==0xfff40000,
                 'All original square-wave twelve-pixel rise fields')
        flight=by[start+9]
        need(flight['floor']-flight['y']==96 and flight['vx']==(sign*0xa0000)&0xffffffff and
             flight['vy']==flight['gravity']==0,'Own ground-relative 96-pixel square-wave flight begins')
        for at in range(start+10,start+35):
            r=by[at];need(r['xraw']==(flight['xraw']+sign*(at-start-9)*10*0x10000)&0xffffffff and
                         r['yraw']==flight['yraw'] and r['vx']==flight['vx'] and
                         r['vy']==r['gravity']==r['trail']==0 and
                         r['pose']==(0xff031340 if at<start+13 else 0xff031380 if at<start+16 else 0xff0313c0),
                         'Every full square-wave constant-height/speed field and owned flight pose')
        fling,fall,landing=calls('fling'),calls('fall'),calls('landing')
        need(len(fling)==len(fall)==len(landing)==1,'Whole original square-wave drop and landing chain')
        if len(fling)!=1 or len(fall)!=1 or len(landing)!=1:return {}
        split=start+34
        need(fling[0]['frame']==fall[0]['frame']==split and
             all(tuple(r['a'+str(i)]for i in range(4))==(0,0x20000,0x8000,0xfff)for r in (fling[0],fall[0])) and
             (fling[0]['entry'],fling[0]['pc'])==(0xff876650,0xff876660) and
             (fall[0]['entry'],fall[0]['pc'])==(0xff876660,0xff876670),
             'All twenty-six original flight checks precede exact native drop parameters')
        land=landing[0]['frame'];drop=by[split+1]
        need(drop['xraw']==(by[split]['xraw']+flight['vx'])&0xffffffff and
             drop['yraw']==flight['yraw'] and drop['vx']==0 and drop['vy']==0x20000 and
             drop['gravity']==0x8000,'Native final horizontal handoff and first drop field')
        for at in range(split+2,land+1):
            r=by[at];advance(by[at-1],r,0x8000)
            need(r['vx']==0 and r['gravity']==0x8000 and r['pose']==0xfe835c20,
                 'Every native square-wave fixed-point drop field and original jump pose')
        need(ready==land+4 and landing[0]['entry']==0xff876420 and landing[0]['pc']==0xff876430 and
             by[land]['y']<by[land]['floor'] and
             (by[land]['yraw']+by[land]['vy']+0x8000)>>16>=by[land]['floor'],
             'First drop floor crossing enters full four-field original landing recovery')
        need(all(by[at]['y']==by[at]['floor'] and by[at]['vx']==by[at]['vy']==by[at]['gravity']==0 and
                 by[at]['action']==0x304 and by[at]['pose']==0xfe835c20
                 for at in range(land+1,ready+1)),
             'Complete original grounded square-wave landing pose holds')
    return dict(move=move,entry=start,ready=ready,fields=ready-start,
                native_state_stores=len(selected),damage=0,
                scope='three_actual_owned_post_grab_miss_continuations_not_all_contacts_or_full_port')
