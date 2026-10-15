"""Existing physical CPU leg -> Square -> ordinary attack, not idle-tail acceptance.

Keep the original standalone rejection. Retain every original Square mechanic
through its clean first post-regain callback; replace only the idle-tail context
with the independently observed complete native state/HP ledgers and a separate
new-attack setup/contact/recovery check. No new game, pixels or audio claim.
"""
import datetime, inspect, json, re, subprocess, traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import inventory_current_cpu_leg_choices_v6276 as inventory
import inventory_current_cpu_leg_choices_v6278 as mutations
import current_sonya_cpu_square_contract_v2045 as square

ROOT, need, sha = current.ROOT, current.need, current.sha
OUT = ROOT / 'audit_v6283_current_cpu_leg_square_compound_checked'
PARENT = ROOT / 'audit_v6281_current_existing_cpu_inventory/report.json'


def square_through_handoff():
    source = inspect.getsource(square.verify)
    changes = {
        'set(range(start,ready+32))': 'set(range(start,ready+2))',
        'for at in range(start,ready+32):': 'for at in range(start,ready+2):',
        "start<=r['frame']<=ready+30": "start<=r['frame']<=ready",
        'for at in range(ready+1,ready+32):': 'for at in range(ready+1,ready+2):',
        'everyPostRegainCallback=True,lastScene=ready+30': 'firstPostRegainCallback=True,lastScene=ready+1',
        "'Miss and whole recovery tail have no invented damage'": "'Square miss and native recovery have no invented damage'",
    }
    for before, after in changes.items():
        need(source.count(before) == 1, 'Only explicit idle-tail context adaptation: ' + before)
        source = source.replace(before, after, 1)
    scope = dict(square.verify.__globals__)
    exec(compile(source, str(Path(__file__)) + '::whole_original_square_through_handoff', 'exec'), scope)
    return scope['verify'], changes


def clean(r, prefix=''):
    return (r[prefix+'flags'] & 0x1c == 0 and r[prefix+'body'] & 0xc == 0
            and r[prefix+'trail'] == r[prefix+'vy'] == r[prefix+'gravity'] == 0
            and r['vypos' if prefix else 'y'] == r[prefix+'floor'])


def gate(text, guest, square_gate):
    base = inventory.gate(text, guest)
    leg = base['originalLegContracts'][2]
    special = square_gate(text, guest)
    need(leg['own_handoff'] < special['start'] < leg['victim_handoff'] < special['ready'],
         'Square is a new action after own leg cleanup, overlapping only victim recovery')
    fields = square.P.rows(text, 'FIELD'); by = {r['frame']: r for r in fields}
    events = square.original.rows(text, 'EVENT'); flags = square.P.flag_rows(text)
    handoff = special['ready']; origin = by[handoff+1]
    actor, main = origin['actor'], origin['main']
    own = [r for r in events if r['a8'] == actor and r['a13'] == main]
    next_regain = next(r for r in own if r['kind'] == 'regain' and r['frame'] > handoff)
    finish = next_regain['frame']
    need(0 < finish-handoff < 100, 'Next ordinary attack naturally reaches native recovery')
    need(set(range(handoff+1, finish+32)) <= set(by), 'Continuous next-attack and thirty post-recovery callbacks')
    need(clean(origin) and clean(by[finish+1]), 'Separate clean callbacks before and after NEW ordinary attack')
    owned = [r for r in flags if r['slot'] == 2 and handoff < r['frame'] <= finish]
    for r in owned:
        need((r['actor'], r['main'], r['a8'], r['a13'], r['id'], r['state']) ==
             (actor, main, actor, main, 18, 0), 'Next attack stores execute under true Sonya Main')
    actions = [r for r in owned if r['kind'] == 'action']
    changed = [r for r in actions if r['before'] != r['after']]
    expected = [(handoff+1, 0x303, 0x104, 0xff83c340),
                (handoff+25, 0x104, 0x60c, 0xff83c340),
                (finish, 0x60c, 0, 0xff83edd0), (finish, 0, 0x303, 0xff9065d0)]
    need([(r['frame'], r['before'], r['after'], r['pc']) for r in changed] == expected,
         'Native animation consumer publishes ordinary attack and its recovery, not another special')
    for r in actions:
        register = 'a1' if r['pc'] == 0xff83c340 else 'a0'
        need(r[register] & 65535 == r['after'] and (r['op0'], r['op1']) ==
             (0xb02d if register == 'a1' else 0xb00d, 0x1f0), 'Original action store consumes actual live register')
    for kind, mask, setup, cleanup in [('body', 4, 0xff838cf0, 0xff83eeb0),
                                      ('flags', 0x10, 0xff877d50, 0xff83efc0)]:
        stores = [r for r in owned if r['kind'] == kind]
        sets = [r for r in stores if r['pc'] == setup]
        clears = [r for r in stores if r['pc'] == cleanup]
        need(len(sets) == 2 and all(r['frame'] == handoff+1 and
             r['after'] == r['before'] | mask for r in sets) and sets[0]['before'] & mask == 0,
             'New native ' + kind + ' setup after clean Square handoff')
        clear_mask = 0xc if kind == 'body' else 0x14
        need(len(clears) == 3 and all(r['frame'] == finish and
             r['after'] == r['before'] & ~clear_mask for r in clears)
             and clears[0]['before'] & mask and not clears[-1]['after'] & mask,
             'Entire new ordinary ' + kind + ' lock clears at native recovery')
        need(len(stores) == len(sets)+len(clears), 'No unaccounted next-attack lock store')
    hits = [r for r in square.original.rows(text, 'HEALTH')
            if handoff < r['frame'] <= finish and r['before'] != r['after']]
    need(len(hits) == 1, 'Exactly one subsequent native ordinary damage store')
    hit = hits[0]
    need((hit['frame'], hit['slot'], hit['pc'], hit['mask'], hit['a8'], hit['a13'], hit['a10']) ==
         (handoff+7, 1, 0xff836700, 65535, actor, main, 26)
         and hit['before']-hit['after'] == 26, 'Physical native ordinary contact, not Square damage or injected HP')
    guard = [r for r in own if r['kind'] == 'guard' and r['frame'] == hit['frame']]
    need(len(guard) == 1 and guard[0]['action'] == 0x104 and guard[0]['a0'] == origin['vactor']
         and guard[0]['pc'] == 0xff837d50, 'Original collision guard runs under new ordinary action')
    for at in range(handoff+1, finish+2):
        r = by[at]
        need(r['hp'] == origin['hp'] and r['vhp'] ==
             (hit['before'] if at <= hit['frame'] else hit['after']), 'Next ordinary damage ledger covers every callback')
        need(r['y'] == r['floor'] and r['vy'] == r['gravity'] == r['trail'] == 0,
             'Ordinary continuation remains grounded without special trail/gravity')
        if handoff+2 <= at <= finish:
            need(r['flags'] & 0x1c == 0x10 and r['body'] & 0xc == 4,
                 'Only new ordinary attack locks persist before its own cleanup')
    need(next_regain['entry'] == 0xff861500 and next_regain['pc'] == 0xff861510
         and next_regain['action'] == 0 and next_regain['main_owner'] == actor
         and next_regain['flags'] & 0x1c == next_regain['body'] & 0xc == 0
         and next_regain['vx'] == next_regain['vy'] == next_regain['gravity'] == next_regain['trail'] == 0
         and next_regain['yraw'] == origin['floor'] << 16, 'Native ordinary ready restores detached grounded control')
    need(clean(by[finish+1], 'v'), 'Victim is also detached after ordinary attack recovery')
    return dict(passed=True, leg=leg, square=special, wholeNativeHealthLedger=base['wholeNativeHealthLedger'],
                wholeNativeStateLedger=base['wholeNativeStateLedger'], standaloneRejectionPreserved=True,
                ordinaryContinuation=dict(setup=handoff+1, contact=hit['frame'], damage=26,
                                          ready=finish, cleanCallback=finish+1, lastObservedTail=finish+31),
                fullOrdinaryChoreographyAcceptance=False, artShadowAudioAcceptance=False)


def change(text, prefix, key, value, predicate):
    return inventory.prior.mutate_field(text, prefix, key, value, predicate)


def main():
    need(not OUT.exists(), 'Fresh compound acceptance evidence')
    parent = json.loads(PARENT.read_text()); need(parent['passed'], 'Existing original CPU inventory remains passed')
    need(all(sha(p) == h for p, h in parent['inputHashes'].items()), 'Whole previous sources/evidence unchanged')
    need(not inventory.prior.census.prior.census(), 'No live native jobs; reuse actual existing captures')
    guest = current.expected(); inventory.prior.phase_source.phase_contract_source()
    square_gate, adaptations = square_through_handoff()
    pins = dict(parent['inputHashes']); cases=[]; faults=[]
    for suffix in ('samples', 'nosamples'):
        folder = ROOT / ('audit_v5324_current_cpu_bicycle_ram_' + suffix)
        text = (folder/'run.log').read_text(); result = gate(text, guest, square_gate)
        a = result['square']['start']; b = result['square']['ready']; end = result['ordinaryContinuation']['ready']
        tests = [
            ('leg_held_pose', mutations.held_mutation(text, 'MK2_CPU_PAIR_FIELD', 'pose', '00000000', lambda r:r.get('action')=='272')),
            ('leg_release_damage', change(text, 'MK2_CPU_PAIR_EVENT', 'a10', '00000022', lambda r:r.get('kind')=='damage')),
            ('leg_cleanup_lock', change(text, 'MK2_CPU_PAIR_OWN_REGAIN', 'body', '0004', lambda r:r.get('cycle')=='3')),
            ('square_rise_y', change(text, 'MK2_CPU_PAIR_FIELD', 'yraw', '00000000', lambda r:r.get('frame')==str(a+2))),
            ('square_flight_pose', change(text, 'MK2_CPU_PAIR_FIELD', 'pose', '00000000', lambda r:r.get('frame')==str(a+15))),
            ('square_fall_gravity', change(text, 'MK2_CPU_PAIR_FIELD', 'gravity', '00000000', lambda r:r.get('frame')==str(a+36))),
            ('square_regain_lock', change(text, 'MK2_CPU_OVERLAP_EVENT', 'flags', '0010', lambda r:r.get('kind')=='regain' and r.get('frame')==str(b))),
            ('new_attack_publication', change(text, 'MK2_CPU_PAIR_FLAG', 'after', '0207', lambda r:r.get('kind')=='action' and r.get('frame')==str(b+1))),
            ('new_attack_owner', change(text, 'MK2_CPU_PAIR_FLAG', 'a13', '01000000', lambda r:r.get('kind')=='body' and r.get('frame')==str(b+1))),
            ('ordinary_damage', change(text, 'MK2_CPU_OVERLAP_HEALTH', 'a10', '00000019', lambda r:r.get('frame')==str(b+7))),
            ('ordinary_cleanup', change(text, 'MK2_CPU_OVERLAP_EVENT', 'body', '0004', lambda r:r.get('kind')=='regain' and r.get('frame')==str(end))),
            ('recovery_tail_missing', text.replace(next(line+'\n' for line in text.splitlines() if line.startswith('MK2_CPU_PAIR_FIELD ') and f'frame={end+31} ' in line), '', 1)),
        ]
        for label, bad in tests:
            need(bad != text, 'Fault changes actual target record: '+label)
            try: gate(bad, guest, square_gate)
            except (ValueError, AssertionError, KeyError) as error:
                faults.append(dict(case=suffix, fault=label, rejectedBy=str(error)))
            else: raise ValueError('Compound actual-record fault accepted: '+label)
        need(gate(text, guest, square_gate) == result, 'Full original positive restored after faults')
        cases.append(dict(samplesEnabled=suffix=='samples', folder=str(folder), qualification=result))
        print(json.dumps(dict(case=suffix, passed=True, compoundSquareFields=result['square']['fields'], faultsRejected=len(tests))), flush=True)
    for p in (PARENT, Path(__file__).resolve(), Path(square.__file__).resolve()): pins[str(p)]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()), 'Exact source and existing capture pins before terminal report')
    report=dict(passed=True, observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(), candidate=current.NAME,
                guestSHA256=current.GUEST_SHA, goalStatus='active', parentAdditiveJournal=str(PARENT), remaining=parent['remaining'],
                cases=cases, actualFaultsRejected=faults, inputHashes=pins, squareContextAdaptations=adaptations,
                fullPortAcceptance=False, fullGoalComplete=False, newNativeBoots=0, newBuilds=0, newZIPs=0, newRawMedia=0,
                previousGoalTurnClassification='no progress: acknowledgement only; revalidated live state and took next safe test',
                thisGoalTurnClassification='progress: existing mixed CPU choreography, cleanup and real subsequent attack qualified',
                scope=__doc__, nextActions=['Current Kano CPU knife/ball/blade branch fidelity', 'Remaining branch-specific art/audio and combined release acceptance'])
    OUT.mkdir(); p=OUT/'report.json'; p.write_text(json.dumps(report, indent=2)+'\n'); digest=sha(p)
    need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0
         and sha(p)==digest, 'Lossless exact-file terminal report compression')
    print(json.dumps(dict(passed=True, compoundSequences=len(cases), faultsRejected=len(faults), newNativeBoots=0, fullPortAcceptance=False)), flush=True)


if __name__ == '__main__':
    try: main()
    except Exception as error:
        OUT.mkdir(exist_ok=True); (OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n')
        raise
