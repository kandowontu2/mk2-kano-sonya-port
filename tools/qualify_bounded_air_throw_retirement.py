"""Finite real catches/ownership/damage/recovery/followup, not full art/audio."""
import copy
import json
import re
import verify_native_source_sync as sync


def gate(rows, fighter, side):
    assert not rows.get('FAILED')
    result = rows['RESULT']
    assert len(result) == 1 and result[0]['phases'] == '2' and result[0]['completed'] == '1'
    fields = rows['FIELD']
    assert fields
    expected = {side: 17 if fighter == 'kano' else 18, 3-side: 11}
    for row in fields:
        assert int(row['id']) == int(row['roster']) == expected[int(row['slot'])]
        assert row['actor'] == row['owner'] and int(row['hp']) > 0
    events = rows['AIR_EVENT']
    recovered = rows['RECOVERED']
    done = rows['CYCLE_DONE']
    assert len(recovered) == len(done) == 2
    amounts = []
    for cycle in (1, 2):
        ev = [r for r in events if int(r['cycle']) == cycle]
        catches = [r for r in ev if r['kind'] == 'action']
        assert len(catches) == 1
        catch = catches[0]
        attacker = side if fighter == 'kano' and cycle == 1 else 3-side
        victim = 3-attacker
        assert int(catch['slot']) == attacker and int(catch['id']) == expected[attacker]
        assert catch['address'] == 'FF8B6FF0' and catch['a8'] == catch['actor'] == catch['owner']
        assert catch['a13'] == catch['main']
        recovery = next(r for r in recovered if int(r['cycle']) == cycle)
        finish = next(r for r in done if int(r['cycle']) == cycle)
        lo, hi = int(catch['frame']), int(recovery['frame'])
        assert int(finish['frame']) > hi > lo
        for slot in (1, 2):
            native = [r for r in ev if r['kind'] == 'recovery' and int(r['slot']) == slot
                      and lo < int(r['frame']) <= hi and int(r['a6'], 16) < 0xfe800000]
            assert native
            last = max(int(r['frame']) for r in native)
            assert not any(r['kind'] == 'victim_callback' and int(r['slot']) == slot
                           and last < int(r['frame']) <= int(finish['frame']) for r in ev)
            final = next(r for r in fields if int(r['frame']) == int(finish['frame']) and int(r['slot']) == slot)
            assert final['action'] == '771' and final['y'] == final['floor']
            assert all(int(final[key], 16) == 0 for key in ('vx', 'vy', 'gravity', 'trail'))
            assert int(final['flags'], 16) & 0x1c == int(final['body'], 16) & 0x0c == 0
        hits = [r for r in rows['HEALTH'] if lo <= int(r['frame']) <= hi
                and int(r['slot']) == victim and int(r['before']) > int(r['after'])]
        amount = sum(int(r['before']) - int(r['after']) for r in hits)
        assert amount == (16 if expected[attacker] == 17 else 32)
        assert all(r['pc'] == 'FF836700' for r in hits)
        amounts.append(amount)
    assert all(r['clean'] == '1' for r in rows['FINAL'])
    return amounts


if __name__ == '__main__':
    out = sync.ROOT / 'audit_bounded_air_throw_retirement_checked'
    assert not out.exists()
    results = {}
    for fighter in ('kano', 'sonya'):
        for side in (1, 2):
            folder = sync.ROOT / f'audit_bounded_air_throw_retirement_{fighter}_p{side}_runtime'
            terminal = json.loads((folder / 'terminal.json').read_text())
            assert terminal['exitCode'] == 0 and terminal['limitReason'] is None
            assert terminal['peakWorkingSetBytes'] <= 320*1024**2 and terminal['elapsedSeconds'] <= 90
            assert not (folder / 'stderr.log').read_text().strip()
            assert not any(p.suffix.lower() in ('.png', '.bin', '.wav') for p in folder.rglob('*'))
            rows = {}
            for line in (folder / 'run.log').read_text().splitlines():
                assert '[LUA ERROR]' not in line and 'hex=' not in line
                if line.startswith('MK2_BASIC_'):
                    rows.setdefault(line.split()[0][10:], []).append(dict(re.findall(r'(\w+)=([^\s]+)', line)))
            damage = gate(rows, fighter, side)
            broken = copy.deepcopy(rows)
            broken['AIR_EVENT'][0]['owner'] = '00000000'
            # Select the actual catch, not an unrelated eligibility event.
            next(r for r in broken['AIR_EVENT'] if r['kind'] == 'action')['owner'] = '00000000'
            try:
                gate(broken, fighter, side)
            except AssertionError:
                pass
            else:
                raise AssertionError('Wrong catch ownership accepted')
            results[f'{fighter}P{side}'] = dict(damage=damage, terminal=terminal,
                logSHA256=sync.sha(folder/'run.log'), wrongCatchOwnerRejected=True)
    report = dict(passed=True, results=results, sourceSync=sync.verify(),
                  fullPortAcceptance=False, fullVisualAudioAcceptance=False,
                  scope='Eight actual native airborne catches against Jax, correct real identities/owned native action/damage/recovery events/no later observed own callback/both ordinary followups. No saved-scratch-zero assumption; not all victims, geometry, art or audio.')
    out.mkdir()
    (out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(passed=True, contexts=4, catches=8, fullPortAcceptance=False)))
