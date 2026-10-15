"""All three native leg releases plus the previously unaccounted ring follow-up.

Preserves the old repeated driver and its INCOMPLETE record. That record counts
all later chip/ordinary damage until a later input-loop regain, not just the
35-point leg. Proves the distinct original floor/lock cleanup and owned blocked
ring lifetime. Does not certify every later ordinary attack, pixels or audio.
"""
import json,re,struct
from pathlib import Path
import verify_current_cpu_round_trace_v1900 as round_model
from verify_cpu_projectile_followup_v635 import BODY,FLIGHT,IMPACT

ROOT=round_model.ROOT
CASE=ROOT/'audit_v1908_sonya_cpu_all_cycle_overlap_human_kano'
OUT=ROOT/'audit_v1910_current_cpu_overlap_checked'
HEX=set('entry pc a8 a13 main_owner shot_owner action pose xraw yraw flags body vx vy gravity trail at mask actor main owner parameter start stop'.split())|{'a'+str(n) for n in range(15)}
TEXT={'kind','assistance','scope','words'}

def rows(log,tag):
    result=[]
    for line in log.splitlines():
        if not line.startswith('MK2_CPU_OVERLAP_'+tag+' '):continue
        pairs=re.findall(r'(\w+)=([^\s]+)',line)
        assert len(pairs)==len(dict(pairs)),'Unique observation keys'
        result.append({k:v if k in TEXT else int(v,16 if k in HEX else 10) for k,v in pairs})
    return result

def one(records,label):
    assert len(records)==1,label
    return records[0]

def code(log,guest):
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    windows=rows(log,'CODE')
    expected={(0xff83ed80,0xff83f060),(0xff837d40,0xff837dc0),(0xff861350,0xff861700),(0xfffc4800,0xfffc5800),(0xfffc7000,0xfffc8000)}
    assert len(windows)==5 and {(r['start'],r['stop'])for r in windows}==expected
    for r in windows:
        start,stop=((r[k]-0xff800000)//8 for k in ('start','stop'))
        words=[int(w,16)for w in r['words'].split(',')]
        assert len(words)==(r['stop']-r['start'])//16
        assert struct.pack('<'+'H'*len(words),*words)==guest[start:stop],'Entire actual native code window'
        if r['start']<0xfffc0000:assert guest[start:stop]==original[start:stop],'Stock cleanup, ready and guard programs unchanged'
    def check(at,words):
        assert struct.unpack_from('<'+'H'*len(words),guest,(at-0xff800000)//8)==tuple(words),'Source-bound release code'
    def movi(n,v):return [0x09e0+n,v&0xffff,v>>16&0xffff]
    def call(v):return [0x0d5f,v&0xffff,v>>16]
    def sleep(n):return movi(0,n)+call(0xff80dcc0)
    words=[0x574a]+call(0xff8a5c20)+movi(1,4)+[0xb02d,0x1f0]+movi(0,5)+call(0xffa12530)
    for pose in BODY[18]:words+=movi(0,pose)+call(0xff838790)+sleep(3)
    words+=call(0xfffc5c00)+movi(1,0x604)+[0xb02d,0x1f0]+sleep(35)+[0xc080,0x1350,0xff86]
    check(0xfffc4800,words)
    check(0xff837d40,(0xb7a0,0x170,0xb404,0x210,0x1fe4,0xcb02,0x0320,0x0960))

def grab_cleanup(log,cycle,events):
    p=round_model.paired
    entry=one([r for r in p.rows(log,'ENTRY')if r['cycle']==cycle],'Each actual leg entry')
    start=entry['frame']
    ev=[r for r in p.rows(log,'EVENT')if r['cycle']==cycle]
    release=one([r for r in ev if r['kind']=='release'],'Native release')['frame']
    cleanup=one([r for r in events if r['cycle']==cycle and r['kind']=='cleanup' and r['a8']==entry['vactor'] and
        r['a13']==entry['vmain'] and release<r['frame']<release+30],'First original victim cleanup')
    assert cleanup['frame']==release+29 and cleanup['entry']==0xff83ed80 and cleanup['pc']==0xff83ed90
    assert cleanup['main_owner']==entry['vactor'] and cleanup['id']==17
    assert cleanup['action']==0x506 and cleanup['flags']&0x14==4 and cleanup['body']&0xc==8
    assert cleanup['vx']==cleanup['vy']==cleanup['trail']==cleanup['gravity']==0
    assert cleanup['yraw']>>16==cleanup['floor']==entry['vfloor']
    fields=[r for r in p.rows(log,'FIELD')if r['cycle']==cycle and start<r['frame']<=cleanup['frame']+1]
    by={r['frame']:r for r in fields}
    assert len(fields)==len(by)==cleanup['frame']+1-start and set(by)==set(range(start+1,cleanup['frame']+2))
    for r in [entry,*fields]:
        assert (r['id'],r['vid'],r['roster'],r['vroster'],r['state'],r['vstate'])==(18,17,18,17,0,1)
        assert r['owner']==r['actor']==entry['actor'] and r['vowner']==r['vactor']==entry['vactor']
        assert (r['main'],r['vmain'])==(entry['main'],entry['vmain'])
        assert r['floor']==r['stage_floor']-135 and r['vfloor']==r['stage_floor']-134
        assert r['writes']==0 and r['assistance']=='none' and r['hp']==entry['hp']
    steps=[r for r in ev if r['kind']=='step'];times=[r['frame']for r in steps]
    assert len(steps)==5 and [r['group']for r in steps]==list(round_model.LEG_OWN)
    assert times==[times[0]+n for n in (0,30,34,38,42)] and release==times[0]+47
    origin=by[times[0]+1];direction=-1 if origin['facing']&0x10 else 1
    for elapsed in range(46):
        r=by[times[0]+1+elapsed];phase=0 if elapsed<30 else 1+(elapsed-30)//4
        dx,dy=round_model.LEG_XY[17][phase];shake=3 if elapsed<30 and(elapsed//3)%2==0 else 0
        assert (r['pose'],r['vpose'])==(round_model.LEG_OWN[phase],round_model.LEG_GROUPS[17][phase])
        assert (r['x'],r['y'],r['vxpos'],r['vypos'])==(origin['x'],origin['y'],origin['x']+direction*dx,origin['y']+dy+shake)
        assert r['vx']==r['vy']==r['vvx']==r['vvy']==0 and r['suppression']>0
        assert (r['action'],r['vaction'])==(0x110,0x111) and (r['hp'],r['vhp'])==(origin['hp'],origin['vhp'])
    changed=[r for r in p.rows(log,'HEALTH')if r['cycle']==cycle and start<=r['frame']<=cleanup['frame'] and r['before']!=r['after']]
    h=one(changed,'Exactly leg damage before native cleanup')
    assert h['slot']==2 and h['before']-h['after']==35 and h['pc']==0xff836700 and h['frame']==release
    assert (h['a8'],h['a13'])==(entry['vactor'],entry['vmain'])
    for r in fields:assert r['vhp']==h['before']if r['frame']<=release else r['vhp']==h['after']
    fling=one([r for r in ev if r['kind']=='fling'and r['frame']==release],'One actual leg fling')
    assert tuple(fling['a'+str(n)]for n in range(4))==(0x30000,0xfffa0000,0x8000,4)
    flight=[by[f]for f in range(release+1,release+24)]
    assert all(r['vgravity']==0x8000 and r['vvx']==(-direction*0x30000)&0xffffffff for r in flight)
    assert flight[0]['vvy']==0xfffa0000 and flight[0]['vyraw']==entry['vfloor']*0x10000
    for a,b in zip(flight,flight[1:]):
        assert b['vvy']==(a['vvy']+0x8000)&0xffffffff and b['vyraw']==(a['vyraw']+b['vvy'])&0xffffffff
        assert b['vxraw']==(a['vxraw']+a['vvx'])&0xffffffff
    for f in range(release+24,cleanup['frame']+2):
        r=by[f];assert r['vypos']==r['vfloor'] and r['vvx']==r['vvy']==r['vgravity']==0
    flags=p.flag_rows(log)
    for field,pc,at,mask in (('action',0xff83edd0,entry['vmain']+0x1f0,0xffff),('body',0xff83eeb0,entry['vactor']+0x160,0xc),('flags',0xff83efc0,entry['vmain']+0x210,0x14)):
        q=one([r for r in flags if r['cycle']==cycle and r['slot']==2 and r['frame']==cleanup['frame'] and r['kind']==field and r['pc']==pc],'Actual first original cleanup store '+field)
        assert (q['at'],q['actor'],q['main'],q['a8'],q['a13'])==(at,entry['vactor'],entry['vmain'],entry['vactor'],entry['vmain'])
        assert q['after']==q['before']&(~mask&0xffff)
    clean=by[cleanup['frame']+1]
    assert clean['vaction']==0 and clean['vflags']&0x1c==0 and clean['vbody']&0xc==0 and clean['vtrail']==0
    return dict(cycle=cycle,start=start,release=release,firstOriginalVictimCleanup=cleanup['frame'],damage=35,heldFields=46,nativeFlightFields=23)

def verify(log):
    assert not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',log,re.I)
    guest,_,_=round_model.launch.current.expected();code(log,guest)
    base=round_model.verify(log) # Unchanged complete contacts and ALL-mode HP ledger.
    events=rows(log,'EVENT')
    for tag in ('EVENT','CHILD','CHILD_FIELD','HEALTH','RETIRE','RESULT','CODE'):
        assert all(r['writes']==0 and r['assistance']=='none'for r in rows(log,tag))
    entries=round_model.paired.rows(log,'ENTRY');assert [r['cycle']for r in entries]==[1,2,3]
    grabs=[grab_cleanup(log,r['cycle'],events)for r in entries]
    mid=grabs[1];pairfields={r['frame']:r for r in round_model.paired.rows(log,'FIELD')if r['cycle']==2}
    own=one([r for r in round_model.paired.rows(log,'OWN_REGAIN')if r['cycle']==2],'Actual own recovery')
    assert own['frame']==mid['release']+9 and own['action']==0 and own['flags']&0x1c==0 and own['body']&0xc==0
    ring=one([r for r in events if r['kind']=='ring'],'Unique natural ring action')
    assert ring['cycle']==2 and ring['frame']>own['frame'] and ring['entry']==0xffffb400
    start=ring['frame'];child=one(rows(log,'CHILD'),'Unique owned ring child');retire=one(rows(log,'RETIRE'),'Original child retirement')
    birth=child['frame'];end=retire['frame'];a,m=child['a8'],child['a13']
    assert (child['id'],child['entry'],child['pc'],child['main_owner'],child['shot_owner'])==(18,0xfffc7000,0xfffc7010,a,ring['a8'])
    assert len({a,m,ring['a8'],ring['a13'],pairfields[start]['vactor'],pairfields[start]['vmain']})==6
    assert birth==start+15 and retire['child_cycle']==2 and retire['child_serial']==1
    assert (retire['a8'],retire['a13'],retire['shot_owner'],retire['pc'])==(a,m,ring['a8'],0xff8b6830)
    hp=one([r for r in rows(log,'HEALTH')if r['a8']==a and r['before']!=r['after']],'Exactly one owned projectile chip store')
    hit=hp['frame'];assert hp['slot']==2 and hp['at']==0x01060ec0 and hp['mask']==0xffff
    assert (hp['before']-hp['after'],hp['a10'],hp['a13'],hp['pc'],hp['main_owner'],hp['shot_owner'])==(6,6,m,0xff836700,a,ring['a8'])
    guard=one([r for r in events if r['kind']=='guard' and r['frame']==hit and r['a8']==a],'Original guard test from child')
    assert guard['a13']==m and guard['a0']==pairfields[hit]['vactor'] and guard['pc']==0xff837d50
    assert mid['firstOriginalVictimCleanup']<hit and pairfields[hit]['vflags']&1
    assert pairfields[hit]['vaction']==0 and pairfields[hit]['vflags']&0x1c==0 and pairfields[hit]['vbody']&0xc==0
    assert end==hit+4*len(IMPACT[18]) and end==start+49
    children=rows(log,'CHILD_FIELD');assert [r['frame']for r in children]==list(range(birth+1,end+1))
    groups=[r for r in events if r['kind']=='group'];travel=[r for r in groups if r['vx']==0x80000]
    assert [r['frame']for r in travel]==list(range(start+16,hit+1,3))
    assert [r['a0']for r in travel]==list(FLIGHT[18][:len(travel)])
    bursts=[r for r in groups if r['a0']in IMPACT[18]]
    assert [r['a0']for r in bursts]==list(IMPACT[18]) and [r['frame']for r in bursts]==list(range(hit,end,4))
    redraws=[r for r in groups if r not in travel and r not in bursts]
    assert len(redraws)==2 and all(r['frame']==hit and r['vx']==0 and r['a0']==travel[-1]['a0']for r in redraws)
    for i,r in enumerate(travel):
        assert r['xraw']==ring['xraw']+(1+i*3)*0x80000 and r['yraw']==ring['yraw']
    origin=bursts[0]
    for i,r in enumerate(bursts):
        assert r['xraw']==origin['xraw']+i*4*0x20000 and r['yraw']==ring['yraw'] and r['vx']==0x20000
    for r in children:
        assert (r['actor'],r['main'],r['owner'],r['shot_owner'],r['id'],r['type'],r['parameter'])==(a,m,a,ring['a8'],18,81,0x80000)
        assert r['child_cycle']==2 and r['child_serial']==1 and r['vy']==0
        if r['frame']<=hit:
            elapsed=r['frame']-birth-1
            want=(FLIGHT[18][max(0,(elapsed-1)//3)],ring['xraw']+elapsed*0x80000,ring['yraw'],0x80000,0)
        else:
            elapsed=r['frame']-hit-1
            want=(IMPACT[18][elapsed//4],origin['xraw']+elapsed*0x20000,ring['yraw'],0x20000,0x500)
        assert (r['pose'],r['xraw'],r['yraw'],r['vx'],r['action'])==want,'Every owned ring flight/impact field'
    for r in groups:assert r['a8']==a and r['a13']==m and r['shot_owner']==ring['a8'] and r['pc']==0xff8387a0
    for age in range(1,51):
        r=pairfields[start+age]
        assert r['pose']==BODY[18][min((age-1)//3,4)] and r['action']==(4 if age<=15 else 0x604)
        assert r['xraw']==ring['xraw'] and r['yraw']==ring['yraw'] and r['vx']==r['vy']==r['gravity']==r['trail']==0
        assert r['flags']==0x10 and r['body']&0xc==4 and r['y']==r['floor']
    regained=one([r for r in events if r['kind']=='regain'and r['frame']==start+50 and r['a8']==ring['a8']],'Ring original own ready/input handoff')
    assert regained['action']==0 and regained['flags']&0x1c==0 and regained['body']&0xc==0 and regained['trail']==0
    terminal=one(rows(log,'RESULT'),'Terminal observer');assert terminal['live_children']==0 and terminal['frame']==3534
    stores=[r for r in round_model.paired.rows(log,'HEALTH')if r['cycle']==2 and r['slot']==2 and r['before']!=r['after']]
    assert [r['before']-r['after']for r in stores]==[35,6,2,2,2,2,6,20]
    incomplete=one(round_model.paired.rows(log,'INCOMPLETE'),'Original immutable diagnostic label')
    assert incomplete['cycle']==2 and sum(r['before']-r['after']for r in stores)==75
    return dict(passed=True,grabs=grabs,allModePairedFields=base['allModePairedFields'],nativeHealthStores=base['nativeHealthStores'],
        ring=dict(start=start,birth=birth,blockedContact=hit,chipDamage=6,retirement=end,ownReady=start+50,childFields=len(children),impactGroups=len(bursts)),
        legacyIncompleteExplained=dict(cycle=2,legDamage=35,totalUntilLaterInputRegain=75,laterDamage=40,
            reason='Original driver accumulates later owned ring and ordinary damage until the later FF861500 input-loop event, despite original grab cleanup at release+29.'),
        allLaterOrdinaryAttacksAccepted=False,fullCPUAccepted=False,fullPortAcceptance=False,scope=__doc__)

def report():
    pins=round_model.launch.source_pins()
    meta=json.loads((CASE/'result.json').read_text(encoding='utf-8-sig'));before=json.loads((CASE/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    build=json.loads((ROOT/round_model.launch.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    assert meta['exit_code']==0 and meta['candidate']==round_model.launch.NAME and meta['assistance']=='none' and not meta['cheats_enabled']
    assert meta['executable_sha256']==build['executable_sha256'] and meta['payload_sha256']==build['payload_sha256'] and meta['input_hashes']==before
    assert {'mk2ks_cpu_recovery_probe_v1459.lua','mk2ks_cpu_round_trace_v1894.lua','mk2ks_cpu_overlap_trace_v1906.lua'}<={Path(file).name for file in before}
    assert all(before.get(file)==value for file,value in build['input_hashes'].items())
    for file,value in before.items():
        assert round_model.sha(file)==value;pins[file]=value
        if Path(file).suffix in('.lua','.ps1','.json'):assert round_model.sha(CASE/'input_sources'/Path(file).name)==value
        if Path(file).suffix=='.lua':assert not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',Path(file).read_text())
    result=verify((CASE/'run.log').read_text(encoding='utf-8-sig'))
    for path in CASE.rglob('*'):
        if path.is_file():pins[str(path)]=round_model.sha(path)
    round_model.launch.module_pins(pins)
    result.update(candidate=round_model.launch.NAME,inputHashes=pins,gameBytesChanged=False)
    return result

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed evidence'
    try:result=report()
    except Exception as error:result=dict(passed=False,error=repr(error),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k]for k in ('passed','error','grabs','ring','legacyIncompleteExplained')if k in result}),flush=True)
    raise SystemExit(0 if result['passed']else 1)
