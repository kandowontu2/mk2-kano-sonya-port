"""Current close-pair/air-throw regressions through actual endings and joins.

Health assistance belongs only to the source campaign. This is not proof of
unassisted tower completion, CPU paired choreography or complete integration.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

from verify_post_ending_restart import verify as restart
from check_post_restart_assistance import verify as assistance
from verify_p2_campaign import expected_orders
from verify_current_post_ending_choreography import CANDIDATE, EXE_SHA, PAYLOAD_SHA
from verify_restart_pair import CHOKE_OWN


def choke_holds(log):
    """Every held paired field, not just the first field of each native step.

    The existing native-pair verifier independently checks each step anchor's
    original grip/pose and the separate release/flight/recovery chain. Between
    those anchors neither the held pose nor paired coordinates may drift.
    """
    rows=[dict(re.findall(r'(\w+)=([^\s]+)',s)) for s in log.splitlines()
          if s.startswith('MK2_RESTART_PAIR_STATE ')]
    steps=[dict(re.findall(r'(\w+)=([^\s]+)',s)) for s in log.splitlines()
           if s.startswith('MK2_RESTART_PAIR_EVENT ') and ' kind=step ' in s]
    errors=[]
    keys=('pose','vpose','action','vaction','x','y','vx','vy','vxpos','vypos','vvx','vvy')
    for cycle in sorted({r['cycle'] for r in steps}):
        frames={int(r['frame']):r for r in rows if r['cycle']==cycle}
        own=[int(r['frame']) for r in steps if r['cycle']==cycle]
        if len(own)!=22:continue # The parent rejects incomplete phase chains.
        for index,(start,end) in enumerate(zip(own,own[1:])):
            first=frames.get(start+1,{})
            phase=index if index<3 else (index-3)%4+3
            if first.get('pose')!=f'{CHOKE_OWN[phase]:08X}':
                errors.append('Actual current choke phase anchor')
            for field in range(start+1,end+1):
                row=frames.get(field,{})
                if any(row.get(k)!=first.get(k) for k in keys):
                    errors.append('Every original held choke field must preserve paired poses and grip coordinates')
                    break
    return errors


def verify_log(log, source, target, source_side, new_side, mode, victim='sonya', followup=False):
    if mode not in ('pair', 'airthrow'):
        raise ValueError('Only actual close-pair/airthrow evidence is in scope')
    proof=restart(log,source,target,source_side,new_side,mode,followup)
    health=assistance(log,source,source_side,all_regen=True)
    errors=proof['errors']+['Assistance: '+e for e in health['errors']]
    if mode=='pair' and target=='kano':errors+=choke_holds(log)
    cpu=re.findall(r'MK2_RESTART_CPU frame=(\d+) state=(\d+) roster=(\d+) id=(\d+) actor=([0-9A-F]+) order=(\d+) schedule=([0-9A-F]+) expected=(\d+) cpu_side=(\d+)',log)
    matches=re.findall(r'MK2_RESTART_MATCH frame=(\d+)',log)
    if len(cpu)!=2 or len(matches)!=1:
        errors.append('Two actual fresh CPU ownership/schedule anchors')
    orders=expected_orders()
    for index,c in enumerate(cpu):
        frame,state,roster,identity,actor,order,schedule,expected,side=c;order=int(order)
        if not (matches and int(frame)==int(matches[0])+index*600 and state=='0' and int(side)==3-new_side and
                0x01000000<=int(actor,16)<0x01100000 and order in range(6) and
                int(schedule,16)==0xfffa3000+order*0x180 and
                int(roster)==int(identity)==int(expected)==orders[order][0]):
            errors.append('Actual native fresh CPU slot, first ladder opponent and schedule')
    if len(cpu)==2 and cpu[0][1:]!=cpu[1][1:]:
        errors.append('Stable fresh native CPU ownership across the bounded game')
    if mode=='airthrow':
        begin=re.findall(r'MK2_AIR_JOIN_BEGIN[^\r\n]* victim=(\w+)',log)
        if begin!=[victim]:errors.append('Actual requested air-throw victim')
    return dict(passed=not errors,errors=errors,source=source,target=target,source_side=source_side,new_side=new_side,
                mode=mode,victim=victim if mode=='airthrow' else None,followup=followup,restart=proof,assistance=health,
                scope='current_health_assisted_endings_then_input_only_fresh_CPU_game_close_pair_or_real_join_airthrow_not_unassisted_tower_all_victims_CPU_choreography_or_full_goal',
                whole_character_integration_complete=False)


def verify(folder,source,target,source_side,new_side,mode,victim='sonya',followup=False):
    proof=verify_log((folder/'run.log').read_text(encoding='utf-8-sig'),source,target,source_side,new_side,mode,victim,followup)
    errors=proof['errors']
    def check(ok,label):
        if not ok and label not in errors:errors.append(label)
    metadata=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    check((metadata.get('exit_code'),metadata.get('fighter'),metadata.get('target'),metadata.get('source_side'),
           metadata.get('new_game_side'),metadata.get('special_mode'),metadata.get('candidate'))==
          (0,source,target,source_side,new_side,mode,CANDIDATE),'Exact terminal current case scope/build identity')
    check(metadata.get('passed') and metadata.get('independent_verification') and metadata.get('restart_health_assistance_excluded') and
          metadata.get('all_campaign_regeneration_logged') and not metadata.get('cheats_enabled') and
          metadata.get('tower_assistance')=='health_only' and metadata.get('restart_assistance')=='none',
          'Terminal native path and exact assistance boundary')
    if mode=='airthrow':
        check(metadata.get('air_victim')==victim and metadata.get('air_followup')==followup,'Terminal actual air victim/follow-up scope')
    check(metadata.get('candidate_executable_sha256','').lower()==EXE_SHA and metadata.get('payload_sha256','').lower()==PAYLOAD_SHA,
          'Exact current executable and full choreography payload')
    hashes=metadata.get('input_hashes',{})
    required={'mkport_candidate.exe','mk2ks.mdata','build-info.json','mk2ks_post_ending_restart.lua','mk2ks_cpu_ladder_trace.lua',
              'mk2ks_p2_tower_probe.lua','mk2ks_selector_exit_test.lua','verify_post_ending_restart.py',
              'check_post_restart_assistance.py','verify_p2_tower.py','verify_p2_campaign.py','run_post_ending_restart.ps1',
              'mk2ks_restart_'+mode+'.lua','verify_restart_'+mode+'.py'}
    check(required<={Path(p).name for p in hashes},'Complete frozen campaign/special/verifier launch inventory')
    for path,expected in hashes.items():
        item=Path(path)
        if item.suffix.lower() in ('.lua','.ps1','.py','.json','.cpp','.h'):item=folder/'input_sources'/item.name
        check(item.exists() and hashlib.sha256(item.read_bytes()).hexdigest().upper()==expected,'Exact frozen launch input: '+item.name)
    build=json.loads((folder/'input_sources/build-info.json').read_text(encoding='utf-8-sig'))
    check(build.get('executable_sha256','').lower()==EXE_SHA and build.get('payload_sha256','').lower()==PAYLOAD_SHA,
          'Frozen current build identity')
    for path,expected in build.get('input_hashes',{}).items():
        check(hashes.get(path)==expected,'All actual current build inputs included: '+Path(path).name)
    check(bool(build.get('input_hashes')),'Frozen build must include actual source inputs')
    proof['passed']=not errors
    return proof


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder',type=Path)
    p.add_argument('--source',choices=('kano','sonya'),required=True);p.add_argument('--target',choices=('kano','sonya'),required=True)
    p.add_argument('--source-side',choices=(1,2),type=int,required=True);p.add_argument('--new-side',choices=(1,2),type=int,required=True)
    p.add_argument('--mode',choices=('pair','airthrow'),required=True);p.add_argument('--victim',choices=('sonya','sub_zero'),default='sonya')
    p.add_argument('--followup',action='store_true');a=p.parse_args()
    try:result=verify(a.folder,a.source,a.target,a.source_side,a.new_side,a.mode,a.victim,a.followup)
    except (ValueError,KeyError,IndexError,StopIteration,OSError) as e:result=dict(passed=False,errors=['Malformed/missing current special evidence: '+str(e)])
    print(json.dumps(result,indent=2));raise SystemExit(0 if result['passed'] else 1)
