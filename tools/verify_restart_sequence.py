"""Independently verify actual owned blade/bicycle paths after native restart."""
import argparse
import json
import re
from pathlib import Path

SPECS = {
    'kano': ('blade', 17, 0xfff8c800, 0xfff8cc00, 0xfff8e800, 0xfff8e400, 0x117),
    'sonya': ('bicycle', 18, 0xfff9a000, 0xfff9a400, 0xfff9e800, 0xfff9ee00, 0x204),
}
KINDS = ('parser', 'action', 'intro', 'loop', 'attack', 'effect', 'step', 'recovery', 'ready')


def verify(log, target, side):
    name, identity, parser, action, intro, attack, state = SPECS[target]
    errors = []
    counts = dict.fromkeys(KINDS, 0)

    def one(pattern, label):
        rows = re.findall(pattern, log)
        if len(rows) != 1:
            errors.append(label + ' must occur exactly once')
            return None
        return rows[0]

    guard = one(r'MK2_RESTART_SEQUENCE_ROM target=(\w+) side=(\d+) move=(\w+) parser=([0-9A-F]+) action=([0-9A-F]+) intro=([0-9A-F]+) attack=([0-9A-F]+) state=([0-9A-F]+) writes=(\d+)', 'Native code guard')
    if guard and (guard[:3] != (target, str(side), name) or tuple(int(v, 16) for v in guard[3:8]) != (parser, action, intro, attack, state) or guard[8] != '0'):
        errors.append('Wrong native parser/action/script/descriptor/state')
    match = one(r'MK2_RESTART_MATCH frame=(\d+) target=(\w+) id=(\d+) actor=([0-9A-F]+) stage=(\d+)', 'Actual match')
    done = one(r'MK2_RESTART_COMPLETE frame=(\d+)[^\r\n]* live=(\d+) errors=(\d+) restart_writes=(\d+)', 'Actual match completion')
    result = one(r'MK2_RESTART_SEQUENCE_RESULT pass=(\w+) target=(\w+) side=(\d+) move=(\w+) commands=(\d+) parsers=(\d+) actions=(\d+) intros=(\d+) loops=(\d+) attacks=(\d+) effects=(\d+) steps=(\d+) recoveries=(\d+) ready=(\d+) errors=(\d+) writes=(\d+)', 'Actual sequence result')
    if not match or not done:
        return {'passed': False, 'errors': errors, 'scope': 'owned_sequence_after_restart'}
    mf, df, actor = int(match[0]), int(done[0]), match[3]
    if match[1:3] != (target, str(identity)) or match[4] != '0' or df - mf != 600 or done[1:] != ('601', '0', '0'):
        errors.append('Incorrect actual identity/stage/601-field completion')

    def valid_ram(value):
        return 0x01000000 <= int(value, 16) < 0x01100000

    def owned(field, age, slot, own, owner, process):
        if not mf <= int(field) <= df or int(age) != int(field) - mf or (slot, own, owner) != (str(side), str(identity), actor) or not valid_ram(process):
            errors.append('Wrong actor/identity/slot/process/epoch')

    plans = re.findall(r'MK2_RESTART_SEQUENCE_PLAN first=(\d+) interval=(\d+) commands=(\d+) writes=(\d+)', log)
    first = 0  # Exact archived initial driver had fixed ages 0/180/360.
    if plans:
        if len(plans) != 1 or not 0 <= int(plans[0][0]) <= 140 or plans[0][1:] != ('180', '3', '0'):
            errors.append('Wrong input timing plan')
        first = int(plans[0][0])
    command_rows = re.findall(r'MK2_RESTART_SEQUENCE_COMMAND frame=(\d+) age=(\d+) side=(\d+) target=(\w+) move=(\w+) forward=(\w+) back=(\w+) button=(\w+) writes=(\d+)', log)
    if len(command_rows) != 3 or [int(row[1]) for row in command_rows] != [first, first + 180, first + 360]:
        errors.append('Missing actual three command attempts')
    commands = []
    for field, age, slot, fighter, move, forward, back, button, writes in command_rows:
        if int(field) != mf + int(age) or (slot, fighter, move, button, writes) != (str(side), target, name, 'hp' if target == 'kano' else 'hk', '0') or {forward, back} != {'left', 'right'}:
            errors.append('Wrong real input command')
        commands.append(int(field))
    entries = {'parser': parser, 'action': action, 'intro': intro, 'attack': attack, 'recovery': 0xff861350}
    if target == 'kano':
        entries.update(effect=0xfff8d800, step=0xfff8e000)
    else:
        entries['loop'] = 0xfff9eb00
    cycles, latest_parser = {}, None
    rows = re.findall(r'MK2_RESTART_SEQUENCE_EVENT frame=(\d+) age=(\d+) kind=(\w+) cycle=(\d+) side=(\d+) id=(\d+) actor=([0-9A-F]+) process=([0-9A-F]+) a13=([0-9A-F]+) pc=([0-9A-F]+) entry=([0-9A-F]+) count=(\d+)', log)
    for field, age, kind, cycle, slot, own, owner, process, a13, pc, entry, count in rows:
        f, c = int(field), int(cycle)
        owned(field, age, slot, own, owner, process)
        if kind not in entries:
            errors.append('Unexpected native event kind')
            continue
        counts[kind] += 1
        if int(entry, 16) != entries[kind] or int(count) != counts[kind] or not valid_ram(a13) or not 0xff800000 <= int(pc, 16) <= 0xffffffff:
            errors.append('Wrong native entry/process/event count')
        if kind != 'parser' and a13 != process:
            errors.append('Action/script/effect does not execute in owned main process')
        if kind == 'parser':
            latest_parser = f
            continue
        if kind == 'action':
            prior = [command for command in commands if command <= f]
            if not prior or not 1 <= f - max(prior) <= 36 or latest_parser is None or not 0 <= f - latest_parser <= 36 or c != counts['action']:
                errors.append('Action lacks the actual command/parser')
            cycles[c] = {'start': f, 'process': process, 'states': [], 'ready': [], **{k: [] for k in entries if k not in ('parser', 'action')}}
        elif c not in cycles:
            errors.append('Event has no actual owned action cycle')
        else:
            data = cycles[c]
            if process != data['process'] or not data['start'] <= f <= df:
                errors.append('Wrong action-cycle ownership/chronology')
            if kind == 'recovery' and (not data['attack'] or f < data['attack'][-1]):
                errors.append('Recovery precedes native collision check')
            data[kind].append(f)
    states = re.findall(r'MK2_RESTART_SEQUENCE_STATE frame=(\d+) age=(\d+) cycle=(\d+) side=(\d+) id=(\d+) actor=([0-9A-F]+) process=([0-9A-F]+) action=([0-9A-F]+) y=(-?\d+) floor=(-?\d+) vx=([0-9A-F]+) vy=([0-9A-F]+) flags=([0-9A-F]+) body=([0-9A-F]+) trail=([0-9A-F]+) victim=([0-9A-F]+) vid=(\d+) vprocess=([0-9A-F]+) vaction=([0-9A-F]+)', log)
    for field, age, cycle, slot, own, owner, process, act, y, floor, vx, vy, flags, body, trail, victim, vid, vprocess, vaction in states:
        owned(field, age, slot, own, owner, process)
        c, f = int(cycle), int(field)
        if c not in cycles or process != cycles[c]['process'] or not cycles[c]['start'] <= f <= df or not valid_ram(victim) or not valid_ram(vprocess) or not 0 <= int(vid) <= 18:
            errors.append('State is not bound to the actual actor/action/victim')
            continue
        cycles[c]['states'].append((f, int(act, 16), int(floor) - int(y), int(vx, 16), int(vy, 16), int(trail, 16), int(vaction, 16)))
    ready = re.findall(r'MK2_RESTART_SEQUENCE_READY frame=(\d+) age=(\d+) cycle=(\d+) side=(\d+) id=(\d+) actor=([0-9A-F]+) process=([0-9A-F]+) y=(-?\d+) floor=(-?\d+) vx=([0-9A-F]+) vy=([0-9A-F]+) flags=([0-9A-F]+) body=([0-9A-F]+) trail=([0-9A-F]+) count=(\d+) writes=(\d+)', log)
    for field, age, cycle, slot, own, owner, process, y, floor, vx, vy, flags, body, trail, count, writes in ready:
        owned(field, age, slot, own, owner, process)
        c, f = int(cycle), int(field)
        counts['ready'] += 1
        if int(count) != counts['ready'] or y != floor or int(vx, 16) or int(vy, 16) or int(flags, 16) & 0x1c or int(body, 16) & 8 or int(trail, 16) or writes != '0':
            errors.append('Incomplete grounded/flag/effect cleanup')
        if c not in cycles or process != cycles[c]['process'] or not cycles[c]['recovery'] or not cycles[c]['recovery'][0] <= f <= df:
            errors.append('Ready state lacks actual owned native recovery')
        else:
            cycles[c]['ready'].append(f)
    complete, paired = [], []
    for c, data in cycles.items():
        required = ('intro', 'attack', 'recovery', 'ready', 'effect', 'step') if target == 'kano' else ('intro', 'loop', 'attack', 'recovery', 'ready')
        if not all(data[k] for k in required):
            continue
        state_rows = [row for row in data['states'] if row[0] <= data['recovery'][0]]
        if target == 'kano':
            live_motion = any(act in (0x117, 0x618) and 0x01000000 <= trail < 0x01100000 for f, act, height, vx, vy, trail, victim_act in state_rows)
        else:
            live_motion = any(act in (0x204, 0x214, 0x611) and height >= 20 and vx != 0 for f, act, height, vx, vy, trail, victim_act in state_rows)
            if any(act == 0x214 and victim_act == 0x215 for f, act, height, vx, vy, trail, victim_act in state_rows):
                paired.append(c)
        if live_motion:
            complete.append(c)
    if not complete:
        errors.append('No complete native blade-effect/bicycle-flight and recovery cycle')
    if result and result != ('true', target, str(side), name, str(len(commands)), *(str(counts[k]) for k in KINDS), '0', '0'):
        errors.append('Result contradicts actual owned events')
    if 'MK2_RESTART_SEQUENCE_ERROR' in log:
        errors.append('Actual sequence observer errors')
    return {'passed': not errors, 'errors': errors, 'target': target, 'side': side, 'move': name,
            'native_counts': counts, 'completed_owned_cycles': complete, 'bicycle_paired_cycles': paired,
            'memory_writes': 0, 'scope': 'owned_blade_effect_or_bicycle_flight_collision_checks_and_recovery_after_restart_not_damage_parity_or_other_specials'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('log', type=Path)
    parser.add_argument('--target', choices=SPECS, required=True)
    parser.add_argument('--side', type=int, choices=(1, 2), required=True)
    args = parser.parse_args()
    result = verify(args.log.read_text(encoding='utf-8-sig'), args.target, args.side)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()
