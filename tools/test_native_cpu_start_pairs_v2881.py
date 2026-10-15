"""Actual corruption tests for fresh accepted native Kano CPU paired contacts.

Unchanged original typed pair/ordinary continuation contracts. Every mutation
must differ from all real captures and must be rejected. Original rejected
fixtures and stock-opponent scenario misses are never promoted by these units.
"""
import json
import sys
import traceback
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_native_cpu_start_inventory_v2879 as model
from test_current_cpu_overlap_v1912 import mutate

ROOT = model.ROOT
OUT = ROOT / 'audit_v2882_native_cpu_start_pairs_units'


def verify():
    proof_path = model.OUT / 'report.json'
    proof = json.loads(proof_path.read_text())
    model.assembly.need(proof['passed'] and proof['diagnosticInventoryOnly'] and proof['candidate'] == model.assembly.NAME and
                        len(proof['cases']) == 16 and proof['originalTypedContractsUnchanged'] and
                        not proof['allFixturesGameplayAccepted'], 'Actual bounded inventory, no universal gameplay acceptance')
    pins = dict(proof['inputHashes'])
    pins[str(proof_path)] = model.assembly.sha(proof_path)
    guest, _, _, _, _ = model.assembly.expected()
    cases = [r for r in proof['cases'] if r['status'] == 'accepted_original_pair_and_ordinary_followup']
    actual_logs = {(ROOT / r['case'] / 'run.log').read_text(encoding='utf-8-sig') for r in proof['cases']}
    rejected = []
    for case in cases:
        player, cpu_id = case['player'], case['actualCPU']
        log = (ROOT / case['case'] / 'run.log').read_text(encoding='utf-8-sig')
        base = model.typed_pair(log, player, guest, cpu_id)['originalContract']
        start, release, own, victim = (base[k] for k in ('start', 'release', 'own_handoff', 'victim_handoff'))
        ready, cycle = base['native_followup']['first_ready'], base['cycle']
        P = 'MK2_CPU_PAIR_'
        clear = [r for r in model.MODEL.flag_rows(log) if r['frame'] == own and r['slot'] == 2 and
                 r['kind'] == 'body' and r['before'] != r['after']]
        model.assembly.need(len(clear) == 1, 'Unique actual owned ready clear')
        damage = [r for r in model.MODEL.rows(log, 'EVENT') if r['kind'] == 'damage' and r['cycle'] == cycle and start <= r['frame'] <= release]
        stores = [r for r in model.MODEL.rows(log, 'HEALTH') if r['slot'] == 1 and r['cycle'] == cycle and
                  start <= r['frame'] <= release and r['before'] > r['after']]
        step = next(r for r in model.MODEL.rows(log, 'EVENT') if r['kind'] == 'step' and r['cycle'] == cycle)
        model.assembly.need(damage and stores, 'Actual native paired damage calls and physically owned health stores')
        tests = [
            ('wrong physical CPU slot', P+'FIELD', {'frame': str(start+20)}, 'cpu_slot', '1'),
            ('CPU proxy identity', P+'FIELD', {'frame': str(start+20)}, 'id', '1'),
            ('wrong victim Main owner', P+'FIELD', {'frame': str(start+20)}, 'vowner', '010350A0'),
            ('wrong original held victim pose', P+'FIELD', {'frame': str(start+20)}, 'vpose', 'FE82AAA0'),
            ('wrong physical human floor', P+'FIELD', {'frame': str(start+20)}, 'vfloor', '83'),
            ('wrong CPU floor', P+'FIELD', {'frame': str(start+20)}, 'floor', '83'),
            ('wrong original fling vertical velocity', P+'FIELD', {'frame': str(release+1)}, 'vvy', '00000000'),
            ('wrong physical health slot', P+'HEALTH', {'frame': str(stores[0]['frame']), 'slot': '1', 'before': str(stores[0]['before'])}, 'slot', '2'),
            ('wrong choke damage request', P+'EVENT', {'frame': str(damage[0]['frame']), 'kind': 'damage'}, 'a10', '00000009'),
            ('stale own lock at ready', P+'OWN_REGAIN', {'frame': str(own)}, 'flags', '00000010'),
            ('stale victim child at ready', P+'VICTIM_REGAIN', {'frame': str(victim)}, 'vtrail', '010350A0'),
            ('wrong native ready opcode', P+'FLAG', {'frame': str(own), 'slot': '2', 'kind': 'body', 'before': f"{clear[0]['before']:04X}"}, 'op0', '0000'),
            ('stale follow-up lock', P+'FOLLOW_REGAIN', {'frame': str(ready)}, 'flags', '00000010'),
            ('missing actual follow-up ready', P+'FOLLOW_READY_INSTRUCTION', {'frame': str(ready), 'kind': 'regained'}, None, None),
            ('wrong terminal continuation', P+'RESULT', {}, 'frame', str(ready+31)),
            ('missing paired callback', P+'FIELD', {'frame': str(start+20)}, None, None),
            ('missing independent continuation callback', P+'FOLLOW_FIELD', {'frame': str(base['complete']+5)}, None, None),
            ('wrong own choke phase composite', P+'EVENT', {'frame': str(step['frame']), 'kind': 'step'}, 'group', 'FE82AAA0'),
            ('unlogged victim health', P+'FIELD', {'frame': str(start+20)}, 'vhp', '160'),
            ('guest-state assistance', P+'FIELD', {'frame': str(start+20)}, 'writes', '1'),
        ]
        for label, tag, criteria, key, value in tests:
            damaged = mutate(log, tag, criteria, key, value)
            model.assembly.need(damaged not in actual_logs, 'Non-vacuous actual corruption ' + label)
            try:
                model.typed_pair(damaged, player, guest, cpu_id)
            except (AssertionError, KeyError, IndexError, ValueError) as error:
                rejected.append(dict(case=case['case'], name=label, error=repr(error)))
            else:
                raise AssertionError('Accepted actual corruption: ' + case['case'] + ' ' + label)
        print(case['case'] + ': all twenty actual corruptions rejected', flush=True)
    model.assembly.need(len(rejected) == len(cases)*20 and len(cases) == proof['acceptedPairFixtures'],
                        'Every actual accepted CPU pair independently tested')
    for module in tuple(sys.modules.values()):
        file = getattr(module, '__file__', None)
        if file:
            path = Path(file).absolute()
            if path.is_relative_to(ROOT / 'tools') and path.suffix == '.py':
                pins[str(path)] = model.assembly.sha(path)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for (file, wanted), actual in zip(pins.items(), pool.map(model.assembly.sha, pins)):
            model.assembly.need(actual == wanted, 'Actual capture and source unchanged ' + file)
    return dict(passed=True, candidate=model.assembly.NAME, acceptedFixturesTested=len(cases),
                actualOriginalCounterexamplesRejected=len(rejected), counterexamples=rejected,
                originalTypedContractsUnchanged=True, mutationNonVacuityRequired=True,
                actualCapturesUnmodified=True, gameBytesChanged=False, fullPortAcceptance=False,
                allCPUAccepted=False, scope=__doc__, inputHashes=pins)


if __name__ == '__main__':
    model.assembly.need(not OUT.exists(), 'Immutable actual CPU counterexamples')
    try:
        report = verify()
    except Exception as error:
        report = dict(passed=False, error=repr(error), traceback=traceback.format_exc(), fullPortAcceptance=False)
    OUT.mkdir()
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('inputHashes', 'counterexamples')}, indent=2), flush=True)
    raise SystemExit(0 if report['passed'] else 1)
