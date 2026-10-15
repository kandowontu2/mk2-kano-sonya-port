"""Actual unblocked CPU Bicycle: full paired vertical/pose and recovery history.

Uses real guard, health, action and cleanup records, not fabricated contact or
victim-ready taps. Released horizontal push and direct contact instruction
observation remain separate gaps. Full port acceptance is not inferred.
"""
import copy,json,struct,traceback
from pathlib import Path
import qualify_native_selector_sonya_cpu_air_control as control
import native_cpu_bicycle_hit_contract_v3317 as original
import qualify_native_selector_existing_sonya_travel_phases_finish_boundary as boundary

ROOT,need,sha=control.ROOT,control.need,control.sha
OUT=ROOT/'audit_native_selector_sonya_cpu_air_contact_checked'
U=lambda v:v&0xffffffff
S=lambda v:v-0x100000000 if v&0x80000000 else v


def data(text):
    ledger=control.capture.previous.base.choices.native_state
    return dict(fields=ledger.original.pair.rows(text,'FIELD'),
        events=original.base.overlap(text,'EVENT'),
        flags=ledger.original.pair.flag_rows(text),
        health=ledger.rows(text,'MK2_CPU_ROUND_HEALTH'),
        choices=ledger.rows(text,'MK2_SONYA_CHOICE_EVENT'))


def gate(records,guest):
    fields=records['fields'];by={r['frame']:r for r in fields}
    need(len(by)==len(fields),'Every original physical callback unique')
    events=records['events'];entries=[r for r in events if r['kind']=='bicycle']
    choices=[r for r in records['choices'] if r['kind']=='bicycle']
    need([r['frame'] for r in entries]==[int(r['frame']) for r in choices]==[2391,2731,2806],
         'All three actual CPU choices/entries retained, including both misses')
    contacts=[r for r in records['health'] if r['slot']=='1' and int(r['before'])-int(r['after'])==22 and
              int(r['frame'])+1 in by and by[int(r['frame'])+1]['action']==0x214 and by[int(r['frame'])+1]['vaction']==0x215]
    need(len(contacts)==1,'Exactly one actual owned 22HP paired contact, not relabeled miss or ordinary damage')
    dose=contacts[0];hit=int(dose['frame']);entry=max((r for r in entries if r['frame']<hit),key=lambda r:r['frame'])
    start=entry['frame'];actor,main=entry['a8'],entry['a13'];victim_actor,victim_main=by[hit]['vactor'],by[hit]['vmain']
    need((entry['entry'],entry['pc'],entry['id'],entry['main_owner'],entry['action'])==
         (0xfff9a400,0xfff9a410,18,actor,0x303),'Actual typed CPU Sonya entry, not proxy')
    own=[r for r in events if start<r['frame'] and (r['a8'],r['a13'])==(actor,main)]
    regain=next(r for r in own if r['kind']=='regain');ready=regain['frame']
    land=next(r for r in own if r['kind']=='landing')['frame']
    victim_events=[r for r in events if hit<r['frame'] and (r['a8'],r['a13'])==(victim_actor,victim_main)]
    fling=next(r for r in victim_events if r['kind']=='fling');release=fling['frame']
    clean_event=next(r for r in victim_events if r['kind']=='cleanup');clear=clean_event['frame']
    need((start,hit,ready,clear)==(2731,2750,2805,2812) and set(range(start+1,clear+2))<=set(by),
         'Whole actually recorded contact and distinct recovery chronology')
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    boundary.adjacent_finish_operand(guest,stock)
    for lo,hi in ((0xff876650,0xff876b50),(0xff83ed80,0xff83f060),(0xff861350,0xff861700)):
        a,b=(lo-0xff800000)//8,(hi-0xff800000)//8
        need(guest[a:b]==stock[a:b],'Entire original native fall/cleanup/ready bytes')
    need(struct.unpack_from('<9H',guest,(0xfff9ee00-0xff800000)//8)==(54,3,57,53,0x1a01,0x1603,0,0,1),
         'Source typed 22-damage/3-block Bicycle collision record')
    record=0xf3e80+17*0x40
    need(struct.unpack_from('<8I',guest,record)==(*original.VICTIM_POSES,1,0xff800000+record*8),
         'Whole true Kano six-pose victim sequence and loop')
    donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    need(struct.unpack_from('<6I',donor,(0xff8292c0-0xff800000)//8)==tuple(p+0x1000000 for p in original.VICTIM_POSES),
         'All actual original Kano stumble poses, not stand-in art')
    need((int(dose['before']),int(dose['after']),dose['pc'],dose['a8'],dose['a13'],dose['at'],dose['mask'])==
         (52,30,'FF836700',f'{actor:08X}',f'{main:08X}','010602F0','FFFF'),
         'Original actor-owned health store: 52 to30, exactly22')
    need(struct.unpack_from('<3H',guest,(int(dose['pc'],16)-48-0xff800000)//8)==tuple(int(dose['op'+str(i)],16) for i in range(3)),
         'Every actual contact-health opcode source bound')
    health=[r for r in records['health'] if start<=int(r['frame'])<=clear]
    need(health==[dose],'No other health changes silently omitted before both recoveries')
    guard=[r for r in events if r['kind']=='guard' and r['frame']==hit]
    need(len(guard)==1 and (guard[0]['entry'],guard[0]['pc'],guard[0]['a8'],guard[0]['a13'],guard[0]['a0'])==
         (0xff837d40,0xff837d50,actor,main,victim_actor), 'Actual native guard and typed victim at actual damage field')
    for at in range(start+1,clear+2):
        r=by[at]
        need((r['actor'],r['main'],r['owner'],r['id'],r['roster'],r['state'],r['vactor'],r['vmain'],r['vowner'],r['vid'],r['vroster'],r['vstate'],r['mode'])==
             (actor,main,actor,18,18,0,victim_actor,victim_main,victim_actor,17,17,1,2),'All actual IDs, owner pointers and roles retained')
        need(r['floor']==r['stage_floor']-135 and r['vfloor']==r['stage_floor']-134 and r['stage']==0 and r['schedule']==0xfffa3780 and
             r['hp']==161 and r['vhp']==(52 if at<=hit else 30) and r['writes']==0 and r['assistance']=='none','Entire genuine health and native floor history')
        need((r['x'],r['y'],r['vxpos'],r['vypos'])==tuple(S(r[k])>>16 for k in ('xraw','yraw','vxraw','vyraw')),'Every signed fixed-point coordinate agrees')
    first=by[start+1];sign=-1 if first['facing']&16 else 1
    need((first['xraw'],first['yraw'])==(U(entry['xraw']+sign*5*65536),U(entry['yraw']+10*65536)), 'Original first displaced startup')
    for elapsed in range(6):
        r=by[start+1+elapsed];phase=elapsed//2
        need(r['pose']==original.INTRO[phase] and r['xraw']==U(first['xraw']+sign*phase*5*65536) and
             r['yraw']==U(first['yraw']+phase*10*65536) and r['vx']==r['vy']==r['gravity']==r['trail']==0,'Every original startup pose and fixed-point displacement')
    flight=by[start+7]
    need((flight['pose'],flight['vx'],flight['vy'],flight['gravity'])==(original.INTRO[-1],U(sign*0x40000),0xfffe0000,0xffff4000),'Original rising seek initialization')
    for at in range(start+8,hit+2):
        a,r=by[at-1],by[at]
        need(r['xraw']==U(a['xraw']+a['vx']) and r['yraw']==U(a['yraw']+a['vy']+0xffff4000),'Every original seek XY integration')
        if at<=hit:
            need(r['vx']==flight['vx'] and r['vy']==U(a['vy']+0xffff4000) and r['gravity']==0xffff4000 and
                 r['pose']==original.BIKE_CYCLE[((at-start-8)//4)%len(original.BIKE_CYCLE)],'Every seek gravity, velocity and cycle pose')
    float_start=next(at for at in range(hit+2,ready) if by[at]['stage_floor']-by[at]['y']>=0xe0)
    need(float_start-hit-1<32 and by[float_start-1]['stage_floor']-by[float_start-1]['y']<0xe0 and release==float_start+15,'Stage-ground E0 ceiling and sixteen complete floating callbacks')
    r=by[hit+1]
    need((r['pose'],r['vpose'],r['vx'],r['vy'],r['vvx'],r['vvy'])==
         (original.BIKE_CYCLE[3],original.VICTIM_POSES[0],U(sign*0x30000),0xfffd0000,0,0),'First actual paired pose and lift initialization')
    for at in range(hit+2,release+1):
        a,r=by[at-1],by[at];floating=at>=float_start
        need((r['pose'],r['vpose'])==(original.BIKE_CYCLE[(4+(at-hit-2)//4)%len(original.BIKE_CYCLE)],original.VICTIM_POSES[(1+(at-hit-2)//4)%len(original.VICTIM_POSES)]),'Every paired four-field native animation step')
        need(r['xraw']==U(a['xraw']+a['vx']) and r['yraw']==U(a['yraw']+a['vy']) and
             r['vxraw']==U(r['xraw']+sign*48*65536) and r['vyraw']==U(r['yraw']-32*65536),'Every actual paired integration and48/-32 victim offset')
        velocity=U(sign*(0x10000 if floating else 0x30000));vertical=0x8000 if floating else 0xfffd0000
        need(r['vx']==r['vvx']==velocity and r['vy']==r['vvy']==vertical and r['gravity']==r['vgravity']==0,'Both physical actors publish exact paired lift/float velocities')
    need(tuple(fling['a'+str(i)] for i in range(4))==(0x40000,0xfffa0000,0xa000,5) and fling['main_owner']==victim_actor,'True victim release through native fling')
    for elapsed in range(12):
        r=by[release+1+elapsed]
        need(r['pose']==original.INTRO[2-elapsed//4] and r['vy']==0x8000 and r['gravity']==0 and r['yraw']==U(by[release]['yraw']+(elapsed+1)*0x8000),'All twelve original reverse-intro release callbacks')
    own_drop=next(r for r in own if r['kind']=='fling');drop=own_drop['frame']
    need(drop==release+12 and tuple(own_drop['a'+str(i)] for i in range(4))==(0,0x20000,0x8000,0xfff),'Original own drop after full reverse intro')
    for at in range(drop+1,land+1):
        r=by[at]
        need(r['pose']==0xfe835c80 and r['xraw']==by[drop+1]['xraw'] and r['vx']==0 and r['gravity']==0x8000,'Entire original stationary own fall')
        if at==drop+1:need(r['vy']==0x20000 and r['yraw']==own_drop['yraw'],'Unshifted actual own fall initialization')
        else:
            a=by[at-1];need(r['vy']==a['vy']+0x8000 and r['yraw']==U(a['yraw']+r['vy']),'Every actual native own vertical fall step')
    predicted=U(by[land]['yraw']+by[land]['vy']+0x8000)
    need(by[land]['y']<by[land]['floor'] and S(predicted)>>16>=by[land]['floor'] and ready==land+4,'Actual floor crossing and four-field landing')
    floor_raw=(by[land]['floor']<<16)|(predicted&65535)
    for at in range(land+1,ready+1):
        r=by[at];need(r['yraw']==floor_raw and r['vx']==r['vy']==r['gravity']==0,'Native floor clamp retains fractional low word, not a host integer-Y overwrite')
    vland=next(at for at in range(release+2,clear) if by[at]['vgravity']==0 and by[at-1]['vgravity']==0xa000)
    for at in range(release+1,vland):
        r=by[at]
        need(r['vaction']==0x506 and r['vflags']&0x1c==4 and r['vbody']&12==0 and r['vgravity']==0xa000,'Every released native victim hurt/fall callback')
        if at==release+1:need(r['vvy']==0xfffa0000 and r['vyraw']==fling['yraw'],'Unshifted actual victim fall initialization')
        else:
            a=by[at-1];need(r['vvy']==U(a['vvy']+0xa000) and r['vyraw']==U(a['vyraw']+r['vvy']),'Every actual victim native vertical fall step')
    vpredicted=U(by[vland-1]['vyraw']+by[vland-1]['vvy']+0xa000)
    vfloor_raw=(by[vland]['vfloor']<<16)|(vpredicted&65535)
    need(S(vpredicted)>>16>=by[vland]['vfloor'] and clear==vland+5,'Original victim floor crossing and distinct five-field hurt hold')
    for at in range(vland,clear+1):
        r=by[at];need(r['vyraw']==vfloor_raw and r['vvx']==r['vvy']==r['vgravity']==0 and r['vaction']==0x506,'All victim fractional grounded hurt callbacks')
    flags=[r for r in records['flags'] if start<=r['frame']<=clear]
    for r in flags:
        need(r['at']==(r['actor']+0x160 if r['kind']=='body' else r['main']+(0x1f0 if r['kind']=='action' else 0x210)) and
             struct.unpack_from('<2H',guest,(r['pc']-32-0xff800000)//8)==(r['op0'],r['op1']) and r['writes']==0 and r['assistance']=='none','Every actual actor/Main action/lock store source exact')
    for at in range(start+1,ready+1):
        r=by[at];action=0x204 if at<=hit else 0x214 if at<=land else 0x304
        need(r['action']==action and r['flags']&0x1c==16 and r['body']&12==4 and r['trail']==0,'Entire own native phase/action/lock history')
    for at in range(hit+1,release+1):
        r=by[at];need(r['vaction']==0x215 and r['vflags']&0x1c==4 and r['vbody']&12==0 and r['vtrail']==0,'Entire true Kano paired phase/action/lock history')
    need(regain['action']==0 and regain['flags']&0x1c==regain['body']&12==0 and regain['vx']==regain['vy']==regain['gravity']==regain['trail']==0 and regain['yraw']==floor_raw,'Real Sonya native regain event clean')
    need(by[ready+1]['action']==0x303 and by[ready+1]['flags']&0x1c==by[ready+1]['body']&12==0,'Sonya real control callback restored before next actual kick')
    clearing=[r for r in flags if r['slot']==1 and r['kind']=='action' and r['before']==0x506 and r['after']==0]
    need(len(clearing)==1 and clearing[0]['frame']==clear and clearing[0]['pc']==0xff83edd0,'Actual human cleanup action store, no synthesized victim ready event')
    r=by[clear+1]
    need(r['vaction']==0 and r['vflags']&0x1c==r['vbody']&12==0 and r['vyraw']==vfloor_raw and r['vvx']==r['vvy']==r['vgravity']==r['vtrail']==0,'Human clean grounded callback independently restored')
    return dict(start=start,contactHealthStore=hit,damage=22,floatStart=float_start,release=release,ownDrop=drop,ownLanding=land,
        ownReady=ready,victimLanding=vland,victimHurtClear=clear,firstCleanHumanCallback=clear+1,fields=clear-start+1,
        actualBicycleEntries=[r['frame'] for r in entries],pairedFloatFields=16,reverseIntroFields=12,
        ownFractionalGroundY=f'{floor_raw:08X}',victimFractionalGroundY=f'{vfloor_raw:08X}',
        pairedVerticalPosesAndSeparateRecoveryAccepted=True,directContactInstructionTapAccepted=False,
        directVictimReadyTapAccepted=False,releasedHorizontalPushReplayAccepted=False,allContactsArenasAccepted=False,fullPortAcceptance=False)


def execute(state):
    need(not OUT.exists(),'Fresh immutable actual contact qualification')
    parent=control.OUT/'report.json';proof=json.loads(parent.read_text());capture=control.capture
    held=capture.NATIVE_HANDLES[capture.KEY];pins=dict(proof['inputHashes'])
    need(proof['passed'] and held['process'].poll()==0 and held['identity']==proof['actualNativeIdentity'] and all(sha(p)==h for p,h in pins.items()),'Same terminal50372 and whole accepted control/source evidence')
    records=data(capture.RAM_CASES[capture.KEY][1]);positive=gate(records,state['guest']);faults=[]
    def corrupt_field(frame,key,value):
        changed=dict(records,fields=[dict(r,**{key:value}) if r['frame']==frame else r for r in records['fields']]);return changed
    cases=[('missing_contact_callback',dict(records,fields=[r for r in records['fields'] if r['frame']!=2752]))]
    for label,frame,key,value in (
        ('true_actor_identity',2752,'id',1),('startup_pose',2734,'pose',0),('seek_gravity',2740,'gravity',0),
        ('paired_own_pose',2753,'pose',0),('paired_victim_pose',2753,'vpose',0),('paired_offset',2753,'vxraw',0),
        ('paired_lift_velocity',2753,'vvy',0),('paired_float_velocity',2762,'vx',0),('reverse_intro',2780,'pose',0),
        ('own_drop_gravity',2790,'gravity',0),('own_fractional_landing',2803,'yraw',81<<16),
        ('victim_fall_gravity',2780,'vgravity',0),('victim_hurt_hold',2809,'vaction',0),('human_recovery_lock',2813,'vflags',5)):
        cases.append((label,corrupt_field(frame,key,value)))
    dose=next(r for r in records['health'] if r['frame']=='2750')
    cases.append(('native_damage_opcode',dict(records,health=[dict(r,op0='FFFF') if r is dose else r for r in records['health']])))
    for label,bad in cases:
        try:gate(bad,state['guest'])
        except (ValueError,AssertionError,KeyError,StopIteration) as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Effective actual contact fault admitted: '+label)
    need(len(faults)==16 and gate(records,state['guest'])==positive,'All16 effective phase faults reject and full original positive restored')
    for p in (Path(__file__),parent,Path(original.__file__),Path(boundary.__file__),ROOT/'mk2/mk2-maincpu.bin',ROOT/'mk3/mk3-maincpu.bin'):
        key=str(p.resolve());digest=sha(p);need(key not in pins or pins[key]==digest,'No earlier source/current evidence altered');pins[key]=digest
    need(all(sha(p)==h for p,h in pins.items()),'Whole contact/capture/source inventory unchanged')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        actualContact=positive,effectiveFaultsRejected=faults,inputHashes=pins,requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        fullPortAcceptance=False,publicPlayableChanged=False,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n');return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual contact proof failure')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
