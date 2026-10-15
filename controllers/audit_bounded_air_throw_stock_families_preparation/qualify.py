import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
"""Retain prior ownership/damage/recovery gate, adjust declared real victim roles."""
import copy
import inspect
import json
import re
import qualify_bounded_air_throw_retirement as prior
import verify_native_source_sync as sync


if __name__ == '__main__':
    out = sync.ROOT / 'audit_bounded_air_throw_stock_families_checked'
    assert not out.exists()
    original = inspect.getsource(prior.gate)
    source = original.replace('def gate(rows, fighter, side):', 'def gate(rows, fighter, side, victim_id):')
    assert source.count('3-side: 11') == 1
    source = source.replace('3-side: 11', '3-side: victim_id')
    before = "attacker = side if fighter == 'kano' and cycle == 1 else 3-side"
    assert source.count(before) == 1
    source = source.replace(before, "attacker = side if victim_id != 11 or fighter == 'kano' and cycle == 1 else 3-side")
    scope = {}
    exec(compile(source, __file__ + '::same_gate_declared_roles', 'exec'), scope)
    gate = scope['gate']
    results = {}
    for victim, identity in (('sub_zero', 8), ('raiden', 7), ('shang_tsung', 6)):
        for side in (1, 2):
            folder = sync.ROOT / f'audit_bounded_air_throw_stock_family_{victim}_p{side}_runtime'
            terminal = json.loads((folder/'terminal.json').read_text())
            assert terminal['exitCode'] == 0 and terminal['limitReason'] is None
            assert terminal['peakWorkingSetBytes'] <= 320*1024**2 and terminal['elapsedSeconds'] <= 90
            assert not (folder/'stderr.log').read_text().strip()
            assert not any(p.suffix.lower() in ('.png', '.bin', '.wav') for p in folder.rglob('*'))
            rows = {}
            for line in (folder/'run.log').read_text().splitlines():
                assert '[LUA ERROR]' not in line and 'hex=' not in line
                if line.startswith('MK2_BASIC_'):
                    rows.setdefault(line.split()[0][10:], []).append(dict(re.findall(r'(\w+)=([^\s]+)', line)))
            damage = gate(rows, 'kano', side, identity)
            faults = []
            for fault in ('catch_owner', 'damage', 'victim_identity'):
                broken = copy.deepcopy(rows)
                if fault == 'catch_owner':
                    next(r for r in broken['AIR_EVENT'] if r['kind'] == 'action')['owner'] = '00000000'
                elif fault == 'damage':
                    broken['HEALTH'][0]['after'] = broken['HEALTH'][0]['before']
                else:
                    next(r for r in broken['FIELD'] if int(r['slot']) == 3-side)['id'] = '1'
                try:
                    gate(broken, 'kano', side, identity)
                except AssertionError:
                    faults.append(fault)
                else:
                    raise AssertionError('Fault accepted: ' + fault)
            results[f'{victim}P{side}'] = dict(damage=damage, rejectedFaults=faults,
                terminal=terminal, logSHA256=sync.sha(folder/'run.log'))
    report = dict(passed=True, results=results, priorGateSHA256=sync.sha(prior.__file__),
                  sourceSync=sync.verify(), fullPortAcceptance=False,
                  scope='Twelve current actual Kano catches: SubZero/Raiden/Shang victims in bothslots, same native ownership/damage/recovery/followup gate. No full choreography/audio/all-victim acceptance.')
    out.mkdir()
    (out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(passed=True, contexts=6, catches=12, fullPortAcceptance=False)))
