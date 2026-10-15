"""Actual native CPU paired contact, every held pose, fling and both recoveries.

Natural P2 CPU/P1 human evidence only; not all victims/slots/CPU moves or pixels.
"""
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path

from verify_p2_campaign import expected_orders
from verify_restart_pair import SPECS,CHOKE_OWN,CHOKE_XY,CHOKE_GROUPS,CHOKE_GRIP,LEG_OWN,LEG_XY,LEG_GROUPS
from verify_stock_reaction import ROOT,NAME,EXE,PAYLOAD

HEX=set('actor main owner pose list xraw yraw vx vy gravity flags body facing trail vactor vmain vowner vpose vlist vxraw vyraw vvx vvy vgravity vflags vbody vfacing vtrail schedule table pc entry victim group word a0 a1 a2 a3 a8 a9 a10 a13'.split())
TEXT={'kind','ids','buttons','scope','assistance'}
SCOPE='natural_P2_CPU_complete_close_contact_original_paired_holds_health_release_flight_both_recoveries_not_all_victims_slots_CPU_moves_bitmap_audio_or_full_goal'


def rows(log,tag):
    result=[]
    for line in log.splitlines():
        if not line.startswith('MK2_CPU_PAIR_'+tag+' '):continue
        pairs=re.findall(r'(\w+)=([^\s]+)',line)
        if len({k for k,v in pairs})!=len(pairs):raise ValueError('Ambiguous duplicate observer fields')
        result.append({k:v if k in TEXT else int(v,16 if k in HEX else 10)for k,v in pairs})
    return result


def _verify_log(log,player):
    errors=[]
    def need(ok,label):
        if not ok and label not in errors:errors.append(label)
    fields,entries,events,health,complete,results=[rows(log,t) for t in ('FIELD','ENTRY','EVENT','HEALTH','COMPLETE','RESULT')]
    need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|stack traceback',log,re.I),'No emulator or Lua observer error')
    need(len(complete)==len(results)==1 and bool(entries),'Actual paired completion/result/entry required')
    need(len(results)==1 and results[0].get('schema')==2,'Unambiguous CPU/pair position and velocity schema required')
    need(all(r.get('writes')==0 and r.get('assistance')=='none' for tag in ('ROM','FIELD','ENTRY','EVENT','HEALTH','COMPLETE','RESULT','INPUT','INCOMPLETE') for r in rows(log,tag)),'Read-only observations and input-only natural scope')
    orders=expected_orders();roms=rows(log,'ROM')
    need(len(roms)==6 and [r.get('order') for r in roms]==list(range(6)) and all(r.get('table')==0xfffa2c00 and r.get('list')==0xfffa3000+i*0x180 and tuple(map(int,r.get('ids','').split(',')))==orders[i] for i,r in enumerate(roms)),'Every native order equals original stock ladder plus both actual new IDs')
    for pattern in ('MK2KS_CPU_DIAGNOSTIC_RESULT requested=nil injected=false','MK2KS_CPU_DIAGNOSTIC_LADDER_RESULT requested=nil injected=false','MK2KS_CPU_DIAGNOSTIC_HEALTH_RESULT requested=nil all_stages=false writes=0','MK2KS_CPU_DIAGNOSTIC_P1_REGEN_RESULT enabled=false writes=0','MK2KS_STABILITY stalled_frames=0 trap_frames=0','MK2KS_DISPLAY_RESULT pass=true '):
        need(pattern in log,'Natural clean runtime: '+pattern)
    need(not re.search(r'MK2KS_CPU_DIAGNOSTIC_WRITE|MK2KS_CPU_DIAGNOSTIC_LADDER_WRITE|MK2KS_DIAGNOSTIC_HEALTH_WRITE|MK2KS_DIAGNOSTIC_P1_REGEN frame=',log),'No observer CPU ID/stage/health assistance')
    if not complete or not entries or not results:return dict(passed=False,errors=errors,scope=SCOPE,whole_character_integration_complete=False)
    done=complete[0];cycle=done['cycle'];starts=[r for r in entries if r['cycle']==cycle]
    need(len(starts)==1,'Unique actual CPU action for completed cycle')
    if not starts:return dict(passed=False,errors=errors,scope=SCOPE,whole_character_integration_complete=False)
    entry=starts[0];start,end=entry['frame'],done['frame'];target='kano' if entry['id']==17 else 'sonya';spec=SPECS[target]
    pid={'kano':17,'sonya':18,'liu_kang':1}[player]
    timeline=[r for r in fields if start<r['frame']<=end];by={r['frame']:r for r in timeline}
    need(len(timeline)==len(by)==end-start and set(by)==set(range(start+1,end+1)) and 0<end-start<300,'Every real paired callback field through complete two-actor recovery')
    need(all(r.get('cycle')==cycle for r in timeline),'No unrelated cycle spliced into contact proof')
    identities=('actor','main','vactor','vmain')
    need(len({entry[k] for k in identities})==4 and all(0x01000000<=entry[k]<0x01100000 for k in identities),'Distinct native executing actors and Main processes')
    for r in [entry,*timeline,done]:
        order=(r['schedule']-0xfffa3000)//0x180
        need(order in range(6) and r['schedule']==0xfffa3000+order*0x180 and r['stage'] in range(17) and r['id']==orders[order][r['stage']],'Actual native selected CPU identity follows original-derived schedule')
        need(all(r[k]==entry[k] for k in identities) and r['owner']==r['actor'] and r['vowner']==r['vactor'] and r['id']==r['roster']==spec['id'] and r['vid']==r['vroster']==pid and r['state']==0 and r['vstate']==1 and r['mode']==2 and 0<r['hp']<=161 and 0<r['vhp']<=161,'Stable published actual CPU/human roles through contact and recovery')
    chain=[r for r in events if r['cycle']==cycle and start<=r['frame']<=end]
    def event(kind):return [r for r in chain if r['kind']==kind]
    steps=event('step');releases=event('release');flings=event('fling');calls=event('damage');pulses=event('pulse')
    wanted=22 if target=='kano' else 5;doses=4 if target=='kano' else 1
    need(len(steps)==wanted and len(releases)==len(flings)==1 and len(calls)==doses and len(pulses)==(4 if target=='kano' else 0),'Complete original paired phase/damage/release chain, not activation only')
    need(event('intro') and event('attack') and len(event('action'))==1 and event('action')[0]['frame']==start,'Actual native action startup and catch descriptor execution')
    addresses=dict(action=spec['action'],intro=spec['intro'],attack=spec['attack'],release=spec['release'],step=0xfff89400,pulse=0xfff93400,damage=0xff837340,fling=0xff876650,velocity=0xff831bd0,own_ready=0xff861350,victim_ready=0xff861350)
    for r in chain:
        own=r['kind'] in ('action','intro','attack','step','own_ready')
        pc_ok=r['pc']=={'intro':0xff83bb10,'attack':0xff835480}[r['kind']] if r['kind']in('intro','attack')else r['pc']==r['entry']+16
        need(r['kind'] in addresses and r['entry']==addresses[r['kind']] and pc_ok and (r['actor'],r['main'],r['victim'],r['vmain'])==(entry['actor'],entry['main'],entry['vactor'],entry['vmain']) and r['a8']==entry['actor' if own else 'vactor'] and r['a13'] in ([entry['main'],entry['vmain']] if r['kind'] in ('damage','pulse') else [entry['main' if own else 'vmain']]),'Original instructions execute under real owning Main, never forced actor/task aliases')
        if r['kind']=='attack':need(r['word']==(101 if target=='kano'else 115),'Actual own native catch descriptor first word')
        if r['kind']=='intro':need(r['word']==(0x0420 if target=='kano'else 3),'Actual own original startup sequence first word')
    if len(steps)!=wanted or len(releases)!=1 or len(flings)!=1:return dict(passed=False,errors=errors,target=target,scope=SCOPE,whole_character_integration_complete=False)
    release=releases[0]['frame'];times=[r['frame'] for r in steps]
    origin=by.get(times[0]+1,{})
    direction=-1 if origin.get('facing',0)&0x10 else 1
    vid=entry['vid'];held_fields=0
    if target=='kano':
        need(all(times[i]-times[i-1]==(5 if i<=3 else 3) for i in range(1,22)) and release in (times[-1],times[-1]+1),'Original 22-step choke hold cadence')
        need([r['frame'] for r in pulses]==[times[3]+12*i for i in range(1,5)] and [r['frame'] for r in calls]==[r['frame'] for r in pulses] and all(r['a10']==8 for r in calls),'Original four native eight-point squeezes at twelve-field intervals')
        for i,step in enumerate(steps):
            phase=i if i<3 else (i-3)%4+3
            need(step['group']==CHOKE_OWN[phase] and step['steps']==i+1,'Own original choke composite sequence and actual step accounting')
            if vid in (17,18):
                dx,dy=CHOKE_XY[vid][phase];vpose=0xfe836860 if vid==18 else (0xfe8294a0 if phase==6 else 0xfe829500)
            else:
                dx,dy=CHOKE_XY[18][phase];gx,gy=CHOKE_GRIP[vid];dx+=8+gx;dy+=54-gy;vpose=CHOKE_GROUPS[vid]
            final=times[i+1] if i+1<len(times) else times[i]+1
            for at in range(times[i]+1,final+1):
                r=by.get(at,{})
                need(r.get('pose')==CHOKE_OWN[phase] and r.get('vpose')==vpose and r.get('vx')==r.get('vy')==0 and r.get('y')==r.get('floor') and r.get('x')==origin.get('x') and r.get('vxpos')==r.get('x',0)+direction*dx and r.get('vypos')==r.get('y',0)+dy,'Every held original choke pose, grip offset and grounded own position')
                allowed=(spec['victim_state'],0x506) if i==21 and release<=times[i] else (spec['victim_state'],)
                need(r.get('action')==spec['state'] and r.get('vaction')in allowed,'Every original paired choke action state')
                held_fields+=1
    else:
        need(times==[times[0]+n for n in (0,30,34,38,42)] and release in (times[0]+46,times[0]+47) and [r['group'] for r in steps]==list(LEG_OWN),'Original five-phase/46-field leg choreography')
        need(all(r['a10']==35 and r['frame']==release for r in calls),'Native 35-point leg damage occurs at actual release')
        for elapsed in range(46):
            r=by.get(times[0]+1+elapsed,{})
            phase=0 if elapsed<30 else 1+(elapsed-30)//4
            shake=3 if elapsed<30 and(elapsed//3)%2==0 else 0
            dx,dy=LEG_XY[vid][phase]
            need(r.get('pose')==LEG_OWN[phase] and r.get('vpose')==LEG_GROUPS[vid][phase] and r.get('x')==origin.get('x') and r.get('y')==origin.get('y') and r.get('vx')==r.get('vy')==r.get('vvx')==r.get('vvy')==0 and r.get('vxpos')==origin.get('x',0)+direction*dx and r.get('vypos')==origin.get('y',0)+dy+shake,'Every original leg paired pose/offset/three-field shake')
            need(r.get('hp')==origin.get('hp') and r.get('vhp')==origin.get('vhp') and r.get('action')==spec['state'] and r.get('vaction')==spec['victim_state'] and r.get('suppression',0)>0,'Every held leg field retains health, native lock and push suppression')
            held_fields+=1
    stores=[r for r in health if r['cycle']==cycle and times[0]<=r['frame']<=end and r['slot']==1 and r['before']!=r['after']]
    need(all(r['pc']==0xff836700 and r['slot']in(1,2)and 0<=r['after']<=r['before']<=161 for r in health if r['cycle']==cycle and start<=r['frame']<=end),'Every original health-store instruction in completed pair, including zero-damage contacts')
    need(len(stores)==doses and sum(r['before']-r['after']for r in stores)==spec['damage'] and all(r['pc']==0xff836700 and r['a8']==entry['vactor'] and r['a13']in(entry['main'],entry['vmain']) for r in stores),'Complete actual native paired victim health ledger')
    need(all(b['after']==a['before']for b,a in zip(stores,stores[1:])) and bool(stores) and done['vhp']==stores[-1]['after'],'Continuous actual damage ledger and recovered live health')
    for dose,store in zip(calls,stores):need(0<=store['frame']-dose['frame']<=1,'Every native damage call has its own original health store')
    wanted_health=entry['vhp'];store_index=0
    for r in timeline:
        while store_index<len(stores)and stores[store_index]['frame']<r['frame']:
            wanted_health=stores[store_index]['after'];store_index+=1
        if not any(h['frame']==r['frame']for h in stores):need(r['vhp']==wanted_health,'No unlogged victim health changes during the pair')
        need(r['hp']==entry['hp'],'Completed uninterrupted CPU pair is not silently interrupted by human damage')
    params=(0x40000,0xfffc0000,0x8000,5)if target=='kano'else(0x30000,0xfffa0000,0x8000,4)
    need(tuple(flings[0]['a'+str(i)]for i in range(4))==params and release<=flings[0]['frame']<=release+1,'Original victim fixed-point fling arguments')
    wanted_vx=direction*(0x40000 if target=='kano'else-0x30000)&0xffffffff
    need(any(release<=r['frame']<=release+1 and r['a0']==wanted_vx and r['a1']==0x010602d0 for r in event('velocity')),'Actual native P1-victim signed horizontal launch request')
    launch=by.get(release+1,{})
    need(launch.get('vvy')==params[1] and launch.get('vgravity')==params[2] and launch.get('vaction')==0x506,'Actual original victim airborne continuation begins')
    if target=='sonya':need(launch.get('vypos')==launch.get('vfloor'),'Leg victim floor restored at release before flight')
    flight=[]
    for at in range(release+1,end):
        r=by.get(at,{})
        if r.get('vgravity')!=params[2]:break
        flight.append(r)
    need(len(flight)>8,'Whole original victim flight is sampled, not an isolated airborne pose')
    for a,b in zip(flight,flight[1:]):
        need(b['frame']==a['frame']+1 and b['vvy']==(a['vvy']+a['vgravity'])&0xffffffff and b['vyraw']==(a['vyraw']+b['vvy'])&0xffffffff,'Every native fixed-point victim gravity and Y step')
    def clean(r,prefix):
        velocity=r[prefix+'vx'];velocity=velocity-0x100000000 if velocity&0x80000000 else velocity
        y=r['vypos']if prefix else r['y']
        return y==r[prefix+'floor'] and r[prefix+'vy']==r[prefix+'gravity']==r[prefix+'trail']==0 and r[prefix+'flags']&0x1c==0 and r[prefix+'body']&0x0c==0 and(velocity==0 or r[prefix+'action']==0x303 and abs(velocity)<=0x30000)
    need(clean(done,'')and clean(done,'v')and done['action']!=spec['state']and done['vaction']!=spec['victim_state'],'Both living native actors recover grounded, cleared and detached; ordinary CPU walking is allowed')
    # Both actor roles must return through native ready, with live grounded cleanup.
    need(any(release<=r['frame']<end for r in event('own_ready')) and any(release<r['frame']<end for r in event('victim_ready')),'Both actual owning Main processes return through native ready code')
    need(results[0]['complete']==end and results[0]['frame']==end+30 and results[0]['cycles']==len(entries),'Terminal observation declares exact actual completed cycle and later bounded follow-up')
    return dict(passed=not errors,errors=errors,target=target,player=player,cycle=cycle,start=start,release=release,complete=end,paired_fields=len(timeline),held_fields=held_fields,victim_flight_fields=len(flight),damage=spec['damage'],observed_cycles=len(entries),completed_cycle_scope='only_declared_uninterrupted_completed_pair_other_misses_interruptions_and_later_entries_not_claimed_complete',scope=SCOPE,whole_character_integration_complete=False)


def verify_log(log,player):
    try:return _verify_log(log,player)
    except (ValueError,KeyError,IndexError,TypeError)as error:
        return dict(passed=False,errors=['Malformed/incomplete actual evidence: '+str(error)],scope=SCOPE,whole_character_integration_complete=False)


def verify(folder,player):
    proof=verify_log((folder/'run.log').read_text(encoding='utf-8-sig'),player)
    errors=proof['errors'];meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    if (meta.get('exit_code'),meta.get('candidate'),meta.get('executable_sha256'),meta.get('payload_sha256'),meta.get('player'),meta.get('assistance'))!=(0,NAME,EXE,PAYLOAD,player,'none'):errors.append('Exact current terminal native case identity')
    if before!=meta.get('input_hashes'):errors.append('Frozen before/after observed launch inputs')
    for file,expected in before.items():
        path=Path(file)
        if path.suffix.lower()in('.lua','.ps1','.json'):path=folder/'input_sources'/path.name
        if not path.is_file()or hashlib.sha256(path.read_bytes()).hexdigest().upper()!=expected:errors.append('Exact frozen launch input: '+str(path))
    build=json.loads((folder/'input_sources/build-info.json').read_text(encoding='utf-8-sig'))
    for file,expected in build['input_hashes'].items():
        path=Path(file)
        if not path.is_file()or hashlib.sha256(path.read_bytes()).hexdigest().upper()!=expected:errors.append('Exact current build input: '+file)
    probe=(folder/'input_sources/mk2ks_cpu_pair_probe.lua').read_text()
    if re.search(r':write_|\.value\s*=(?!=)|load_state|loadstate',probe):errors.append('New CPU pair observer must never write guest state')
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    if hashlib.sha256(original).hexdigest().upper()!='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23' or any(struct.unpack_from('<H',original,(at-0xff800000)//8)[0]!=opcode for at,opcode in ((0xff83bb00,0x9720),(0xff835470,0x9401))):errors.append('Original native sequence/collision descriptor read instructions')
    proof.update(passed=not errors,checked_inputs=len(before)+len(build['input_hashes']))
    return proof


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('case',type=Path);parser.add_argument('player');parser.add_argument('--output',type=Path);args=parser.parse_args()
    proof=verify(args.case,args.player)
    if args.output:
        if args.output.exists():raise SystemExit('Refusing to overwrite evidence')
        args.output.write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps(proof,indent=2));raise SystemExit(0 if proof['passed'] else 1)
