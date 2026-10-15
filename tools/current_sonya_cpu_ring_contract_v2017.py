"""Naturally selected current physical P2 Sonya ring hitting P1 Kano.

Complete authored release, actual native guard/physical button branch,
single 22-point collision, all owned flight and seven impact holds, retirement,
and independent parent lock cleanup. Not all contacts, arenas, audio or goal.
"""
import re,struct
import verify_current_physical_p2_cpu_v1916 as launch
import verify_current_cpu_overlap_v1911 as original
from verify_cpu_projectile_followup_v635 import BODY,FLIGHT,IMPACT

ROOT=launch.ROOT
P=launch.original
HEX=original.HEX|set('parent victim vmain vowner vflags vbody vxraw vyraw facing loaded_main tested_flags controls'.split())
TEXT=original.TEXT
one=original.one

def rows(log,tag):
    result=[]
    for line in log.splitlines():
        if not line.startswith('MK2_RING_PAIR_'+tag+' '):continue
        pairs=re.findall(r'(\w+)=([^\s]+)',line)
        assert len(pairs)==len(dict(pairs)),'Unique actual observation keys'
        result.append({k:v if k in TEXT else int(v,16 if k in HEX else 10)for k,v in pairs})
    return result

def source(log,guest):
    base=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    windows=original.rows(log,'CODE')+rows(log,'CODE')
    expected={(0xff83ed80,0xff83f060),(0xff837d40,0xff837dc0),(0xff861350,0xff861700),
        (0xfffc3800,0xfffc5800),(0xfffc6000,0xfffc8000),(0xffffb400,0xffffb480),
        (0xfffc5c00,0xfffc6000),(0xff837900,0xff837dd0),(0xff832040,0xff8321a0)}
    assert len(windows)==len(expected)and {(r['start'],r['stop'])for r in windows}==expected
    for r in windows:
        lo,hi=((r[k]-0xff800000)//8 for k in('start','stop'))
        words=[int(v,16)for v in r['words'].split(',')]
        assert len(words)==(hi-lo)//2 and struct.pack('<'+'H'*len(words),*words)==guest[lo:hi]
        if r['start']<0xfffc0000:assert guest[lo:hi]==base[lo:hi],'Original lock/guard/input routines unchanged'
    def check(at,words):
        assert struct.unpack_from('<'+'H'*len(words),guest,(at-0xff800000)//8)==tuple(words)
    def movi(n,v):return [0x09e0+n,v&65535,v>>16&65535]
    def call(v):return [0x0d5f,v&65535,v>>16]
    def sleep(n):return movi(0,n)+call(0xff80dcc0)
    check(0xffffb400,[0x574a,0xc080,0x4800,0xfffc])
    words=[0x574a]+call(0xff8a5c20)+movi(1,4)+[0xb02d,0x1f0]+movi(0,5)+call(0xffa12530)
    for pose in BODY[18]:words+=movi(0,pose)+call(0xff838790)+sleep(3)
    words+=call(0xfffc5c00)+movi(1,0x604)+[0xb02d,0x1f0]+sleep(35)+[0xc080,0x1350,0xff86]
    check(0xfffc4800,words)
    check(0xff837d40,[0xb7a0,0x170,0xb404,0x210,0x1fe4,0xcb02,0x0320,0x0960])
    check(0xff837ae0,[0x0320,0x0960])

def verify(log,guest):
    assert not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',log,re.I)
    source(log,guest)
    roms=P.rows(log,'ROM');orders=P.expected_orders()
    assert len(roms)==6 and all(r['table']==0xfffa2c00 and r['order']==i and r['list']==0xfffa3000+i*0x180 and tuple(map(int,r['ids'].split(',')))==orders[i]for i,r in enumerate(roms))
    sel=one(P.rows_prefix(log,'MK2_P2CPU_SELECT_RESULT '),'One real physical selection')
    cold=one(P.rows_prefix(log,'MK2_P2CPU_COLD_LIVE '),'One native cold CPU fight')
    assert sel['human']==cold['human']=='kano'and sel['human_id']==cold['human_id']==17
    assert 700<sel['css']<sel['exit']<sel['live']==cold['frame']and sel['checks']>=30 and sel['errors']==0
    assert sel['initial_cpu']==cold['cpu_id']==18 and cold['stage']==0
    order=(cold['schedule']-0xfffa3000)//0x180
    assert cold['schedule']==0xfffa3000+order*0x180 and orders[order][0]==18
    for r in(sel,cold):assert r['writes']==0 and r['assistance']=='none'
    events=original.rows(log,'EVENT')
    ring=one([r for r in events if r['kind']=='ring'],'One native CPU ring choice')
    assert(ring['entry'],ring['pc'],ring['id'],ring['main_owner'])==(0xffffb400,0xffffb410,18,ring['a8'])
    start=ring['frame'];actor,main=ring['a8'],ring['a13']
    birth=one(original.rows(log,'CHILD'),'One actual native child')
    retire=one(original.rows(log,'RETIRE'),'One actual native child retirement')
    child,process=birth['a8'],birth['a13'];end=retire['frame']
    assert birth['frame']==start+15 and (birth['id'],birth['entry'],birth['pc'])==(18,0xfffc7000,0xfffc7010)
    assert birth['main_owner']==child and birth['shot_owner']==actor and retire['shot_owner']==actor
    assert(retire['a8'],retire['a13'],retire['pc'])==(child,process,0xff8b6830)
    own=one([r for r in events if r['kind']=='regain'and r['a8']==actor and r['a13']==main and start<r['frame']<end],'Original parent ready before child retirement')
    ready=own['frame'];assert ready==start+50
    assert own['action']==0 and own['flags']&0x1c==0 and own['body']&0xc==0
    assert own['vx']==own['vy']==own['gravity']==own['trail']==0 and own['yraw']>>16==own['floor']
    fields=P.rows(log,'FIELD');by={r['frame']:r for r in fields};assert len(by)==len(fields)
    last=max(ready,end)+30;assert set(range(start,last+2))<=set(by)
    initial=by[start];victim,vmain=initial['vactor'],initial['vmain']
    assert len({actor,main,victim,vmain,child,process})==6
    for at in range(start,last+2):
        r=by[at]
        assert all(r[k]==initial[k]for k in('actor','main','owner','id','roster','state','vactor','vmain','vowner','vid','vroster','vstate','mode','stage','schedule','floor','vfloor','stage_floor'))
        assert(r['id'],r['vid'],r['state'],r['vstate'],r['mode'],r['stage'])==(18,17,0,1,2,0)
        assert r['schedule']==cold['schedule']and r['owner']==actor and r['vowner']==victim
        assert r['floor']==r['stage_floor']-135 and r['vfloor']==r['stage_floor']-134
        assert r['writes']==0 and r['assistance']=='none'and(r['cpu_slot'],r['human_slot'])==(2,1)
        assert 0<r['hp']<=161 and 0<r['vhp']<=161
    hp=one([r for r in original.rows(log,'HEALTH')if r['a8']==child and r['before']!=r['after']],'One complete actual ring damage writer')
    hit=hp['frame']
    assert hp['slot']==1 and hp['at']==0x010602f0 and hp['mask']==65535
    assert(hp['before']-hp['after'],hp['a10'],hp['a13'],hp['pc'],hp['main_owner'],hp['shot_owner'])==(22,22,process,0xff836700,child,actor)
    assert end==hit+4*len(IMPACT[18])
    guard=one([r for r in rows(log,'GUARD')if r['actor']==child],'Actual guard victim Main')
    tested=one([r for r in rows(log,'TESTED')if r['actor']==child],'Actual loaded/tested guard word')
    blocks=[r for r in rows(log,'BLOCK')if r['frame']==hit and r['actor']==child]
    physical=one([r for r in blocks if r['decision']==2],'Original human controls test')
    rejected=one([r for r in blocks if r['decision']==0],'Original CLRC branch')
    assert guard['frame']==tested['frame']==hit and guard['main']==tested['main']==process
    assert(guard['owner'],guard['parent'],guard['victim'],guard['vmain'],guard['vowner'],guard['vid'])==(child,actor,victim,vmain,victim,17)
    assert tested['vmain']==tested['loaded_main']==vmain and tested['tested_flags']==tested['vflags']==guard['vflags']==1
    assert(physical['entry'],physical['pc'],physical['main'],physical['owner'],physical['process_slot'])==(0xff832040,0xff832050,vmain,victim,1)
    assert(rejected['entry'],rejected['pc'],rejected['main'],rejected['parent'])==(0xff837ae0,0xff837af0,process,actor)
    assert physical['controls']==rejected['controls']and physical['controls']&0x20,'Real active-low Block released, despite lingering flag1'
    assert not any(r['decision']==1 for r in blocks),'Not a blocked-chip throw'
    stores=[r for r in P.rows(log,'HEALTH')if start<=r['frame']<=last]
    assert len(stores)==1 and stores[0]['frame']==hit and stores[0]['before']-stores[0]['after']==22
    for at in range(start,last+1):
        for slot,key in((1,'vhp'),(2,'hp')):
            changes=[r for r in stores if(r['frame'],r['slot'])==(at,slot)];health=by[at][key]
            for r in changes:assert r['before']==health;health=r['after']
            assert by[at+1][key]==health,'Complete health ledger through post-retirement tail'
    flags=[r for r in P.flag_rows(log)if start<=r['frame']<=ready]
    for r in flags:
        offset=(r['pc']-32-0xff800000)//8
        assert offset>=0 and struct.unpack_from('<HH',guest,offset)==(r['op0'],r['op1'])
        assert r['at']==(r['actor']+0x160 if r['kind']=='body'else r['main']+(0x1f0 if r['kind']=='action'else 0x210))
    actions=[r for r in flags if r['slot']==2 and r['kind']=='action']
    assert[(r['frame'],r['before'],r['after'],r['pc'])for r in actions]==[
        (start,0x303,4,0xfffc4890),(start+15,4,0x604,0xfffc4d30),
        (ready,0x604,0,0xff83edd0),(ready,0,0,0xff83edd0),(ready,0,0x303,0xff9065d0)]
    for kind,mask,offset,setpc,clearpc in(('body',4,0x160,0xff838cf0,0xff83eeb0),('flags',0x10,0x210,0xff877d50,0xff83efc0)):
        setters=[r for r in flags if r['slot']==2 and r['kind']==kind and r['pc']==setpc]
        q=one(setters,'One new ring lock '+kind)
        assert q['frame']==start and q['before']&mask==0 and q['after']==q['before']|mask
        cleared=[r for r in flags if r['slot']==2 and r['kind']==kind and r['pc']==clearpc]
        assert len(cleared)==2 and all(r['frame']==ready and r['after']==r['before']&~mask for r in cleared)
        assert cleared[0]['before']&mask and not cleared[1]['before']&mask
    for age in range(1,51):
        r=by[start+age]
        assert r['pose']==BODY[18][min((age-1)//3,4)]and r['action']==(4 if age<=15 else 0x604)
        assert r['xraw']==ring['xraw']and r['yraw']==ring['yraw']and r['vx']==r['vy']==r['gravity']==r['trail']==0
        assert r['flags']&0x1c==0x10 and r['body']&0xc==4 and r['y']==r['floor']
    assert by[ready+1]['flags']&0x1c==0 and by[ready+1]['body']&0xc==0 and by[ready+1]['action']==0x303
    children=original.rows(log,'CHILD_FIELD')
    assert[r['frame']for r in children]==list(range(birth['frame']+1,end+1))
    groups=[r for r in events if r['kind']=='group']
    sign=-1 if by[start+1]['facing']&0x10 else 1
    travel=[r for r in groups if r['vx']==(sign*0x80000)&0xffffffff]
    bursts=[r for r in groups if r['a0']in IMPACT[18]]
    assert[r['frame']for r in travel]==list(range(start+16,hit+1,3))
    assert[r['a0']for r in travel]==[FLIGHT[18][i%len(FLIGHT[18])]for i in range(len(travel))]
    assert[r['a0']for r in bursts]==list(IMPACT[18])and[r['frame']for r in bursts]==list(range(hit,end,4))
    redraws=[r for r in groups if r not in travel and r not in bursts]
    assert len(redraws)==2 and all(r['frame']==hit and r['vx']==0 and r['a0']==travel[-1]['a0']for r in redraws)
    for i,r in enumerate(travel):assert r['xraw']==(ring['xraw']+sign*(1+i*3)*0x80000)&0xffffffff and r['yraw']==ring['yraw']
    origin=bursts[0]
    for i,r in enumerate(bursts):
        assert r['xraw']==(origin['xraw']+sign*i*4*0x20000)&0xffffffff and r['yraw']==ring['yraw']and r['vx']==(sign*0x20000)&0xffffffff
    for r in children:
        assert(r['actor'],r['main'],r['owner'],r['shot_owner'],r['id'],r['type'],r['parameter'])==(child,process,child,actor,18,81,0x80000)
        assert r['child_cycle']==ring['cycle']and r['child_serial']==1 and r['vy']==0
        if r['frame']<=hit:
            elapsed=r['frame']-birth['frame']-1
            expected=(FLIGHT[18][max(0,(elapsed-1)//3)%len(FLIGHT[18])],(ring['xraw']+sign*elapsed*0x80000)&0xffffffff,ring['yraw'],(sign*0x80000)&0xffffffff,0)
        else:
            elapsed=r['frame']-hit-1
            expected=(IMPACT[18][elapsed//4],(origin['xraw']+sign*elapsed*0x20000)&0xffffffff,ring['yraw'],(sign*0x20000)&0xffffffff,0x500)
        assert(r['pose'],r['xraw'],r['yraw'],r['vx'],r['action'])==expected,'Every complete ring flight/impact field'
    for r in groups:assert(r['a8'],r['a13'],r['main_owner'],r['shot_owner'],r['pc'])==(child,process,child,actor,0xff8387a0)
    terminal=one(original.rows(log,'RESULT'),'Complete observer result')
    assert terminal['live_children']==0 and terminal['frame']>last
    for tag in('EVENT','CHILD','CHILD_FIELD','HEALTH','RETIRE','RESULT','CODE'):
        assert all(r['writes']==0 and r['assistance']=='none'for r in original.rows(log,tag))
    return dict(passed=True,start=start,birth=birth['frame'],hit=hit,damage=22,blocked=False,
        ownReady=ready,retirement=end,lastScene=last,childFields=len(children),impactGroups=len(bursts),
        activeParentFields=ready-start,nativeLockAndActionStores=len(flags),actualPhysicalBlockReleased=True,
        allCPUAccepted=False,fullPortAcceptance=False,scope=__doc__)
