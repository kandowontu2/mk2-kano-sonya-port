"""Actual native CPU paired contact, every held pose, fling and both recoveries.

Natural cold P1 CPU/P2 human paired recovery at original individual ready handoffs.
Not all victims, interruptions, KO continuations, CPU moves, pixels or audio.
"""
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path

from verify_p2_campaign import expected_orders
from verify_restart_pair import SPECS,CHOKE_OWN,CHOKE_XY,CHOKE_GROUPS,CHOKE_GRIP,LEG_OWN,LEG_XY,LEG_GROUPS
from verify_native_candidate_v635 import ROOT,NAME,EXE,PAYLOAD,matched

HEX=set('actor main owner pose list xraw yraw vx vy gravity flags body facing trail vactor vmain vowner vpose vlist vxraw vyraw vvx vvy vgravity vflags vbody vfacing vtrail schedule table pc entry victim group word a0 a1 a2 a3 a6 a8 a9 a10 a13'.split())
TEXT={'kind','ids','buttons','scope','assistance','human','phase','move'}
HUMANS=dict(kano=17,sonya=18,liu_kang=1,kung_lao=0,cage=2,baraka=3,kitana=4,mileena=5,shang_tsung=6,raiden=7,sub_zero=8,reptile=9,scorpion=10,jax=11)
CPU_SLOT,HUMAN_SLOT=1,2
# Handoff keys are logical roles; provenance rows keep actual physical slot numbers.
PHYSICAL_ROLE={1:CPU_SLOT,2:HUMAN_SLOT}
SCOPE='natural_P1_CPU_repeated_full_pairs_original_individual_handoffs_and_whole_native_state_flag_health_stream_not_all_victims_KO_pixels_audio_or_goal'


def rows(log,tag):
    result=[]
    for line in log.splitlines():
        if not line.startswith('MK2_CPU_PAIR_'+tag+' '):continue
        pairs=re.findall(r'(\w+)=([^\s]+)',line)
        if len({k for k,v in pairs})!=len(pairs):raise ValueError('Ambiguous duplicate observer fields')
        result.append({k:v if k in TEXT else int(v,16 if k in HEX else 10)for k,v in pairs})
    return result


def flag_rows(log):
    result=[]
    extra_hex={'at','before','after','op0','op1'}
    for line in log.splitlines():
        if not line.startswith('MK2_CPU_PAIR_FLAG '):continue
        pairs=re.findall(r'(\w+)=([^\s]+)',line)
        if len({k for k,v in pairs})!=len(pairs):raise ValueError('Ambiguous duplicate native flag provenance')
        result.append({k:v if k in TEXT else int(v,16 if k in HEX or k in extra_hex else 10)for k,v in pairs})
    return result


def rows_prefix(log,prefix):
    result=[]
    for line in log.splitlines():
        if not line.startswith(prefix):continue
        pairs=re.findall(r'(\w+)=([^\s]+)',line)
        if len({k for k,v in pairs})!=len(pairs):raise ValueError('Ambiguous duplicate cold-selection fields')
        result.append({k:v if k in TEXT or k in ('states','roster') else int(v,16 if k in HEX else 10)for k,v in pairs})
    return result


def _verify_log(log,player,selected_cycle):
    errors=[]
    def need(ok,label):
        if not ok and label not in errors:errors.append(label)
    fields,entries,events,health,complete,results=[rows(log,t) for t in ('FIELD','ENTRY','EVENT','HEALTH','COMPLETE','RESULT')]
    need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|stack traceback',log,re.I),'No emulator or Lua observer error')
    all_complete=complete
    complete=[r for r in all_complete if r['cycle']==selected_cycle]
    need(len(complete)==len(results)==1 and bool(entries),'Actual selected paired completion/result/entry required')
    need(len(all_complete)>=2 and len(results)==1 and results[0].get('complete_count')==len(all_complete),'At least two real completed pairs and their exact terminal count')
    need(len(results)==1 and results[0].get('schema')==9,'Actual repeated-pair observation schema 9 required')
    need(all(r.get('cpu_slot')==CPU_SLOT and r.get('human_slot')==HUMAN_SLOT and r.get('writes')==0 and r.get('assistance')=='none' for tag in ('ROM','FIELD','ENTRY','EVENT','HEALTH','COMPLETE','RESULT','INPUT','INCOMPLETE','OWN_REGAIN','VICTIM_REGAIN') for r in rows(log,tag)),'Read-only observations and input-only natural scope')
    orders=expected_orders();roms=rows(log,'ROM')
    need(len(roms)==6 and [r.get('order') for r in roms]==list(range(6)) and all(r.get('table')==0xfffa2c00 and r.get('list')==0xfffa3000+i*0x180 and tuple(map(int,r.get('ids','').split(',')))==orders[i] for i,r in enumerate(roms)),'Every native order equals original stock ladder plus both actual new IDs')
    select=rows_prefix(log,'MK2_P1CPU_SELECT_RESULT ')
    cold=rows_prefix(log,'MK2_P1CPU_COLD_LIVE ')
    need(len(select)==len(cold)==1,'One real cold P2-only selection and native CPU fight')
    for r in [*select,*cold,*rows_prefix(log,'MK2_P1CPU_BOOT_STATE '),*rows_prefix(log,'MK2_P1CPU_SELECT_CSS ')]:
        need(r.get('writes')==0 and r.get('assistance')=='none','Cold selection inputs only; no proxy or health/stage fixture')
    if select and cold:
        sel,c=select[0],cold[0]
        need(sel['human']==c['human']==player and sel['human_id']==c['human_id']==HUMANS[player] and
             700<sel['css']<sel['exit']<sel['live']==c['frame'] and
             sel['checks']>=30 and sel['errors']==0 and sel['initial_cpu']==c['cpu_id'],
             'Actual P2 selection holds true identity then enters native P1 CPU fight')
        order=(c['schedule']-0xfffa3000)//0x180
        need(order in range(6) and c['schedule']==0xfffa3000+order*0x180 and c['stage']==0 and
             c['cpu_id']==orders[order][0],'Cold campaign starts at native stage zero of original-derived order')
    need(not re.search(r'MK2KS_CPU_DIAGNOSTIC_WRITE|MK2KS_CPU_DIAGNOSTIC_LADDER_WRITE|MK2KS_DIAGNOSTIC_HEALTH_WRITE|MK2KS_DIAGNOSTIC_P1_REGEN frame=',log),'No observer CPU ID/stage/health assistance')
    if not complete or not entries or not results:return dict(passed=False,errors=errors,scope=SCOPE,whole_character_integration_complete=False)
    done=complete[0];cycle=done['cycle'];starts=[r for r in entries if r['cycle']==cycle]
    need(len(starts)==1,'Unique actual CPU action for completed cycle')
    if not starts:return dict(passed=False,errors=errors,scope=SCOPE,whole_character_integration_complete=False)
    entry=starts[0];start,end=entry['frame'],done['frame'];target='kano' if entry['id']==17 else 'sonya';spec=SPECS[target]
    pid=HUMANS[player]
    timeline=[r for r in fields if start<r['frame']<=end];by={r['frame']:r for r in timeline}
    need(len(timeline)==len(by)==end-start and set(by)==set(range(start+1,end+1)) and 0<end-start<300,'Every real paired callback field through complete two-actor recovery')
    need(all(r.get('cycle')==cycle for r in timeline),'No unrelated cycle spliced into contact proof')
    identities=('actor','main','vactor','vmain')
    need(len({entry[k] for k in identities})==4 and all(0x01000000<=entry[k]<0x01100000 for k in identities),'Distinct native executing actors and Main processes')
    regains=[*rows(log,'OWN_REGAIN'),*rows(log,'VICTIM_REGAIN')]
    selected_regains=[r for r in regains if r['cycle']==cycle]
    for r in [entry,*timeline,done,*selected_regains]:
        order=(r['schedule']-0xfffa3000)//0x180
        need(order in range(6) and r['schedule']==0xfffa3000+order*0x180 and r['stage'] in range(17) and r['id']==orders[order][r['stage']],'Actual native selected CPU identity follows original-derived schedule')
        need(all(r[k]==entry[k] for k in identities) and r['owner']==r['actor'] and r['vowner']==r['vactor'] and r['id']==r['roster']==spec['id'] and r['vid']==r['vroster']==pid and r['state']==0 and r['vstate']==1 and r['mode']==2 and 0<r['hp']<=161 and 0<r['vhp']<=161,'Stable published actual CPU/human roles through contact and recovery')
    chain=[r for r in events if r['cycle']==cycle and start<=r['frame']<=end]
    def event(kind):return [r for r in chain if r['kind']==kind]
    steps=event('step');releases=event('release');flings=event('fling');calls=event('damage');pulses=event('pulse')
    wanted=22 if target=='kano' else 5;doses=4 if target=='kano' else 1
    need(len(steps)==wanted and len(releases)==len(flings)==1 and len(calls)==doses and len(pulses)==(4 if target=='kano' else 0),'Complete original paired phase/damage/release chain, not activation only')
    need(event('intro') and event('attack') and len(event('action'))==1 and event('action')[0]['frame']==start,'Actual native action startup and catch descriptor execution')
    addresses=dict(action=spec['action'],intro=spec['intro'],attack=spec['attack'],release=spec['release'],step=0xfff89400,pulse=0xfff93400,damage=0xff837340,fling=0xff876650,velocity=0xff831bd0,own_ready=0xff861350,victim_ready=0xff861350,own_regain=0xff861500,victim_regain=0xff861500)
    for r in chain:
        own=r['kind'] in ('action','intro','attack','step','own_ready','own_regain')
        pc_ok=r['pc']=={'intro':0xff83bb10,'attack':0xff835480}[r['kind']] if r['kind']in('intro','attack')else r['pc']==r['entry']+16
        need(r['kind'] in addresses and r['entry']==addresses[r['kind']] and pc_ok and (r['actor'],r['main'],r['victim'],r['vmain'])==(entry['actor'],entry['main'],entry['vactor'],entry['vmain']) and r['a8']==entry['actor' if own else 'vactor'] and r['a13'] in ([entry['main'],entry['vmain']] if r['kind'] in ('damage','pulse') else [entry['main' if own else 'vmain']]),'Original instructions execute under real owning Main, never forced actor/task aliases')
        if r['kind']=='attack':need(r['word']==(101 if target=='kano'else 115),'Actual own native catch descriptor first word')
        if r['kind']=='intro':need(r['word']==(0x0420 if target=='kano'else 3),'Actual own original startup sequence first word')
        if r['kind']=='velocity':need(r['a1']==0x01060ea0,'Every native victim velocity request targets the actual P2 slot')
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
    stores=[r for r in health if r['cycle']==cycle and times[0]<=r['frame']<=end and r['slot']==HUMAN_SLOT and r['before']!=r['after']]
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
    need(any(release<=r['frame']<=release+1 and r['a0']==wanted_vx and r['a1']==0x01060ea0 for r in event('velocity')),'Actual native P2-victim signed horizontal launch request')
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
    need(clean(done,'v') and done['action']!=spec['state'] and done['vaction']!=spec['victim_state'],'Final living victim remains grounded and detached; CPU is no longer in the paired action')
    flags=flag_rows(log)
    handoffs={}
    for tag,prefix,slot in (('OWN_REGAIN','',1),('VICTIM_REGAIN','v',2)):
        records=[r for r in rows(log,tag) if r['cycle']==cycle]
        kind='own_regain'if slot==1 else'victim_regain'
        need(len(records)==len(event(kind))==1,'Each owning Main has one first native post-cleanup handoff')
        if not records or not event(kind):continue
        r,e=records[0],event(kind)[0];handoffs[slot]=r
        need(r['frame']==e['frame'] and r['action'if slot==1 else'vaction']==0 and
             clean(r,prefix) and r[prefix+'vx']==0,
             'Actual original ready handoff is fully cleared, stopped, grounded and detached for its own actor')
        need(any(n['frame']==r['frame'] for n in event('own_ready'if slot==1 else'victim_ready')),
             'Original ready entry and post-cleanup handoff occur under the same real Main in the same field')
        target_actor=entry['actor'if slot==1 else'vactor'];target_main=entry['main'if slot==1 else'vmain']
        for field,pc,at,mask in (('body',0xff83eeb0,target_actor+0x160,0x0c),('flags',0xff83efc0,target_main+0x210,0x14)):
            need(any(n['cycle']==cycle and n['slot']==PHYSICAL_ROLE[slot] and n['frame']==r['frame']and
                     n['kind']==field and n['pc']==pc and n['at']==at and
                     n['actor']==target_actor and n['main']==target_main and n['a8']==target_actor and
                     n['a13']==target_main and n['after']==n['before']&(~mask&0xffff)
                     for n in flags),'Actual original body/Main cleanup stores precede each owning ready handoff')
    if len(handoffs)==2:
        own,victim=handoffs[1],handoffs[2]
        need(own['frame']-release in ((13,14)if target=='kano'else(9,10)),
             'Complete original own recovery holds end at the native ready handoff')
        need(release<victim['frame']<end and own['frame']<end and end==max(own['frame'],victim['frame'])+1,
             'Completion follows both actual individual handoffs, not a later coincidental clean pose')
        # Replay actual post-pair Main action stores against EVERY callback.
        # Flags can be set while walking, before the original animation consumer
        # publishes its attack state in the same field. Require that instruction,
        # live operands, owning registers, ordering and a continuous state ledger.
        action_stores=[n for n in flags if n['cycle']==cycle and n['slot']==CPU_SLOT and
                       n['kind']=='action' and own['frame']<=n['frame']<end]
        need(bool(action_stores) and action_stores[0]['before']==spec['state'] and
             action_stores[0]['frame']==own['frame'] and action_stores[0]['after']==0,
             'Actual paired state clears at the owning native ready handoff')
        current=spec['state'];previous_frame=own['frame']
        for n in action_stores:
            register='a1' if n['pc']==0xff83c340 else 'a0'
            opcode=0xb02d if register=='a1' else 0xb00d
            allowed=(n['pc']==0xff83edd0 and n['after']==0 or
                     n['pc']==0xff9065d0 and n['after']==0x303 or
                     n['pc']==0xff83c340 and n['after']==0x106)
            need(allowed and n['actor']==entry['actor'] and n['main']==entry['main'] and
                 n['a8']==entry['actor'] and n['a13']==entry['main'] and
                 n['at']==entry['main']+0x1f0 and n['action']==n['before']==current and
                 n[register]&0xffff==n['after'] and (n['op0'],n['op1'])==(opcode,0x1f0) and
                 n['state']==0 and n['id']==spec['id'] and n['frame']>=previous_frame,
                 'Continuous real original action-store instruction/register/ownership ledger')
            current=n['after'];previous_frame=n['frame']
        cursor=0;current=spec['state']
        for r in timeline:
            if r['frame']<=own['frame']:continue
            while cursor<len(action_stores) and action_stores[cursor]['frame']<r['frame']:
                current=action_stores[cursor]['after'];cursor+=1
            need(r['action']==current,'Every post-handoff callback agrees with original action stores')
        need(current==done['action'],'Completed CPU state agrees with the full native action ledger')
        if done['flags']&0x1c or done['body']&0x0c or done['trail']:
            need(done['flags']&0x1c==0x10 and done['body']&0x0c==4 and done['trail']==0,
                 'Only the actual original follow-up attack locks may be active')
            changed=[n for n in action_stores if n['pc']==0xff83c340 and
                     n['before']==0x303 and n['after']==done['action']]
            need(len(changed)==1 or (not changed and done['action']==0x303),
                 'Original follow-up is either unchanged-state native setup or exact walking-to-attack publication')
            if not changed and done['action']==0x303:
                # Some original ordinary attacks retain the walking state.
                # Keep the prior exact NEW-setup gate; do not demand a state
                # publication that the native engine does not perform.
                for field,pc,mask in (('body',0xff838cf0,4),('flags',0xff877d50,0x10)):
                    need(any(n['cycle']==cycle and own['frame']<n['frame']<end and
                             n['slot']==CPU_SLOT and n['kind']==field and n['pc']==pc and
                             n['actor']==entry['actor'] and n['main']==entry['main'] and
                             n['a8']==entry['actor'] and n['a13']==entry['main'] and
                             n['at']==(entry['actor']+0x160 if field=='body' else entry['main']+0x210) and
                             n['action']==done['action'] and not n['before']&mask and
                             n['after']==n['before']|mask for n in flags),
                         'Unchanged-state attack locks originate in NEW original setup after paired cleanup')
            if changed:
                published=changed[0];publication_index=flags.index(published)
                for field,pc,mask in (('body',0xff838cf0,4),('flags',0xff877d50,0x10)):
                    setups=[n for n in flags[:publication_index] if n['cycle']==cycle and
                            own['frame']<n['frame']==published['frame'] and n['slot']==CPU_SLOT and
                            n['kind']==field and n['pc']==pc and n['actor']==entry['actor'] and
                            n['main']==entry['main'] and n['a8']==entry['actor'] and
                            n['a13']==entry['main'] and n['action']==published['before'] and
                            n['at']==(entry['actor']+0x160 if field=='body' else entry['main']+0x210) and
                            not n['before']&mask and n['after']==n['before']|mask]
                    need(bool(setups),'NEW original attack setup precedes its exact action publication')
                # Keep observing after paired completion: the new attack must
                # itself clear through original cleanup, not become a new lock.
                for field,pc,mask in (('body',0xff83eeb0,0x0c),('flags',0xff83efc0,0x14)):
                    need(any(n['cycle']==cycle and end<n['frame']<=results[0]['frame'] and
                             n['slot']==CPU_SLOT and n['kind']==field and n['pc']==pc and
                             n['actor']==entry['actor'] and n['main']==entry['main'] and
                             n['a8']==entry['actor'] and n['a13']==entry['main'] and
                             n['at']==(entry['actor']+0x160 if field=='body' else entry['main']+0x210) and
                             n['action']==0 and n['before']&mask and
                             n['after']==n['before']&(~mask&0xffff)
                             for n in flags),'Original follow-up attack also clears within observed continuation')
    need(all(r.get('writes')==0 and r.get('assistance')=='none' and r.get('cpu_slot')==CPU_SLOT and r.get('human_slot')==HUMAN_SLOT for r in flags),
         'Every flag-store observer declares actual read-only native scope')
    # Both actor roles must return through native ready, with live grounded cleanup.
    need(any(release<=r['frame']<end for r in event('own_ready')) and any(release<r['frame']<end for r in event('victim_ready')),'Both actual owning Main processes return through native ready code')
    # v5 adds first subsequent ready and independent continuation records to
    # schema 6's unchanged pair/flag-store observations. Do not relabel an
    # actual signature move as an ordinary attack or merely allow more time.
    follow=verify_repeated_stream(log,entry,fields,health,all_complete,results[0],need)
    verify_cpu_flag_ledger(entry,fields,flags,results[0],need)
    need(results[0]['complete']==all_complete[-1]['frame'] and results[0]['frame']==all_complete[-1]['frame']+30 and results[0]['cycles']==len(entries),'Terminal observation declares last full pair and exact thirty-field continuation')
    return dict(passed=not errors,errors=errors,target=target,player=player,cycle=cycle,start=start,release=release,complete=end,paired_fields=len(timeline),held_fields=held_fields,victim_flight_fields=len(flight),damage=spec['damage'],observed_cycles=len(entries),CPU_slot=CPU_SLOT,human_slot=HUMAN_SLOT,own_handoff=handoffs.get(1,{}).get('frame'),victim_handoff=handoffs.get(2,{}).get('frame'),native_cleanup_store_rows=len(flags),native_followup=follow,native_followup_actions=[dict(frame=n['frame'],before=n['before'],after=n['after'],pc=hex(n['pc']))for n in action_stores] if len(handoffs)==2 else [],completed_cycle_scope='only_declared_uninterrupted_completed_pair_other_misses_interruptions_and_later_entries_not_claimed_complete',scope=SCOPE,whole_character_integration_complete=False)


def verify_ordinary_followup(log,entry,done,fields,flags,terminal,need):
    cycle=done['cycle'];end=terminal['frame'];ready=terminal['follow_regain']
    instructions=rows(log,'FOLLOW_INSTRUCTION')
    need(not any(r['kind']=='action' for r in instructions),
         'Ordinary follow-up cannot substitute for an observed signature entry')
    regains=rows(log,'FOLLOW_REGAIN');events=rows(log,'FOLLOW_READY_INSTRUCTION')
    need(len(regains)==1 and done['frame']<ready<end and end==ready+30,
         'One actual later first regain and thirty-field continuation')
    if len(regains)!=1:return {}
    regained=regains[0]
    need([(r['kind'],r['entry'],r['pc'],r['frame']) for r in events]==
         [('recovery',0xff861350,0xff861360,ready),('regained',0xff861500,0xff861510,ready)],
         'First ordinary recovery executes both original ready instructions')
    by={r['frame']:r for r in fields if entry['frame']<r['frame']<=end}
    need(len(by)==len([r for r in fields if entry['frame']<r['frame']<=end])==end-entry['frame'] and
         set(by)==set(range(entry['frame']+1,end+1)),
         'Every pair and subsequent ordinary callback remains recorded')
    continuation=rows(log,'FOLLOW_FIELD')
    grab_entries=rows(log,'ENTRY')
    def same_state(r):
        current=by.get(r['frame'])
        if current is None:return False
        observed=max([entry['cycle']]+[q['cycle']for q in grab_entries if q['frame']<r['frame']])
        return(r['cycle']==cycle and current['cycle']==observed and
               {k:v for k,v in r.items()if k!='cycle'}=={k:v for k,v in current.items()if k!='cycle'})
    need([r['frame'] for r in continuation]==list(range(done['frame'],end+1)) and
         all(same_state(r) for r in continuation),
         'Independent ordinary continuation equals full callback stream')
    for r in [*continuation,regained]:
        need(all(r[k]==entry[k] for k in ('actor','main','vactor','vmain','id','vid','roster','vroster','schedule','stage')) and
             r['owner']==r['actor'] and r['vowner']==r['vactor'] and r['state']==0 and r['vstate']==1 and
             r['mode']==2 and r['hp']==entry['hp'] and 0<r['vhp']<=done['vhp'] and
             r['writes']==0 and r['assistance']=='none' and
             r['cpu_slot']==CPU_SLOT and r['human_slot']==HUMAN_SLOT,
             'Living unassisted original CPU/human ownership throughout ordinary continuation')
    for r in [*events,*instructions]:
        need(r['actor']==entry['actor'] and r['main']==entry['main'] and
             r['a8']==entry['actor'] and r['a13']==entry['main'] and r['cycle']==cycle and
             r['writes']==0 and r['assistance']=='none' and r['cpu_slot']==CPU_SLOT and r['human_slot']==HUMAN_SLOT,
             'Actual ordinary instructions execute under the owning native Main')
    need(regained['frame']==ready and regained['action']==0 and regained['y']==regained['floor'] and
         regained['vx']==regained['vy']==regained['gravity']==regained['trail']==0 and
         regained['flags']&0x1c==0 and regained['body']&0x0c==0,
         'Subsequent ordinary action really regains cleared grounded control')
    for kind,pc,offset,mask,opcode in (('body',0xff83eeb0,0x160,0x0c,0xb088),
                                      ('flags',0xff83efc0,0x210,0x14,0xb08d)):
        # The ordinary hit can clear its attack locks before the later walking
        # ready instruction. Require the real intervening cleanup AND the
        # ready-time native clear; the latter need not clear already-zero bits.
        need(any(n['cycle']==cycle and done['frame']<n['frame']<=ready and n['slot']==CPU_SLOT and n['kind']==kind and
                 n['pc']==pc and n['at']==entry['actor' if kind=='body' else 'main']+offset and
                 n['actor']==entry['actor'] and n['main']==entry['main'] and
                 n['a8']==entry['actor'] and n['a13']==entry['main'] and n['action']==0 and
                 n['before']&mask and n['after']==n['before']&(~mask&0xffff) and
                 (n['op0'],n['op1'])==(opcode,offset) for n in flags),
             'Later ordinary locks clear at original instruction with actual opcode and ownership')
        need(any(n['cycle']==cycle and n['frame']==ready and n['slot']==CPU_SLOT and n['kind']==kind and
                 n['pc']==pc and n['at']==entry['actor'if kind=='body'else'main']+offset and
                 n['actor']==entry['actor']and n['main']==entry['main']and n['a8']==entry['actor']and
                 n['a13']==entry['main']and n['action']==0 and n['after']==n['before']&(~mask&0xffff)and
                 (n['op0'],n['op1'])==(opcode,offset)for n in flags),
             'First later ready still executes the real original cleanup under its own Main')
    stores=[n for n in flags if n['cycle']==cycle and n['slot']==CPU_SLOT and n['kind']=='action' and
            done['frame']<=n['frame']<ready]
    current=done['action']
    for n in stores:
        register='a1' if n['pc']==0xff83c340 else 'a0'
        native_ordinary=(n['pc'],n['after']) in ((0xff83edd0,0),(0xff9065d0,0x303),(0xff83c340,0x106))
        native_recovery=(n['pc'],n['before'],n['after'],n['a0'])==(0xff83c340,0x106,0x600,6)
        need((native_ordinary or native_recovery) and
             n['before']==n['action']==current and n[register]&0xffff==n['after'] and
             (n['op0'],n['op1'])==((0xb02d if register=='a1' else 0xb00d),0x1f0) and
             n['at']==entry['main']+0x1f0 and n['actor']==entry['actor'] and n['main']==entry['main'] and
             n['a8']==entry['actor'] and n['a13']==entry['main'],
             'Continuous exact original ordinary state stores after paired completion')
        current=n['after']
    cursor=0;current=done['action']
    for at in range(done['frame']+1,ready+1):
        while cursor<len(stores) and stores[cursor]['frame']<at:
            current=stores[cursor]['after'];cursor+=1
        need(by.get(at,{}).get('action')==current,'Every ordinary callback matches state-store history')
    # The final ready executes later than its callback; its zero publication
    # and clean handoff are checked separately, not against pre-execution state.
    health=[r for r in rows(log,'HEALTH') if done['frame']<=r['frame']<end and r['slot']==HUMAN_SLOT]
    hp=done['vhp'];cursor=0
    for r in continuation:
        while cursor<len(health) and health[cursor]['frame']<r['frame']:
            n=health[cursor]
            need(n['before']==hp and 0<n['after']<=hp and n['pc']==0xff836700 and
                 n['a8']==entry['actor'] and n['a13']==entry['main'],
                 'Every ordinary follow-up victim health change executes in the original attacking CPU Main')
            hp=n['after'];cursor+=1
        if not any(n['frame']==r['frame'] for n in health):
            need(r['vhp']==hp,'No unlogged health changes after paired completion')
    return dict(kind='ordinary',first_ready=ready,continuation_fields=len(continuation),
                scope='actual_first_ordinary_followup_cleanup_not_signature_move_or_all_contacts')


def verify_cpu_flag_ledger(entry,fields,flags,terminal,need):
    """Replay every real CPU action/body/Main store against every callback.

    In particular an earlier ordinary hit cleanup is not a waiver for a later
    busy lock: no raw flag/action changes can appear without an owning native
    store, and both sides of every recorded store must remain continuous.
    """
    start,end=entry['frame'],terminal['frame']
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    need(hashlib.sha256(original).hexdigest().upper()=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23',
         'Actual original shared native store instruction program')
    by={r['frame']:r for r in fields if start<=r['frame']<=end}
    need(set(by)==set(range(start,end+1)),'Full CPU flag-ledger callback coverage')
    if set(by)!=set(range(start,end+1)):return
    for kind,offset in (('body',0x160),('flags',0x210),('action',0x1f0)):
        stores=[n for n in flags if n['slot']==CPU_SLOT and n['kind']==kind and start<=n['frame']<end]
        need(bool(stores),'Native CPU '+kind+' store ledger exists')
        current=by[start][kind];cursor=0
        for at in range(start,end):
            need(by[at][kind]==current,'Every raw CPU '+kind+' callback matches its complete native store history')
            while cursor<len(stores)and stores[cursor]['frame']==at:
                n=stores[cursor]
                need(n['before']==current and n['actor']==entry['actor']and n['main']==entry['main']and
                     n['a8']==entry['actor']and n['a13']==entry['main']and n['id']==entry['id']and
                     n['state']==0 and n['at']==entry['actor'if kind=='body'else'main']+offset and
                     0xff800000<=n['pc']<0xfffffff0,
                     'Continuous physically owned native CPU '+kind+' store operands and address')
                instruction_offset=(n['pc']-32-0xff800000)//8
                need(0<=instruction_offset<=len(original)-4 and struct.unpack_from('<HH',original,instruction_offset)==(n['op0'],n['op1']),
                     'Every shared native CPU '+kind+' store PC matches both actual original instruction words')
                current=n['after'];cursor+=1
        need(cursor==len(stores)and by[end][kind]==current,'Complete terminal CPU '+kind+' ledger')


def verify_repeated_stream(log,entry,fields,health,complete,terminal,need):
    start,end=entry['frame'],terminal['frame']
    by={r['frame']:r for r in fields if start<=r['frame']<=end}
    need(set(by)==set(range(start,end+1)),'All repeated-grab and intervening native callback fields')
    if set(by)!=set(range(start,end+1)):return {}
    entries=rows(log,'ENTRY')
    for r in by.values():
        observed=max([entry['cycle']]+[q['cycle']for q in entries if q['frame']<r['frame']])
        need(r['cycle']==observed and all(r[k]==entry[k]for k in ('actor','main','vactor','vmain','id','vid','roster','vroster','stage','schedule'))and
             r['owner']==r['actor']and r['vowner']==r['vactor']and r['state']==0 and r['vstate']==1 and
             r['mode']==2 and r['hp']==entry['hp']and r['vhp']>0 and r['cpu_slot']==CPU_SLOT and
             r['human_slot']==HUMAN_SLOT and r['writes']==0 and r['assistance']=='none',
             'Exact living physical CPU/human ownership and real entry ordinals throughout repetitions')
    independent=[r for r in rows(log,'FOLLOW_FIELD')if start<=r['frame']<=end]
    first=max(start,complete[0]['frame'])
    need([r['frame']for r in independent]==list(range(first,end+1)),'Every repeated-pair independent continuation callback')
    for r in independent:
        current=by[r['frame']];completed=max(q['cycle']for q in complete if q['frame']<=r['frame'])
        need(r['cycle']==completed and {k:v for k,v in r.items()if k!='cycle'}=={k:v for k,v in current.items()if k!='cycle'},
             'Independent continuation matches every actual state while completed and current ordinals stay distinct')
    for slot,key in ((CPU_SLOT,'hp'),(HUMAN_SLOT,'vhp')):
        current=by[start][key];stores=[r for r in health if r['slot']==slot and start<=r['frame']<end];cursor=0
        for at in range(start,end):
            need(by[at][key]==current,'Continuous whole repeated-pair native health ledger')
            while cursor<len(stores)and stores[cursor]['frame']==at:
                n=stores[cursor]
                need(n['pc']==0xff836700 and n['before']==current and 0<n['after']<=n['before']<=161 and
                     n['a8']in(entry['actor'],entry['vactor'])and n['a13']in(entry['main'],entry['vmain'])and
                     n['cpu_slot']==CPU_SLOT and n['human_slot']==HUMAN_SLOT and n['writes']==0 and n['assistance']=='none',
                     'Every repeated-pair health store is real owned original collision code')
                current=n['after'];cursor+=1
        need(cursor==len(stores)and by[end][key]==current,'All health changes through terminal observation explained')
    return dict(kind='real_repeated_pair_stream',callbacks=len(by),completed_pairs=len(complete),ordinaryFollowupSubstituted=False)

def verify_log(log,player):
    try:
        completed=rows(log,'COMPLETE')
        proofs=[_verify_log(log,player,q['cycle'])for q in completed]
        errors=list(dict.fromkeys(error for p in proofs for error in p['errors']))
        if len(proofs)<2:errors.append('Two completed actual pairs required')
        if not proofs:return dict(passed=False,errors=errors,whole_character_integration_complete=False)
        return dict(**{k:v for k,v in proofs[0].items()if k not in ('passed','errors')},
                    passed=not errors,errors=errors,pairs=proofs,repeatedPairsAccepted=not errors,
                    allSubsequentCPUMovesAccepted=False)
    except (ValueError,KeyError,IndexError,TypeError)as error:
        return dict(passed=False,errors=['Malformed/incomplete real repeated-pair evidence: '+str(error)],whole_character_integration_complete=False)
