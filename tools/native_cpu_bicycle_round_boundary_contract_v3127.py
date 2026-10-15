"""Source-bound naturally selected P2 Sonya Bicycle miss on normal v1997 inputs.

Complete original61-field startup/seek/ceiling/fall/fractional-landing and
individual lock/ready checks at an independently observed round-reveal boundary. The caller binds the actual build/input/whole
native state/HP context; no legacy ordinary-pair substitution, other contacts,
arena/KO/audio/full-CPU or full-port acceptance.
"""
import re,struct
import native_cpu_mobility_capture_contract_v3036 as native
import verify_current_physical_p2_cpu_v1916 as state
from cpu_followup_contract_v1423 import BIKE_CYCLE

INTRO=(0xfe83ea40,0xfe83ea80,0xfe83eae0)
POSES=set(INTRO)|set(BIKE_CYCLE)
HEX=set('a8 a13 pc entry main_owner shot_owner action pose xraw yraw flags body vx vy gravity trail start stop'.split())|{'a'+str(n)for n in range(15)}
TEXT={'kind','words','assistance','scope'}

def overlap(log,tag):
    result=[]
    for line in log.splitlines():
        if not line.startswith('MK2_CPU_OVERLAP_'+tag+' '):continue
        pairs=re.findall(r'(\w+)=([^\s]+)',line)
        assert len({k for k,v in pairs})==len(pairs),'Unambiguous native event'
        result.append({k:v if k in TEXT else int(v,16 if k in HEX else 10)for k,v in pairs})
    return result

def verify(log,guest):
    pair=dict(accepted=False,scope='Full raw native state/HP independently checked; no ordinary paired-contact acceptance substituted')
    events=overlap(log,'EVENT')
    entries=[r for r in events if r['kind']=='bicycle']
    assert len(entries)==1,'One genuine bicycle entry in this unchanged physical run'
    entry=entries[0];start=entry['frame'];actor,main=entry['a8'],entry['a13']
    own=[r for r in events if r['frame']>start and r['a8']==actor and r['a13']==main]
    ready=next(r for r in own if r['kind']=='ready')
    regain=next(r for r in own if r['kind']=='regain')
    end=ready['frame'];assert regain['frame']==end
    assert (entry['entry'],entry['pc'],entry['id'],entry['main_owner'])==(0xfff9a400,0xfff9a410,18,actor)
    assert entry['action']==0x303 and entry['flags']&0x1c==0 and entry['body']&0x0c==0
    assert (ready['entry'],ready['pc'],ready['action'])==(0xff861350,0xff861360,0x611)
    assert (regain['entry'],regain['pc'],regain['action'])==(0xff861500,0xff861510,0)
    assert regain['main_owner']==actor and regain['flags']&0x1c==0 and regain['body']&0x0c==0
    assert regain['vx']==regain['vy']==regain['gravity']==regain['trail']==0 and regain['yraw']>>16==regain['floor']
    relevant=[r for r in own if r['frame']<=end]
    for r in [entry,*relevant]:
        assert r['id']==18 and r['main_owner']==actor and r['writes']==0 and r['assistance']=='none'
        assert r['pc']==r['entry']+16
    # These original shared routines have not been replaced by compatibility code.
    original=(state.ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for lo,hi in ((0xff876650,0xff876b60),(0xff83ed80,0xff83f060),(0xff861350,0xff861700)):
        a,b=(lo-0xff800000)//8,(hi-0xff800000)//8
        assert guest[a:b]==original[a:b],'Original physical fall/cleanup/ready unchanged'
    codes=overlap(log,'CODE')+native.rows(log,'MK2_MOBILITY_CODE')
    assert any(r['start']==0xfff9a400 and r['stop']>=0xfff9ad00 for r in codes)
    for r in codes:
        words=tuple(int(x,16)for x in r['words'].split(','))
        assert words==struct.unpack_from('<'+'H'*len(words),guest,(r['start']-0xff800000)//8),'All actual native routine words source-bound'
    fields=state.original.rows(log,'FIELD');by={r['frame']:r for r in fields}
    assert len(by)==len(fields)
    assert start not in by,'This fixture is an actual first-live round boundary, not an omitted interior callback'
    all_mode=native.ledgers.rounds.rows(log,'FIELD')
    before=[r for r in all_mode if r['frame']==start]
    assert len(before)==2 and {r['slot']for r in before}=={1,2}
    assert all(r['mode']==7 and r['states']=='1,0' and r['ids']=='17,18' for r in before),'Actual previous all-mode callback is round reveal, not a fabricated live field'
    snapshots=[r for r in native.rows(log,'MK2_MOBILITY_ENTRY_STATE')if r['frame']==start and r['move']=='bicycle']
    assert len(snapshots)==2 and {r['slot']for r in snapshots}=={1,2}
    assert set(range(start+1,end+2))<=set(by)
    baseline=by[start+1]
    for snapshot in snapshots:
        prefix=''if snapshot['slot']==2 else 'v'
        assert snapshot['mode']==2 and snapshot['hp']>0
        assert all(snapshot[k]==baseline[prefix+k]for k in('actor','main','owner','id','roster','state','hp','floor'))
    for at in range(start+1,end+2):
        r=by[at]
        assert all(r[k]==baseline[k]for k in('actor','main','owner','id','roster','state','vactor','vmain','vowner','vid','vroster','vstate','mode','stage','schedule','hp','vhp','floor','vfloor','stage_floor'))
        assert r['id']==r['roster']==18 and r['vid']==r['vroster']==17 and r['owner']==actor and r['vowner']==r['vactor']
        assert r['mode']==2 and (r['state'],r['vstate'],r['cpu_slot'],r['human_slot'])==(0,1,2,1)
        assert r['floor']==r['stage_floor']-135 and r['vfloor']==r['stage_floor']-134
        assert r['hp']>0 and r['vhp']>0 and r['writes']==0 and r['assistance']=='none'
        signed=lambda v:(v&65535)-65536 if v&32768 else v&65535
        assert (r['x'],r['y'],r['vxpos'],r['vypos'])==tuple(signed(r[k]>>16)for k in('xraw','yraw','vxraw','vyraw'))
    assert not any(start<=r['frame']<=end for r in state.original.rows(log,'HEALTH')),'Actual bicycle is a miss, not relabelled collision'
    flags=[r for r in native.rows(log,'MK2_MOBILITY_FLAG')if r['slot']==2 and start<=r['frame']<=end]
    for r in flags:
        assert (r['actor'],r['main'],r['a8'],r['a13'],r['id'],r['state'])==(actor,main,actor,main,18,0)
    actions=[r for r in flags if r['kind']=='action']
    assert [(r['frame'],r['before'],r['after'],r['pc'])for r in actions]==[
        (start,0x303,0x204,0xff877bc0),
        (start+19,0x204,0x611,0xfff9ab60),
        (end,0x611,0,0xff83edd0),(end,0,0,0xff83edd0),(end,0,0x303,0xff9065d0)]
    # Derive the recovery store from this current routine, not the older
    # pre-guard-insertion FFF9AAA0 address in legacy missed-move profiles.
    assert struct.unpack_from('<5H',guest,(0xfff9ab10-0xff800000)//8)==(0x09e0,0x0611,0,0xb00d,0x01f0)
    for kind,offset,mask,setpc,clearpc in (('body',0x160,4,0xff838cf0,0xff83eeb0),('flags',0x210,0x10,0xff877d50,0xff83efc0)):
        stores=[r for r in flags if r['kind']==kind]
        assert len(stores)==3
        assert stores[0]['frame']==start and stores[0]['pc']==setpc and stores[0]['before']&mask==0 and stores[0]['after']==stores[0]['before']|mask
        assert all(r['frame']==end and r['pc']==clearpc and r['after']==r['before']&~mask for r in stores[1:])
        assert stores[1]['before']&mask and not stores[2]['before']&mask
        assert all(r['at']==(actor if kind=='body'else main)+offset for r in stores)
    for at in range(start+1,end+1):
        r=by[at]
        assert r['action']==(0x204 if at<=start+19 else 0x611)
        assert r['flags']&0x1c==0x10 and r['body']&0x0c==4 and r['trail']==0
    first=by[start+1];sign=-1 if first['facing']&0x10 else 1
    assert first['xraw']==(entry['xraw']+sign*5*65536)&0xffffffff and first['yraw']==entry['yraw']+10*65536
    for elapsed in range(6):
        r=by[start+1+elapsed];phase=elapsed//2
        assert r['pose']==INTRO[phase] and r['xraw']==(first['xraw']+sign*phase*5*65536)&0xffffffff
        assert r['yraw']==first['yraw']+phase*10*65536 and r['vx']==r['vy']==r['gravity']==r['trail']==0
    flight=by[start+7]
    assert flight['pose']==INTRO[-1] and flight['vx']==(sign*0x40000)&0xffffffff
    assert flight['vy']==0xfffe0000 and flight['gravity']==0xffff4000
    falls=[r for r in native.rows(log,'MK2_MOBILITY_EVENT')if r['kind']=='native_fall'and r['move']=='bicycle'and r['actor']==actor and r['main']==main and start<=r['frame']<=end];assert len(falls)==1
    fall=falls[0];split=fall['frame']
    assert (fall['entry'],fall['pc'])==(0xff876660,0xff876670)
    assert tuple(fall['a'+str(i)]for i in range(4))==(13,13,0xa000,4) and fall['a6']==0xfff9dc00
    def advance(a,b,g):
        assert b['vy']==(a['vy']+g)&0xffffffff and b['yraw']==(a['yraw']+b['vy'])&0xffffffff
        assert b['xraw']==(a['xraw']+a['vx'])&0xffffffff and b['vx']==flight['vx']
    for at in range(start+8,split+2):
        r=by[at];advance(by[at-1],r,0xffff4000)
        assert r['gravity']==(0xa000 if at==split+1 else 0xffff4000)
        assert r['pose']==BIKE_CYCLE[((at-start-8)//4)%len(BIKE_CYCLE)]
    assert by[split]['stage_floor']-by[split]['y']<0xc0 and by[split+1]['stage_floor']-by[split+1]['y']>=0xc0
    base=(split-start-8)//4+2
    for at in range(split+2,end+1):
        r=by[at];advance(by[at-1],r,0xa000)
        assert r['gravity']==0xa000 and r['pose']==BIKE_CYCLE[(base+(at-split-2)//4)%len(BIKE_CYCLE)]
    last=by[end];next_y=(last['yraw']+last['vy']+last['gravity'])&0xffffffff
    assert last['y']<last['floor'] and next_y>>16>=last['floor']
    assert regain['yraw']==(last['floor']<<16)|(next_y&65535)
    assert regain['xraw']==(last['xraw']+last['vx'])&0xffffffff
    r=by[end+1]
    assert r['xraw']==regain['xraw'] and r['yraw']==regain['yraw'] and r['action']==0x303
    assert r['flags']&0x1c==0 and r['body']&0x0c==0 and r['vx']==r['vy']==r['gravity']==r['trail']==0
    return dict(passed=True,start=start,fall=split,ready=end,fields=end-start,damage=0,
        nativeActionStores=len(actions),nativeLockStores=len(flags)-len(actions),
        fractionalLandingY=regain['yraw']&65535,poses=sorted(POSES),
        originalPairAndOrdinaryAcceptanceNotSubstituted=True,subsequentPairAcceptance=False,allCPUAccepted=False,fullPortAcceptance=False,scope=__doc__)
