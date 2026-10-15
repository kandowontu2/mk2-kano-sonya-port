"""Independently check P2-human/P1-CPU ownership against original ROM orders."""
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROM = ROOT / 'mk2/mk2-maincpu.bin'
INSERTS = ((0,5),(0,7),(2,8),(3,9),(1,6),(0,8))
IDENTITIES = {'kano':17, 'sonya':18}


def expected_orders():
    original = ROM.read_bytes()
    offset = lambda address: (address-0xff800000)//8
    if struct.unpack_from('<I',original,offset(0xff8a11f0))[0] != 0xff8a1260:
        raise ValueError('Unsupported original ladder layout')
    orders = []
    for order,insertions in enumerate(INSERTS):
        pointer = struct.unpack_from('<I',original,offset(0xff8a1260)+order*4)[0]
        if pointer != 0xff8a1320+order*0x100:
            raise ValueError('Original order pointer changed')
        old = struct.unpack_from('<16H',original,offset(pointer))
        ordinary,remaining = [],iter(old[:11])
        for stage in range(13):
            if stage == insertions[0]: ordinary.append(18 if order&1 else 17)
            elif stage == insertions[1]: ordinary.append(17 if order&1 else 18)
            else: ordinary.append(next(remaining))
        orders.append(tuple(ordinary)+old[11:15])
    return orders


def verify(log, fighter, require_advance=False):
    errors = []
    identity = IDENTITIES[fighter]
    orders = expected_orders()
    captured = {}
    for match in re.finditer(r'MK2_P2_CAMPAIGN_ROM table=([0-9A-F]+) order=(\d+) list=([0-9A-F]+) ids=([0-9,]+)',log):
        table,order,pointer,ids = match.groups()
        order = int(order)
        if order not in range(6) or order in captured:
            errors.append('Missing/duplicated or invalid native order');continue
        captured[order] = tuple(map(int,ids.split(',')))
        if int(table,16) != 0xfffa2c00 or int(pointer,16) != 0xfffa3000+order*0x180 or captured[order] != orders[order]:
            errors.append(f'Order {order} differs from original stock order plus both new IDs')
    if set(captured) != set(range(6)): errors.append('Six actual native schedules not captured')

    result = re.search(r'MK2_P2_CAMPAIGN_RESULT pass=(\w+) fighter=(\w+) checks=(\d+) errors=(\d+) first=(\w+) stage_changes=(\d+) last_stage=(\w+) wins=(\d+) initial_action=(\w+) assistance=(\w+)',log)
    first = None
    if not result:
        errors.append('Missing final campaign result')
    else:
        passed,name,checks,error_count,initial,changes,last,wins,action,assistance = result.groups()
        if passed!='true' or name!=fighter or int(checks)<500 or int(error_count)!=0 or int(wins)<2 or action!='true' or assistance!='none' or initial=='nil':
            errors.append('Campaign result lacks clean input-only live ownership checks')
        if initial!='nil': first=int(initial)

    live = []
    pattern = r'MK2_P2_CAMPAIGN_LIVE frame=(\d+) mode=(\d+) states=(\d+),(\d+) stage=(\d+) order=(\d+) schedule=([0-9A-F]+) cpu=(\d+):(\d+) human=(\d+):(\d+) flags=([0-9A-F]+),([0-9A-F]+) health=(\d+),(\d+)'
    for match in re.finditer(pattern,log):
        frame,mode,s1,s2,stage,order,schedule,cpu,cpu_actor,human,human_actor,flag1,flag2,h1,h2 = match.groups()
        frame,mode,s1,s2,stage,order,cpu,cpu_actor,human,human_actor,h1,h2 = map(int,(frame,mode,s1,s2,stage,order,cpu,cpu_actor,human,human_actor,h1,h2))
        if order not in range(6) or stage not in range(17):
            errors.append('Invalid selected native order/stage');continue
        expected = orders[order][stage]
        if mode not in (2,7) or (s1,s2)!=(0,1) or int(schedule,16)!=0xfffa3000+order*0x180 or (cpu,cpu_actor)!=(expected,expected) or (human,human_actor)!=(identity,identity) or h1<=0 or h2<=0:
            errors.append(f'Live frame {frame}: wrong native CPU or human ownership')
        live.append({'frame':frame,'stage':stage,'order':order,'cpu':cpu,'human':human,
                     'alternate_cpu':bool(int(flag1,16)&64),'alternate_human':bool(int(flag2,16)&64)})
    if len(live)<500: errors.append('Fewer than 500 independent live samples')
    if live and first is not None and live[0]['frame']!=first: errors.append('First published campaign sample is missing')
    states=[]
    state_pattern=r'MK2_P2_CAMPAIGN_STATE frame=(\d+) mode=(\d+) states=(\d+),(\d+) stage=(\d+) order=(\d+) schedule=([0-9A-F]+) expected=(\d+) roster=(\d+),(\d+) actors=([0-9A-F]+):(\d+),([0-9A-F]+):(\d+) health=(\d+),(\d+) winner=(\d+) hud_read=(\d+)'
    for match in re.finditer(state_pattern,log):
        groups=match.groups()
        states.append(dict(zip(('frame','mode','s1','s2','stage','order','schedule','expected','r1','r2','a1','id1','a2','id2','h1','h2','winner','hud'),
            (int(value,16) if index in (6,10,12) else int(value) for index,value in enumerate(groups)))))
    # The first 500 LIVE fields may span an ordinary native round break.
    # Every non-contiguous interval must have an independently captured native
    # victory plus the exact one-field HUD constructor before the new actors.
    # Missing arbitrary live samples, or an unexplained actor gap, still fail.
    round_breaks=0
    for before,after in zip(live[:500],live[1:500]):
        a,b=before['frame'],after['frame']
        if b==a+1: continue
        interval=[row for row in states if a<row['frame']<b]
        victory=any(row['mode']==5 and (row['s1'],row['s2'])==(0,1) and
            row['r1']==row['expected']==before['cpu'] and row['r2']==identity and
            ((row['winner']==1 and row['h2']==0 and row['h1']>0) or
             (row['winner']==2 and row['h1']==0 and row['h2']>0)) for row in interval)
        constructor=any(row['frame']==b-1 and row['mode']==6 and (row['s1'],row['s2'])==(0,1) and
            row['a1']==row['a2']==0 and row['h1']==row['h2']==161 and row['hud']==b-2 and
            row['r1']==after['cpu'] and row['r2']==identity for row in interval)
        if b-a>600 or not victory or not constructor:
            errors.append(f'Unexplained gap in first 500 live fields: {a}..{b}')
        else: round_breaks+=1
    stages=sorted({row['stage'] for row in live})
    terminals=list(re.finditer(r'MK2_P2_CAMPAIGN_TERMINAL frame=(\d+) stage=(\d+) outcome=(\w+) mode=(\d+) states=(\d+),(\d+) actors=([0-9A-F]+),([0-9A-F]+)',log))
    if len(terminals)>1: errors.append('Duplicated terminal campaign outcome')
    for terminal in terminals:
        frame,stage,outcome,mode,s1,s2,a1,a2=terminal.groups()
        frame,stage,mode,s1,s2=int(frame),int(stage),int(mode),int(s1),int(s2)
        if outcome!='loss' or mode!=11 or (s1,s2)!=(0,0) or int(a1,16)!=0 or int(a2,16)!=0:
            errors.append('Terminal marker is not an actual retired native GAME OVER')
        actual=any(row['frame']==frame and row['mode']==11 and (row['s1'],row['s2'])==(0,0) and
            row['stage']==stage and row['a1']==row['a2']==0 and row['h2']==0 and row['winner']==1 for row in states)
        losses=[row for row in states if row['frame']<frame and row['mode']==3 and (row['s1'],row['s2'])==(0,2) and
            row['stage']==stage and row['r1']==row['id1']==row['expected'] and row['r2']==row['id2']==identity and
            row['h1']>0 and row['h2']==0 and row['winner']==1]
        loss=False
        if losses:
            start=losses[-1]
            # Native CONTINUE lasts longer than a combat round break. Require
            # the actual retained loss state throughout its captured countdown,
            # rather than imposing an unrelated 600-field round-break limit.
            countdown=[row for row in states if start['frame']<=row['frame']<frame]
            loss=all(row['mode']==3 and (row['s1'],row['s2'])==(0,2) and row['stage']==stage and
                row['order']==start['order'] and row['schedule']==start['schedule'] and
                row['r1']==start['r1'] and row['r2']==identity and row['h1']==start['h1'] and
                row['h2']==0 and row['winner']==1 and
                (row['a1']==row['a2']==0 or row['id1']==start['r1'] and row['id2']==identity) for row in countdown)
        if not actual or not loss: errors.append('Terminal loss lacks actual owned native CONTINUE and GAME OVER states')
    if require_advance and (not stages or max(stages)<1): errors.append('No subsequent native ladder opponent reached')
    wins=list(re.finditer(r'MK2_P2_CAMPAIGN_WIN frame=(\d+) stage=(\d+) actor=([0-9A-F]+) wins=(\d+) states=(\d+),(\d+)',log))
    if len(wins)<2 or any(int(m.group(3),16)<0x01000000 or int(m.group(3),16)>=0x01100000 or m.group(6)!='1' for m in wins):
        errors.append('Native human P2 wins are not established')
    if 'MK2KS_EXIT_RESULT pass=true ' not in log: errors.append('Base selection/HUD/identity lifecycle acceptance failed')
    for marker in ('MK2KS_DISPLAY_RESULT pass=true ','MK2KS_HUD_SHADOW_RESULT pass=true ',
                   'MK2KS_STABILITY stalled_frames=0 trap_frames=0'):
        if marker not in log: errors.append('Missing base display/shadow/stability evidence')
    if re.search(r'MK2_FINISH_POSITION_ASSIST|\[LUA ERROR\]|fatal error|access violation|MK2_P2_CAMPAIGN_ERROR',log,re.I):
        errors.append('Forbidden assistance or runtime/ownership error')
    return {'passed':not errors,'fighter':fighter,'errors':errors,'live_samples':len(live),
            'stages':stages,'native_orders_checked':len(captured),'native_human_wins':len(wins),
            'verified_native_round_breaks':round_breaks,
            'naturally_alternate_human_samples':sum(row['alternate_human'] for row in live),
            'verified_native_terminal_losses':len(terminals),
            'require_advance':require_advance,'original_rom_sha256':hashlib.sha256(ROM.read_bytes()).hexdigest().upper(),
            'scope':'p2_campaign_ownership_not_full_ladder_or_whole_game'}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('log',type=Path)
    parser.add_argument('--fighter',required=True,choices=IDENTITIES)
    parser.add_argument('--require-advance',action='store_true')
    args=parser.parse_args()
    result=verify(args.log.read_text(encoding='utf-8-sig'),args.fighter,args.require_advance)
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if result['passed'] else 1)
