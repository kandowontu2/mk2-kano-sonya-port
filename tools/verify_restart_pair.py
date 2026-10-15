"""Verify real post-ending close-move pairs, native damage and both recoveries."""
import argparse
import json
import re
from pathlib import Path

SPECS = {
    'kano': dict(name='choke', id=17, parser=0xfff91000, action=0xfff91400,
                 intro=0xfff94000, attack=0xfff94800, release=0xfff93800,
                 state=0x111, victim_state=0x112, damage=32,
                 descriptor='101,32,63,17,6656,0,0,0,1'),
    'sonya': dict(name='leg', id=18, parser=0xfff80000, action=0xfff80800,
                  intro=0xfff83000, attack=0xfff83800, release=0xfff82200,
                  state=0x110, victim_state=0x111, damage=35,
                  descriptor='115,34,72,77,6400,0,0,0,2'),
}
KINDS = ('parser', 'action', 'intro', 'attack', 'step', 'pulse', 'damage',
         'release', 'fling', 'velocity', 'own_recovery', 'victim_recovery')
CHOKE_OWN = (0xfe8304e0, 0xfe830540, 0xfe8305a0, 0xfe830600, 0xfe830660, 0xfe8306c0, 0xfe830660)
CHOKE_XY = {17: ((79, -8), (56, -31), (27, -28), (29, -26), (51, -43), (68, -45), (51, -43)),
            18: ((77, -19), (52, -43), (26, -36), (29, -36), (54, -50), (64, -50), (54, -50))}
CHOKE_GROUPS = (0xff917430, 0xff924db0, 0xff930c00, 0xff93e430, 0xff94f340, 0xff94f340,
                0xff95c500, 0xff96aaf0, 0xff97bcb0, 0xff97bcb0, 0xff97bcb0, 0xff991030)
CHOKE_GRIP = ((-9, 50), (-7, 44), (-11, 48), (-14, 47), (-12, 47), (-12, 47),
              (-19, 48), (-7, 43), (-9, 41), (-9, 41), (-9, 41), (-6, 44))
LEG_OWN = (0xfe83be60, 0xfe83be00, 0xfe83bda0, 0xfe83bd40, 0xfe83bce0)
LEG_XY = {
    0: ((86, -4), (67, -53), (14, -50), (-48, 5), (-94, 33)),
    1: ((84, 1), (64, -42), (1, -49), (-48, -23), (-92, 12)),
    2: ((85, -8), (59, -33), (4, -50), (-53, -18), (-98, 1)),
    3: ((86, -10), (59, -23), (10, -61), (-68, -26), (-106, 16)),
    4: ((87, -3), (68, -41), (19, -62), (-56, -21), (-96, 31)),
    6: ((90, 0), (68, -48), (10, -65), (-55, -50), (-99, 13)),
    7: ((91, -8), (66, -50), (2, -77), (-57, -32), (-107, 30)),
    8: ((83, -13), (62, -43), (8, -62), (-64, -41), (-107, 16)),
    11: ((86, -12), (63, -52), (4, -85), (-52, -35), (-96, 25)),
    17: ((85, 0), (68, -41), (10, -80), (-56, -55), (-100, 0)),
    18: ((88, 3), (67, -41), (7, -74), (-55, -38), (-111, 0)),
}
LEG_GROUPS = {
    0: (0xff916f90, 0xff91a190, 0xff91d860, 0xff91d8e0, 0xff91d9e0),
    1: (0xff926750, 0xff928410, 0xff928470, 0xff9284f0, 0xff928550),
    2: (0xff9307c0, 0xff936c50, 0xff936cb0, 0xff936d30, 0xff936d90),
    3: (0xff93dff0, 0xff945070, 0xff9450d0, 0xff945150, 0xff9451d0),
    4: (0xff94dce0, 0xff94d900, 0xff954f70, 0xff955010, 0xff955070),
    6: (0xff95c080, 0xff960100, 0xff9631c0, 0xff963220, 0xff963260),
    7: (0xff96a670, 0xff9707f0, 0xff970850, 0xff9708f0, 0xff970970),
    8: (0xff97b850, 0xff983db0, 0xff983df0, 0xff983e50, 0xff983eb0),
    11: (0xff992df0, 0xff994e90, 0xff994ed0, 0xff994f30, 0xff994f90),
    17: (0xfe829800, 0xfe82aa60, 0xfe82aae0, 0xfe82ab40, 0xfe82ab80),
    18: (0xfe836f00, 0xfe83adc0, 0xfe83ae60, 0xfe83aec0, 0xfe83af20),
}
for alias, body in ((5, 4), (9, 8), (10, 8), (14, 8), (15, 8), (16, 4)):
    LEG_XY[alias], LEG_GROUPS[alias] = LEG_XY[body], LEG_GROUPS[body]


def verify(log, target, side):
    spec = SPECS[target]
    if side not in (1, 2):
        raise ValueError('Invalid paired-move side')
    errors, counts, cycles = [], dict.fromkeys(KINDS, 0), {}

    def rows(tag):
        return [dict(re.findall(r'(\w+)=([^\s]+)', line)) for line in log.splitlines()
                if line.startswith('MK2_RESTART_PAIR_' + tag + ' ')]

    def unique(tag):
        found = rows(tag)
        if len(found) != 1:
            errors.append('Missing/duplicate ' + tag)
            return {}
        return found[0]

    def number(row, key, base=10):
        try:
            return int(row[key], base)
        except (KeyError, ValueError):
            errors.append('Missing/invalid numeric ' + key)
            return 0

    def ram(row, key):
        value = number(row, key, 16)
        if not 0x01000000 <= value < 0x01100000:
            errors.append('Invalid RAM ' + key)
        return value

    matches = re.findall(r'MK2_RESTART_MATCH frame=(\d+) target=(\w+) id=(\d+) actor=([0-9A-F]+) stage=(\d+)', log)
    ends = re.findall(r'MK2_RESTART_COMPLETE frame=(\d+)[^\r\n]* live=(\d+) errors=(\d+) restart_writes=(\d+)', log)
    if len(matches) != 1 or len(ends) != 1:
        return dict(passed=False, errors=['Actual fresh match/completion missing'], target=target, side=side)
    match, done = matches[0], ends[0]
    mf, df, actor = int(match[0]), int(done[0]), match[3]
    if match[1:3] != (target, str(spec['id'])) or match[4] != '0' or df - mf != 600 or done[1:] != ('601', '0', '0'):
        errors.append('Wrong actual target/stage/601-field coverage')
    cpu_rows = re.findall(r'MK2_RESTART_CPU frame=(\d+) state=(\d+) roster=(\d+) id=(\d+) actor=([0-9A-F]+)[^\r\n]* cpu_side=(\d+)', log)
    victim, vid = None, None
    if len(cpu_rows) != 2 or [int(row[0]) for row in cpu_rows] != [mf, df]:
        errors.append('Actual CPU bookends missing')
    else:
        victim, vid = cpu_rows[0][4], int(cpu_rows[0][3])
        if cpu_rows[0][1:] != cpu_rows[1][1:] or any(row[1] != '0' or row[2] != row[3] or row[5] != str(3-side) for row in cpu_rows):
            errors.append('Wrong/stale opposite CPU ownership')
    guard, plan, result = unique('ROM'), unique('PLAN'), unique('RESULT')
    if (guard.get('target'), guard.get('side'), guard.get('move'), guard.get('writes')) != (target, str(side), spec['name'], '0'):
        errors.append('Wrong native move guard')
    for key in ('parser', 'action', 'intro', 'attack', 'release', 'state', 'victim_state'):
        if number(guard, key, 16) != spec[key]:
            errors.append('Wrong native ' + key)
    if number(guard, 'damage') != spec['damage'] or guard.get('descriptor') != spec['descriptor']:
        errors.append('Wrong native catch descriptor/damage')
    first = number(plan, 'first')
    if not 0 <= first <= 140 or {k: plan.get(k) for k in ('gap', 'attempts', 'latest', 'cooldown', 'approach', 'command', 'writes')} != dict(
            gap='104', attempts='4', latest='400', cooldown='90', approach='walk_continuous', command='grounded_walk_or_idle', writes='0'):
        errors.append('Wrong real-input plan')

    def owned(row):
        f = number(row, 'frame')
        if not mf <= f <= df or number(row, 'age') != f-mf or (row.get('side'), row.get('id'), row.get('actor')) != (str(side), str(spec['id']), actor):
            errors.append('Wrong actor/side/identity/epoch')
        ram(row, 'process'); ram(row, 'vprocess'); ram(row, 'victim')
        if row.get('victim') != victim or number(row, 'vid') != vid:
            errors.append('Wrong actual native victim')
        return f

    def clean(row, victim_too=False):
        ok = (number(row, 'y') == number(row, 'floor') and number(row, 'vx', 16) == 0 and number(row, 'vy', 16) == 0 and
              number(row, 'flags', 16) & 0x1c == 0 and number(row, 'body', 16) & 8 == 0 and number(row, 'trail', 16) == 0)
        if victim_too:
            vx = number(row, 'vvx', 16)
            vx = vx-0x100000000 if vx >= 0x80000000 else vx
            ready_velocity = vx == 0 or (number(row, 'vaction', 16) == 0x303 and abs(vx) <= 0x30000)
            ok = ok and (number(row, 'vypos') == number(row, 'vfloor') and ready_velocity and number(row, 'vvy', 16) == 0 and
                         number(row, 'vflags', 16) & 0x1c == 0 and number(row, 'vbody', 16) & 8 == 0 and number(row, 'vtrail', 16) == 0)
        return ok

    commands = rows('COMMAND')
    if not 1 <= len(commands) <= 4:
        errors.append('Missing actual command attempts')
    previous = -1000
    for index, row in enumerate(commands, 1):
        f = owned(row)
        direction = 'right' if number(row, 'x') < number(row, 'vxpos') else 'left'
        gap = abs(number(row, 'x')-number(row, 'vxpos'))
        if (row.get('target'), row.get('move'), row.get('forward'), row.get('button'), row.get('writes')) != (
                target, spec['name'], direction, 'lp' if target == 'kano' else 'lp_block', '0') or number(row, 'attempt') != index:
            errors.append('Wrong actual direction/button/attempt')
        vx = number(row, 'vx', 16)
        vx = vx-0x100000000 if vx >= 0x80000000 else vx
        command_ready = (number(row, 'y') == number(row, 'floor') and number(row, 'vy', 16) == 0 and
                         abs(vx) <= 0x28000 and number(row, 'flags', 16) & 0x1c == 0 and
                         number(row, 'body', 16) & 8 == 0 and number(row, 'trail', 16) == 0)
        if not first <= f-mf <= 400 or f-previous < 90 or gap > 104 or number(row, 'gap') != gap or not command_ready or number(row, 'vypos') != number(row, 'vfloor') or number(row, 'vvy', 16):
            errors.append('Wrong actual grounded command/range/cooldown')
        previous = f
    entries = {key: spec[key] for key in ('parser', 'action', 'intro', 'attack', 'release')}
    entries.update(step=0xfff89400, pulse=0xfff93400, damage=0xff837340, fling=0xff876650,
                   velocity=0xff831bd0, own_recovery=0xff861350, victim_recovery=0xff861350)
    latest_parser = None
    for row in rows('EVENT'):
        f, c, kind = owned(row), number(row, 'cycle'), row.get('kind')
        if kind not in counts:
            errors.append('Unknown native event'); continue
        counts[kind] += 1
        if number(row, 'entry', 16) != entries[kind] or number(row, 'count') != counts[kind] or not 0xff800000 <= number(row, 'pc', 16) <= 0xffffffff:
            errors.append('Wrong native event/entry/count/PC')
        a8, a13 = row.get('a8'), ram(row, 'a13')
        own_kind = kind in ('parser', 'action', 'intro', 'attack', 'step', 'own_recovery')
        if a8 != (actor if own_kind else victim):
            errors.append('Wrong actual executing actor')
        if kind != 'parser' and a13 not in ([number(row, 'process', 16), number(row, 'vprocess', 16)] if kind in ('pulse', 'damage') else
                                          [number(row, 'process' if own_kind else 'vprocess', 16)]):
            errors.append('Wrong actual native main process')
        if kind == 'parser':
            latest_parser = f; continue
        if kind == 'action':
            prior = [r for r in commands if number(r, 'frame') <= f]
            if not prior or not 1 <= f-number(prior[-1], 'frame') <= 36 or latest_parser is None or not 0 <= f-latest_parser <= 36 or c != counts['action']:
                errors.append('Action lacks actual command/parser')
            cycles[c] = dict(start=f, process=row.get('process'), vprocess=row.get('vprocess'),
                             direction=1 if prior and prior[-1].get('forward') == 'right' else -1,
                             states={}, health=[], ready=[], **{k: [] for k in KINDS if k not in ('parser', 'action')})
        elif c not in cycles:
            errors.append('Native event has no owned action cycle')
        else:
            data = cycles[c]
            if row.get('process') != data['process'] or row.get('vprocess') != data['vprocess'] or f < data['start']:
                errors.append('Wrong live action-cycle ownership')
            if kind == 'damage' and number(row, 'value', 16) != (8 if target == 'kano' else 35):
                errors.append('Wrong native damage argument')
            data[kind].append(row)
    health_count = 0
    for row in rows('HEALTH'):
        owned(row); c = number(row, 'cycle'); health_count += 1
        if c not in cycles or row.get('process') != cycles[c]['process'] or row.get('vprocess') != cycles[c]['vprocess'] or row.get('a8') != victim or number(row, 'a13', 16) not in (number(row, 'process', 16), number(row, 'vprocess', 16)):
            errors.append('Health store is not actual paired victim execution')
        if number(row, 'before')-number(row, 'after') != (8 if target == 'kano' else 35) or number(row, 'count') != health_count or row.get('observer_writes') != '0' or number(row, 'pc', 16) != 0xff836700:
            errors.append('Wrong native health delta/store/count/observer writes')
        if c in cycles:
            cycles[c]['health'].append(row)
    for tag in ('STATE', 'READY', 'MISS'):
        for row in rows(tag):
            f, c = owned(row), number(row, 'cycle')
            if c not in cycles or row.get('process') != cycles[c]['process'] or row.get('vprocess') != cycles[c]['vprocess'] or f < cycles[c]['start'] or row.get('writes') != '0':
                errors.append('Wrong actual cycle state'); continue
            if tag == 'STATE':
                if f in cycles[c]['states']:
                    errors.append('Duplicate actual state field')
                cycles[c]['states'][f] = row
            elif tag == 'READY':
                cycles[c]['ready'].append(row)
                if not clean(row, True) or number(row, 'action', 16) == spec['state'] or number(row, 'vaction', 16) == spec['victim_state']:
                    errors.append('Incomplete two-actor grounded/flag/attachment cleanup')
            elif not clean(row):
                errors.append('Miss did not recover normally')
    complete = []
    for c, data in cycles.items():
        if not data['ready']:
            continue
        before = len(errors)
        expected_steps, expected_calls = (22, 4) if target == 'kano' else (5, 1)
        if len(data['step']) != expected_steps or len(data['health']) != expected_calls or len(data['damage']) != expected_calls or len(data['release']) != 1 or len(data['fling']) != 1 or len(data['velocity']) != 1 or not data['attack'] or not data['intro'] or len(data['own_recovery']) != 1 or len(data['victim_recovery']) != 1 or len(data['ready']) != 1:
            errors.append('Incomplete actual pair/damage/fling/two-process recovery chain'); continue
        steps = [number(r, 'frame') for r in data['step']]
        release = number(data['release'][0], 'frame')
        ready = number(data['ready'][0], 'frame')
        if not data['start'] < steps[0] <= release < ready <= df or any(number(data[k][0], 'frame') > ready for k in ('own_recovery', 'victim_recovery')):
            errors.append('Wrong paired release/recovery chronology')
        if set(data['states']) != set(range(data['start']+1, ready+1)):
            errors.append('Missing actual per-field paired/recovery state coverage')
        if sum(number(r, 'before')-number(r, 'after') for r in data['health']) != spec['damage']:
            errors.append('Incorrect complete native damage total')
        if any(number(previous, 'after') != number(following, 'before') for previous, following in zip(data['health'], data['health'][1:])):
            errors.append('Native health stores do not form a continuous damage chain')
        if number(data['ready'][0], 'vhealth') != number(data['health'][-1], 'after'):
            errors.append('Recovered victim health contradicts actual native stores')
        for dose, store in zip(data['damage'], data['health']):
            if not 0 <= number(store, 'frame')-number(dose, 'frame') <= 1:
                errors.append('Health change lacks actual native damage call')
        fling = data['fling'][0]
        params = (0x40000, 0xfffc0000, 0x8000, 5) if target == 'kano' else (0x30000, 0xfffa0000, 0x8000, 4)
        if tuple(number(fling, 'a'+str(n), 16) for n in range(4)) != params or not 0 <= number(fling, 'frame')-release <= 1:
            errors.append('Wrong original native fling parameters')
        vx = data['direction'] * (0x40000 if target == 'kano' else -0x30000) & 0xffffffff
        velocity = data['velocity'][0]
        destination = 0x01060ea0 if side == 1 else 0x010602d0
        if number(velocity, 'a0', 16) != vx or number(velocity, 'a1', 16) != destination or not 0 <= number(velocity, 'frame')-release <= 1:
            errors.append('Wrong actual victim signed velocity request')
        if target == 'kano':
            if any(steps[i]-steps[i-1] != (5 if i <= 3 else 3) for i in range(1, 22)):
                errors.append('Wrong original 22-pose timing')
            pulses = [number(r, 'frame') for r in data['pulse']]
            if pulses != [steps[3]+12*n for n in range(1, 5)] or [number(r, 'frame') for r in data['damage']] != pulses:
                errors.append('Wrong original four-squeeze/12-field damage cadence')
            if release not in (steps[-1], steps[-1]+1):
                errors.append('Wrong actual last held pose/release timing')
            for i, step in enumerate(data['step']):
                phase = i if i < 3 else (i-3) % 4+3
                row = data['states'].get(steps[i]+1, {})
                if vid in (17, 18):
                    dx, dy = CHOKE_XY[vid][phase]
                    pose = 0xfe836860 if vid == 18 else (0xfe8294a0 if phase == 6 else 0xfe829500)
                else:
                    body = vid if vid is not None and vid < 12 else (4 if vid == 16 else 8)
                    dx, dy = CHOKE_XY[18][phase]; gx, gy = CHOKE_GRIP[body]
                    dx += 8+gx; dy += 54-gy; pose = CHOKE_GROUPS[body]
                if number(step, 'value', 16) != CHOKE_OWN[phase] or number(row, 'pose', 16) != CHOKE_OWN[phase] or number(row, 'vpose', 16) != pose or number(row, 'vxpos') != number(row, 'x')+data['direction']*dx or number(row, 'vypos') != number(row, 'y')+dy or number(row, 'y') != number(row, 'floor') or number(row, 'vx', 16) or number(row, 'vy', 16):
                    errors.append('Wrong actual original choke composite/contact phase')
                allowed = (spec['victim_state'], 0x506) if i == 21 and release <= steps[i] else (spec['victim_state'],)
                if number(row, 'vaction', 16) not in allowed:
                    errors.append('Wrong paired choke victim state')
            held = data['states'].get(steps[-1]+1, {})
            if number(held, 'vypos') >= number(held, 'vfloor'):
                errors.append('Choke did not release from the actual lifted height')
        else:
            if steps != [steps[0]+n for n in (0, 30, 34, 38, 42)] or release not in (steps[0]+46, steps[0]+47):
                errors.append('Wrong original five-phase/46-field leg timing')
            if data['pulse']:
                errors.append('Leg release cannot use choke damage pulses')
            origin = data['states'].get(steps[0]+1, {})
            for elapsed in range(46):
                row = data['states'].get(steps[0]+1+elapsed, {})
                phase = 0 if elapsed < 30 else 1+(elapsed-30)//4
                shake = 3 if elapsed < 30 and (elapsed//3) % 2 == 0 else 0
                if vid not in LEG_XY:
                    errors.append('Unsupported actual leg victim'); break
                dx, dy = LEG_XY[vid][phase]
                if number(row, 'x') != number(origin, 'x') or number(row, 'y') != number(origin, 'y') or number(row, 'vx', 16) or number(row, 'vy', 16) or number(row, 'vvx', 16) or number(row, 'vvy', 16) or number(row, 'vxpos') != number(origin, 'x')+data['direction']*dx or number(row, 'vypos') != number(origin, 'y')+dy+shake or number(row, 'pose', 16) != LEG_OWN[phase] or number(row, 'vpose', 16) != LEG_GROUPS[vid][phase]:
                    errors.append('Wrong original per-field leg pose/contact/shake')
                if number(row, 'health') != number(origin, 'health') or number(row, 'vhealth') != number(origin, 'vhealth') or number(row, 'suppression') <= 0 or number(row, 'action', 16) != spec['state'] or number(row, 'vaction', 16) != spec['victim_state']:
                    errors.append('Wrong paired leg state/health/native push suppression')
            if [number(r, 'value', 16) for r in data['step']] != list(LEG_OWN) or number(data['health'][0], 'frame') != release:
                errors.append('Leg damage does not belong to actual release')
            released = data['states'].get(release+1, {})
            if number(released, 'vypos') != number(released, 'vfloor') or number(released, 'vvy', 16) != 0xfffa0000 or number(released, 'vaction', 16) != 0x506:
                errors.append('Missing native floor-restored leg release/launch')
        if number(data['ready'][0], 'damage') != spec['damage'] or number(data['ready'][0], 'stores') != expected_calls or number(data['ready'][0], 'steps') != expected_steps:
            errors.append('Ready summary contradicts actual paired damage/poses')
        if len(errors) == before:
            complete.append(c)
    if not complete:
        errors.append('No complete native paired choreography, damage and two-actor recovery')
    result_keys = {'parsers': 'parser', 'actions': 'action', 'intros': 'intro', 'attacks': 'attack', 'steps': 'step',
                   'pulses': 'pulse', 'damage_calls': 'damage', 'releases': 'release', 'flings': 'fling', 'velocities': 'velocity',
                   'own_recoveries': 'own_recovery', 'victim_recoveries': 'victim_recovery'}
    if (result.get('pass'), result.get('target'), result.get('side'), result.get('move'), result.get('errors'), result.get('writes')) != ('true', target, str(side), spec['name'], '0', '0'):
        errors.append('Wrong observer result')
    if any(number(result, key) != counts[kind] for key, kind in result_keys.items()) or number(result, 'commands') != len(commands) or number(result, 'health_stores') != health_count or number(result, 'ready') != len(rows('READY')) or number(result, 'misses') != len(rows('MISS')):
        errors.append('Result counts contradict actual events')
    if 'MK2_RESTART_PAIR_ERROR' in log or re.search(r'\[LUA ERROR\]|fatal error|access violation', log, re.I):
        errors.append('Actual runtime errors')
    return dict(passed=not errors, errors=errors, target=target, side=side, move=spec['name'],
                native_counts=counts, completed_owned_cycles=complete, damage_per_cycle=spec['damage'],
                memory_writes=0, scope='full_native_close_pair_poses_health_fling_and_both_recoveries_after_restart_not_all_specials_or_unassisted_tower')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('log', type=Path)
    parser.add_argument('--target', choices=SPECS, required=True)
    parser.add_argument('--side', choices=(1, 2), type=int, required=True)
    args = parser.parse_args()
    result = verify(args.log.read_text(encoding='utf-8-sig'), args.target, args.side)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()
