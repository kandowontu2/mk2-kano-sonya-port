"""Link actual physical Shao jump plans to original native stores and real motion.
An Up attempt, an action assignment and rising flight are separate evidence.
Ignored/interrupted attempts are reported, not promoted to completed moves.
This is not all-move, boss-clear, ending, audio or full-port acceptance.
"""
import argparse, copy, json, struct
from collections import defaultdict
from pathlib import Path
import verify_current_shao_cooldown_retreat_boss_ledger_v2637 as ledger

ROOT = ledger.ROOT
launch = ledger.launch
CASES = {
    f'{fighter}_{policy}': (fighter, capture, proof, policy)
    for fighter in ('kano', 'sonya')
    for capture, proof, policy in ((2633, 2634, 'cooldown_retreat'),)
}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def check(rows, identity):
    plans = [r for r in rows if r['tag'] == 'BOSS_PLAN' and r['stage'] == 16]
    actions = [r for r in rows if r['tag'] == 'BOSS_ACTION' and
               r['stage'] == 16 and r['after'] == 0x308]
    fields = {r['frame']: r for r in rows if r['tag'] == 'BOSS_FIELD' and r['stage'] == 16}
    responses = defaultdict(list)
    for r in rows:
        if r['tag'] == 'BOSS_RESPONSE' and r['stage'] == 16:
            responses[r['frame']].append(r)
    need(plans and actions, 'Non-vacuous actual stage16 plans and native jump assignments')
    need(len({r['event'] for r in actions}) == len(actions), 'Unique actual jump assignment events')
    need(len({r['event'] for r in plans}) == len(plans), 'Unique actual jump plan events')
    by_owner = defaultdict(list)
    for p in plans:
        need(p['human_id'] == identity and p['cpu_id'] == 13 and p['height'] == 0,
             'Actual true own grounded Shao plan')
        by_owner[p['human_actor'], p['human_main']].append(p)
    activated = set()
    matched = []
    for a in actions:
        need(a['pc'] == 0xff831360 and a['mask'] == 0xffff and
             a['id'] == a['roster'] == identity and a['state'] == 1 and
             a['actor'] == a['owner'] == a['a8'] and a['main'] == a['a13'] and
             a['at'] == a['main'] + 0x1f0 and all(0 < int(h) <= 161 for h in a['health'].split(',')),
             'Original native308 store and actual physical actor/Main/register provenance')
        candidates = [p for p in by_owner[a['actor'], a['main']]
                      if p['event'] < a['event'] and 0 <= a['frame'] - p['frame'] < 16]
        need(len(candidates) == 1, 'Exactly one own physical Up plan precedes each native308 assignment')
        p = candidates[0]
        need(p['event'] not in activated, 'One native308 assignment per physical Up plan')
        activated.add(p['event'])
        flying = [fields[f] for f in range(a['frame'] + 1, a['frame'] + 17)
                  if f in fields and fields[f]['human_actor'] == a['actor'] and
                  fields[f]['human_main'] == a['main'] and fields[f]['human_id'] == identity and
                  fields[f]['human_action'] == 0x308 and fields[f]['height'] > 8 and
                  fields[f]['human_vy'] >= 0x80000000]
        motion = flying[0] if flying else None
        if motion:
            real = [r for r in responses[motion['frame']] if
                    r['event'] > motion['event'] and r['kind'] == 'actual_airborne' and
                    r['attempt'] == p['frame'] and r['actor'] == a['actor'] and
                    r['main'] == a['main'] and r['id'] == identity and
                    r['height'] == motion['height'] and r['x'] == motion['h_x'] and
                    r['y'] == motion['h_y']]
            need(len(real) == 1, 'Actual original rising jump field has its own matching motion observation')
        matched.append(dict(planFrame=p['frame'], planEvent=p['event'],
                            nativeAssignmentFrame=a['frame'], nativeAssignmentEvent=a['event'],
                            nativeActor=a['actor'], nativeMain=a['main'],
                            risingFlightFrame=motion['frame'] if motion else None))
    ignored = [dict(frame=p['frame'], action=p['human_action'], actor=p['human_actor'],
                    main=p['human_main'], health=p['health'])
               for p in plans if p['event'] not in activated]
    return dict(physicalJumpAttempts=len(plans), actualOriginal308Assignments=len(actions),
                individuallyMatchedAssignments=len(matched), attemptsWithoutNative308=len(ignored),
                actualRisingFlightAttempts=sum(r['risingFlightFrame'] is not None for r in matched),
                assignedWithoutObservedRisingFlight=sum(r['risingFlightFrame'] is None for r in matched),
                matchedAttempts=matched, unactivatedAttempts=ignored)


def verify(case):
    fighter, capture_version, proof_version, policy = CASES[case]
    identity = 17 if fighter == 'kano' else 18
    capture = ROOT / f'audit_v{capture_version}_current_{fighter}_p1_shao_{policy}_campaign'
    proof_path = ROOT / f'audit_v{proof_version}_current_{fighter}_p1_shao_{policy}_checked/report.json'
    proof = json.loads(proof_path.read_text())
    need(proof['passed'] and proof['bounded_campaign_evidence_proven'] and
         proof['human_slot'] == 1 and proof['player'] == fighter and not proof['fullPortAcceptance'],
         'Accepted complete immutable physical campaign of matching true character')
    pins = dict(proof['inputHashes'])
    for file, wanted in pins.items():
        need(launch.sha(file) == wanted, 'Unchanged actual accepted source/capture ' + file)
    pins[str(proof_path)] = launch.sha(proof_path)
    original_path = ROOT / 'mk2/mk2-maincpu.bin'
    need(launch.sha(original_path) == '45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23',
         'Pinned original native main CPU ROM')
    offset = (0xff831320 - 0xff800000) // 8
    native_code = original_path.read_bytes()[offset:offset + 8]
    need(struct.unpack('<4H', native_code) == (0x09c0, 0x0308, 0xb00d, 0x01f0) and
         (capture / 'guest_maincpu.bin').read_bytes()[offset:offset + 8] == native_code,
         'Original MOVI308 and Main+1F0 native assignment bytes unchanged in actual guest')
    pins[str(original_path)] = launch.sha(original_path)
    rows = ledger.native.parse((capture / 'run.log').read_text(encoding='utf-8-sig'), 1, fighter)
    control = check(rows, identity)
    first = control['matchedAttempts'][0]
    action_index = next(i for i, r in enumerate(rows) if r['event'] == first['nativeAssignmentEvent'])
    plan_index = next(i for i, r in enumerate(rows) if r['event'] == first['planEvent'])
    mutations = [
        ('wrong_original_jump_pc', action_index, 'pc', 16, 'Original native308 store'),
        ('wrong_native_jump_main_register', action_index, 'a13', 16, 'Original native308 store'),
        ('missing_own_actual_jump_plan', plan_index, None, None, 'Exactly one own physical Up plan'),
        ('swapped_own_jump_plan_actor', plan_index, 'human_actor', 32, 'Exactly one own physical Up plan'),
        ('jump_plan_after_activation', plan_index, 'frame', 100, 'Exactly one own physical Up plan'),
        ('duplicate_native_jump_assignment', action_index, 'duplicate', None, 'Unique actual jump assignment events')]
    real = next(r for r in control['matchedAttempts'] if r['risingFlightFrame'] is not None)
    response_index = next(i for i, r in enumerate(rows) if r['tag'] == 'BOSS_RESPONSE' and
                          r['stage'] == 16 and r['frame'] == real['risingFlightFrame'])
    mutations.append(('missing_actual_jump_motion', response_index, None, None,
                      'Actual original rising jump field'))
    outcomes = []
    for name, index, key, delta, label in mutations:
        changed = copy.deepcopy(rows)
        if key is None:
            changed.pop(index)
        elif key == 'duplicate':
            changed.insert(index, copy.deepcopy(changed[index]))
        else:
            changed[index][key] += delta
        try:
            check(changed, identity)
        except ValueError as error:
            need(label in str(error), 'Specific intended rejection, not incidental failure: ' + str(error))
            outcomes.append(dict(name=name, rejectedBy=str(error)))
        else:
            raise ValueError('Malformed native jump chronology accepted: ' + name)
    need(check(rows, identity) == control, 'Final untouched full actual jump correspondence control')
    pins[str(Path(__file__).resolve())] = launch.sha(__file__)
    launch.module_pins(pins)
    return dict(passed=True, case=case, campaignReport=str(proof_path), **control,
                rejectedSpecificCounterexamples=len(outcomes), outcomes=outcomes,
                finalUnmodifiedControlPassed=True, attemptsNeverAssumedActivations=True,
                gameChanged=False, fullPortAcceptance=False, inputHashes=pins, scope=__doc__)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('case', choices=CASES)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    need(not args.output.exists(), 'Immutable actual individual jump proof')
    report = verify(args.case)
    args.output.mkdir()
    (args.output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items()
                      if k not in ('inputHashes', 'outcomes', 'matchedAttempts', 'unactivatedAttempts')}, indent=2), flush=True)
