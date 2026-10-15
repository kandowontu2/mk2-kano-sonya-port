"""Physical P2 Kano mirror: both choke releases, two owned knives and round reset.

Every native paired/child field, actual block-button test and original branch,
damage writer, individual cleanup and all-mode health transition is checked.
Original INCOMPLETE and COMPLETE labels are retained, not reclassified by
discarding knife entries. No universal CPU, collision-box, raster/audio,
campaign, ending or full-port acceptance.
"""
import json,re,struct
from pathlib import Path
import verify_current_kano_physical_p2_cpu_v1941 as launch
import verify_current_cpu_overlap_v1911 as overlap
from verify_cpu_projectile_followup_v635 import BODY,INTRO,FLIGHT,IMPACT
from verify_restart_pair import CHOKE_OWN,CHOKE_XY

ROOT=launch.ROOT;CASE=ROOT/'audit_v1957_current_kano_p2_cpu_knife_guard'
OUT=ROOT/'audit_v1961_current_kano_cpu_overlap_checked'
P=launch.original;R=overlap.round_model
HEX=overlap.HEX|set('parent victim vmain vowner vflags vbody vxraw vyraw facing loaded_main tested_flags controls'.split())
TEXT=overlap.TEXT

def rows(log,tag):
    result=[]
    for line in log.splitlines():
        if not line.startswith('MK2_KNIFE_PAIR_'+tag+' '):continue
        pairs=re.findall(r'(\w+)=([^\s]+)',line)
        assert len(pairs)==len(dict(pairs)),'Unique actual observation keys'
        result.append({k:v if k in TEXT else int(v,16 if k in HEX else 10)for k,v in pairs})
    return result

one=overlap.one

def source(log,guest):
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    windows=overlap.rows(log,'CODE')+rows(log,'CODE')
    ranges={(0xff83ed80,0xff83f060),(0xff837d40,0xff837dc0),(0xff861350,0xff861700),
        (0xfffc3800,0xfffc5800),(0xfffc6000,0xfffc8000),(0xffffb000,0xffffb080),
        (0xfffc5800,0xfffc6000),(0xff837900,0xff837dd0),(0xff832040,0xff8321a0)}
    assert len(windows)==len(ranges) and {(r['start'],r['stop'])for r in windows}==ranges
    for r in windows:
        lo,hi=((r[k]-0xff800000)//8 for k in('start','stop'))
        words=[int(w,16)for w in r['words'].split(',')]
        assert len(words)==(hi-lo)//2 and struct.pack('<'+'H'*len(words),*words)==guest[lo:hi],'Entire actual code window matches independent current guest'
        if r['start']<0xfffc0000:assert guest[lo:hi]==original[lo:hi],'Original cleanup, guard, block decision and physical input programs unchanged'
    def check(at,words):
        assert struct.unpack_from('<'+'H'*len(words),guest,(at-0xff800000)//8)==tuple(words),'Independent authored knife program'
    def movi(n,v):return [0x09e0+n,v&65535,v>>16&65535]
    def call(v):return [0x0d5f,v&65535,v>>16]
    def sleep(n):return movi(0,n)+call(0xff80dcc0)
    check(0xffffb000,[0x574a,0xc080,0x3800,0xfffc])
    words=[0x574a]+call(0xff8a5c20)+movi(1,4)+[0xb02d,0x1f0]+movi(0,5)+call(0xffa12530)
    for i,pose in enumerate(BODY[17]):
        if i==1:words+=call(0xfffc5800)
        words+=movi(0,pose)+call(0xff838790)+sleep(4 if i==7 else 3)
    words+=movi(1,0x604)+[0xb02d,0x1f0]+sleep(24)+[0xc080,0x1350,0xff86]
    check(0xfffc3800,words)
    words=movi(9,39)+call(0xff906090)+call(0xff8b6450)+movi(0,-100)+movi(1,-72)
    words+=[0x4d45]+call(0xff83cbb0)+[0x4d40]+call(0xff8093e0)+movi(1,0x700)+movi(7,0xfffc6000)
    words+=call(0xff8b5d20)+movi(1,0x80000)+[0xb220,0x250,0x0960]
    check(0xfffc5800,words)
    words=[]
    for pose in INTRO:words+=movi(0,pose)+call(0xff838790)+sleep(3)
    words+=movi(0,19)+call(0xff8b6a10)+movi(0,19)+call(0xff8b6ac0)+[0xc880,0xffb0,0xff8a]
    words+=movi(0,0x80000)+call(0xff8b68e0)+sleep(1)+movi(0,80)+movi(1,32)+call(0xff83cc20)
    words+=movi(9,39)+call(0xff838650)+movi(0,1)+call(0xff83c870)+[0xc080,0xfe80,0xff8a]
    check(0xfffc6000,words)
    check(0xff837d40,[0xb7a0,0x170,0xb404,0x210,0x1fe4,0xcb02,0x0320,0x0960])
    check(0xff837ae0,[0x0320,0x0960]);check(0xff837bd0,[0x0de0,0x0960])

def health_round(log,guest):
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    lo,hi=((at-0xff800000)//8 for at in(0xff9dec90,0xff9def80))
    assert guest[lo:hi]==original[lo:hi],'Entire stock lifebar fill unchanged'
    for address,words in((0xff9dec90,(0x09c0,0xffff)),(0xff9ded80,(0x188a,)),(0xff9dee00,(0x104a,)),(0xff9dee10,(0x0b4a,0xff5e)),(0xff9dee40,(0x09ca,0xa1))):
        assert struct.unpack_from('<'+'H'*len(words),original,(address-0xff800000)//8)==words
    begin=one(R.rows(log,'BEGIN'),'Actual round begin');end=one(R.rows(log,'RESULT'),'Actual terminal')
    first,last=begin['frame'],end['frame'];fields=R.rows(log,'FIELD');by={(r['frame'],r['slot']):r for r in fields}
    assert len(fields)==len(by)==(last-first+1)*2 and set(by)=={(f,s)for f in range(first,last+1)for s in(1,2)}
    for r in [begin,*fields,end]:
        assert r['writes']==0 and r['assistance']=='none'and r['ids']=='17,17'and r['schedule']==0xfffa3000 and r['stage']==0
        if 'actor'in r and r['mode']==2 and r['states']=='1,0':
            assert r['valid']==1 and 0x01000000<=r['actor']<0x01100000 and 0x01000000<=r['main']<0x01100000
            assert r['owner']==r['actor']and r['id']==17
    stores=R.rows(log,'HEALTH')
    for r in stores:
        assert r['mask']==65535 and r['at']==(0x010602f0 if r['slot']==1 else 0x01060ec0)
        assert r['writes']==0 and r['assistance']=='none'
        ordinary=0<=r['before']<=161 and 0<=r['after']<=161
        sentinel=r['mode']==7 and ((r['pc']==(0xff9dece0 if r['slot']==1 else 0xff9ded10)and(r['before'],r['after'])==(161,65535))or
            (r['pc']==(0xff9def40 if r['slot']==1 else 0xff9def70)and(r['before'],r['after'])==(65535,4)))
        assert ordinary or sentinel,'Only exact original mode-7 sentinel, no invalid live HP'
        offset=(r['pc']-48-0xff800000)//8
        assert offset>=0 and struct.unpack_from('<HHH',guest,offset)==tuple(r['op'+str(n)]for n in range(3)),'Actual source-bound ordered HP store'
        if r['before']>r['after']and r['mode']==2:assert r['pc']==0xff836700
    for slot in(1,2):
        for frame in range(first,last):
            hp=by[frame,slot]['hp']
            for r in [r for r in stores if(r['frame'],r['slot'])==(frame,slot)]:assert r['before']==hp;hp=r['after']
            assert by[frame+1,slot]['hp']==hp,'Every all-mode callback agrees with original ordered health stores'
    ko=one([r for r in stores if r['slot']==1 and r['mode']==2 and r['before']>0 and r['after']==0],'One earned physical human KO')
    resets=[r for r in stores if r['mode']==6 and r['after']==161 and r['pc']in(0xff825930,0xff825960)]
    assert len(resets)==2 and {r['slot']for r in resets}=={1,2}and len({r['frame']for r in resets})==1
    assert all(r['winner']==2 and r['frame']>ko['frame']for r in resets)
    assert next(r for r in resets if r['slot']==1)['before']==0
    sentinels=[r for r in stores if r['mode']==7 and r['after']==65535]
    assert len(sentinels)==2 and {r['slot']for r in sentinels}=={1,2}and len({r['frame']for r in sentinels})==1
    for slot in(1,2):
        fill=[r for r in stores if r['slot']==slot and r['mode']==7 and r['pc']==(0xff9def40 if slot==1 else 0xff9def70)]
        assert [r['after']for r in fill]==list(range(4,161,2))+[161]
        origin=next(r['frame']for r in sentinels if r['slot']==slot)
        assert [r['frame']for r in fill]==list(range(origin,origin+len(fill)))
        assert fill[0]['before']==65535 and all(a['after']==b['before']for a,b in zip(fill,fill[1:]))
    return dict(allModePairedFields=len(fields),nativeHealthStores=len(stores),earnedKOFrame=ko['frame'],originalResetFrame=resets[0]['frame'],originalFillSentinelProven=True),by

def cleanup_store(log,guest,entry,frame,slot):
    actor,main=entry['actor'],entry['main']
    for field,pc,at,mask in(('action',0xff83edd0,main+0x1f0,65535),('body',0xff83eeb0,actor+0x160,12),('flags',0xff83efc0,main+0x210,0x14)):
        candidates=[r for r in P.flag_rows(log)if r['slot']==slot and r['frame']==frame and r['kind']==field and r['pc']==pc]
        assert candidates,'Actual original individual cleanup '+field
        for q in candidates:
            assert(q['at'],q['actor'],q['main'],q['a8'],q['a13'])==(at,actor,main,actor,main)
            assert q['after']==q['before']&(~mask&65535)
            assert struct.unpack_from('<HH',guest,(q['pc']-32-0xff800000)//8)==(q['op0'],q['op1'])

def chokes(log,guest):
    proofs=[];events=overlap.rows(log,'EVENT');fields=P.rows(log,'FIELD')
    for entry in P.rows(log,'ENTRY'):
        cycle,start=entry['cycle'],entry['frame'];ev=[r for r in P.rows(log,'EVENT')if r['cycle']==cycle]
        release=one([r for r in ev if r['kind']=='release'],'Actual choke release')['frame']
        clean=one([r for r in events if r['cycle']==cycle and r['kind']=='cleanup'and r['a8']==entry['vactor']and r['a13']==entry['vmain']and release<r['frame']<=release+29],'First original victim cleanup')
        assert clean['frame']==release+29 and(clean['entry'],clean['pc'])==(0xff83ed80,0xff83ed90)
        assert clean['main_owner']==entry['vactor']and clean['id']==17 and clean['action']==0x506 and clean['flags']&0x14==4
        assert clean['vx']==clean['vy']==clean['gravity']==clean['trail']==0 and clean['yraw']==entry['vfloor']*65536
        timeline=[r for r in fields if r['cycle']==cycle and start<r['frame']<=clean['frame']+1];by={r['frame']:r for r in timeline}
        assert len(timeline)==len(by)==clean['frame']+1-start and set(by)==set(range(start+1,clean['frame']+2))
        for r in[entry,*timeline]:
            assert(r['id'],r['vid'],r['roster'],r['vroster'],r['state'],r['vstate'],r['mode'])==(17,17,17,17,0,1,2)
            assert r['owner']==r['actor']==entry['actor']and r['vowner']==r['vactor']==entry['vactor']and(r['main'],r['vmain'])==(entry['main'],entry['vmain'])
            assert r['floor']==r['vfloor']==r['stage_floor']-134 and r['hp']==entry['hp']and r['writes']==0 and r['assistance']=='none'
        addresses=dict(action=0xfff91400,intro=0xfff94000,attack=0xfff94800,release=0xfff93800,step=0xfff89400,pulse=0xfff93400,damage=0xff837340,fling=0xff876650,velocity=0xff831bd0,own_ready=0xff861350,victim_ready=0xff861350,own_regain=0xff861500,victim_regain=0xff861500)
        for q in ev:
            assert q['kind']in addresses and q['entry']==addresses[q['kind']]
            assert q['pc']=={'intro':0xff83bb10,'attack':0xff835480}.get(q['kind'],q['entry']+16)
            own=q['kind']in('action','intro','attack','step','own_ready','own_regain')
            assert(q['actor'],q['main'],q['victim'],q['vmain'])==(entry['actor'],entry['main'],entry['vactor'],entry['vmain'])
            assert q['a8']==entry['actor'if own else'vactor']
            assert q['a13']in([entry['main'],entry['vmain']]if q['kind']in('damage','pulse')else[entry['main'if own else'vmain']])
            if q['kind']=='attack':assert q['word']==101
            if q['kind']=='intro':assert q['word']==0x420
            if q['kind']=='velocity':assert q['a1']==0x010602d0
        assert len([q for q in ev if q['kind']=='action'])==1 and any(q['kind']=='intro'for q in ev)and any(q['kind']=='attack'for q in ev)
        steps=[r for r in ev if r['kind']=='step'];times=[r['frame']for r in steps]
        assert len(steps)==22 and all(times[i]-times[i-1]==(5 if i<=3 else 3)for i in range(1,22))and release in(times[-1],times[-1]+1)
        pulses=[r for r in ev if r['kind']=='pulse'];doses=[r for r in ev if r['kind']=='damage']
        assert [r['frame']for r in pulses]==[times[3]+12*i for i in range(1,5)]==[r['frame']for r in doses]
        assert all(r['a10']==8 and r['a8']==entry['vactor']and r['a13']in(entry['main'],entry['vmain'])for r in doses)
        origin=by[times[0]+1];direction=-1 if origin['facing']&16 else 1;held=0
        for i,step in enumerate(steps):
            phase=i if i<3 else(i-3)%4+3;dx,dy=CHOKE_XY[17][phase]
            assert step['group']==CHOKE_OWN[phase]and step['steps']==i+1
            for at in range(times[i]+1,(times[i+1]if i+1<len(times)else times[i]+1)+1):
                r=by[at];assert(r['pose'],r['vpose'])==(CHOKE_OWN[phase],0xfe8294a0 if phase==6 else 0xfe829500)
                assert(r['x'],r['y'],r['vxpos'],r['vypos'])==(origin['x'],origin['y'],origin['x']+direction*dx,origin['y']+dy)
                assert r['vx']==r['vy']==0 and r['action']==0x111 and r['vaction']in((0x112,0x506)if i==21 and release<=times[i]else(0x112,));held+=1
        assert held==70
        changed=[r for r in P.rows(log,'HEALTH')if r['cycle']==cycle and start<=r['frame']<=clean['frame']and r['before']!=r['after']]
        assert len(changed)==4 and [r['before']-r['after']for r in changed]==[8]*4
        assert [r['frame']for r in changed]==[r['frame']for r in doses]
        assert all(q['slot']==1 and q['pc']==0xff836700 and q['a8']==entry['vactor']and q['a13']in(entry['main'],entry['vmain'])and 0<q['after']<q['before']<=161 for q in changed)
        assert all(a['after']==b['before']for a,b in zip(changed,changed[1:]))
        hp=entry['vhp']
        for r in timeline:
            hp=entry['vhp']-sum(h['before']-h['after']for h in changed if h['frame']<r['frame'])
            assert r['vhp']==hp
        fling=one([r for r in ev if r['kind']=='fling'],'Original choke fling')
        assert fling['frame']==release and tuple(fling['a'+str(n)]for n in range(4))==(0x40000,0xfffc0000,0x8000,5)
        flight=[]
        for f in range(release+1,clean['frame']+1):
            if by[f]['vgravity']!=0x8000:break
            flight.append(by[f])
        assert len(flight)in(23,24)and flight[0]['vvy']==0xfffc0000
        assert all(q['vaction']==0x506 for q in flight)
        assert any(q['kind']=='velocity'and release<=q['frame']<=release+1 and q['a0']==direction*0x40000&0xffffffff for q in ev),'Actual original signed physical victim launch'
        for a,b in zip(flight,flight[1:]):assert b['vvy']==(a['vvy']+0x8000)&0xffffffff and b['vyraw']==(a['vyraw']+b['vvy'])&0xffffffff
        for f in range(flight[-1]['frame']+1,clean['frame']+2):
            r=by[f];assert r['vypos']==r['vfloor']and r['vvx']==r['vvy']==r['vgravity']==0
        cleanup_store(log,guest,dict(actor=entry['vactor'],main=entry['vmain']),clean['frame'],1)
        r=by[clean['frame']+1];assert r['vaction']==0 and r['vflags']&0x1c==0 and r['vbody']&12==0 and r['vtrail']==0
        own=one([r for r in P.rows(log,'OWN_REGAIN')if r['cycle']==cycle],'Own first original regain')
        assert own['frame']==release+14 and own['action']==0 and own['flags']&0x1c==0 and own['body']&12==0
        assert own['y']==own['floor']and own['vx']==own['vy']==own['gravity']==own['trail']==0
        cleanup_store(log,guest,entry,own['frame'],2)
        proofs.append(dict(cycle=cycle,start=start,release=release,firstOriginalVictimCleanup=clean['frame'],ownReady=own['frame'],heldFields=held,victimFlightFields=len(flight),damage=32))
    assert [r['cycle']for r in proofs]==[1,2]
    return proofs

def knives(log,guest):
    events=overlap.rows(log,'EVENT');actions=[r for r in events if r['kind']=='knife'];births=overlap.rows(log,'CHILD')
    assert len(actions)==len(births)==2
    allfields=rows(log,'FIELD');by={(r['frame'],r['slot']):r for r in allfields}
    assert len(allfields)==len(by)
    for r in allfields:
        assert r['id']==17 and r['owner']==r['actor']and r['floor']==r['stage_floor']-134 and r['writes']==0 and r['assistance']=='none'
    proofs=[]
    for serial,(entry,child)in enumerate(zip(actions,births),1):
        start=entry['frame'];actor,main=entry['a8'],entry['a13'];a,m=child['a8'],child['a13']
        victim=by[start+1,1];direction=-1 if by[start+1,2]['facing']&16 else 1
        # The second action executes after the original mode-7->2 change in
        # this scheduler field. Its first callback is start+1; no fabricated
        # mode-2 callback at the beginning of that transition field.
        native=one([r for r in R.rows(log,'FIELD')if r['frame']==start and r['slot']==1],'Original entry-field physical identity')
        assert(native['actor'],native['main'],native['owner'],native['id'])==(victim['actor'],victim['main'],victim['actor'],17)
        assert native['mode']==(2 if serial==1 else 7)and by[start+1,2]['actor']==actor and by[start+1,2]['main']==main
        assert(entry['entry'],entry['pc'],entry['id'],entry['main_owner'])==(0xffffb000,0xffffb010,17,actor)
        assert child['serial']==serial and child['cycle']==1 and child['frame']==start+3
        assert(child['entry'],child['pc'],child['id'],child['main_owner'],child['shot_owner'])==(0xfffc6000,0xfffc6010,17,a,actor)
        assert len({actor,main,a,m,victim['actor'],victim['main']})==6
        health=one([r for r in overlap.rows(log,'HEALTH')if r['a8']==a and r['before']!=r['after']],'One actual owned knife contact')
        hit=health['frame'];damage=22 if serial==1 else 6
        assert(health['slot'],health['at'],health['mask'],health['pc'],health['a13'],health['main_owner'],health['shot_owner'],health['a10'])==(1,0x010602f0,65535,0xff836700,m,a,actor,damage)
        assert health['before']-health['after']==damage
        guard=one([r for r in rows(log,'GUARD')if r['actor']==a],'Actual native guard entry')
        tested=one([r for r in rows(log,'TESTED')if r['actor']==a],'Actual loaded victim guard flag')
        assert guard['frame']==tested['frame']==hit and guard['vflags']==tested['tested_flags']==tested['vflags']==1
        assert guard['vowner']==guard['victim']==victim['actor']and guard['vmain']==tested['vmain']==tested['loaded_main']==victim['main']
        assert(guard['main'],guard['owner'],guard['parent'],tested['main'],tested['owner'],tested['parent'])==(m,a,actor,m,a,actor)
        button=one([r for r in rows(log,'BLOCK')if r['frame']==hit and r['actor']==a and r['decision']==2],'Actual physical human Block query')
        assert(button['entry'],button['pc'],button['main'],button['owner'],button['process_slot'])==(0xff832040,0xff832050,victim['main'],victim['actor'],1)
        pressed=bool((~button['controls']&0xffffffff)&0x80000020)
        assert pressed==(serial==2),'Guard flag alone is not an actually held Block button'
        decision=one([r for r in rows(log,'BLOCK')if r['frame']==hit and r['actor']==a and r['decision']in(0,1)],'Actual native block decision')
        assert(decision['main'],decision['owner'],decision['parent'],decision['controls'])==(m,a,actor,button['controls'])
        assert decision['decision']==int(pressed)and decision['entry']==(0xff837bd0 if pressed else 0xff837ae0)and decision['pc']==decision['entry']+16
        retire=one([r for r in overlap.rows(log,'RETIRE')if r['a8']==a],'Actual child retirement');end=retire['frame']
        assert(end,retire['a13'],retire['pc'],retire['shot_owner'],retire['child_serial'],retire['child_cycle'])==(hit+24,m,0xff8b6830,actor,serial,1)
        groups=[r for r in events if r['kind']=='group'and r['a8']==a]
        intro=[r for r in groups if r['a0']in INTRO];travel=[r for r in groups if r['a0']in FLIGHT[17]and r['vx']!=0]
        bursts=[r for r in groups if r['a0']in IMPACT[17]];redraw=[r for r in groups if r not in intro and r not in travel and r not in bursts]
        assert [r['frame']for r in intro]==list(range(start+3,start+21,3))and [r['a0']for r in intro]==list(INTRO)
        intro_x=entry['xraw']-direction*100*65536;intro_y=entry['yraw']-72*65536
        assert all((r['xraw'],r['yraw'],r['vx'])==(intro_x,intro_y,0)for r in intro)
        assert [r['frame']for r in travel]==list(range(start+22,hit+1))and [r['a0']for r in travel]==list(FLIGHT[17][:len(travel)])
        fly_x=entry['xraw']-direction*12*65536;fly_y=entry['yraw']-40*65536;vx=direction*0x80000&0xffffffff
        for i,r in enumerate(travel):assert(r['xraw'],r['yraw'],r['vx'])==(fly_x+direction*i*0x80000,fly_y,vx)
        assert len(redraw)==(2 if pressed else 0)
        for r in redraw:assert r['frame']==hit and r['a0']==travel[-1]['a0']and r['vx']==0 and(r['xraw'],r['yraw'])==(guard['vxraw'],guard['vyraw'])
        assert [r['a0']for r in bursts]==list(IMPACT[17])and [r['frame']for r in bursts]==list(range(hit,end,4))
        impact_x=guard['vxraw']-direction*34*65536;impact_y=guard['vyraw']+32*65536
        assert all((r['xraw'],r['yraw'],r['vx'],r['action'])==(impact_x,impact_y,0,0x500)for r in bursts)
        for r in groups:assert(r['a13'],r['main_owner'],r['shot_owner'],r['pc'],r['serial'],r['id'])==(m,a,actor,0xff8387a0,serial,17)
        children=[r for r in overlap.rows(log,'CHILD_FIELD')if r['actor']==a]
        assert [r['frame']for r in children]==list(range(child['frame']+1,end+1))
        for r in children:
            assert(r['main'],r['owner'],r['shot_owner'],r['id'],r['type'],r['parameter'],r['child_serial'],r['child_cycle'],r['vy'],r['body'])==(m,a,actor,17,81,0x80000,serial,1,0,2)
            age=r['frame']-start
            if age<=22:want=(INTRO[min((age-4)//3,5)],intro_x,intro_y,vx if age==22 else 0,0)
            elif r['frame']<=hit:
                elapsed=age-23;want=(FLIGHT[17][elapsed],fly_x+direction*elapsed*0x80000,fly_y,vx,0)
            else:want=(IMPACT[17][(r['frame']-hit-1)//4],impact_x,impact_y,0,0x500)
            assert(r['pose'],r['xraw'],r['yraw'],r['vx'],r['action'])==want,'Every owned knife intro, travel, impact and retirement field'
        for age in range(1,50):
            r=by[start+age,2]
            assert(r['actor'],r['main'],r['pose'],r['action'],r['flags'],r['body'])==(actor,main,BODY[17][min((age-1)//3,7)],4 if age<=25 else 0x604,0x10,entry['body']|4)
            assert(r['xraw'],r['yraw'])==(entry['xraw'],entry['yraw'])and r['vx']==r['vy']==r['gravity']==r['trail']==0
            assert r['yraw']==r['floor']*65536
        ready=one([r for r in events if r['kind']=='regain'and r['frame']==start+49 and r['a8']==actor],'Original individual knife handoff')
        assert ready['a13']==main and ready['action']==0 and ready['flags']&0x1c==0 and ready['body']&12==0
        assert ready['vx']==ready['vy']==ready['gravity']==ready['trail']==0 and ready['yraw']==ready['floor']*65536
        cleanup_store(log,guest,dict(actor=actor,main=main),start+49,2)
        r=by[start+50,2];assert r['action']==0x303 and r['flags']&0x1c==0 and r['body']&12==0 and r['vy']==r['gravity']==r['trail']==0
        proofs.append(dict(serial=serial,start=start,birth=child['frame'],contact=hit,damage=damage,actuallyBlocked=pressed,ownReady=start+49,retirement=end,childFields=len(children),bodyFields=49,impactGroups=len(bursts)))
    terminal=one(overlap.rows(log,'RESULT'),'Original terminal');assert terminal['live_children']==0
    return proofs

def verify(log,guest):
    assert not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',log,re.I)
    for parser,tags in((rows,('FIELD','GUARD','TESTED','BLOCK','RESULT','CODE')),(overlap.rows,('EVENT','CHILD','CHILD_FIELD','HEALTH','RETIRE','RESULT','CODE'))):
        for tag in tags:assert all(r['writes']==0 and r['assistance']=='none'for r in parser(log,tag))
    source(log,guest)
    for q in P.flag_rows(log):
        offset=(q['pc']-32-0xff800000)//8
        assert offset>=0 and struct.unpack_from('<HH',guest,offset)==(q['op0'],q['op1'])
        assert q['at']==q['actor']+0x160 if q['kind']=='body'else q['at']==q['main']+(0x1f0 if q['kind']=='action'else 0x210)
        assert(q['a8'],q['a13'])==(q['actor'],q['main'])and q['id']==17 and q['slot']in(1,2)
    rounds,_=health_round(log,guest);grabs=chokes(log,guest);shots=knives(log,guest)
    cold=one(P.rows_prefix(log,'MK2_P2CPU_SELECT_RESULT '),'Actual natural human selection')
    assert cold['human']=='kano'and cold['human_id']==cold['initial_cpu']==17 and cold['checks']>=30 and cold['errors']==0
    incomplete=one(P.rows(log,'INCOMPLETE'),'Original incomplete label retained');done=one(P.rows(log,'COMPLETE'),'Original complete label retained')
    assert incomplete['cycle']==1 and done['cycle']==2 and shots[0]['start']>grabs[0]['ownReady']
    assert grabs[0]['firstOriginalVictimCleanup']<shots[0]['contact']<incomplete['frame']<rounds['earnedKOFrame']<rounds['originalResetFrame']<shots[1]['start']<grabs[1]['start']
    damage=[r for r in P.rows(log,'HEALTH')if r['cycle']==1 and r['frame']<=incomplete['frame']and r['before']!=r['after']]
    assert [r['before']-r['after']for r in damage]==[8,8,8,8,22] and sum(r['before']-r['after']for r in damage)==54
    terminal=one(P.rows(log,'RESULT'),'Unchanged original exit');assert terminal['frame']==done['frame']+65
    return dict(passed=True,grabs=grabs,knives=shots,**rounds,legacyIncompleteExplained=dict(cycle=1,chokeDamage=32,laterKnifeDamage=22,diagnosticTotal=54,firstOriginalVictimCleanup=grabs[0]['firstOriginalVictimCleanup']),
        allLaterOrdinaryAttacksAccepted=False,allCPUAccepted=False,fullPortAcceptance=False,scope=__doc__)

def report():
    pins=launch.launch.source_pins();guest,_,_=launch.launch.current.expected();meta=launch.matched(CASE,pins)
    assert meta['player']=='kano'and(meta['boot_frame'],meta['confirm_age'],meta['approach'])==(960,264,'guard_until_close')
    assert {'mk2ks_cpu_recovery_probe_v1438.lua','mk2ks_physical_p2_cpu_round_trace_v1940.lua','mk2ks_physical_p2_cpu_overlap_trace_v1942.lua','mk2ks_physical_p2_cpu_knife_trace_v1955.lua'}<={Path(f).name for f in meta['input_hashes']}
    log=(CASE/'run.log').read_text(encoding='utf-8-sig');previous=ROOT/'audit_v1944_current_kano_p2_cpu_mirror_overlap/run.log'
    prefixes=('MK2_CPU_PAIR_','MK2_P2CPU_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_')
    assert [r for r in log.splitlines()if r.startswith(prefixes)]==[r for r in previous.read_text(encoding='utf-8-sig').splitlines()if r.startswith(prefixes)],'Exact unchanged physical trajectory under added read-only observers'
    pins[str(previous)]=launch.sha(previous);result=verify(log,guest);launch.launch.module_pins(pins)
    result.update(candidate=launch.launch.NAME,inputHashes=pins,gameBytesChanged=False,originalTrajectoryUnchanged=True)
    return result

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed evidence'
    try:result=report()
    except Exception as error:
        import traceback
        result=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k]for k in('passed','error','grabs','knives','allModePairedFields','nativeHealthStores','earnedKOFrame')if k in result}),flush=True)
    raise SystemExit(0 if result['passed']else 1)
