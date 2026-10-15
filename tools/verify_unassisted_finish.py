"""Check native damage chains and P1 fatality ownership against original MKII."""
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDENTITIES = {'kano':17, 'sonya':18, 'raiden':7, 'sub_zero':8}


def verify(log, fighter, victim):
    errors = []
    own_id, victim_id = IDENTITIES[fighter], IDENTITIES[victim]
    original = (ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    word = lambda address: struct.unpack_from('<H', original, (address-0xff800000)//8)[0]
    if (word(0xff8366c0),word(0xff8366f0)) != (0x4541,0x8026):
        errors.append('Original native subtract/store damage instructions changed')
    rows = []
    pattern = r'MK2_UNASSISTED_DAMAGE frame=(\d+) pc=([0-9A-F]+) actor=([0-9A-F]+) id=(\d+) health=(\d+),(\d+) damage=(\d+)'
    for match in re.finditer(pattern, log):
        frame, pc, actor, identity, before, after, damage = match.groups()
        rows.append(dict(frame=int(frame),pc=int(pc,16),actor=int(actor,16),id=int(identity),
                         before=int(before),after=int(after),damage=int(damage)))
    chains, active, last_frame = [], [], -1
    constructors = [int(m.group(1)) for m in re.finditer(r'MK2KS_NATIVE_P2_HUD frame=(\d+) ',log)]
    for row in rows:
        if row['frame']<=last_frame or row['pc']!=0xff836700 or row['id']!=victim_id or not 0x01000000<=row['actor']<0x01100000:
            errors.append('Wrong/duplicated native damage writer or victim ownership')
        last_frame=row['frame']
        if not 0<=row['after']<row['before']<=161 or row['damage']!=row['before']-row['after']:
            errors.append('Invalid native health decrement')
        if not active:
            if row['before']!=161: errors.append('Native round damage does not begin at full health')
            if chains and not any(chains[-1][-1]['frame']<field<row['frame'] for field in constructors):
                errors.append('New full-health round lacks actual native HUD reconstruction')
        elif row['before']!=active[-1]['after'] or row['actor']!=active[-1]['actor']:
            errors.append('Unexplained health/actor change within a native round')
        active.append(row)
        if row['after']==0:
            if sum(r['damage'] for r in active)!=161: errors.append('Round did not earn all 161 native health points')
            chains.append(active);active=[]
    if active or len(chains)!=2: errors.append('Exactly two complete native knockout chains are required')
    wins = []
    for match in re.finditer(r'MK2_UNASSISTED_WIN frame=(\d+) fighter=(\w+) wins=(\d+) damage=(\d+)',log):
        frame,name,count,damage=match.groups()
        if name!=fighter: errors.append('Wrong native human winner')
        wins.append(tuple(map(int,(frame,count,damage))))
    if len(wins)!=2 or [r[1:] for r in wins]!=[(1,161),(2,322)]: errors.append('Two naturally earned owned native victories not proven')
    gates = list(re.finditer(r'MK2_RANGE_GATE frame=(\d+) fighter=(\w+) side=(\d+) actor=([0-9A-F]+) action=([0-9A-F]+) distance=(\d+) limit=(\d+) expected=(\w+)',log))
    actions = list(re.finditer(r'MK2_RANGE_ACTION frame=(\d+) fighter=(\w+) side=(\d+) actor=([0-9A-F]+)',log))
    expected_action = 0xfffaae00 if fighter=='kano' else 0xfffab200
    expected_limit = 80 if fighter=='kano' else 128
    if len(gates)!=1 or len(actions)!=1: errors.append('Exactly one native fatality gate and activation are required')
    elif len(chains)==2:
        gate, action = gates[0], actions[0]
        gate_frame,name,side,actor,routine,distance,bound,outcome=gate.groups()
        action_frame,action_name,action_side,action_actor=action.groups()
        if name!=fighter or action_name!=fighter or side!='1' or action_side!='1' or actor!=action_actor or not 0x01000000<=int(actor,16)<0x01100000:
            errors.append('Native fatality does not belong to the selected human P1')
        if int(routine,16)!=expected_action or int(bound)!=expected_limit or int(distance)>expected_limit or outcome!='activate':
            errors.append('Wrong native fatality range/routine')
        if not chains[-1][-1]['frame']<int(gate_frame)<=int(action_frame)<=int(gate_frame)+2:
            errors.append('Fatality did not follow the actual second knockout and native range gate')
        if wins and wins[-1][0]<=int(action_frame): errors.append('Final native victory did not follow the fatality')
    result = re.search(r'MK2_UNASSISTED_RESULT fighter=(\w+) damage_events=(\d+) total_damage=(\d+) wins=(\d+) errors=(\d+) writers=([0-9A-F,]+) writes=0 assistance=none',log)
    if not result or result.groups()!=(fighter,str(len(rows)),'322','2','0','FF836700'):
        errors.append('Final damage totals/ownership do not match the independent native chains')
    for marker in ('MK2_RANGE_RESULT pass=true ','MK2KS_EXIT_RESULT pass=true ',
                   'MK2KS_DISPLAY_RESULT pass=true ','MK2KS_HUD_SHADOW_RESULT pass=true ',
                   'MK2KS_STABILITY stalled_frames=0 trap_frames=0'):
        if marker not in log: errors.append('Missing native lifecycle/range/display acceptance')
    if re.search(r'MK2_FINISH_POSITION_ASSIST|MK2KS_DIAGNOSTIC_HEALTH_WRITE|\[LUA ERROR\]|fatal error|access violation',log,re.I):
        errors.append('Forbidden assistance or runtime error')
    return {'passed':not errors,'fighter':fighter,'victim':victim,'errors':errors,
            'complete_native_rounds':len(chains),'damage_events':len(rows),
            'total_native_damage':sum(r['damage'] for r in rows),'native_writer_pc':'FF836700',
            'original_rom_sha256':hashlib.sha256(original).hexdigest().upper(),
            'scope':'unassisted_two_player_p1_damage_and_fatality_not_cpu_tower'}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('log',type=Path)
    parser.add_argument('--fighter',required=True,choices=('kano','sonya'))
    parser.add_argument('--victim',required=True,choices=IDENTITIES)
    args=parser.parse_args()
    result=verify(args.log.read_text(encoding='utf-8-sig'),args.fighter,args.victim)
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if result['passed'] else 1)
