"""Natural Sonya CPU leg contacts on both sides of an earned native round reset.

All-mode paired callbacks and every original health store are replayed, including
original mode-6 resets and mode-7 lifebar fill. Each declared full leg contact has
the unchanged authored phases/physics, actual damage and individual ready clears.
Not a waiver for interrupted/missed entries or all follow-up attacks/AI/raster.
"""
import json
import re
import struct
from pathlib import Path
import verify_current_interrupt_v1870 as launch
import verify_repeated_sonya_cpu_v1463 as paired
from verify_restart_pair import LEG_OWN,LEG_XY,LEG_GROUPS
from verify_human_special_phases_v1767 import sha

ROOT=launch.ROOT
CASE=ROOT/'audit_v1896_sonya_cpu_natural_round_repeat_human_kano'
OUT=ROOT/'audit_v1900_current_cpu_round_repeat_checked'
HEX={'actor','main','owner','action','vx','vy','gravity','flags','body','trail','schedule','at','mask','pc','a8','a13','op0','op1','op2'}
TEXT={'states','ids','assistance'}

def rows(log,tag):
    result=[]
    for line in log.splitlines():
        if not line.startswith('MK2_CPU_ROUND_'+tag+' '):continue
        values=re.findall(r'(\w+)=([^\s]+)',line)
        assert len(dict(values))==len(values),'Duplicate observed fields'
        result.append({key:value if key in TEXT else int(value,16 if key in HEX else 10)for key,value in values})
    return result

def verify_pair(log,done):
    cycle=done['cycle'];entries=[r for r in paired.rows(log,'ENTRY')if r['cycle']==cycle]
    assert len(entries)==1
    entry=entries[0];start,end=entry['frame'],done['frame']
    fields=[r for r in paired.rows(log,'FIELD')if start<r['frame']<=end]
    by={r['frame']:r for r in fields}
    assert len(fields)==len(by)==end-start and set(by)==set(range(start+1,end+1))
    for r in [entry,*fields,done]:
        assert r['writes']==0 and r['assistance']=='none' and (r['cpu_slot'],r['human_slot'])==(1,2)
        assert (r['id'],r['roster'],r['state'],r['vid'],r['vroster'],r['vstate'],r['mode'])==(18,18,0,17,17,1,2)
        assert (r['schedule'],r['stage'])==(0xfffa3780,0)
        assert r['owner']==r['actor'] and r['vowner']==r['vactor']
        assert all(r[key]==entry[key]for key in ('actor','main','vactor','vmain'))
        assert r['cycle']==cycle and r['hp']==entry['hp'] and 0<r['vhp']<=161
    assert len({entry[key]for key in ('actor','main','vactor','vmain')})==4
    events=[r for r in paired.rows(log,'EVENT')if r['cycle']==cycle and start<=r['frame']<=end]
    addresses=dict(action=0xfff80800,intro=0xfff83000,attack=0xfff83800,step=0xfff89400,
                   release=0xfff82200,damage=0xff837340,fling=0xff876650,velocity=0xff831bd0,
                   own_ready=0xff861350,victim_ready=0xff861350,own_regain=0xff861500,victim_regain=0xff861500)
    for r in events:
        own=r['kind']in ('action','intro','attack','step','own_ready','own_regain')
        assert r['kind']in addresses and r['entry']==addresses[r['kind']]
        assert r['pc']==({'intro':0xff83bb10,'attack':0xff835480}.get(r['kind'],r['entry']+16))
        assert r['a8']==entry['actor'if own else'vactor']
        assert r['a13']in ([entry['main'],entry['vmain']]if r['kind']=='damage'else[entry['main'if own else'vmain']])
        assert all(r[key]==entry[source]for key,source in (('actor','actor'),('main','main'),('victim','vactor'),('vmain','vmain')))
    def kind(name):return [r for r in events if r['kind']==name]
    for name in ('action','release','damage','fling','own_regain','victim_regain'):
        assert len(kind(name))==1,'Full native event '+name
    assert kind('action')[0]['frame']==start and kind('intro')and kind('attack')
    assert all(r['word']==3 for r in kind('intro'))and all(r['word']==115 for r in kind('attack'))
    steps=kind('step');assert len(steps)==5
    times=[r['frame']for r in steps];assert times==[times[0]+n for n in (0,30,34,38,42)]
    assert [r['group']for r in steps]==list(LEG_OWN)
    release=kind('release')[0]['frame'];assert release in (times[0]+46,times[0]+47)
    origin=by[times[0]+1];direction=-1 if origin['facing']&0x10 else 1
    for elapsed in range(46):
        r=by[times[0]+1+elapsed];phase=0 if elapsed<30 else 1+(elapsed-30)//4
        dx,dy=LEG_XY[17][phase];shake=3 if elapsed<30 and(elapsed//3)%2==0 else 0
        assert (r['pose'],r['vpose'])==(LEG_OWN[phase],LEG_GROUPS[17][phase])
        assert (r['x'],r['y'])==(origin['x'],origin['y'])
        assert (r['vxpos'],r['vypos'])==(origin['x']+direction*dx,origin['y']+dy+shake)
        assert r['vx']==r['vy']==r['vvx']==r['vvy']==0 and r['suppression']>0
        assert (r['action'],r['vaction'])==(0x110,0x111) and (r['hp'],r['vhp'])==(origin['hp'],origin['vhp'])
    damage=kind('damage')[0];assert damage['frame']==release and damage['a10']==35
    stores=[r for r in paired.rows(log,'HEALTH')if r['cycle']==cycle and start<=r['frame']<=end and r['before']!=r['after']]
    assert len(stores)==1
    h=stores[0];assert h['slot']==2 and h['pc']==0xff836700 and h['before']-h['after']==35
    assert h['a8']==entry['vactor'] and h['a13']in(entry['main'],entry['vmain'])and 0<=h['frame']-release<=1
    for r in fields:assert r['vhp']==(h['before']if r['frame']<=h['frame']else h['after'])
    assert tuple(kind('fling')[0]['a'+str(n)]for n in range(4))==(0x30000,0xfffa0000,0x8000,4)
    velocities=kind('velocity')
    assert velocities and all(r['a1']==0x01060ea0 for r in velocities),'Every velocity request targets actual P2'
    launch_calls=[r for r in velocities if release<=r['frame']<=release+1]
    assert len(launch_calls)==1 and launch_calls[0]['a0']==(-direction*0x30000)&0xffffffff
    assert all(r['a0']==0 for r in velocities if r not in launch_calls),'Only native freeze/landing zero requests outside original release'
    flight=[]
    for frame in range(release+1,end):
        r=by[frame]
        if r['vgravity']!=0x8000:break
        flight.append(r)
    assert len(flight)>8 and flight[0]['vvy']==0xfffa0000 and flight[0]['vypos']==flight[0]['vfloor']
    for a,b in zip(flight,flight[1:]):
        assert b['vvy']==(a['vvy']+0x8000)&0xffffffff and b['vyraw']==(a['vyraw']+b['vvy'])&0xffffffff
    flags=paired.flag_rows(log);handoffs=[]
    for tag,prefix,slot in (('OWN_REGAIN','',1),('VICTIM_REGAIN','v',2)):
        records=[r for r in paired.rows(log,tag)if r['cycle']==cycle];assert len(records)==1
        r=records[0];handoffs.append(r['frame']);event=kind('own_regain'if slot==1 else'victim_regain')[0]
        assert r['frame']==event['frame']and r[prefix+'action']==0
        assert r['y'if slot==1 else'vypos']==r[prefix+'floor']
        assert r[prefix+'vx']==r[prefix+'vy']==r[prefix+'gravity']==r[prefix+'trail']==0
        assert r[prefix+'flags']&0x1c==0 and r[prefix+'body']&0xc==0
        assert any(q['frame']==r['frame']for q in kind('own_ready'if slot==1 else'victim_ready'))
        actor,main=entry['actor'if slot==1 else'vactor'],entry['main'if slot==1 else'vmain']
        for field,pc,at,mask in (('body',0xff83eeb0,actor+0x160,0xc),('flags',0xff83efc0,main+0x210,0x14)):
            assert any(q['cycle']==cycle and q['slot']==slot and q['frame']==r['frame']and q['kind']==field and
                q['pc']==pc and q['at']==at and(q['actor'],q['main'],q['a8'],q['a13'])==(actor,main,actor,main)and
                q['after']==q['before']&(~mask&0xffff)for q in flags),'Real original individual ready cleanup'
    assert handoffs[0]-release in(9,10)and end==max(handoffs)+1
    return dict(cycle=cycle,start=start,release=release,complete=end,heldFields=46,pairedFields=len(fields),
                victimFlightFields=len(flight),damage=35,ownReady=handoffs[0],victimReady=handoffs[1])

def verify(log):
    guest,_,_=launch.current.expected()
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    start=(0xff9dec90-0xff800000)//8;stop=(0xff9def80-0xff800000)//8
    assert guest[start:stop]==original[start:stop],'Entire original lifebar-fill program unchanged'
    for address,words in ((0xff9dec90,(0x09c0,0xffff)),(0xff9ded80,(0x188a,)),
                          (0xff9dee00,(0x104a,)),(0xff9dee10,(0x0b4a,0xff5e)),(0xff9dee40,(0x09ca,0x00a1))):
        assert struct.unpack_from('<'+'H'*len(words),original,(address-0xff800000)//8)==words
    begins=rows(log,'BEGIN');ends=rows(log,'RESULT');assert len(begins)==len(ends)==1
    first,last=begins[0]['frame'],ends[0]['frame']
    fields=rows(log,'FIELD');by={(r['frame'],r['slot']):r for r in fields}
    assert len(fields)==len(by)==(last-first+1)*2 and set(by)=={(f,s)for f in range(first,last+1)for s in(1,2)}
    for r in [*begins,*fields,*ends]:
        assert r['writes']==0 and r['assistance']=='none'and r['ids']=='18,17'and r['schedule']==0xfffa3780 and r['stage']==0
        if 'actor'in r and r['mode']==2 and r['states']=='0,1':
            assert r['valid']==1 and 0x01000000<=r['actor']<0x01100000 and 0x01000000<=r['main']<0x01100000
            assert r['owner']==r['actor']and r['id']==(18 if r['slot']==1 else 17),'Actual live native actor/Main identity across all round phases'
    stores=rows(log,'HEALTH')
    for r in stores:
        assert r['mask']==0xffff and r['at']==(0x010602f0 if r['slot']==1 else 0x01060ec0)
        assert r['writes']==0 and r['assistance']=='none'
        ordinary=0<=r['before']<=161 and 0<=r['after']<=161
        sentinel=(r['mode']==7 and (
            (r['pc']==(0xff9dece0 if r['slot']==1 else 0xff9ded10) and (r['before'],r['after'])==(161,0xffff)) or
            (r['pc']==(0xff9def40 if r['slot']==1 else 0xff9def70) and (r['before'],r['after'])==(0xffff,4))))
        assert ordinary or sentinel,'Only original same-field mode-7 fill sentinel, never live invalid health'
        off=(r['pc']-48-0xff800000)//8
        assert off>=0 and struct.unpack_from('<HHH',guest,off)==tuple(r['op'+str(n)]for n in range(3)),'Actual original store instruction words'
        if r['before']>r['after']and r['mode']==2:assert r['pc']==0xff836700,'Only original live collision damage'
    for slot in(1,2):
        for frame in range(first,last):
            changes=[r for r in stores if(r['frame'],r['slot'])==(frame,slot)]
            hp=by[frame,slot]['hp']
            for r in changes:assert r['before']==hp;hp=r['after']
            assert by[frame+1,slot]['hp']==hp,'Every callback agrees with original ordered health stores'
    ko=[r for r in stores if r['slot']==2 and r['mode']==2 and r['before']>0 and r['after']==0]
    assert len(ko)==1
    resets=[r for r in stores if r['mode']==6 and r['after']==161 and r['pc']in(0xff825930,0xff825960)]
    assert len(resets)==2 and {r['slot']for r in resets}=={1,2}and len({r['frame']for r in resets})==1
    assert all(r['winner']==1 and r['frame']>ko[0]['frame']for r in resets)
    assert next(r for r in resets if r['slot']==2)['before']==0
    sentinel_stores=[r for r in stores if r['mode']==7 and r['after']==0xffff]
    assert len(sentinel_stores)==2 and {r['slot']for r in sentinel_stores}=={1,2}
    assert len({r['frame']for r in sentinel_stores})==1
    for slot in (1,2):
        fill=[r for r in stores if r['slot']==slot and r['mode']==7 and r['pc']==(0xff9def40 if slot==1 else 0xff9def70)]
        assert [r['after']for r in fill]==list(range(4,161,2))+[161],'Every original 4/6/.../160/161 fill value'
        origin=next(r['frame']for r in sentinel_stores if r['slot']==slot)
        assert [r['frame']for r in fill]==list(range(origin,origin+len(fill))),'Original one-field fill cadence'
        assert fill[0]['before']==0xffff and all(a['after']==b['before']for a,b in zip(fill,fill[1:]))
    complete=paired.rows(log,'COMPLETE');terminal=paired.rows(log,'RESULT')
    assert len(complete)==2 and len(terminal)==1 and terminal[0]['complete_count']==2 and terminal[0]['frame']==last==complete[-1]['frame']+30
    proofs=[verify_pair(log,done)for done in complete]
    assert proofs[0]['complete']<ko[0]['frame']<resets[0]['frame']<proofs[1]['start']
    cold=paired.rows_prefix(log,'MK2_P1CPU_SELECT_RESULT ');assert len(cold)==1
    assert cold[0]['human']=='kano'and cold[0]['human_id']==17 and cold[0]['initial_cpu']==18 and cold[0]['checks']>=30 and cold[0]['errors']==0
    return dict(passed=True,allModePairedFields=len(fields),nativeHealthStores=len(stores),pairs=proofs,
                earnedKOFrame=ko[0]['frame'],originalResetFrame=resets[0]['frame'],originalFillSentinelProven=True,
                fullCPUAccepted=False,fullPortAcceptance=False,scope=__doc__)

def report():
    pins=launch.source_pins();meta=json.loads((CASE/'result.json').read_text(encoding='utf-8-sig'))
    before=json.loads((CASE/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    build=json.loads((ROOT/launch.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    assert meta['exit_code']==0 and meta['candidate']==launch.NAME and meta['assistance']=='none'and not meta['cheats_enabled']
    assert meta['executable_sha256']==build['executable_sha256']and meta['payload_sha256']==build['payload_sha256']
    assert before==meta['input_hashes']and all(before.get(file)==wanted for file,wanted in build['input_hashes'].items())
    for file,wanted in before.items():
        assert sha(file)==wanted;pins[file]=wanted
        if Path(file).suffix in('.lua','.ps1','.json'):assert sha(CASE/'input_sources'/Path(file).name)==wanted
        if Path(file).suffix=='.lua':assert not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',Path(file).read_text())
    proof=verify((CASE/'run.log').read_text(encoding='utf-8-sig'))
    for path in CASE.rglob('*'):
        if path.is_file():pins[str(path)]=sha(path)
    launch.module_pins(pins)
    proof.update(candidate=launch.NAME,inputHashes=pins)
    return proof

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed evidence'
    try:proof=report()
    except Exception as error:proof=dict(passed=False,error=repr(error),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps({key:proof[key]for key in('passed','error','allModePairedFields','nativeHealthStores','earnedKOFrame','originalResetFrame')if key in proof}),flush=True)
    raise SystemExit(0 if proof['passed']else 1)
