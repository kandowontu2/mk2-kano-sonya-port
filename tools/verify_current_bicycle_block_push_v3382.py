"""Both real human slots: native standing-block dispatch, waits and horizontal push.

Current3172, stage0, one actual Sonya Bicycle versus Kano per physical order.
Whole previous input/state/contact/vertical checks retained. No audio, broad
CPU/KO/arena/overlap or complete-port acceptance follows from these fixtures.
"""
import inspect
import json
import re
import struct
import traceback
from collections import defaultdict
from pathlib import Path
import verify_current_bicycle_block_v3350 as prior

ROOT=prior.ROOT;OUT=ROOT/'audit_v3383_current_bicycle_block_push_checked';need=prior.need
HEX={'actor','main','at','pc','opcode','mask','op0','before','after','value','requested'}|{'a'+str(n)for n in range(15)}
MASK=0xffffffff
EXPECTED_LOOKUPS=None

def rows(log,tag):
    result=[]
    for line in log.splitlines():
        if not line.startswith('MK2_BBPUSH_'+tag+' '):continue
        values=re.findall(r'(\w+)=([^\s]+)',line)
        need(len(values)==len(dict(values)),'Unambiguous original push trace')
        result.append({k:v if k in ('kind','assistance','fullPortAcceptance')else int(v,16 if k in HEX else 10)for k,v in values})
    return result

def source_contract(guest):
    global EXPECTED_LOOKUPS
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    # These two exact operand relocations already belong to the independently
    # assembled full port: nineteen actual IDs, not proxies or invalid table
    # overreads. All original opcodes/control flow remain bound byte-for-byte.
    native=bytearray(original)
    for operand,target in ((0xff8d4a70,0xffff8800),(0xff9060a0,0xfffe4000)):
        struct.pack_into('<I',native,(operand-0xff800000)//8,target)
    if EXPECTED_LOOKUPS is None:EXPECTED_LOOKUPS=prior.current.expected_current()[0]
    for table in (0xffff8800,0xfffe4000):
        at=(table-0xff800000)//8
        need(guest[at:at+19*4]==EXPECTED_LOOKUPS[at:at+19*4],
             'Entire actual nineteen-ID lookup equals independent whole-port assembly')
    at=(0xffff8800-0xff800000)//8;old_at=(0xff8d5340-0xff800000)//8
    need(guest[at:at+17*4]==original[old_at:old_at+17*4] and guest[at+17*4:at+19*4]==bytes(8),
         'Every original guard callback preserved; own humans use genuine common reaction')
    ranges=((0xff836040,0xff836240),(0xff8e7c30,0xff8e7c70),(0xff8e8230,0xff8e8350),
            (0xff8d4a50,0xff8d4bb0),(0xff8d4e20,0xff8d5300),(0xff8e9cf0,0xff8ea180),
            (0xff876be0,0xff876d00),(0xff83d330,0xff83d3f0),(0xff831a60,0xff831bf0),
            (0xff827c40,0xff828b10),(0xff80dcc0,0xff80de20),(0xff906090,0xff906150))
    for low,high in ranges:
        a,b=(low-0xff800000)//8,(high-0xff800000)//8
        need(guest[a:b]==native[a:b],'Original native blocked source with exactly two independently verified table relocations')
    word=lambda at:struct.unpack_from('<H',guest,(at-0xff800000)//8)[0]
    dword=lambda at:struct.unpack_from('<I',guest,(at-0xff800000)//8)[0]
    need(word(0xff8e82b0)==0x09e0 and word(0xff8e8310)==0x184b and word(0xff8e8320)==0x186a and
         word(0xff8ea110)==0x3e2a and word(0xff8ea040)==word(0xff8ea0b0)==0x4d60,
         'Actual MOVI speed/MOVK delay/MOVK cycles/two waits/DSJS loop instructions')
    index=word(0xfff9ee00+4*16)&255
    speed=dword(0xff8e82c0);delay=(word(0xff8e8310)>>5)&31;cycles=(word(0xff8e8320)>>5)&31
    handler=dword(0xff8e7c30+index*32)
    need((index,handler,speed,delay,cycles)==(1,0xff8e8230,0x20000,2,3),
         'Actual Bicycle descriptor selects original two-pixel/two-wait/three-cycle guard reaction')
    return dict(index=index,handler=handler,speed=speed,delay=delay,cycles=cycles,duration=2*delay*cycles)

def verify(log,guest,side,typed):
    native=source_contract(guest);start=typed['start'];contact=typed['contact'];last=start+180;victim=3-side
    fields=prior.rows(log,'FIELD');initial=prior.rows(log,'ENTRY_STATE')
    by={(r['frame'],r['slot']):r for r in [*initial,*fields]}
    need(len(by)==362 and set(by)=={(f,s)for f in range(start,last+1)for s in (1,2)},'Complete actual blocked physical callback set')
    owners={s:(by[start,s]['actor'],by[start,s]['main'])for s in (1,2)}
    events=rows(log,'EVENT');kinds=defaultdict(list)
    addresses={'own_entry':0xfff9a400,'guard_handler':native['handler'],'away_request':0xff876be0,
               'guard_cycle':0xff8e9fc0,'sleep':0xff80dcc0,'guard_stop':0xff8ea120,'guard_return':0xff8e9d80}
    for r in events:
        n=r['slot'];at=addresses.get(r['kind'])
        need(n in (1,2) and at is not None and r['at']==at and r['pc']==at+16 and r['mask']==65535 and
             r['opcode']==struct.unpack_from('<H',guest,(at-0xff800000)//8)[0] and
             (r['actor'],r['main'])==(r['a8'],r['a13'])==owners[n] and r['side']==side and r['writes']==0 and r['assistance']=='none',
             'Every actual guard event has its native source and physical owner')
        need(n==(side if r['kind']=='own_entry'else victim),'Guard events cannot attach to attacking human')
        kinds[r['kind']].append(r)
    need(len(kinds['own_entry'])==1 and kinds['own_entry'][0]['frame']==start,'Exact actual attacking entry')
    for kind in ('guard_handler','away_request','guard_cycle','guard_stop','guard_return'):
        need(len(kinds[kind])==1,'Exactly one actual native '+kind)
    handler=kinds['guard_handler'][0];speed=kinds['away_request'][0];cycle=kinds['guard_cycle'][0]
    stop=kinds['guard_stop'][0];returned=kinds['guard_return'][0]
    # Original linked-process order permits the scheduled victim to execute
    # later in this field or in the next field. Anchor at its actual owned
    # handler instruction, not an assumed universal one-field delay.
    first=handler['frame'];end=first+native['duration']
    need(first in (contact,contact+1) and speed['frame']==cycle['frame']==first and stop['frame']==returned['frame']==end,
         'Original causal guard dispatch and complete twelve-field stop/return timing')
    contact_line=next(i for i,line in enumerate(log.splitlines())if line.startswith('MK2_BBLOCK_EVENT ')and'kind=contact 'in line)
    handler_line=next(i for i,line in enumerate(log.splitlines())if line.startswith('MK2_BBPUSH_EVENT ')and'kind=guard_handler 'in line)
    need(contact_line<handler_line,'Actual native contact precedes scheduled owned guard reaction')
    need(handler['a7']==native['handler'] and speed['a0']==native['speed'] and speed['a6']==2 and
         (cycle['a10'],cycle['a11'],cycle['a9'])==(native['cycles'],native['delay'],11),
         'Actual source-selected reaction/speed/two-wait/three-cycle standing-block parameters')
    relevant=[r for r in events if first<=r['frame']<=end and r['kind']!='sleep']
    need([r['kind']for r in relevant]==['guard_handler','away_request','guard_cycle','guard_stop','guard_return'],
         'Exact dispatch/request/cycle/stop/return causal order')
    sleeps=[r for r in kinds['sleep']if first<=r['frame']<end]
    need(len(sleeps)==2*native['cycles'] and [r['frame']for r in sleeps]==list(range(first,end,native['delay'])) and
         all(r['a0']==r['a11']==native['delay'] and r['a10']==native['cycles']-i//2 for i,r in enumerate(sleeps)),
         'Every actual native two-field wait and three-cycle decrement')
    requests=rows(log,'REQUEST');states=rows(log,'REQUEST_STATE')
    requested={(r['frame'],r['slot']):r for r in states}
    need(len(states)==len(requested)==360 and set(requested)=={(f,s)for f in range(start+1,last+1)for s in (1,2)},
         'Every complete physical requested-velocity callback')
    for r in states:
        need((r['actor'],r['main'])==owners[r['slot']] and r['side']==side and r['writes']==0 and r['assistance']=='none',
             'Requested velocity remains attached to its actual physical human')
    stores=defaultdict(list)
    for r in requests:
        n=r['slot'];base=0x010602d0 if n==1 else 0x01060ea0;shift=r['shift']
        need(n in (1,2) and shift in (0,16) and r['at']==base+shift and r['mask']==65535 and
             r['value']<=65535 and r['pc']==0xff831be0 and r['op0']==0x8201 and
             (r['actor'],r['main'])==(r['a8'],r['a13'])==owners[n] and r['writes']==0 and r['assistance']=='none'and r['side']==side,
             'Every native physical request half-write and owner source-bound')
        need(r['after']==((r['before']&~(65535<<shift))|(r['value']<<shift))&MASK,'Exact native half-write replacement')
        stores[r['frame'],n].append(r)
    expected_stores=[(start,side),(start+6,side),(contact,side),(first,victim),(first,victim),
                     (end,victim),(typed['landing'],side),(typed['regain'],side)]
    need(len(requests)==2*len(expected_stores) and all([r['shift']for r in requests[i:i+2]]==[0,16] and
         requests[i]['frame']==requests[i+1]['frame'] and requests[i]['slot']==requests[i+1]['slot'] and
         requests[i]['after']==requests[i+1]['before']for i in range(0,len(requests),2)),
         'Every actual thirty-two-bit request includes both ordered sixteen-bit stores')
    need([(r['frame'],r['slot'])for r in requests[::2]]==expected_stores,
         'Exact native startup/seek/rebound/guard-reset/request/stop/landing/ready request writers')
    for frame in range(start+1,last):
        for n in (1,2):
            value=requested[frame,n]['requested']
            for r in stores[frame,n]:
                need(r['before']==value,'Entire ordered native requested-velocity store chain');value=r['after']
            need(requested[frame+1,n]['requested']==value,'Every requested-velocity callback matches all native stores')
    own_x=by[contact+1,side]['xraw'];victim_x=by[first,victim]['xraw']
    sign=1 if victim_x>own_x else -1
    need(own_x!=victim_x,'Distinct physical blocked reaction order')
    moving=[]
    for frame in range(contact+1,last+1):
        for n in (1,2):
            a,r=by[frame-1,n],by[frame,n]
            need(r['xraw']==(a['xraw']+a['vx'])&MASK,'Both exact blocked horizontal fixed-point integrations')
        own,v=by[frame,side],by[frame,victim]
        need(64<=abs((own['xraw']>>16)-(v['xraw']>>16))<304,
             'Captured block remains outside close and maximum body-push thresholds')
        desired=sign*native['speed']&MASK if first<frame<=end else 0
        need(v['vx']==requested[frame,victim]['requested']==desired and own['vx']==requested[frame,side]['requested']==0,
             'Every source-derived native requested/published blocked velocity')
        need(v['xraw']==(victim_x+sign*native['speed']*max(0,min(native['duration'],frame-first-1)))&MASK and own['xraw']==own_x,
             'Whole original twelve-field push distance and stationary attacking rebound')
        need(v['yraw']==v['floor']<<16 and v['vy']==v['gravity']==0 and v['action']==0x700,
             'Actual defender remains naturally grounded in standing block')
        if desired:moving.append(frame)
    need(len(moving)==native['duration'] and by[end+1,victim]['xraw']-victim_x==sign*24*65536,
         'Actual complete native twenty-four-pixel guarded pushback')
    return dict(passed=True,side=side,native=native,guardEntry=first,guardStop=end,
                actualNativeWaits=len(sleeps),horizontalPhysicalFields=2*(last-contact),
                requestedVelocityFields=len(states),sourceBoundRequestHalfStores=len(requests),
                defenderPushPixels=24,defenderGuardReturnAccepted=True,
                bothCapturedHorizontalTrajectoriesAccepted=True,allPushBranchesOrCPUOrAudioAccepted=False,fullPortAcceptance=False)

def run():
    source=inspect.getsource(prior.run)
    before="f'audit_v3347_current_bicycle_block_p{side}_kano'"
    need(source.count(before)==1,'Exactly one declared physical fixture address adaptation')
    namespace=dict(vars(prior))
    exec(compile(source.replace(before,"f'audit_v3375_current_bicycle_block_push_p{side}_kano'"),__file__+'::whole_previous_state_run','exec'),namespace)
    state=namespace['run']();need(state['passed'],'Whole previous native block/state/input proof remains required')
    guest,old,payload,ends,ranges=prior.current.expected_current();pins=dict(state['inputHashes']);cases=[]
    for side in (1,2):
        folder=ROOT/f'audit_v3375_current_bicycle_block_push_p{side}_kano';log=(folder/'run.log').read_text(encoding='utf-8-sig')
        oldlog=(ROOT/f'audit_v3347_current_bicycle_block_p{side}_kano'/'run.log').read_text(encoding='utf-8-sig')
        selected=lambda text:[line for line in text.splitlines()if line.startswith(('MK2_HSPECIAL_','MK2_BBLOCK_'))]
        need(selected(log)==selected(oldlog),'Every original human-input and native blocked state/event trajectory identical')
        observer=(folder/'input_sources/tree/mk2ks_human_bicycle_block_push_v3373.lua').read_text()
        need(observer==(ROOT/'mk2ks_human_bicycle_block_push_v3373.lua').read_text() and
             observer.count("dofile('mk2ks_human_bicycle_block_trace_v3345.lua')")==1 and not re.search(
             r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|:reset\(|set_value|clear_value',observer),
             'Entire actual additional observer read-only, no game/CPU/state/button assistance')
        cases.append(verify(log,guest,side,state['cases'][side-1]))
        pins[str(ROOT/f'audit_v3347_current_bicycle_block_p{side}_kano'/'run.log')]=prior.current.assembly.sha(ROOT/f'audit_v3347_current_bicycle_block_p{side}_kano'/'run.log')
    for file,digest in pins.items():need(prior.current.assembly.sha(file)==digest,'Actual sources/captures unchanged')
    pins[str(Path(__file__).resolve())]=prior.current.assembly.sha(__file__)
    return dict(passed=True,candidate=state['candidate'],physicalSlots=2,cases=cases,state=state,
                actualBothPhysicalSlotsNativeBlockedHorizontalAccepted=True,
                actualNativeWaits=sum(c['actualNativeWaits']for c in cases),
                horizontalPhysicalFields=sum(c['horizontalPhysicalFields']for c in cases),
                requestedVelocityFields=sum(c['requestedVelocityFields']for c in cases),
                sourceBoundRequestHalfStores=sum(c['sourceBoundRequestHalfStores']for c in cases),
                noGameOrPublicBuildChanges=True,noNewExecutableROMOrAudioCopies=True,
                allCPUOrArenasKOAudioAccepted=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Never overwrite actual native push evidence')
    try:value=run()
    except Exception as error:value=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({k:v for k,v in value.items()if k not in ('inputHashes','state')},indent=2),flush=True)
    raise SystemExit(0 if value['passed']else 1)
