"""Natural CPU Bicycle contact, paired animation/vertical physics and recovery.

Bounded native CPU Sonya18 versus human Kano17. Horizontal original close-body
push during the first released fields is retained, not replaced with a guessed
constant-velocity model; complete independent push replay remains unaccepted.
"""
import struct
import native_cpu_mobility_capture_contract_v3036 as native
import native_cpu_bicycle_round_boundary_contract_v3127 as base
INTRO=base.INTRO
BIKE_CYCLE=base.BIKE_CYCLE
POSES=base.POSES
VICTIM_POSES=(0xfe8294a0,0xfe829500,0xfe829560,0xfe8295a0,0xfe829620,0xfe829680)
need=native.need

def verify(log,guest):
    events=base.overlap(log,'EVENT')
    entries=[r for r in events if r['kind']=='bicycle'];need(len(entries)==1,'One actual owned Bicycle entry')
    entry=entries[0];start=entry['frame'];actor,main=entry['a8'],entry['a13']
    own=[r for r in events if r['frame']>start and (r['a8'],r['a13'])==(actor,main)]
    regain=next(r for r in own if r['kind']=='regain');ready=regain['frame']
    land=next(r for r in own if r['kind']=='landing')['frame']
    fields=native.ledgers.pair.rows(log,'FIELD');by={r['frame']:r for r in fields}
    need(len(by)==len(fields),'No duplicated native physical callback')
    mobility=native.rows(log,'MK2_MOBILITY_EVENT')
    contact=[r for r in mobility if r['move']=='bicycle' and r['kind']=='bicycle_contact']
    need(len(contact)==1,'One real Bicycle contact branch, not unrelated ordinary damage')
    hit=contact[0]['frame'];serial=contact[0]['serial']
    victim_actor,victim_main=by[hit]['vactor'],by[hit]['vmain']
    vevents=[r for r in events if r['frame']>hit and (r['a8'],r['a13'])==(victim_actor,victim_main)]
    victim_ready=next(r for r in vevents if r['kind']=='regain');vend=victim_ready['frame']
    need(set(range(start+1,vend+2))<=set(by),'Every physical field through both individual recoveries')
    need((entry['entry'],entry['pc'],entry['id'],entry['main_owner'],entry['action'])==
         (0xfff9a400,0xfff9a410,18,actor,0x303),'Actual native CPU Sonya action, no proxy')
    original=(native.ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for lo,hi in ((0xff876650,0xff876b60),(0xff83ed80,0xff83f060),(0xff861350,0xff861700)):
        a,b=(lo-0xff800000)//8,(hi-0xff800000)//8
        need(guest[a:b]==original[a:b],'Original physical fall/cleanup/ready unchanged')
    need(struct.unpack_from('<9H',guest,(0xfff9ee00-0xff800000)//8)==(54,3,57,53,0x1a01,0x1603,0,0,1),
         'Own original 22-damage/3-block-damage Bicycle collision record')
    record=0xf3e80+17*0x40
    need(struct.unpack_from('<8I',guest,record)==(*VICTIM_POSES,1,0xff800000+record*8),'Actual owned Kano six-pose victim loop')
    donor=(native.ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    need(struct.unpack_from('<6I',donor,(0xff8292c0-0xff800000)//8)==tuple(p+0x1000000 for p in VICTIM_POSES),
         'Victim cycle is the actual original Kano Bicycle stumble sequence')
    health=[r for r in native.rows(log,'MK2_MOBILITY_HEALTH') if start<=r['frame']<=vend]
    need(len(health)==1,'One owned contact health writer before both recoveries')
    dose=health[0]
    need((dose['frame'],dose['slot'],dose['before'],dose['after'],dose['pc'],dose['a8'],dose['a13'],dose['at'],dose['mask'])==
         (hit,1,161,139,0xff836700,actor,main,0x010602f0,65535),'Exactly 22 actual HP through original owned health store')
    need(struct.unpack_from('<3H',guest,(dose['pc']-48-0xff800000)//8)==tuple(dose['op'+str(i)]for i in range(3)),
         'Contact health opcode source-bound')
    for at in range(start+1,vend+2):
        r=by[at]
        need((r['actor'],r['main'],r['owner'],r['id'],r['roster'],r['state'],r['vactor'],r['vmain'],r['vowner'],r['vid'],r['vroster'],r['vstate'],r['mode'])==
             (actor,main,actor,18,18,0,victim_actor,victim_main,victim_actor,17,17,1,2),'Every actual owner, real ID and physical role retained')
        need(r['floor']==r['stage_floor']-135 and r['vfloor']==r['stage_floor']-134 and r['schedule']==0xfffa3180 and r['stage']==0 and
             r['hp']==161 and r['vhp']==(161 if at<=hit else 139) and r['writes']==0 and r['assistance']=='none','Entire actual HP/floor/stage history')
        signed=lambda v:(v&65535)-65536 if v&32768 else v&65535
        need((r['x'],r['y'],r['vxpos'],r['vypos'])==tuple(signed(r[k]>>16)for k in ('xraw','yraw','vxraw','vyraw')),'All raw signed world coordinates agree')
    first=by[start+1];sign=-1 if first['facing']&16 else 1
    need(first['xraw']==(entry['xraw']+sign*5*65536)&0xffffffff and first['yraw']==entry['yraw']+10*65536,'First original displaced startup')
    for elapsed in range(6):
        r=by[start+1+elapsed];phase=elapsed//2
        need(r['pose']==INTRO[phase] and r['xraw']==(first['xraw']+sign*phase*5*65536)&0xffffffff and
             r['yraw']==first['yraw']+phase*10*65536 and r['vx']==r['vy']==r['gravity']==r['trail']==0,'All six original startup fields')
    flight=by[start+7]
    need(flight['pose']==INTRO[-1] and flight['vx']==(sign*0x40000)&0xffffffff and flight['vy']==0xfffe0000 and flight['gravity']==0xffff4000,'Own original rising seek initialization')
    for at in range(start+8,hit+2):
        a,r=by[at-1],by[at]
        need(r['xraw']==(a['xraw']+a['vx'])&0xffffffff and r['yraw']==(a['yraw']+a['vy']+0xffff4000)&0xffffffff,'Every original seek fixed-point position')
        if at<=hit:
            need(r['vx']==flight['vx'] and r['vy']==(a['vy']+0xffff4000)&0xffffffff and r['gravity']==0xffff4000 and
                 r['pose']==BIKE_CYCLE[((at-start-8)//4)%len(BIKE_CYCLE)],'Every original rising seek velocity and cycle pose')
    float_start=next(at for at in range(hit+2,ready)if by[at]['stage_floor']-by[at]['y']>=0xe0)
    release=float_start+15
    need(float_start-hit-1<32 and by[float_start-1]['stage_floor']-by[float_start-1]['y']<0xe0,'Original stage-ground E0 ceiling, not a changed floor or timeout')
    need(by[hit+1]['pose']==BIKE_CYCLE[3] and by[hit+1]['vpose']==VICTIM_POSES[0] and
         by[hit+1]['vx']==(sign*0x30000)&0xffffffff and by[hit+1]['vy']==0xfffd0000 and
         by[hit+1]['vvx']==by[hit+1]['vvy']==0,'First paired native ownership and original lift initialization')
    for at in range(hit+2,release+1):
        a,r=by[at-1],by[at];floating=at>=float_start
        need(r['pose']==BIKE_CYCLE[(4+(at-hit-2)//4)%len(BIKE_CYCLE)] and r['vpose']==VICTIM_POSES[(1+(at-hit-2)//4)%len(VICTIM_POSES)],
             'Every paired original four-field attacker/victim animation step')
        need(r['xraw']==(a['xraw']+a['vx'])&0xffffffff and r['yraw']==(a['yraw']+a['vy'])&0xffffffff and
             r['vxraw']==(r['xraw']+sign*48*65536)&0xffffffff and r['vyraw']==(r['yraw']-32*65536)&0xffffffff,
             'Original paired integration and +48/-32 owned victim offset')
        velocity=(sign*(0x10000 if floating else 0x30000))&0xffffffff;vertical=0x8000 if floating else 0xfffd0000
        need(r['vx']==r['vvx']==velocity and r['vy']==r['vvy']==vertical and r['gravity']==r['vgravity']==0,'Full paired lift/float velocity publication on both physical actors')
    fling=next(r for r in vevents if r['kind']=='fling')
    need(fling['frame']==release and tuple(fling['a'+str(i)]for i in range(4))==(0x40000,0xfffa0000,0xa000,5) and
         fling['main_owner']==victim_actor,'Actual owned victim release parameters after exactly sixteen float fields')
    for elapsed in range(12):
        r=by[release+1+elapsed]
        need(r['pose']==INTRO[2-elapsed//4] and r['vy']==0x8000 and r['gravity']==0 and r['yraw']==(by[release]['yraw']+(elapsed+1)*0x8000)&0xffffffff,'All twelve original reverse-intro release fields')
    own_drop=next(r for r in own if r['kind']=='fling');drop=own_drop['frame']
    need(drop==release+12 and tuple(own_drop['a'+str(i)]for i in range(4))==(0,0x20000,0x8000,0xfff),'Original own drop only after full reverse intro')
    for at in range(drop+1,land+1):
        r=by[at]
        need(r['pose']==0xfe835c80 and r['xraw']==by[drop+1]['xraw'] and r['vx']==0 and r['gravity']==0x8000,'Original stationary own falling pose')
        if at==drop+1:need(r['vy']==0x20000 and r['yraw']==own_drop['yraw'],'Unshifted native drop initialization')
        else:
            a=by[at-1];need(r['vy']==a['vy']+0x8000 and r['yraw']==a['yraw']+r['vy'],'Every original own vertical fall step')
    need(by[land]['y']<by[land]['floor'] and (by[land]['yraw']+by[land]['vy']+0x8000)>>16>=by[land]['floor'] and ready==land+4,'Native floor crossing and four-field landing')
    for at in range(land+1,ready+1):
        r=by[at];need(r['yraw']==r['floor']<<16 and r['vx']==r['vy']==r['gravity']==0,'Every own grounded landing hold')
    vland=next(at for at in range(release+2,vend)if by[at]['vgravity']==0 and by[at-1]['vgravity']==0xa000)
    for at in range(release+1,vland):
        r=by[at];need(r['vaction']==0x506 and r['vflags']&0x1c==4 and r['vbody']&12==0 and r['vgravity']==0xa000,'Entire native released victim hurt/fall state')
        if at==release+1:need(r['vvy']==0xfffa0000 and r['vyraw']==fling['yraw'],'Unshifted original victim fall initialization')
        else:
            a=by[at-1];need(r['vvy']==(a['vvy']+0xa000)&0xffffffff and r['vyraw']==(a['vyraw']+r['vvy'])&0xffffffff,'Every original victim vertical fall step')
    flags=[r for r in native.rows(log,'MK2_MOBILITY_FLAG')if r['serial']==serial and start<=r['frame']<=vend]
    for r in flags:
        need(r['owner']==r['actor'] and r['at']==(r['actor']+0x160 if r['kind']=='body'else r['main']+(0x1f0 if r['kind']=='action'else 0x210)) and
             struct.unpack_from('<2H',guest,(r['pc']-32-0xff800000)//8)==(r['op0'],r['op1']) and r['mask']==65535 and r['writes']==0 and r['assistance']=='none',
             'Every native actor/Main lock/action store source-bound')
    clear=next(r['frame']for r in flags if r['slot']==1 and r['kind']=='action'and (r['before'],r['after'])==(0x506,0))
    need(clear==vland+5 and ready<clear<vend,'Original distinct own ready, victim landing/hurt-clear and victim ready')
    for at in range(start+1,ready+1):
        r=by[at];action=0x204 if at<=hit else 0x214 if at<=land else 0x304
        need(r['action']==action and r['flags']&0x1c==16 and r['body']&12==4 and r['trail']==0,'Every own native phase lock/action')
    for at in range(hit+1,release+1):
        r=by[at];need(r['vaction']==0x215 and r['vflags']&0x1c==4 and r['vbody']&12==0 and r['vtrail']==0,'Every victim native paired phase lock/action')
    for at in range(clear+1,vend+1):
        r=by[at];need(r['vaction']==0 and r['vflags']&0x1c==r['vbody']&12==0 and r['vypos']==r['vfloor'] and r['vvx']==r['vvy']==r['vgravity']==r['vtrail']==0,'Every victim grounded hurt recovery field')
    for r in (regain,victim_ready):
        need(r['action']==0 and r['flags']&0x1c==r['body']&12==0 and r['vx']==r['vy']==r['gravity']==r['trail']==0 and r['yraw']>>16==r['floor'],'Both individual native ready events actually clean')
    need(by[ready+1]['action']==0x303 and by[ready+1]['flags']&0x1c==by[ready+1]['body']&12==0 and by[vend+1]['vaction']==0x303,'Both real control callbacks restored separately')
    return dict(passed=True,start=start,hit=hit,ready=ready,landing=land,floatStart=float_start,release=release,fall=drop,
                victimLanding=vland,victimHurtClear=clear,victimReady=vend,fields=ready-start,damage=22,
                pairedLiftFields=float_start-hit-1,pairedFloatFields=16,reverseIntroFields=12,
                separatelyRecovered=True,allCPUAccepted=False,fullHorizontalNativePushReplayAccepted=False,
                fullMovePhaseAccepted=False,fullPortAcceptance=False,scope=__doc__)
