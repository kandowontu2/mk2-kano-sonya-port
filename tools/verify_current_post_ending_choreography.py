"""Matched current build: endings, fresh native CPU game, join and full throws."""
import argparse
import hashlib
import json
import re
from pathlib import Path

from verify_post_ending_restart import verify as restart
from check_post_restart_assistance import verify as assistance
from verify_p2_campaign import expected_orders
from verify_projectile_choreography import ROOT,PAYLOAD_SHA

EXE_SHA='b67d9fd07b285c5bd186086125b6568bbd2d8fb001e887bb73df353a216d6d20'
CANDIDATE='diagnostic_v300_native_projectile_choreography'


def verify(folder,source,target,source_side,new_side,scenario):
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    proof=restart(log,source,target,source_side,new_side,'projectile_choreography')
    health=assistance(log,source,source_side,all_regen=True)
    errors=proof['errors']+['Assistance: '+e for e in health['errors']]
    def check(ok,label):
        if not ok and label not in errors:errors.append(label)
    metadata=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    check((metadata.get('exit_code'),metadata.get('fighter'),metadata.get('target'),metadata.get('source_side'),
           metadata.get('new_game_side'),metadata.get('special_mode'),metadata.get('contact_scenario'),metadata.get('candidate'))==
          (0,source,target,source_side,new_side,'projectile_choreography',scenario,CANDIDATE), 'Exact terminal current case scope/build identity')
    check(metadata.get('passed') and metadata.get('independent_verification') and metadata.get('restart_health_assistance_excluded') and
          not metadata.get('cheats_enabled') and metadata.get('restart_assistance')=='none', 'Terminal full native path and no restarted-game assistance')
    check(metadata.get('candidate_executable_sha256','').lower()==EXE_SHA and metadata.get('payload_sha256','').lower()==PAYLOAD_SHA,
          'Exact current executable and full choreography payload')
    hashes=metadata.get('input_hashes',{})
    required={'mkport_candidate.exe','mk2ks.mdata','mk2ks_post_ending_restart.lua','mk2ks_cpu_ladder_trace.lua',
              'mk2ks_p2_tower_probe.lua','mk2ks_selector_exit_test.lua','mk2ks_restart_lifecycle.lua','mk2ks_projectile_contact.lua',
              'mk2ks_projectile_choreography_probe.lua','mk2ks_projectile_impact_probe.lua','verify_projectile_choreography.py',
              'verify_post_ending_restart.py','check_post_restart_assistance.py','verify_p2_tower.py','run_post_ending_restart.ps1'}
    check(required<={Path(p).name for p in hashes}, 'Complete frozen campaign/observer/verifier launch inventory')
    for path,expected in hashes.items():
        item=Path(path)
        if item.suffix.lower() in ('.lua','.ps1','.py','.json','.cpp','.h'):item=folder/'input_sources'/item.name
        check(item.exists() and hashlib.sha256(item.read_bytes()).hexdigest().upper()==expected, 'Exact frozen launch input: '+item.name)
    # Enforce fresh CPU schedule/ownership in every scope, including P1->P1.
    # The Lua observer asserts it every field; these are independent actual
    # start/end anchors, not a claim of a logged 601-field CPU action trace.
    cpu=re.findall(r'MK2_RESTART_CPU frame=(\d+) state=(\d+) roster=(\d+) id=(\d+) actor=([0-9A-F]+) order=(\d+) schedule=([0-9A-F]+) expected=(\d+) cpu_side=(\d+)',log)
    matches=re.findall(r'MK2_RESTART_MATCH frame=(\d+)',log)
    check(len(cpu)==2 and len(matches)==1, 'Two actual fresh CPU ownership/schedule anchors')
    orders=expected_orders()
    for index,c in enumerate(cpu):
        frame,state,roster,identity,actor,order,schedule,expected,side=c;order=int(order)
        check(matches and int(frame)==int(matches[0])+index*600 and state=='0' and int(side)==3-new_side and
              0x01000000<=int(actor,16)<0x01100000 and order in range(6) and
              int(schedule,16)==0xfffa3000+order*0x180 and int(roster)==int(identity)==int(expected)==orders[order][0],
              'Actual native fresh CPU slot, first ladder opponent and schedule')
    check(len(cpu)!=2 or cpu[0][1:]==cpu[1][1:], 'Stable fresh native CPU ownership across the bounded game')
    check(f'move={"knife" if target=="kano" else "ring"} scenario={scenario} writes=0' in log,
          'Actual selected projectile contact scenario after ending and real join')
    return dict(passed=not errors,errors=errors,source=source,target=target,source_side=source_side,new_side=new_side,
                scenario=scenario,restart=proof,assistance=health,
                scope='current_health_assisted_full_endings_then_input_only_fresh_CPU_game_real_join_full_projectile_fields_not_unassisted_tower_all_CPU_actions_or_pixel_proof',
                whole_character_integration_complete=False)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder',type=Path)
    p.add_argument('--source',choices=('kano','sonya'),required=True);p.add_argument('--target',choices=('kano','sonya'),required=True)
    p.add_argument('--source-side',choices=(1,2),type=int,required=True);p.add_argument('--new-side',choices=(1,2),type=int,required=True)
    p.add_argument('--scenario',choices=('hit','block','miss'),required=True);args=p.parse_args()
    try:result=verify(args.folder,args.source,args.target,args.source_side,args.new_side,args.scenario)
    except (ValueError,KeyError,IndexError,StopIteration,OSError) as e:result=dict(passed=False,errors=['Malformed/missing current ending evidence: '+str(e)])
    print(json.dumps(result,indent=2));raise SystemExit(0 if result['passed'] else 1)
