"""Actual native CPU Square hit, owned startup, pause, drop and both recoveries.

Normal P1 Kano/P2 CPU Sonya, unblocked airborne contact at the original stage
right edge. Preserve the different attacker/victim recovery times and later
ordinary/Leg Grab branches. No idle-tail, other contact/arena/KO/audio claim.
"""
import struct
import native_cpu_square_startup_contract_v3005 as base
import native_cpu_mobility_capture_contract_v3036 as native

ROOT=base.ROOT;INTRO=base.INTRO
POSE_DONORS={0xfe835c80:0xff835c80,0xff031480:0xff8361e0,
             0xfe835c20:0xff835c20,0xfe835bc0:0xff835bc0}
POSES=set(POSE_DONORS);need=native.need

def verify(log,guest,player):
    need(player=='kano','Actual airborne Kano victim context, not universal')
    base.source(log,guest)
    events=base.original.rows(log,'EVENT')
    entry=base.one([r for r in events if r['kind']=='square'],'One actual Square contact entry')
    start,actor,main=entry['frame'],entry['a8'],entry['a13']
    own=[r for r in events if r['a8']==actor and r['a13']==main and r['frame']>start]
    regain=next(r for r in own if r['kind']=='regain');ready=regain['frame']
    land=next(r for r in own if r['kind']=='landing')['frame']
    fields=base.P.rows(log,'FIELD');by={r['frame']:r for r in fields}
    need(len(by)==len(fields),'No duplicated live callbacks')
    snapshots=native.rows(log,'MK2_SQUARE_BOUNDARY_ENTRY_STATE')
    need(len(snapshots)==2 and {r['slot']for r in snapshots}=={1,2},'Both actual native entry snapshots')
    own_entry=next(r for r in snapshots if r['slot']==2);victim=next(r for r in snapshots if r['slot']==1)
    need((entry['entry'],entry['pc'],entry['id'],entry['main_owner'],entry['action'])==(0xffffca00,0xffffca10,18,actor,0x303),
         'Real CPU Sonya owned Square entry')
    need((own_entry['actor'],own_entry['main'],own_entry['id'],own_entry['roster'],own_entry['state'])==(actor,main,18,18,0)and
         (victim['id'],victim['roster'],victim['state'])==(17,17,1),'Actual native CPU and human roles')
    base.entry_boundary(log,guest,player,start,ready)
    boundary=native.rows(log,'MK2_SQUARE_BOUNDARY_EVENT')
    collision=[r for r in boundary if r['kind']=='collision_return'];contact=[r for r in boundary if r['kind']=='hit_entry']
    need([r['kind']for r in boundary]==['entry','collision_return','hit_entry']and len(contact)==1 and len(collision)==1,
         'This true earliest-flight hit has one actual collision and native hit entry')
    hit=contact[0]['frame']
    for r in boundary:
        need(r['serial']==1 and (r['a8'],r['a13'])==(actor,main)and r['pc']==r['entry']+16 and r['mask']==65535 and
             r['carry']==(r['status']>>30)&1 and r['writes']==0 and r['assistance']=='none'and
             struct.unpack_from('<H',guest,(r['entry']-0xff800000)//8)[0]==r['opcode'],'All actual native collision entries source-bound')
    need(hit==start+9 and collision[0]['frame']==hit and collision[0]['carry']==contact[0]['carry']==1 and
         collision[0]['a11']==26 and collision[0]['a0']==0xffffda00 and contact[0]['entry']==0xffffd1c0,
         'First original seek check carries to the real contact continuation')
    choices=base.rows(log,'MK2_CPU_CHOICE_EVENT');chosen=base.one([r for r in choices if r['kind']=='square'],'Actual selected Square chance')
    calls=[r for r in choices if r['serial']==chosen['serial']]
    need([r['kind']for r in calls]==['entry','first_call','first_result','second_call','second_result','square'],
         'Actual unchanged second-chance Square branch')
    for r in calls:
        need(r['frame']==start and (r['actor'],r['main'],r['owner'],r['id'],r['roster'])==(actor,main,actor,18,18)and
             (r['state'],r['human_state'],r['mode'],r['stage'],r['schedule'])==(0,1,2,0,0xfffa3180)and
             r['carry']==(r['status']>>30)&1 and r['pc']==r['entry']+16 and r['mask']==65535 and r['writes']==0 and r['assistance']=='none'and
             struct.unpack_from('<H',guest,(r['entry']-0xff800000)//8)[0]==r['opcode'],'Every native choice is owned/source-bound, no forced RNG')
    need(calls[1]['a0']==250 and calls[3]['a0']==400 and 250<=calls[2]['a0']<1000 and calls[2]['carry']==0 and
         0<=calls[4]['a0']<400 and calls[4]['carry']==1 and calls[-1]['a0']==calls[4]['a0'],'Actual original chance thresholds/status')
    victim_ready=next(r for r in events if r['frame']>hit and r['kind']=='regain'and
                      (r['a8'],r['a13'])==(victim['actor'],victim['main']))
    vend=victim_ready['frame'];need(set(range(start+1,vend+2))<=set(by),'Every callback through both actual individual recoveries')
    health=[r for r in native.rows(log,'MK2_SQUARE_LOCK_HEALTH')if start<=r['frame']<=vend]
    need(len(health)==1,'Exactly one contact HP writer before both recoveries')
    dose=health[0]
    need((dose['frame'],dose['slot'],dose['before'],dose['after'],dose['pc'],dose['a8'],dose['a13'],dose['at'],dose['mask'])==
         (hit,1,victim['hp'],victim['hp']-27,0xff836700,actor,main,0x010602f0,65535),
         'Exactly27 actual unblocked damage through the original owned health writer')
    need(struct.unpack_from('<3H',guest,(dose['pc']-48-0xff800000)//8)==tuple(dose[f'op{i}']for i in range(3))and
         dose['writes']==0 and dose['assistance']=='none','Native HP opcode/provenance')
    for at in range(start+1,vend+2):
        r=by[at]
        need((r['actor'],r['main'],r['owner'],r['id'],r['roster'],r['state'],r['vactor'],r['vmain'],r['vowner'],r['vid'],r['vroster'],r['vstate'],r['mode'])==
             (actor,main,actor,18,18,0,victim['actor'],victim['main'],victim['actor'],17,17,1,2),'Every real live callback retains true owners/roles/identities')
        need(r['floor']==r['stage_floor']-135 and r['vfloor']==r['stage_floor']-134 and r['schedule']==0xfffa3180 and r['stage']==0 and
             r['hp']==own_entry['hp']and r['vhp']==victim['hp']-(27 if at>hit else 0)and r['writes']==0 and r['assistance']=='none',
             'Every HP/floor/stage/actual live callback matches its real contact history')
    flags=[r for r in native.rows(log,'MK2_SQUARE_LOCK_FLAG')if start<=r['frame']<=vend]
    for r in flags:
        need(r['mask']==65535 and r['writes']==0 and r['assistance']=='none'and r['owner']==r['actor']and
             r['at']==(r['actor']+0x160 if r['kind']=='body'else r['main']+(0x1f0 if r['kind']=='action'else 0x210))and
             struct.unpack_from('<2H',guest,(r['pc']-32-0xff800000)//8)==(r['op0'],r['op1']), 'Every actual owned lock/state instruction source-bound')
    ownflags=[r for r in flags if r['slot']==2 and r['frame']<=ready]
    need(all((r['actor'],r['main'],r['a8'],r['a13'],r['id'],r['state'])==(actor,main,actor,main,18,0)for r in ownflags),
         'Every Square lock/ready store belongs to actual CPU Main')
    actions=[r for r in ownflags if r['kind']=='action']
    need([(r['frame'],r['before'],r['after'],r['pc'])for r in actions]==[
      (start,0x303,0x207,0xff877bc0),(land,0x207,0x304,0xff876460),
      (ready,0x304,0,0xff83edd0),(ready,0,0,0xff83edd0),(ready,0,0x303,0xff9065d0)],'Exact original Square action/landing/individual-ready stores')
    for kind,mask,setpc,clearpc in(('body',4,0xff838cf0,0xff83eeb0),('flags',16,0xff877d50,0xff83efc0)):
        stores=[r for r in ownflags if r['kind']==kind]
        need(len(stores)==3 and stores[0]['frame']==start and stores[0]['pc']==setpc and
             stores[0]['before']&mask==0 and stores[0]['after']==stores[0]['before']|mask and
             all(r['frame']==ready and r['pc']==clearpc and r['after']==r['before']&~mask for r in stores[1:])and
             stores[1]['before']&mask and not stores[2]['before']&mask,'Original individual own lock acquisition and double cleanup')
    origin=by[start+1];sign=-1 if origin['facing']&16 else 1
    need(origin['xraw']==entry['xraw']and origin['yraw']==entry['yraw'],'Actual own entry position, no shifted startup frame')
    for age in range(8):
        r=by[start+1+age]
        need(r['pose']==0xfe835c80 and r['xraw']==origin['xraw']and r['yraw']==(origin['yraw']-age*12*65536)&0xffffffff and
             r['vy']==0xfff40000 and r['vx']==r['gravity']==0,'All eight original12-pixel own rise fields')
    flight=by[hit]
    need(flight['floor']-flight['y']==96 and flight['vx']==(sign*0xa0000)&0xffffffff and flight['vy']==flight['gravity']==0,
         'Original96-pixel/10-pixel first flight collision field')
    for at in range(hit+1,hit+11):
        r=by[at]
        need(r['xraw']==(flight['xraw']+flight['vx'])&0xffffffff and r['yraw']==flight['yraw']and
             r['vx']==r['vy']==r['gravity']==0 and r['pose']==0xff031480,'All ten actual native hit-pause pose fields')
    fling=base.one([r for r in own if r['kind']=='fling'and r['frame']<=ready],'Actual own contact drop')
    split=hit+10
    need(fling['frame']==split and tuple(fling[f'a{i}']for i in range(4))==(0,0x20000,0x8000,0xfff),
         'Original own drop begins only after full ten-field contact pause')
    drop=by[split+1]
    need((drop['xraw'],drop['yraw'],drop['vx'],drop['vy'],drop['gravity'],drop['pose'])==
         (by[split]['xraw'],flight['yraw'],0,0x20000,0x8000,0xfe835c20),'Actual unshifted original drop initialization')
    for at in range(split+2,land+1):
        a,b=by[at-1],by[at]
        need(b['vy']==(a['vy']+0x8000)&0xffffffff and b['yraw']==(a['yraw']+b['vy'])&0xffffffff and
             b['xraw']==a['xraw']and b['vx']==0 and b['gravity']==0x8000 and b['pose']==0xfe835c20,'Every original own fixed-point fall step')
    last=by[land];next_y=(last['yraw']+last['vy']+0x8000)&0xffffffff
    need(land==split+16 and last['y']<last['floor']and next_y>>16>=last['floor']and ready==land+4,
         'Original sixteen-field fall and four-field landing hold')
    for at in range(start+1,ready+1):
        r=by[at]
        need(r['action']==(0x207 if at<=land else 0x304)and r['flags']&0x1c==16 and r['body']&12==4 and r['trail']==0,
             'Own contact state remains locked only until its actual individual recovery')
    for at in range(land+1,ready+1):
        r=by[at];need(r['yraw']==r['floor']<<16 and r['vx']==r['vy']==r['gravity']==0 and r['pose']==0xfe835c20,'All actual grounded own landing holds')
    need(regain['action']==0 and regain['flags']&0x1c==regain['body']&12==0 and regain['vx']==regain['vy']==regain['gravity']==regain['trail']==0 and
         regain['pose']==0xfe835bc0 and regain['yraw']==last['floor']<<16 and regain['xraw']==drop['xraw'],'Actual original own ready, no retained special lock')
    after=by[ready+1];need(after['action']==0x303 and after['flags']&0x1c==after['body']&12==0 and after['y']==after['floor'],
         'First original own controllable callback, not delayed until victim is ready')
    vf=base.one([r for r in events if r['kind']=='fling'and r['frame']==hit and
                 (r['a8'],r['a13'])==(victim['actor'],victim['main'])],'Actual owned victim fling')
    need(tuple(vf[f'a{i}']for i in range(4))==(0x38000,0xfffa0000,0x8000,5)and vf['main_owner']==victim['actor'],
         'Original3.5/-6/.5 native victim launch parameters')
    vfirst=by[hit+1]
    need(vfirst['vxraw']==vf['xraw']and vfirst['vyraw']==vf['yraw']and vfirst['vvy']==0xfffa0000 and
         vfirst['vgravity']==0x8000 and vfirst['vvx']==0x38000 and vfirst['vxpos']==vfirst['right'],
         'Actual airborne victim initial position/velocity at native stage-right boundary')
    vland=next(at for at in range(hit+2,vend+1)if by[at]['vgravity']==0 and by[at-1]['vgravity']==0x8000)
    for at in range(hit+1,vland):
        r=by[at]
        need(r['vaction']==0x503 and r['vflags']&0x1c==4 and r['vbody']&12==8 and r['vgravity']==0x8000 and
             r['vvx']==0x38000 and r['vxpos']==r['right']and r['vxraw']==vfirst['vxraw'],
             'Every actual airborne native victim field, original stage-right limit retained')
        if at>hit+1:
            a=by[at-1];need(r['vvy']==(a['vvy']+0x8000)&0xffffffff and r['vyraw']==(a['vyraw']+r['vvy'])&0xffffffff,
                            'Every original complete victim fixed-point vertical integration step')
    vbefore=by[vland-1];wanted=(vbefore['vyraw']+vbefore['vvy']+0x8000)&0xffffffff
    need(vbefore['vypos']<vbefore['vfloor']and wanted>>16>=vbefore['vfloor']and by[vland]['vyraw']==by[vland]['vfloor']<<16 and
         by[vland]['vvx']==by[vland]['vvy']==by[vland]['vgravity']==0,'Actual original victim floor crossing/clamp and velocity stop')
    clears=[r for r in flags if r['slot']==1 and r['kind']=='action'and r['before']==0x503 and r['after']==0]
    clear=base.one(clears,'First actual victim hurt cleanup')['frame']
    need(clear==vland+5 and clear<vend and all(r['pc']==0xff83edd0 for r in clears),'Original five held victim landing fields before its hurt cleanup')
    for kind,mask,pc in(('body',8,0xff83eeb0),('flags',4,0xff83efc0)):
        store=base.one([r for r in flags if r['slot']==1 and r['frame']==clear and r['kind']==kind],'Actual victim '+kind+' clear')
        need(store['pc']==pc and store['before']&mask and store['after']==store['before']&~mask and
             (store['actor'],store['main'],store['a8'],store['a13'])==(victim['actor'],victim['main'],victim['actor'],victim['main']),
             'Each actual victim lock cleared by its own original Main')
    for at in range(clear+1,vend+1):
        r=by[at];need(r['vaction']==0 and r['vflags']&0x1c==r['vbody']&12==0 and r['vypos']==r['vfloor']and
             r['vvy']==r['vgravity']==r['vtrail']==0,'Native grounded hurt-recovery animation remains clean until original victim ready')
    need(victim_ready['action']==0 and victim_ready['flags']&0x1c==victim_ready['body']&12==0 and
         victim_ready['vy']==victim_ready['gravity']==victim_ready['trail']==0 and victim_ready['yraw']>>16==victim_ready['floor']and
         by[vend+1]['vaction']==0x303,'Actual later original victim ready and control callback')
    return dict(passed=True,start=start,hit=hit,fall=split,landing=land,ready=ready,victimLanding=vland,victimHurtClear=clear,
      victimReady=vend,fields=ready-start,damage=27,ownRiseFields=8,actualFlightCollisionChecks=1,ownHitPauseFields=10,
      ownFallFields=16,ownLandingHolds=4,victimFlightFields=vland-hit-1,nativeActionStores=len(actions),nativeLockStores=6,
      victimInitialStageRightBoundary=True,separateIndividualRecoveries=True,lastScene=ready+30,
      laterOrdinaryOrLegBranchesNotSubstituted=True,allCPUOrArenasOrKOAudioAccepted=False,fullPortAcceptance=False,scope=__doc__)
