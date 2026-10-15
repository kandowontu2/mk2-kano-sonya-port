"""Independently check full P1/P2 completion followed by a fresh P1/P2 game."""
import argparse
import json
import re
from pathlib import Path

IDS={'kano':17,'sonya':18}

def verify(log,fighter,target,source_side=1,new_side=1,special_mode='none',air_followup=False):
    errors=[]
    if air_followup and special_mode!='airthrow':errors.append('Air follow-up requires actual airthrow mode')
    own,new=IDS[fighter],IDS[target]
    def one(pattern,label):
        rows=re.findall(pattern,log)
        if len(rows)!=1:errors.append(label+' must occur exactly once');return None
        return rows[0]
    if source_side not in (1,2):raise ValueError('Invalid ending source side')
    if new_side not in (1,2):raise ValueError('Invalid fresh game side')
    if source_side==2 or new_side==2:
        boot=one(r'MK2_RESTART_BOOT source=(\w+) target=(\w+) restart_writes=(\d+) source_side=(\d+) new_side=(\d+)','Restart side scope')
        if boot!=(fighter,target,'0',str(source_side),str(new_side)):errors.append('Wrong ending/new-game player scope')
    if source_side==2:
        from verify_p2_tower import verify as verify_tower
        tower=verify_tower(log,fighter)
        errors.extend('P2 tower: '+error for error in tower['errors'])
    summary=one(r'MK2KS_MULTI_FINAL frame=(\d+) last_stage=(\d+) wins=([^ ]+) identity_checks=(\d+) identity_errors=(\d+) stage_errors=(\d+) ended=(\w+) completed=(\w+) diagnostic=(\w+),(\w+)', 'Full tower summary') if source_side==1 else None
    if summary:
        _,stage,wins,checks,identity_errors,stage_errors,ended,complete,di,ds=summary
        actual={int(a):int(b) for a,b in re.findall(r'(\d+):(\d+)',wins)}
        required={i:2 for i in (*range(13),14,15)};required[16]=1
        if (actual!=required or int(stage)!=16 or int(checks)<10000 or identity_errors!='0' or stage_errors!='0' or
            (ended,complete,di,ds)!=('true','true','false','false')):
            errors.append('Full native tower completion/identity coverage not proven')
    attract=one(r'MK2_RESTART_ATTRACT frame=(\d+) source=(\w+) mode=(\d+) roster=(\d+) pictures=(\d+),(\d+) texts=(\d+),(\d+)', 'Actual post-ending attract')
    css=one(r'MK2_RESTART_CSS frame=(\d+) initial=(\d+) target=(\d+) route=([^\r\n]*)','Fresh CSS')
    match=one(r'MK2_RESTART_MATCH frame=(\d+) target=(\w+) id=(\d+) actor=([0-9A-F]+) stage=(\d+)','Fresh match')
    done=one(r'MK2_RESTART_COMPLETE frame=(\d+) source=(\w+) target=(\w+) live=(\d+) errors=(\d+) restart_writes=(\d+)','Restart completion')
    result=one(r'MK2_RESTART_RESULT pass=(\w+) source=(\w+) target=(\w+) ended=(\d+) css=(\d+) match=(\d+) live=(\d+) errors=(\d+) pictures=(\d+),(\d+) texts=(\d+),(\d+) restart_writes=(\d+)','Restart observer summary')
    if attract:
        end,source,mode,roster,*counts=attract
        if source_side==2:
            completion=one(r'MK2_P2_TOWER_COMPLETED frame=(\d+) ending_age=(\d+) mode=(\d+) roster=(\d+),(\d+) pictures=(\d+),(\d+) texts=(\d+),(\d+)','P2 completion before restart')
            if completion and (completion[0]!=end or completion[4]!=roster):
                errors.append('Restart does not follow actual P2 completed ending')
        if source!=fighter or mode!='11' or int(roster)==own or list(map(int,counts))!=[1,1,3,3]:
            errors.append('Wrong or incomplete own ending/attract state')
        for kind,expected_counts in (('PICTURE',[1,1]),('TEXT',[3,3])):
            rows=re.findall(r'MK2_RESTART_'+kind+r' frame=(\d+) page=(\d+) id=(\d+) pc=([0-9A-F]+) value=([0-9A-F]+)',log)
            counts=[0,0]
            for field,page,identity,pc,value in rows:
                if int(page) not in (1,2) or int(identity)!=own or int(field)>=int(end) or not 0xff800000<=int(pc,16)<=0xffffffff:
                    errors.append('Wrong actual own ending fetch');continue
                counts[int(page)-1]+=1
            if counts!=expected_counts:errors.append('Missing actual '+kind+' page fetches')
    if attract and css and match and done:
        ef,cf,mf,df=map(int,(attract[0],css[0],match[0],done[0]))
        if not ef+240<=cf<cf+176<mf<df or df-mf!=600:
            errors.append('Fresh-game event chronology/600-field combat coverage invalid')
        if int(css[2])!=new or match[1]!=target or int(match[2])!=new or match[4]!='0' or not 0x01000000<=int(match[3],16)<0x01100000:
            errors.append('Fresh-game target/actor/ladder reset incorrect')
        highlights=re.findall(r'MK2_RESTART_HIGHLIGHT frame=(\d+) age=(\d+) target=(\d+) roster=(\d+)',log)
        if highlights!=[(str(cf+age),str(age),str(new),str(new)) for age in (140,156)]:
            errors.append('Actual fresh target highlighting not proven')
        if done[1:3]!=(fighter,target) or list(map(int,done[3:]))!=[601,0,0]:
            errors.append('Live restart coverage/errors/assistance incorrect')
        if result and result!=('true',fighter,target,str(ef),str(cf),str(mf),'601','0','1','1','3','3','0'):
            errors.append('Observer result contradicts independently checked events')
        if source_side==2 or new_side==2:
            from verify_p2_campaign import expected_orders
            orders=expected_orders()
            cpus=re.findall(r'MK2_RESTART_CPU frame=(\d+) state=(\d+) roster=(\d+) id=(\d+) actor=([0-9A-F]+) order=(\d+) schedule=([0-9A-F]+) expected=(\d+)',log)
            if len(cpus)!=2 or [int(c[0]) for c in cpus]!=[mf,df]:
                errors.append('Fresh CPU ownership/P2 participation coverage missing')
            else:
                for field,state,roster,identity,actor,order,schedule,expected in cpus:
                    n=int(order)
                    if (n not in range(6) or state!='0' or not 0x01000000<=int(actor,16)<0x01100000 or
                        int(schedule,16)!=0xfffa3000+n*0x180 or
                        (int(roster),int(identity),int(expected))!=(orders[n][0],)*3):
                        errors.append('Fresh CPU is not the native schedule or P2 participation retained')
                if cpus[0][1:]!=cpus[1][1:]:errors.append('Fresh CPU ownership/schedule changed')
            if new_side==2:
                tagged=re.findall(r'MK2_RESTART_CPU[^\r\n]* cpu_side=(\d+)',log)
                if tagged!=['1','1']:errors.append('Fresh P2 game must have native P1 CPU ownership')
    if 'MK2KS_EXIT_RESULT pass=true ' not in log or 'MK2KS_STABILITY stalled_frames=0 trap_frames=0' not in log:
        errors.append('Original campaign/display/stability acceptance missing')
    shadow=one(r'MK2_RESTART_SHADOW target=(\w+) matched=(\d+) expected=(\d+) pass=(\w+)','Fresh target name shadow')
    if shadow and (shadow[0]!=target or int(shadow[1])<=20 or shadow[1]!=shadow[2] or shadow[3]!='true'):
        errors.append('Fresh target name/native shadow not proven')
    if re.search(r'MK2_RESTART_ERROR|\[LUA ERROR\]|fatal error|access violation',log,re.I):errors.append('Actual run errors')
    if special_mode not in ('none','projectile','mobility','sequence','pair','airthrow','lifecycle','mobility_contact','projectile_choreography'):raise ValueError('Invalid special mode')
    if special_mode=='projectile':
        from verify_restart_projectile import verify as verify_projectile
        projectile=verify_projectile(log,target,new_side)
        errors.extend('Projectile: '+error for error in projectile['errors'])
    if special_mode=='mobility':
        from verify_restart_mobility import verify as verify_mobility
        mobility=verify_mobility(log,target,new_side)
        errors.extend('Mobility: '+error for error in mobility['errors'])
    if special_mode=='sequence':
        from verify_restart_sequence import verify as verify_sequence
        sequence=verify_sequence(log,target,new_side)
        errors.extend('Sequence: '+error for error in sequence['errors'])
    if special_mode=='pair':
        from verify_restart_pair import verify as verify_pair
        pair=verify_pair(log,target,new_side)
        errors.extend('Pair: '+error for error in pair['errors'])
    if special_mode=='airthrow':
        from verify_restart_airthrow import verify as verify_airthrow
        airthrow=verify_airthrow(log,target,new_side,require_followup=air_followup)
        errors.extend('Air throw: '+error for error in airthrow['errors'])
    if special_mode=='lifecycle':
        from verify_restart_lifecycle import verify as verify_lifecycle
        lifecycle=verify_lifecycle(log,target,new_side)
        errors.extend('Joined lifecycle: '+error for error in lifecycle['errors'])
    if special_mode=='mobility_contact':
        from verify_restart_lifecycle import verify_mobility_join
        contact=verify_mobility_join(log,target,new_side)
        errors.extend('Joined mobility contact: '+error for error in contact['errors'])
    if special_mode=='projectile_choreography':
        from verify_restart_lifecycle import verify_projectile_join
        from verify_projectile_choreography import verify_contact
        contact=verify_projectile_join(log,target,new_side,True,contact_verifier=verify_contact)
        errors.extend('Joined full projectile choreography: '+error for error in contact['errors'])
    return {'passed':not errors,'errors':errors,'fighter':fighter,'target':target,
            'tower_assistance':'health_only','restart_assistance':'none','unassisted_tower_clear_proven':False,
            'source_side':source_side,'new_game_side':new_side,
            'special_mode':special_mode,
            'scope':f'full_p{source_side}_endings_to_fresh_p{new_side}_game_not_all_restart_modes'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('log',type=Path)
    parser.add_argument('--fighter',choices=IDS,required=True);parser.add_argument('--target',choices=IDS,required=True)
    parser.add_argument('--source-side',type=int,choices=(1,2),default=1)
    parser.add_argument('--new-side',type=int,choices=(1,2),default=1)
    parser.add_argument('--special-mode',choices=('none','projectile','mobility','sequence','pair','airthrow','lifecycle','mobility_contact','projectile_choreography'),default='none')
    parser.add_argument('--air-followup',action='store_true')
    args=parser.parse_args();result=verify(args.log.read_text(encoding='utf-8-sig'),args.fighter,args.target,args.source_side,args.new_side,args.special_mode,args.air_followup)
    print(json.dumps(result,indent=2));raise SystemExit(0 if result['passed'] else 1)

if __name__=='__main__':main()
