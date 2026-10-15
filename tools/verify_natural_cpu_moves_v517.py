"""Natural CPU ownership, finite action returns and full projectile releases.

An entry plus recovery is not proof of every contact/paired animation or pixels.
Interrupted actions are explicitly distinguished, not silently counted as full
uninterrupted choreography. CPU walking can resume on the very first ready field.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

from verify_p2_campaign import expected_orders
from verify_native_candidate_v517 import EXE, NAME as CANDIDATE, PAYLOAD
EXE_SHA, PAYLOAD_SHA = EXE.lower(), PAYLOAD.lower()
from verify_native_candidate_v517 import ROOT
from build_native_projectile_choreography import BODY_GROUPS, TIMING

HEX = set('schedule actor main owner action pose list xraw yraw vx vy gravity flags body trail child entry pc a8 a13 a0 a1 a2 a3 group velocity_parameter'.split())
TEXT = {'move', 'kind'}
SPECS = {'knife':(17,0xffffb000), 'ball':(17,0xffffde00), 'blade':(17,0xfff8cc00), 'choke':(17,0xfff91400),
         'ring':(18,0xffffb400), 'square':(18,0xffffca00), 'bicycle':(18,0xfff9a400), 'leg':(18,0xfff80800)}


def rows(log, tag):
    return [{k:v if k in TEXT else int(v, 16 if k in HEX else 10)
             for k,v in re.findall(r'(\w+)=([^\s]+)', line)}
            for line in log.splitlines() if line.startswith('MK2_NAT_CPU_'+tag+' ')]


def _verify_log(log, player, opponent):
    errors = []
    def check(ok, label):
        if not ok and label not in errors: errors.append(label)
    fields, entries, health, events = [rows(log, t) for t in ('FIELD','ENTRY','HEALTH','EVENT')]
    results = rows(log, 'RESULT')
    if len(results) != 1 or not fields or not entries:
        return dict(passed=False, errors=['Actual natural CPU fields/entries/result missing'])
    result = results[0]
    by = {(f['frame'],f['slot']):f for f in fields}
    frames = {f['frame'] for f in fields}
    check(len(fields)==len(by)==2*len(frames)==2*result['active_fields'] and
          set(by)=={(f,s) for f in frames for s in (1,2)}, 'Every actual paired CPU field without omissions/duplicates')
    check(result['schema']==4 and result['writes']==result['live_children']==0 and result['entries']==len(entries),
          'Exact read-only current observer accounting and child cleanup')
    orders = expected_orders()
    pid = {'kano':17,'sonya':18}[player]
    for f in fields:
        index = (f['schedule']-0xfffa3000)//0x180
        check(index in range(6) and f['schedule']==0xfffa3000+index*0x180 and f['stage'] in range(17) and
              f['scheduled']==orders[index][f['stage']], 'Actual original-derived natural ladder schedule')
        check(f['mode']==2 and f['state']==(1 if f['slot']==1 else 0) and f['id']==f['roster']==(pid if f['slot']==1 else f['scheduled']) and
              0x01000000<=f['actor']<0x01100000 and 0x01000000<=f['main']<0x01100000 and
              f['owner']==f['actor'] and f['writes']==0 and 0<=f['hp']<=161, 'True human/CPU identities, owners and native health')
    for pattern in ('MK2KS_CPU_DIAGNOSTIC_RESULT requested=nil injected=false',
                    'MK2KS_CPU_DIAGNOSTIC_LADDER_RESULT requested=nil injected=false',
                    'MK2KS_CPU_DIAGNOSTIC_HEALTH_RESULT requested=nil all_stages=false writes=0',
                    'MK2KS_CPU_DIAGNOSTIC_P1_REGEN_RESULT enabled=false writes=0',
                    'MK2KS_STABILITY stalled_frames=0 trap_frames=0',
                    'MK2KS_EXIT_RESULT pass=true ', 'MK2KS_DISPLAY_RESULT pass=true ', 'MK2KS_HUD_SHADOW_RESULT pass=true '):
        check(pattern in log, 'Actual clean natural run: '+pattern)
    check(not re.search(r'MK2KS_CPU_DIAGNOSTIC_WRITE|MK2KS_CPU_DIAGNOSTIC_LADDER_WRITE|MK2KS_DIAGNOSTIC_HEALTH_WRITE|MK2KS_DIAGNOSTIC_P1_REGEN frame=|\[LUA ERROR\]|fatal error|access violation', log, re.I),
          'No injected identity/stage/health or actual runtime error')
    changed = [h for h in health if h['before']!=h['after']]
    for h in health:
        check(h['pc']==0xff836700 and h['writes']==0 and 0<=h['after']<=h['before']<=161 and h['slot'] in (1,2),
              'Only original native collision health stores, never regeneration')
        if (h['frame'],h['slot']) in by and (h['frame']+1,h['slot']) in by:
            same = [x for x in health if (x['frame'],x['slot'])==(h['frame'],h['slot'])]
            check(by[h['frame'],h['slot']]['hp']==same[0]['before'] and by[h['frame']+1,h['slot']]['hp']==same[-1]['after'],
                  'Real native health ledger across actual paired fields')
    returns = []
    groups, children, effects, retired = [rows(log,t) for t in ('GROUP','CHILD','EFFECT','RETIRE')]
    for number, e in enumerate(entries, 1):
        move = e['move'];start = e['frame']
        # The initial fight activation may occur after this field's frame
        # callback. Use actual entry-time roles and the next actual callback;
        # never invent an absent pre-entry field or reorder same-frame events.
        f = by.get((start+1,2))
        index = (e['schedule']-0xfffa3000)//0x180
        check(move in SPECS and (e['id'],e['entry'])==SPECS.get(move) and e['pc']==e['entry']+16 and e['serial']==number and e['writes']==0 and
              f is not None and all(e[k]==f[k] for k in ('actor','main','id','stage','schedule')) and e['a8']==e['actor'] and
              e['mode']==2 and e['state']==0 and e['roster']==e['scheduled']==e['id'] and e['human_state']==1 and e['human_roster']==pid and
              index in range(6) and e['schedule']==0xfffa3000+index*0x180 and e['stage'] in range(17) and e['id']==orders[index][e['stage']],
              'Actual canonical CPU-owned special entry and chronology')
        ready = [r for r in events if r['kind']=='ready' and (r['actor'],r['main'])==(e['actor'],e['main']) and start<r['frame']<start+250]
        check(bool(ready), 'Every observed CPU action reaches native ready continuation')
        if not ready: continue
        end = ready[0]['frame']
        after = by.get((end+1,2))
        check(all((at,s) in by for at in range(start+1,end+2) for s in (1,2)), 'Every actual post-entry callback field through ready, including interruptions')
        check(ready[0]['entry']==0xff861350 and ready[0]['pc']==0xff861360 and ready[0]['writes']==0 and after is not None and
              (after['actor'],after['main'],after['id'])==(e['actor'],e['main'],e['id']) and after['action']==0x303 and
              after['y']==after['floor'] and after['vy']==after['gravity']==after['trail']==0 and
              after['flags']&0x1c==0 and after['body']&0x0c==0, 'Actual grounded recovery, detached-effect cleanup and immediate AI return')
        interrupted = any(h['slot']==2 and start<h['frame']<=end for h in changed)
        returns.append(dict(move=move,frame=start,ready=end,fields=end-start+1,received_native_damage=interrupted,
                            scope='native_owned_entry_to_ready_not_full_contact_choreography'))
        if move not in ('knife','ring'): continue
        target = 'kano' if e['id']==17 else 'sonya';timing = TIMING[target]
        poses = [x-0x01000000 for x in BODY_GROUPS[target]]
        elapsed = 1
        for pose,hold in zip(poses,timing['body_holds']):
            for age in range(elapsed,elapsed+hold):
                r = by.get((start+age,2),{})
                check(r.get('pose')==pose and r.get('action')==4 and r.get('vx')==r.get('vy')==0,
                      'All original CPU projectile release poses/holds and own action state')
            elapsed += hold
        births = [c for c in children if c['frame']==start+timing['child_spawn_age'] and c['owner']==e['actor'] and c['id']==e['id']]
        check(len(births)==1, 'Exactly one real owned projectile at original allocation age')
        if len(births)!=1: continue
        child = births[0]
        death = [r for r in retired if (r['actor'],r['main'])==(child['actor'],child['main']) and r['frame']>child['frame']]
        check(len(death)==1 and child['entry']==(0xfffc6000 if target=='kano' else 0xfffc7000) and child['pc']==child['entry']+16 and child['writes']==0,
              'Original character-owned child task, one native retirement')
        if len(death)!=1: continue
        death = death[0]
        life = [r for r in effects if (r['actor'],r['main'])==(child['actor'],child['main']) and child['frame']<r['frame']<=death['frame']]
        check([r['frame'] for r in life]==list(range(child['frame']+1,death['frame']+1)) and
              all(r['id']==e['id'] and r['type']==81 and r['owner']==e['actor'] and r['velocity_parameter']==0x80000 and r['writes']==0 for r in life) and
              death['pc']==0xff8b6830 and death['writes']==0, 'Every owned native child lifetime field and real cleanup')
        travels = list(range(0xff614800,0xff614a80,0x40)) if target=='kano' else list(range(0xff614a80,0xff614b80,0x40))
        flight = [g for g in groups if (g['actor'],g['main'])==(child['actor'],child['main']) and g['group'] in travels and g['vx'] in (0x80000,0xfff80000)]
        check(bool(flight), 'Real full-cycle travelling projectile groups')
        if flight:
            sign = 1 if flight[0]['vx']==0x80000 else -1
            for i,g in enumerate(flight):
                check(g['group']==travels[i%len(travels)] and g['frame']==start+timing['first_flight_age']+i*timing['flight_hold'] and
                      g['pc']==0xff8387a0 and g['id']==e['id'] and g['body']==0 and g['vx']==flight[0]['vx'] and g['vy']==g['writes']==0,
                      'Original complete CPU flight cycle, eight-pixel speed and one/three-field cadence')
                if i: check(g['x']-flight[i-1]['x']==sign*8*timing['flight_hold'] and g['y']==flight[0]['y'], 'Actual CPU projectile native travel geometry')
        if target=='kano':
            intro = [g for g in groups if (g['actor'],g['main'])==(child['actor'],child['main']) and start+3<=g['frame']<start+22]
            check([g['group'] for g in intro]==[0xff614000,0xff614060,0xff6140a0,0xff614100,0xff614180,0xff6141e0] and
                  [g['frame']-start for g in intro]==[3,6,9,12,15,18] and all(g['vx']==g['vy']==0 for g in intro),
                  'All six original CPU knife intro composites and detached three-field holds')
    check(any(e['id']==opponent for e in entries), 'Requested naturally selected CPU fighter actually executes moves')
    return dict(passed=not errors,errors=errors,player=player,opponent=opponent,paired_fields=len(frames),native_damage_stores=len(changed),
                observed_moves=sorted({e['move'] for e in entries}),native_returns=returns,projectile_children=len(children),
                scope='natural_ladder_true_CPU_ownership_action_to_ready_fields_and_projectile_release_child_cadence_not_all_contact_outcomes_components_audio_or_full_tower',
                whole_character_integration_complete=False)


def verify_log(log, player, opponent):
    try: return _verify_log(log, player, opponent)
    except (ValueError,KeyError,TypeError,IndexError) as error:
        return dict(passed=False,errors=['Malformed/incomplete natural CPU trace: '+str(error)])


def verify(folder):
    try:
        metadata = json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        result = verify_log((folder/'run.log').read_text(encoding='utf-8-sig'),metadata['player'],metadata['opponent_id'])
        errors = result['errors']
        def check(ok,label):
            if not ok: errors.append(label)
        check(metadata.get('passed') and metadata.get('natural_only') and metadata.get('exit_code')==0 and
              metadata.get('ladder_index')==-1 and metadata.get('diagnostic_injected')=='false' and metadata.get('cheats') is False and
              metadata.get('memory_assistance')=='none', 'Actual terminal input-only natural run metadata')
        check(metadata.get('executable_sha256','').lower()==EXE_SHA and metadata.get('payload_sha256','').lower()==PAYLOAD_SHA,
              'Exact current matched executable/payload')
        hashes = metadata.get('input_hashes',{})
        check(hashes==json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig')), 'Actual original launch hash manifest')
        required = {'mkport_candidate.exe','mk2ks.mdata','build-info.json','mk2ks_natural_cpu_moves_probe.lua',
                    'mk2ks_cpu_ladder_trace.lua','mk2ks_selector_exit_test.lua','run_cpu_owned_special_v2.ps1'}
        check(required<={Path(p).name for p in hashes}, 'Complete frozen natural CPU launch inventory')
        for path,expected in hashes.items():
            item = Path(path)
            if item.suffix.lower() in ('.lua','.ps1','.json'): item = folder/'input_sources'/item.name
            check(item.exists() and hashlib.sha256(item.read_bytes()).hexdigest().upper()==expected, 'Exact frozen CPU launch input: '+item.name)
        build = json.loads((ROOT/CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
        check(build['name']==CANDIDATE and build['executable_sha256']==EXE and
              build['payload_sha256']==PAYLOAD, 'Exact current build metadata')
        for filename, sha in build['input_hashes'].items():
            check(hashes.get(filename)==sha and
                  hashlib.sha256(Path(filename).read_bytes()).hexdigest().upper()==sha,
                  'Every actual current build input tracked and unchanged: '+filename)
        for filename, sha in ((ROOT/CANDIDATE/'mkport_candidate.exe', EXE),
                              (ROOT/CANDIDATE/'roms/mk2ks/mk2ks.mdata', PAYLOAD)):
            check(hashlib.sha256(filename.read_bytes()).hexdigest().upper()==sha,
                  'Actual exact current executable/payload bytes')
        result['passed'] = not errors
        return result
    except (OSError,ValueError,KeyError,TypeError,IndexError) as error:
        return dict(passed=False,errors=['Missing/malformed CPU proof: '+str(error)])


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path);args=parser.parse_args()
    result=verify(args.folder);print(json.dumps(result,indent=2));raise SystemExit(0 if result['passed'] else 1)
