"""Actual ring following naturally repeated CPU legs, including mirror chip.

Preserve original body/child phases, timing, flight, impact, guard provenance,
damage, native lock stores and independent parent recovery from v2021/v1911.
This differs only in actual entry context (live after a leg, not mode7 startup),
human victim identity and observed original physical block decision. No pixel,
audio, all-CPU/KO/morph/arena or whole-port acceptance is implied.
"""
import struct
import current_sonya_cpu_ring_contract_v2021 as original
import verify_native_extended_cpu_v2946 as stream

need=stream.need

def one(rows,label):
    need(len(rows)==1,label)
    return rows[0]

def verify(log,guest,player):
    original.source(log,guest)
    events=stream.overlap.rows(log,'EVENT')
    rings=[r for r in events if r['kind']=='ring']
    if not rings:
        need(not stream.overlap.rows(log,'CHILD') and not stream.overlap.rows(log,'CHILD_FIELD') and
             not stream.overlap.rows(log,'RETIRE'),'Actual no-ring control has no unexplained child lifetime')
        return dict(reached=False,acceptedRings=[],noRingControl=True,allCPUAccepted=False,fullPortAcceptance=False)
    ring=one(rings,'One actual naturally chosen repeated ring')
    start,actor,main=ring['frame'],ring['a8'],ring['a13']
    need((ring['entry'],ring['pc'],ring['id'],ring['main_owner'])==(0xffffb400,0xffffb410,18,actor),
         'True native ring entry and physically owned parent')
    need(ring['action']==0x303 and ring['flags']&0x1c==0 and ring['body']&0xc==0,
         'Actual original ordinary parent before ring lock')
    born=one(stream.overlap.rows(log,'CHILD'),'One native ring child allocation')
    dead=one(stream.overlap.rows(log,'RETIRE'),'One actual original ring child retirement')
    birth,end,child,process=born['frame'],dead['frame'],born['a8'],born['a13']
    need(birth==start+15 and (born['id'],born['entry'],born['pc'],born['main_owner'],born['shot_owner'])==
         (18,0xfffc7000,0xfffc7010,child,actor),'Original ring child timing, identity and owned process')
    need((dead['a8'],dead['a13'],dead['shot_owner'],dead['pc'],dead['child_cycle'],dead['child_serial'])==
         (child,process,actor,0xff8b6830,ring['cycle'],ring['serial']), 'Exact observed child retires through original native routine')
    fields=stream.pair.rows(log,'FIELD');by={r['frame']:r for r in fields}
    need(len(fields)==len(by) and set(range(start+1,start+52))<=set(by),'Every original parent release and recovery callback')
    initial=by[start+1]
    victim,vmain=initial['vactor'],initial['vmain']
    need(len({actor,main,victim,vmain,child,process})==6,'Independent physical parent/victim/child owners')
    startup=[r for r in stream.rounds.rows(log,'FIELD')if r['frame']==start]
    need(len(startup)==2 and {r['slot']for r in startup}=={1,2},'Both independently observed native entry-boundary actors')
    native_mode7=start not in by
    for row in startup:
        slot=row['slot'];a,m=(victim,vmain)if slot==1 else(actor,main)
        identity=stream.pair.HUMANS[player]if slot==1 else 18
        need((row['mode'],row['states'],row['ids'],row['stage'],row['schedule'])==
             (7 if native_mode7 else 2,'1,0',f'{stream.pair.HUMANS[player]},18',0,initial['schedule']),
             'Actual original mode7-to2 boundary or already-live entry, not an omitted live callback')
        need((row['valid'],row['actor'],row['main'],row['owner'],row['id'])==(1,a,m,a,identity),
             'Original entry-boundary physical actor and Main identity')
        if native_mode7:
            need(row['hp']==161 and row['action']==0x303 and row['y']==row['floor'] and
                 row['vx']==row['vy']==row['gravity']==row['trail']==0 and
                 row['flags']&0x1c==0 and row['body']&0xc==0,
                 'Complete original mode7 lifebar/round-start boundary, no fabricated live state')
    if not native_mode7:
        need((by[start]['actor'],by[start]['main'],by[start]['owner'],by[start]['id'],by[start]['vid'])==
             (actor,main,actor,18,stream.pair.HUMANS[player]),'Already-live entry callback cannot be omitted')

    for frame in range(start+1,start+52):
        row=by[frame]
        need((row['actor'],row['main'],row['owner'],row['id'],row['roster'],row['state'],
              row['vactor'],row['vmain'],row['vowner'],row['vid'],row['vroster'],row['vstate'],
              row['mode'],row['cpu_slot'],row['human_slot'])==
             (actor,main,actor,18,18,0,victim,vmain,victim,stream.pair.HUMANS[player],stream.pair.HUMANS[player],1,2,2,1),
             'True repeated ring physical actor and victim identity throughout release')
        need(row['writes']==0 and row['assistance']=='none','Input-only observed native ring')
    ready=one([r for r in events if r['kind']=='regain' and r['a8']==actor and r['a13']==main and
               start<r['frame']<=start+50],'One independent original ring parent regain')
    need(ready['frame']==start+50 and ready['action']==0 and ready['flags']&0x1c==0 and
         ready['body']&0xc==0 and ready['vx']==ready['vy']==ready['gravity']==ready['trail']==0 and
         ready['yraw']>>16==ready['floor'], 'Original independent fifty-field ring parent recovery')
    for age in range(1,51):
        row=by[start+age]
        need(row['pose']==original.BODY[18][min((age-1)//3,4)] and row['action']==(4 if age<=15 else 0x604),
             'Every original five-pose release and subsequent parent hold')
        need(row['xraw']==ring['xraw'] and row['yraw']==ring['yraw'] and
             row['vx']==row['vy']==row['gravity']==row['trail']==0 and row['flags']&0x1c==0x10 and
             row['body']&0xc==4 and row['y']==row['floor'], 'Exact stationary original ring parent lock and grounding')
    need(by[start+51]['flags']&0x1c==0 and by[start+51]['body']&0xc==0 and by[start+51]['action']==0x303,
         'Original immediate post-ring ordinary callback without retained special lock')
    flags=[r for r in stream.pair.flag_rows(log)if r['slot']==2 and start<=r['frame']<=start+50]
    for row in flags:
        need((row['actor'],row['main'],row['a8'],row['a13'],row['id'],row['state'])==(actor,main,actor,main,18,0),
             'Ring lock/action stores belong to the same real native parent')
        at=(row['pc']-32-0xff800000)//8
        need(struct.unpack_from('<2H',guest,at)==(row['op0'],row['op1']), 'Every ring lock/action instruction source-bound')
    # The mode7-to2 entry also clears the old ordinary guard bit through the
    # untouched stock routine, before setting the special's independent lock.
    # Prove that exact extra store; do not discard unexpected native stores.
    startup_guard=[r for r in flags if r['kind']=='flags' and r['pc']==0xff9b3b40]
    need(len(startup_guard)==int(native_mode7),'Only actual mode7 ring startup has stock ordinary guard-bit clear')
    if native_mode7:
        row=startup_guard[0]
        need(row['frame']==start and row['before']==row['after']==0 and row['at']==main+0x210 and
             row['action']==0x303 and row['flags']==0,
             'Exact native pre-ring round-start guard-bit clear, no lost special flag')
        need(struct.unpack_from('<7H',guest,(0xff9b3ad0-0xff800000)//8)==
             (0xb5a4,0x210,0x0b84,1,0,0xb08d,0x210),
             'Untouched original ordinary guard-bit clear source')
    actions=[r for r in flags if r['kind']=='action']
    need([(r['frame'],r['before'],r['after'],r['pc'])for r in actions]==[
         (start,0x303,4,0xfffc4890),(start+15,4,0x604,0xfffc4d30),
         (start+50,0x604,0,0xff83edd0),(start+50,0,0,0xff83edd0),(start+50,0,0x303,0xff9065d0)],
         'Complete unchanged original ring action stores')
    for kind,mask,offset,setpc,clearpc in (('body',4,0x160,0xff838cf0,0xff83eeb0),('flags',0x10,0x210,0xff877d50,0xff83efc0)):
        stores=[r for r in flags if r['kind']==kind and r not in startup_guard]
        need(len(stores)==3 and stores[0]['frame']==start and stores[0]['pc']==setpc and
             stores[0]['before']&mask==0 and stores[0]['after']==stores[0]['before']|mask,
             'One original ring '+kind+' lock setter')
        need(all(r['frame']==start+50 and r['pc']==clearpc and r['after']==r['before']&~mask and
                 r['at']==(actor if kind=='body'else main)+offset for r in stores[1:]) and
             stores[1]['before']&mask and not stores[2]['before']&mask, 'Both original ring '+kind+' cleanup stores')
    hp=one([r for r in stream.overlap.rows(log,'HEALTH')if r['a8']==child and r['before']!=r['after']],
           'One actual owned ring collision damage store')
    hit=hp['frame']
    guard=one([r for r in original.rows(log,'GUARD')if r['actor']==child],'Original child victim Main guard read')
    tested=one([r for r in original.rows(log,'TESTED')if r['actor']==child],'Original actually tested guard word')
    need(guard['frame']==tested['frame']==hit and (guard['main'],guard['owner'],guard['parent'],guard['victim'],guard['vmain'],guard['vowner'],guard['vid'])==
         (process,child,actor,victim,vmain,victim,stream.pair.HUMANS[player]) and
         (tested['main'],tested['vmain'],tested['loaded_main'],tested['owner'],tested['parent'])==
         (process,vmain,vmain,child,actor) and tested['tested_flags']==tested['vflags']==guard['vflags']==1,
         'Exact actual victim Main, lingering/tested guard word and original child ownership')
    blocks=[r for r in original.rows(log,'BLOCK')if r['frame']==hit and r['actor']==child]
    physical=one([r for r in blocks if r['decision']==2],'Actual human physical Block test')
    decision=one([r for r in blocks if r['decision']in (0,1)],'One actual original Block result')
    blocked=decision['decision']==1;damage=6 if blocked else 22
    need((physical['entry'],physical['pc'],physical['main'],physical['owner'],physical['process_slot'])==
         (0xff832040,0xff832050,vmain,victim,1) and physical['controls']==decision['controls'] and
         bool(physical['controls']&0x20)==(not blocked), 'Original active-low physical Block branch, never flag-only relabeling')
    need(decision['entry']in ((0xff837b90,0xff837bd0)if blocked else (0xff837ae0,)) and
         decision['pc']==decision['entry']+16 and decision['main']==process and decision['owner']==child and decision['parent']==actor,
         'Source-bound original blocked or full-damage branch')
    need(hp['slot']==1 and hp['at']==0x010602f0 and hp['mask']==65535 and
         (hp['before']-hp['after'],hp['a10'],hp['a13'],hp['pc'],hp['main_owner'],hp['shot_owner'])==
         (damage,damage,process,0xff836700,child,actor), 'Original ring damage agrees with actual physical guard branch')
    need(end==hit+4*len(original.IMPACT[18]), 'Every original ring impact hold before retirement')
    children=stream.overlap.rows(log,'CHILD_FIELD')
    need([r['frame']for r in children]==list(range(birth+1,end+1)), 'Every owned ring flight/impact callback without omissions')
    groups=[r for r in events if r['kind']=='group']
    sign=-1 if by[start+1]['facing']&0x10 else 1
    travel=[r for r in groups if r['vx']==(sign*0x80000)&0xffffffff]
    bursts=[r for r in groups if r['a0']in original.IMPACT[18]]
    need([r['frame']for r in travel]==list(range(start+16,hit+1,3)) and
         [r['a0']for r in travel]==[original.FLIGHT[18][i%len(original.FLIGHT[18])]for i in range(len(travel))],
         'Every original cyclic ring flight group and three-field hold')
    need([r['a0']for r in bursts]==list(original.IMPACT[18]) and [r['frame']for r in bursts]==list(range(hit,end,4)),
         'Every original seven impact group and four-field hold')
    redraws=[r for r in groups if r not in travel and r not in bursts]
    need(len(redraws)==2 and all(r['frame']==hit and r['vx']==0 and r['a0']==travel[-1]['a0']for r in redraws),
         'Both actual native contact redraws')
    for index,row in enumerate(travel):
        need(row['xraw']==(ring['xraw']+sign*(1+index*3)*0x80000)&0xffffffff and row['yraw']==ring['yraw'],
             'Exact native ring flight fixed-point geometry')
    # Original impact alignment copies the victim's full coordinates, then
    # restores only the projectile's integer Y. Thus its incoming fractional
    # Y is replaced by the victim's fraction; parent raw Y is NOT the general
    # impact invariant. Derive the result from independent actual guard fields.
    base=(stream.ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for lo,hi in ((0xff842010,0xff8420d0),(0xff83ce60,0xff83cf50),(0xff83cc20,0xff83cd50)):
        a,b=(lo-0xff800000)//8,(hi-0xff800000)//8
        need(guest[a:b]==base[a:b],'Original full-coordinate alignment and integer offset routines unchanged')
    need(struct.unpack_from('<10H',guest,(0xff8b0060-0xff800000)//8)==
         (0xb507,0x00b0,0xa2ef,0x0d5f,0x2800,0xfffc,0x09af,0x0080,0xb0e8,0x00b0),
         'Actual native integer-Y save, source-assembled alignment call and integer-only restore')
    need(struct.unpack_from('<11H',guest,(0xfffc3250-0xff800000)//8)==
         (0x09c0,0xff96,0x09c1,0,0x0d5f,0xcc20,0xff83,0x09e0,0,2,0x0d5f),
         'Actual Sonya minus106 integer offset and original two-pixel impact velocity')
    impact_x=(guard['vxraw']-sign*106*65536)&0xffffffff
    impact_y=(guard['yraw']&0xffff0000)|(guard['vyraw']&65535)
    origin=bursts[0]
    need(origin['xraw']==impact_x and origin['yraw']==impact_y,
         'Independent native aligned impact origin including actual victim fraction')

    for index,row in enumerate(bursts):
        need(row['xraw']==(origin['xraw']+sign*index*4*0x20000)&0xffffffff and row['yraw']==impact_y and
             row['vx']==(sign*0x20000)&0xffffffff, 'Exact native impact fixed-point geometry')
    for row in children:
        need((row['actor'],row['main'],row['owner'],row['shot_owner'],row['id'],row['type'],row['parameter'],
              row['child_cycle'],row['child_serial'],row['vy'])==
             (child,process,child,actor,18,81,0x80000,ring['cycle'],ring['serial'],0), 'Every native child publication belongs to that exact lifetime')
        if row['frame']<=hit:
            elapsed=row['frame']-birth-1
            expected=(original.FLIGHT[18][max(0,(elapsed-1)//3)%len(original.FLIGHT[18])],
                      (ring['xraw']+sign*elapsed*0x80000)&0xffffffff,ring['yraw'],(sign*0x80000)&0xffffffff,0)
        else:
            elapsed=row['frame']-hit-1
            expected=(original.IMPACT[18][elapsed//4],(origin['xraw']+sign*elapsed*0x20000)&0xffffffff,
                      impact_y,(sign*0x20000)&0xffffffff,0x500)
        need((row['pose'],row['xraw'],row['yraw'],row['vx'],row['action'])==expected,
             'Every complete original ring flight/impact pose, geometry and action field')
    for row in groups:
        need((row['a8'],row['a13'],row['main_owner'],row['shot_owner'],row['pc'])==(child,process,child,actor,0xff8387a0),
             'Every source-bound child group published by its physical owner')
    terminal=one(stream.overlap.rows(log,'RESULT'),'One terminal native child inventory')
    need(terminal['live_children']==0 and terminal['frame']>max(end,start+50)+30,'Full physical observation continues after ring retirement and parent recovery')
    return dict(reached=True,acceptedRings=[dict(start=start,birth=birth,hit=hit,retirement=end,
        ownReady=start+50,blocked=blocked,damage=damage,victim=stream.pair.HUMANS[player],
        childFields=len(children),bodyFields=50,impactGroups=len(bursts),
        actualPhysicalBlockDecisionVerified=True,originalNativeLockStores=len(flags),nativeMode7EntryBoundary=native_mode7,
        sourceDerivedImpactOrigin=dict(x=impact_x,y=impact_y,victimFraction=guard['vyraw']&65535,incomingProjectileFraction=guard['yraw']&65535),
        originalBodyFlightImpactPhaseInvariantsRetained=True)],allCPUAccepted=False,
        fullRasterOrAudioAccepted=False,fullPortAcceptance=False,scope=__doc__)
