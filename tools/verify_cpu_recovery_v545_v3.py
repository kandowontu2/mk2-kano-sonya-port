"""Actual native CPU paired contact, every held pose, fling and both recoveries.

Natural cold P2 CPU/P1 human paired recovery at original individual ready handoffs.
Not all victims, interruptions, KO continuations, CPU moves, pixels or audio.
"""
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path

from verify_p2_campaign import expected_orders
from cpu_followup_contract_v545_v2 import verify as verify_followup
from verify_restart_pair import SPECS,CHOKE_OWN,CHOKE_XY,CHOKE_GROUPS,CHOKE_GRIP,LEG_OWN,LEG_XY,LEG_GROUPS
from verify_native_candidate_v545 import ROOT,NAME,EXE,PAYLOAD,matched

HEX=set('actor main owner pose list xraw yraw vx vy gravity flags body facing trail vactor vmain vowner vpose vlist vxraw vyraw vvx vvy vgravity vflags vbody vfacing vtrail schedule table pc entry victim group word a0 a1 a2 a3 a8 a9 a10 a13 a6 actor_at main_at id_at state_at hp_at'.split())
TEXT={'kind','ids','buttons','scope','assistance','human','phase','move'}
HUMANS=dict(kano=17,sonya=18,liu_kang=1,kung_lao=0,cage=2,baraka=3,kitana=4,mileena=5,shang_tsung=6,raiden=7,sub_zero=8,reptile=9,scorpion=10,jax=11)
SCOPE='natural_P2_CPU_full_pair_original_individual_ready_handoffs_and_native_followup_not_all_victims_KO_pixels_audio_or_full_goal'


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


def ordinary_followup(log,entry,own,done,fields,flags,need):
    """Original next-action state ledger and cleanup, not full move art fidelity."""
    cycle=done['cycle'];terminal=rows(log,'RESULT')[0]
    regains=rows(log,'FOLLOW_REGAIN');ready=rows(log,'FOLLOW_READY_INSTRUCTION')
    need(len(regains)==1 and len(ready)==2,'Actual first ordinary follow-up cleanup and regain are observed')
    if len(regains)!=1 or len(ready)!=2:return {}
    regain=regains[0];end=regain['frame']
    need(end>done['frame'] and terminal['follow_regain']==end and terminal['frame']==end+30,
         'Full ordinary continuation observed past paired completion and its first regain')
    need([(r['kind'],r['entry'],r['pc'],r['frame'])for r in ready]==
         [('recovery',0xff861350,0xff861360,end),('regained',0xff861500,0xff861510,end)],
         'First original owning ready and regain, not a later coincidental pose')
    for r in [*ready,regain]:
        need(r['cycle']==cycle and r['actor']==entry['actor'] and r['main']==entry['main'] and
             r['cpu_slot']==2 and r['human_slot']==1 and r['writes']==0 and r['assistance']=='none',
             'Actual physical P2 CPU owns every ordinary follow-up handoff')
        if 'a8' in r:need(r['a8']==entry['actor'] and r['a13']==entry['main'],'Executing native ordinary ready registers')
    need(regain['action']==0 and regain['y']==regain['floor'] and
         regain['vx']==regain['vy']==regain['gravity']==regain['trail']==0 and
         regain['flags']&0x1c==0 and regain['body']&0x0c==0,'Ordinary next action fully detaches and cleans at original ready')
    selected=[n for n in flags if n['cycle']==cycle and n['slot']==2 and
              n['kind']=='action' and own['frame']<=n['frame']<=end]
    need(bool(selected) and selected[0]['frame']==own['frame'] and
         selected[0]['before']==(0x111 if entry['id']==17 else 0x110) and selected[0]['after']==0,
         'Paired state clears at first owning regain')
    current=0x111 if entry['id']==17 else 0x110;previous=own['frame']
    for n in selected:
        register='a1' if n['pc']==0xff83c340 else 'a0'
        opcode=0xb02d if register=='a1' else 0xb00d
        allowed=(n['pc']==0xff83edd0 and n['after']==0 or
                 n['pc']==0xff9065d0 and n['after']==0x303 or
                 n['pc']==0xff83c340 and (n['after'] in (0x104,0x106) or
                 (n['before'],n['after']) in ((0x104,0x60c),(0x106,0x600))))
        need(allowed and n['actor']==entry['actor'] and n['main']==entry['main'] and
             n['a8']==entry['actor'] and n['a13']==entry['main'] and
             n['at']==entry['main']+0x1f0 and n['action']==n['before']==current and
             n[register]&0xffff==n['after'] and (n['op0'],n['op1'])==(opcode,0x1f0) and
             n['state']==0 and n['id']==entry['id'] and n['frame']>=previous,
             'Continuous actual ordinary action-store opcode/register/owner ledger')
        current=n['after'];previous=n['frame']
    by={r['frame']:r for r in fields if own['frame']<r['frame']<=end}
    need(len(by)==end-own['frame'] and set(by)==set(range(own['frame']+1,end+1)),
         'Every ordinary continuation callback is present')
    cursor=0;current=0x111 if entry['id']==17 else 0x110
    for at in range(own['frame']+1,end+1):
        while cursor<len(selected) and selected[cursor]['frame']<at:
            current=selected[cursor]['after'];cursor+=1
        r=by[at]
        need(r['action']==current and all(r[k]==entry[k]for k in ('actor','main','vactor','vmain')) and
             r['id']==r['roster']==entry['id'] and r['vid']==r['vroster']==entry['vid'] and
             r['owner']==r['actor'] and r['vowner']==r['vactor'] and r['state']==0 and r['vstate']==1 and
             r['mode']==2 and r['hp']==entry['hp'] and r['vhp']>0,
             'Every post-grab callback retains actual identities and agrees with native stores')
    setup_frames=[]
    for field,pc,mask,offset in (('body',0xff838cf0,4,0x160),('flags',0xff877d50,0x10,0x210)):
        setters=[n for n in flags if n['cycle']==cycle and n['slot']==2 and own['frame']<n['frame']<end and
                 n['kind']==field and n['pc']==pc and n['actor']==entry['actor'] and n['main']==entry['main'] and
                 n['a8']==entry['actor'] and n['a13']==entry['main'] and
                 n['at']==(entry['actor']if field=='body'else entry['main'])+offset and
                 not n['before']&mask and n['after']==n['before']|mask]
        need(len(setters)==1,'One NEW original next-action lock setup after paired cleanup')
        if setters:setup_frames.append(setters[0]['frame'])
    need(len(setup_frames)==2 and len(set(setup_frames))==1,'Actual original body/Main next-action setup occurs together')
    cleanup_frames=[]
    for field,pc,mask,offset in (('body',0xff83eeb0,0x0c,0x160),('flags',0xff83efc0,0x14,0x210)):
        clears=[n for n in flags if n['cycle']==cycle and n['slot']==2 and
                 setup_frames and max(setup_frames)<n['frame']<=end and n['kind']==field and
                 n['pc']==pc and n['actor']==entry['actor'] and n['main']==entry['main'] and
                 n['a8']==entry['actor'] and n['a13']==entry['main'] and
                 n['at']==(entry['actor']if field=='body'else entry['main'])+offset and
                 n['action']==0 and n['before']&mask and n['after']==n['before']&(~mask&0xffff)
                 ]
        need(len(clears)==1,'Original ordinary follow-up clears its own actual new locks once')
        if clears:cleanup_frames.append(clears[0]['frame'])
        ledger=[n for n in flags if n['cycle']==cycle and n['slot']==2 and
                own['frame']<=n['frame']<=end and n['kind']==field]
        need(bool(ledger),'Full original body/Main store ledger required')
        if not ledger:continue
        value=ledger[0]['before'];previous=own['frame']
        for n in ledger:
            need(n['before']==value and n['frame']>=previous and n['actor']==entry['actor'] and
                 n['main']==entry['main'] and n['a8']==entry['actor'] and n['a13']==entry['main'] and
                 n['at']==(entry['actor']if field=='body'else entry['main'])+offset and
                 ((n['pc']==pc and n['after']==value&(~mask&0xffff)) or
                  (n['pc']==(0xff838cf0 if field=='body'else 0xff877d50) and
                   n['after']==value|(4 if field=='body'else 0x10))),
                 'Every native ordinary body/Main store is continuous and owned setup or cleanup')
            value=n['after'];previous=n['frame']
        cursor=0;value=ledger[0]['before']
        for at in range(own['frame']+1,end+1):
            while cursor<len(ledger) and ledger[cursor]['frame']<at:
                value=ledger[cursor]['after'];cursor+=1
            need(by[at][field]==value,'Every ordinary callback matches actual body/Main store ledger')
    need(len(cleanup_frames)==2 and len(set(cleanup_frames))==1,
         'Both ordinary attack locks clear together before original ready')
    need(not any(r['kind']=='action'for r in rows(log,'FOLLOW_INSTRUCTION')),
         'Ordinary profile must not substitute for an actual new special')
    return dict(move='ordinary',ready=end,attack_cleanup=cleanup_frames[0] if cleanup_frames else None,native_state_stores=len(selected),
                scope='full_paired_grab_and_original_next_action_lock_cleanup_not_complete_ordinary_move_pose_or_damage_fidelity')


def _verify_log(log,player,follow_move):
    errors=[]
    def need(ok,label):
        if not ok and label not in errors:errors.append(label)
    fields,entries,events,health,complete,results=[rows(log,t) for t in ('FIELD','ENTRY','EVENT','HEALTH','COMPLETE','RESULT')]
    need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|stack traceback',log,re.I),'No emulator or Lua observer error')
    need(len(complete)==len(results)==1 and bool(entries),'Actual paired completion/result/entry required')
    need(len(results)==1 and results[0].get('schema')==10,'Unambiguous opposite-slot schema 10 including physical global-pointer bindings required')
    need(all(r.get('cpu_slot')==2 and r.get('human_slot')==1 and r.get('writes')==0 and r.get('assistance')=='none' for tag in ('ROM','BIND','FIELD','ENTRY','EVENT','HEALTH','COMPLETE','RESULT','INPUT','INCOMPLETE','OWN_REGAIN','VICTIM_REGAIN') for r in rows(log,tag)),'Read-only observations and input-only natural scope')
    orders=expected_orders();roms=rows(log,'ROM')
    need(len(roms)==6 and [r.get('order') for r in roms]==list(range(6)) and all(r.get('table')==0xfffa2c00 and r.get('list')==0xfffa3000+i*0x180 and tuple(map(int,r.get('ids','').split(',')))==orders[i] for i,r in enumerate(roms)),'Every native order equals original stock ladder plus both actual new IDs')
    select=rows_prefix(log,'MK2_P2CPU_SELECT_RESULT ')
    cold=rows_prefix(log,'MK2_P2CPU_COLD_LIVE ')
    css_rows=rows_prefix(log,'MK2_P2CPU_SELECT_CSS ')
    need(len(css_rows)==1 and css_rows[0]['slot']==1 and css_rows[0]['human']==player,
         'Actual cold human P1 selection, never a relabeled P2 fixture')
    need(len(select)==len(cold)==1,'One real cold P1-only selection and native CPU fight')
    for r in [*select,*cold,*rows_prefix(log,'MK2_P2CPU_BOOT_STATE '),*rows_prefix(log,'MK2_P2CPU_SELECT_CSS ')]:
        need(r.get('writes')==0 and r.get('assistance')=='none','Cold selection inputs only; no proxy or health/stage fixture')
    if select and cold:
        sel,c=select[0],cold[0]
        need(sel['human']==c['human']==player and sel['human_id']==c['human_id']==HUMANS[player] and
             700<sel['css']<sel['exit']<sel['live']==c['frame'] and
             sel['checks']>=30 and sel['errors']==0 and sel['initial_cpu']==c['cpu_id'],
             'Actual P1 selection holds true identity then enters native P2 CPU fight')
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
    bindings=rows(log,'BIND')
    addresses={1:(0x01060220,0x01060260,0x01060280,0x010601f0,0x010602f0),
               2:(0x01060df0,0x01060e30,0x01060e50,0x01060dc0,0x01060ec0)}
    full_callbacks=[r for r in fields if start<r['frame']<=results[0]['frame']]
    full_by={r['frame']:r for r in full_callbacks}
    need(len(full_callbacks)==len(full_by)==results[0]['frame']-start and
         set(full_by)==set(range(start+1,results[0]['frame']+1)),
         'Every actual callback through final bounded observation is present')
    for r in full_callbacks:
        samples=[n for n in bindings if n['frame']==r['frame']]
        need(len(samples)==2 and {n['slot'] for n in samples}=={1,2},'Every paired callback independently binds both actual physical slots')
        for n in samples:
            slot=n['slot'];prefix='' if slot==2 else 'v'
            need(slot in addresses and tuple(n[k] for k in ('actor_at','main_at','id_at','state_at','hp_at'))==addresses.get(slot) and
                 n['cycle']==cycle and all(n[k]==r[prefix+k] for k in ('actor','main','id','roster','state','hp')),
                 'Native slot-global pointers, roster, human/CPU state and health agree with callback owners')
        for prefix,xkey,ykey in (('','x','y'),('v','vxpos','vypos')):
            def coordinate(value):
                n=(value>>16)&0xffff
                return n-0x10000 if n&0x8000 else n
            need(r[xkey]==coordinate(r[prefix+'xraw']) and r[ykey]==coordinate(r[prefix+'yraw']),
                 'Every original raw/integer participant coordinate agrees')
    later_stores=[r for r in health if start<r['frame']<results[0]['frame']]
    need(all(r['pc']==0xff836700 and r['slot']in(1,2) and 0<=r['after']<=r['before']<=161 and
             r['a8']in(entry['actor'],entry['vactor']) and
             r['a13']in(entry['main'],entry['vmain']) for r in later_stores),
         'Every health store through terminal observation is original and physically owned')
    for at in range(start+1,results[0]['frame']):
        for slot,key in ((2,'hp'),(1,'vhp')):
            changes=[r for r in later_stores if r['frame']==at and r['slot']==slot]
            if changes:
                need(changes[0]['before']==full_by[at][key] and changes[-1]['after']==full_by[at+1][key] and
                     all(a['after']==b['before']for a,b in zip(changes,changes[1:])),
                     'Whole continuing physical-slot health ledger matches adjacent callbacks')
            else:need(full_by[at][key]==full_by[at+1][key],'No unlogged post-grab health changes')
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
        if r['kind']=='velocity':need(r['a1']==0x010602d0,'Every native victim velocity request targets the actual P1 slot')
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
                need(r.get('flags',0)&0x1c==0x10 and r.get('body',0)&0x0c==4 and
                     r.get('vflags',0)&0x1c==4 and r.get('vbody',0)&0x0c==0,
                     'Every held field retains actual own attack and victim paired locks')
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
            need(r.get('flags',0)&0x1c==0x10 and r.get('body',0)&0x0c==4 and
                 r.get('vflags',0)&0x1c==4 and r.get('vbody',0)&0x0c==0,
                 'Every held field retains actual own attack and victim paired locks')
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
    need(clean(done,'v') and done['action']!=spec['state'] and done['vaction']!=spec['victim_state'],'Final living victim remains grounded and detached; CPU is no longer in the paired action')
    flags=flag_rows(log)
    handoffs={};followup_proof={}
    for tag,prefix,slot in (('OWN_REGAIN','',2),('VICTIM_REGAIN','v',1)):
        records=[r for r in rows(log,tag) if r['cycle']==cycle]
        kind='own_regain'if slot==2 else'victim_regain'
        need(len(records)==len(event(kind))==1,'Each owning Main has one first native post-cleanup handoff')
        if not records or not event(kind):continue
        r,e=records[0],event(kind)[0];handoffs[slot]=r
        need(r['frame']==e['frame'] and r['action'if slot==2 else'vaction']==0 and
             clean(r,prefix) and r[prefix+'vx']==0,
             'Actual original ready handoff is fully cleared, stopped, grounded and detached for its own actor')
        need(any(n['frame']==r['frame'] for n in event('own_ready'if slot==2 else'victim_ready')),
             'Original ready entry and post-cleanup handoff occur under the same real Main in the same field')
        target_actor=entry['actor'if slot==2 else'vactor'];target_main=entry['main'if slot==2 else'vmain']
        for field,pc,at,mask in (('body',0xff83eeb0,target_actor+0x160,0x0c),('flags',0xff83efc0,target_main+0x210,0x14)):
            need(any(n['cycle']==cycle and n['slot']==slot and n['frame']==r['frame']and
                     n['kind']==field and n['pc']==pc and n['at']==at and
                     n['actor']==target_actor and n['main']==target_main and n['a8']==target_actor and
                     n['a13']==target_main and n['after']==n['before']&(~mask&0xffff)
                     for n in flags),'Actual original body/Main cleanup stores precede each owning ready handoff')
    if len(handoffs)==2:
        own,victim=handoffs[2],handoffs[1]
        need(own['frame']-release in ((13,14)if target=='kano'else(9,10)),
             'Complete original own recovery holds end at the native ready handoff')
        need(release<victim['frame']<end and own['frame']<end and end==max(own['frame'],victim['frame'])+1,
             'Completion follows both actual individual handoffs, not a later coincidental clean pose')
        if follow_move=='ordinary':
            followup_proof=ordinary_followup(log,entry,own,done,fields,flags,need)
        else:
            followup_proof=verify_followup(log,player,follow_move,entry,own,victim,done,fields,flags,need,rows,cpu_slot=2)
    need(all(r.get('writes')==0 and r.get('assistance')=='none' and r.get('cpu_slot')==2 and r.get('human_slot')==1 for r in flags),
         'Every flag-store observer declares actual read-only native scope')
    # Both actor roles must return through native ready, with live grounded cleanup.
    need(any(release<=r['frame']<end for r in event('own_ready')) and any(release<r['frame']<end for r in event('victim_ready')),'Both actual owning Main processes return through native ready code')
    need(results[0]['complete']==end and results[0]['frame']==results[0]['follow_regain']+30 and results[0]['cycles']==len(entries),'Terminal observation declares exact actual completed cycle and later bounded follow-up')
    return dict(passed=not errors,errors=errors,target=target,player=player,cycle=cycle,start=start,release=release,complete=end,paired_fields=len(timeline),held_fields=held_fields,victim_flight_fields=len(flight),damage=spec['damage'],observed_cycles=len(entries),CPU_slot=2,human_slot=1,own_handoff=handoffs.get(2,{}).get('frame'),victim_handoff=handoffs.get(1,{}).get('frame'),native_cleanup_store_rows=len(flags),native_followup=followup_proof,completed_cycle_scope='only_declared_uninterrupted_completed_pair_other_misses_interruptions_and_later_entries_not_claimed_complete',scope=SCOPE,whole_character_integration_complete=False)


def verify_log(log,player,follow_move):
    try:return _verify_log(log,player,follow_move)
    except (ValueError,KeyError,IndexError,TypeError)as error:
        return dict(passed=False,errors=['Malformed/incomplete actual evidence: '+str(error)],scope=SCOPE,whole_character_integration_complete=False)


def verify(folder,player,follow_move):
    proof=verify_log((folder/'run.log').read_text(encoding='utf-8-sig'),player,follow_move)
    errors=proof['errors']
    try:
        launch_inputs={}
        matched(folder,launch_inputs)
    except (AssertionError,ValueError,KeyError,OSError,TypeError) as error:
        errors.append('Exact v545 launch inventory: '+str(error))
    meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    if (meta.get('exit_code'),meta.get('candidate'),meta.get('executable_sha256'),meta.get('payload_sha256'),meta.get('player'),meta.get('cpu_slot'),meta.get('human_slot'),meta.get('assistance'))!=(0,NAME,EXE,PAYLOAD,player,2,1,'none'):errors.append('Exact current terminal native case identity')
    if before!=meta.get('input_hashes'):errors.append('Frozen before/after observed launch inputs')
    for file,expected in before.items():
        path=Path(file)
        if path.suffix.lower()in('.lua','.ps1','.json'):path=folder/'input_sources'/path.name
        if not path.is_file()or hashlib.sha256(path.read_bytes()).hexdigest().upper()!=expected:errors.append('Exact frozen launch input: '+str(path))
    build=json.loads((folder/'input_sources/build-info.json').read_text(encoding='utf-8-sig'))
    for file,expected in build['input_hashes'].items():
        path=Path(file)
        if not path.is_file()or hashlib.sha256(path.read_bytes()).hexdigest().upper()!=expected:errors.append('Exact current build input: '+file)
    probe=(folder/'input_sources/mk2ks_cpu_recovery_probe_v7.lua').read_text()
    if re.search(r':write_|\.value\s*=(?!=)|load_state|loadstate',probe):errors.append('New CPU pair observer must never write guest state')
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    if hashlib.sha256(original).hexdigest().upper()!='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23' or any(struct.unpack_from('<H',original,(at-0xff800000)//8)[0]!=opcode for at,opcode in ((0xff83bb00,0x9720),(0xff835470,0x9401),(0xff861500,0xb5a4),(0xff83ee90,0xb088),(0xff83efa0,0xb08d),(0xff838cd0,0xb1c8),(0xff877d30,0xb08d),(0xff83c320,0xb02d),(0xff83c330,0x01f0),(0xff9065b0,0xb00d),(0xff9065c0,0x01f0),(0xff83edb0,0xb00d),(0xff83edc0,0x01f0),(0xff877ba0,0xb02d),(0xff877bb0,0x01f0),(0xff876440,0xb02d),(0xff876450,0x01f0),(0xff83df00,0x05a0),(0xff83df10,0xecd0),(0xff83df20,0x0105),(0xff870830,0x09c1),(0xff870840,0x060c),(0xff870920,0x09c1),(0xff870930,0x0106),(0xff870a70,0x09c1),(0xff870a80,0x0600))):errors.append('Original native sequence/collision descriptor read instructions and exact stock kick recovery values')
    proof.update(passed=not errors,checked_inputs=len(before)+len(build['input_hashes']))
    return proof


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('case',type=Path);parser.add_argument('player')
    parser.add_argument('move',choices=('blade','bicycle','square','ordinary'));parser.add_argument('--output',type=Path)
    args=parser.parse_args();proof=verify(args.case,args.player,args.move)
    if args.output:
        if args.output.exists():raise SystemExit('Refusing to overwrite evidence')
        args.output.write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps(proof,indent=2));raise SystemExit(0 if proof['passed'] else 1)
