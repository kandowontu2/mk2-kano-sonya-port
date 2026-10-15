"""Current real two-human Bicycle block in both slots, not full-port acceptance.

Full independently assembled guest/corrected payload; unchanged original input
driver; every physical state/HP field; owned original collision/block/rebound
and ready instructions. Native rebound vertical physics and preserved16-bit
floor clamp, not a guessed full32-bit floor snap. No raster/audio/CPU claim.
"""
import json
import re
import struct
import sys
import traceback
from collections import defaultdict
from pathlib import Path
import verify_current_cpu_square_v3280 as current
import current_cpu_capture_contract_v3270 as snapshots
import verify_human_special_negative_v6 as negative
import native_cpu_bicycle_hit_contract_v3317 as hit

ROOT=current.ROOT;OUT=ROOT/'audit_v3349_current_bicycle_block_checked';need=current.need
HEX={'actor','main','owner','pose','xraw','yraw','vx','vy','gravity','flags','body','facing','trail','action',
     'entry','pc','opcode','mask','status','b2','at','op0','op1','op2'}|{'a'+str(i)for i in range(15)}
TEXT={'kind','assistance','fullPortAcceptance'}
MASK=0xffffffff

def rows(log,tag):
    result=[]
    for line in log.splitlines():
        if not line.startswith('MK2_BBLOCK_'+tag+' '):continue
        values=re.findall(r'(\w+)=([^\s]+)',line)
        need(len(values)==len(dict(values)),'Unambiguous native blocked fields')
        result.append({k:v if k in TEXT else int(v,16 if k in HEX or(tag=='FLAG'and k in ('before','after'))else 10)
                       for k,v in values})
    return result

def phase(log,guest,side):
    baseline=negative.verify_log(log,'bicycle',side,'block','kano')
    entry_states=rows(log,'ENTRY_STATE');events=rows(log,'EVENT');fields=rows(log,'FIELD')
    need(len(entry_states)==2 and {r['slot']for r in entry_states}=={1,2},'Both actual native entry snapshots')
    initial={r['slot']:r for r in entry_states};start=baseline['entry'];last=start+180
    by={(r['frame'],r['slot']):r for r in fields}
    need(len(fields)==len(by)==360 and set(by)=={(f,s)for f in range(start+1,last+1)for s in (1,2)},
         'Every complete180-field original blocked physical callback')
    by.update({(start,s):r for s,r in initial.items()})
    owners={s:(r['actor'],r['main'])for s,r in initial.items()}
    for r in [*entry_states,*fields]:
        ident=18 if r['slot']==side else 17
        need(r['frame']>=start and r['side']==side and r['writes']==0 and r['assistance']=='none'and
             (r['id'],r['roster'],r['state'],r['mode'])==(ident,ident,1,2) and r['owner']==r['actor'] and
             (r['actor'],r['main'])==owners[r['slot']] and r['arena']==0 and r['stage_floor']==216 and
             r['floor']==216-(135 if ident==18 else 134),'Every real selected human ID, owner, arena and native anchor')
        need(r['action']not in (0x214,0x215) and r['trail']==0,'No paired catch or persistent trail after actual block')
    addresses={'entry':0xfff9a400,'collision':0xfff9aa30,'contact':0xfff9acf0,'block_test':0xfff9ad50,
               'blocked':0xfff9b9f0,'paired':0xfff9ade0,'fling':0xff876650,'landing':0xff876420,
               'ready':0xff861350,'regain':0xff861500}
    kinds=defaultdict(list)
    for r in events:
        need(r['kind']in addresses and r['entry']==addresses[r['kind']] and r['pc']==r['entry']+16 and
             (r['a8'],r['a13'])==owners[side] and r['mask']==65535 and r['carry']==(r['status']>>30)&1 and
             r['side']==side and r['writes']==0 and r['assistance']=='none' and
             struct.unpack_from('<H',guest,(r['entry']-0xff800000)//8)[0]==r['opcode'],
             'Every actual blocked native instruction, CPU flags and physical owner source-bound')
        kinds[r['kind']].append(r)
    for kind in ('entry','contact','block_test','blocked','fling','landing','ready','regain'):
        need(len(kinds[kind])==1,'Exactly one owned native blocked '+kind)
    need(not kinds['paired'],'Native blocked branch cannot enter paired catch')
    contact=kinds['contact'][0]['frame'];fling=kinds['fling'][0];land=kinds['landing'][0]['frame'];regain=kinds['regain'][0]['frame']
    checks=kinds['collision']
    need([r['frame']for r in checks]==list(range(start+7,contact+1)) and
         [r['carry']for r in checks]==[0]*(len(checks)-1)+[1] and checks[-1]['b2']==1 and
         all(kinds[k][0]['frame']==contact and kinds[k][0]['b2']==1 for k in ('contact','block_test','blocked')),
         'Actual collision carry and nonzero original block flag reach distinct blocked branch')
    need(tuple(fling['a'+str(n)]for n in range(4))==(0,0xfffa0000,0x8000,4) and fling['frame']==contact,
         'Source-derived blocked stationary -6/half-gravity rebound parameters')
    need(struct.unpack_from('<9H',guest,(0xfff9ee00-0xff800000)//8)==(54,3,57,53,0x1a01,0x1603,0,0,1),
         'Entire actual own22hit/3block collision descriptor')
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for low,high in ((0xff876650,0xff876b40),(0xff83c870,0xff83c950),(0xff83ebd0,0xff83efc0),(0xff861350,0xff861700)):
        a,b=(low-0xff800000)//8,(high-0xff800000)//8
        need(guest[a:b]==original[a:b],'Original fling/timer/cleanup/ready routines unchanged')
    health=rows(log,'HEALTH');need(len(health)==1,'Exactly one actual blocked native health store')
    dose=health[0]
    need((dose['frame'],dose['slot'],dose['before'],dose['after'],dose['pc'],dose['a8'],dose['a13'],dose['mask'],dose['at'])==
         (contact,3-side,161,158,0xff836700,*owners[side],65535,0x01060ec0 if side==1 else 0x010602f0),
         'Exactly3actual chip damage through original attacker-owned physical health writer')
    need(struct.unpack_from('<3H',guest,(dose['pc']-48-0xff800000)//8)==tuple(dose['op'+str(n)]for n in range(3)),
         'Blocked health opcode source-bound')
    flags=rows(log,'FLAG');stores=defaultdict(list)
    for r in flags:
        need(r['kind']in ('action','body','flags') and (r['actor'],r['main'])==owners[r['slot']] and
             r['at']==(r['actor']+0x160 if r['kind']=='body'else r['main']+(0x1f0 if r['kind']=='action'else 0x210)),
             'Each blocked state writer targets its actual owned field')
        need(r['mask']==65535 and r['writes']==0 and r['assistance']=='none' and
             struct.unpack_from('<2H',guest,(r['pc']-32-0xff800000)//8)==(r['op0'],r['op1']),
             'Every blocked state store source-bound')
        stores[r['frame'],r['slot'],r['kind']].append(r)
    for frame in range(start,last):
        for slot in (1,2):
            a,b=by[frame,slot],by[frame+1,slot]
            need(b['hp']==(158 if slot==3-side and frame>=contact else 161),'Every physical HP callback matches exact original chip ledger')
            for kind in ('action','body','flags'):
                value=a[kind]
                for store in stores[frame,slot,kind]:
                    need(store['before']==value,'Entire ordered native blocked state-store chain')
                    value=store['after']
                need(b[kind]==value,'Every blocked state callback matches all native stores')
    first=by[start+1,side];sign=-1 if first['facing']&16 else 1
    need(first['xraw']==(initial[side]['xraw']+sign*5*65536)&MASK and first['yraw']==initial[side]['yraw']+10*65536,
         'Native displaced blocked startup initialization')
    for elapsed in range(6):
        r=by[start+1+elapsed,side];index=elapsed//2
        need(r['pose']==hit.INTRO[index] and r['xraw']==(first['xraw']+sign*index*5*65536)&MASK and
             r['yraw']==first['yraw']+index*10*65536 and r['vx']==r['vy']==r['gravity']==0,
             'All six original blocked startup fields')
    first_flight=by[start+7,side]
    need(first_flight['vx']==sign*0x40000&MASK and first_flight['vy']==0xfffe0000 and first_flight['gravity']==0xffff4000,
         'Original rising blocked seek initialization')
    for frame in range(start+8,contact+1):
        a,r=by[frame-1,side],by[frame,side]
        need(r['xraw']==(a['xraw']+a['vx'])&MASK and r['vy']==(a['vy']+0xffff4000)&MASK and
             r['yraw']==(a['yraw']+r['vy'])&MASK and r['vx']==first_flight['vx'],
             'Every pre-contact original seek integration')
    a,r=by[contact,side],by[contact+1,side]
    next_y=(a['yraw']+a['vy']+0xffff4000)&MASK
    # Original FF8768B0..FF876910 clamps only the upper16-bit integerY.
    expected_y=(r['floor']<<16)|(next_y&65535) if next_y>>16>=r['floor']else next_y
    need(r['xraw']==(a['xraw']+a['vx'])&MASK and r['yraw']==expected_y and r['vx']==0 and
         r['vy']==0xfffa0000 and r['gravity']==0x8000,'Exact original blocked fling initial floor clamp preserves fractional Y')
    for frame in range(contact+2,land+1):
        a,r=by[frame-1,side],by[frame,side]
        need(r['vx']==0 and r['xraw']==by[contact+1,side]['xraw'] and r['vy']==(a['vy']+0x8000)&MASK and
             r['yraw']==(a['yraw']+r['vy'])&MASK and r['gravity']==0x8000 and r['action']==0x611,
             'Every original stationary blocked rebound vertical step')
        need(r['pose']==hit.BIKE_CYCLE[(1+(frame-contact-2)//4)%len(hit.BIKE_CYCLE)],
             'Every original four-field continuing blocked cycle pose')
    a=by[land,side];cross=(a['yraw']+a['vy']+0x8000)&MASK
    need(a['yraw']>>16<a['floor'] and cross>>16>=a['floor'] and regain==land+6,
         'Actual native blocked floor crossing and six-field landing')
    for frame in range(land+1,regain+1):
        r=by[frame,side]
        need(r['yraw']==(r['floor']<<16)|(cross&65535) and r['vx']==r['vy']==r['gravity']==0 and r['action']==0x304,
             'Every original blocked grounded landing hold')
    for frame in range(regain+1,last+1):
        r=by[frame,side]
        need(r['action']==0x303 and r['flags']&0x1c==r['body']&12==0 and r['vx']==r['vy']==r['gravity']==0 and
             r['yraw']>>16==r['floor'],'Actual blocked control callback remains clean after native ready')
    return dict(passed=True,side=side,start=start,contact=contact,nativeChipDamage=3,landing=land,regain=regain,
                nativeFields=len(fields),sourceBoundStateStores=len(flags),ordinaryFollowup=baseline,
                wholeContactStartupSeekAndVerticalReboundAccepted=True,
                defenderFullHorizontalPushAndRasterShadowAudioAccepted=False,allCPUOrKOOrArenasAccepted=False,fullPortAcceptance=False)

def run():
    guest,old,payload,ends,ranges=current.expected_current()
    candidate=ROOT/current.current.CANDIDATE
    need((candidate/'roms/mk2ks/mk2ks.mdata').read_bytes()==payload and
         current.assembly.sha(candidate/'mkport_candidate.exe')==current.current.EXE,'Actual current3172 matched playable pair')
    pins={};cases=[]
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);actual=current.assembly.sha(path)
        need(wanted is None or actual==wanted,'Every actual captured input unchanged: '+key)
        need(key not in pins or pins[key]==actual,'Consistent actual source pin');pins[key]=actual
    for file,digest in current.assembly.source_check().items():pin(file,digest)
    for side in (1,2):
        folder=ROOT/f'audit_v3347_current_bicycle_block_p{side}_kano'
        meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
        build=json.loads((candidate/'build-info.json').read_text(encoding='utf-8-sig'))
        need(meta['exit_code']==0 and meta['candidate']==current.current.CANDIDATE and
             meta['executable_sha256']==build['executable_sha256']==current.current.EXE and
             meta['payload_sha256']==build['payload_sha256']==current.current.PAYLOAD and
             (meta['move'],meta['scenario'],meta['side'],meta['victim'],meta['snapshot_schema'])==('bicycle','block',side,'kano',2) and
             not meta['cheats_enabled'] and meta['assistance']=='none' and before==meta['input_hashes'] and
             all(before.get(file)==digest for file,digest in build['input_hashes'].items()),'Matched unassisted terminal compiled fixture')
        for file,digest in before.items():
            pin(file,digest)
            if Path(file).suffix in ('.lua','.ps1','.json'):snapshots.pin_snapshot(folder,file,digest,pin)
        driver=(folder/'input_sources/tree/mk2ks_human_special_negative_v9.lua').read_text()
        need(driver==(ROOT/'mk2ks_human_special_negative_v9.lua').read_text(),'Entire original two-human input driver unchanged')
        wrapper=(folder/'input_sources/tree/mk2ks_human_bicycle_block_trace_v3345.lua').read_text()
        need(wrapper.count("dofile('mk2ks_human_special_negative_v9.lua')")==1 and not re.search(
             r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|:reset\(|set_value|clear_value',wrapper) and
             not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|:reset\(',driver),
             'No guest/CPU/HP/RNG/position writes; wrapper supplies no buttons')
        need((folder/'guest_maincpu.bin').read_bytes()==guest,'Every guest byte independently assembled, no sampled or masked bytes')
        log=(folder/'run.log').read_text(encoding='utf-8-sig')
        need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation|WRONG CHECKSUMS',log,re.I),'No emulator or observer error')
        value=phase(log,guest,side);value['case']=folder.name;cases.append(value)
        for file in folder.rglob('*'):
            if file.is_file():pin(file)
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).suffix=='.py'and Path(file).resolve().is_relative_to(ROOT/'tools'):pin(file)
    return dict(passed=True,candidate=current.current.CANDIDATE,cases=cases,physicalFixtures=2,
                wholeGuestCorrectedPayloadAndCompiledInputsAccepted=True,actualBothPhysicalSlotsBlockedChipAndRecoveryAccepted=True,
                nativeFields=sum(c['nativeFields']for c in cases),sourceBoundStateStores=sum(c['sourceBoundStateStores']for c in cases),
                noProxyOrStateInjection=True,gameBytesChanged=False,fullRasterShadowAudioOrAllCPUAccepted=False,
                fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Never overwrite fresh blocked evidence')
    try:result=run()
    except Exception as error:result=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k!='inputHashes'},indent=2),flush=True)
    raise SystemExit(0 if result['passed']else 1)
