"""Finite friendship mechanics only; not visual/audio/release acceptance."""
import json
import re
import verify_native_source_sync as sync


def fields(line):
    return dict(re.findall(r'(\w+)=([^\s]+)', line))


def validate(text, fighter, side):
    own = 17 if fighter == 'kano' else 18
    expected = 'FFFCD000' if own == 17 else 'FFFCE000'
    rows = [(line.split()[0], fields(line)) for line in text.splitlines() if line.startswith('MK2_FRIEND_')]
    assert rows
    for _, row in rows:
        assert row['writes'] == '0' and row['assistance'] == 'none'
        assert row['winner'] == fighter and int(row['side']) == side
    windows = [r for tag, r in rows if tag == 'MK2_FRIEND_WINDOW']
    assert len(windows) == 1
    assert windows[0]['kos'] == '2' and windows[0]['damage'] == '322'
    assert windows[0]['hp_counters'] == '0,0' and windows[0]['lp_counters'] == '0,0'
    selections = [r for tag, r in rows if tag == 'MK2_FRIEND_SELECT_ID']
    assert len(selections) == 2
    assert all(r['actual'] == r['target'] for r in selections)
    assert next(r for r in selections if int(r['slot']) == side)['actual'] == str(own)
    entries = [r for tag, r in rows if tag == 'MK2_FRIEND_ENTRY' and r['entry'] == expected]
    assert entries and all(r['id'] == str(own) for r in entries)
    poses = [r for tag, r in rows if tag == 'MK2_FRIEND_POSE']
    assert len(poses) > 2
    assert all(r['id'] == str(own) and r['roster'] == str(own) and r['actor'] == r['owner'] for r in poses)
    results = [r for tag, r in rows if tag == 'MK2_FRIEND_RESULT']
    assert len(results) == 1
    result = results[0]
    assert result['kos'] == '2' and result['damage'] == '322'
    assert int(result['action']) > int(result['window']) > 0
    assert result['cleanup'] == 'true' and result['retired'] == 'true'
    assert not any(tag == 'MK2_FRIEND_HOST_BOUND' for tag, _ in rows)
    return result


def main():
    sync.verify()
    out = sync.ROOT / 'audit_bounded_current_friendships_checked'
    assert not out.exists()
    reports = []
    lua = sync.ROOT / 'audit_bounded_current_friendships_preparation/friendships.lua'
    for fighter in ('kano', 'sonya'):
        for side in (1, 2):
            case = sync.ROOT / f'audit_bounded_current_friendship_{fighter}_p{side}_runtime'
            terminal = json.loads((case / 'terminal.json').read_text(encoding='utf-8-sig'))
            assert terminal['exitCode'] == 0 and terminal['limitReason'] is None
            assert terminal['peakWorkingSetBytes'] <= 320 * 1024**2
            assert terminal['observerSha256'].lower() == sync.sha(lua).lower()
            assert not (case / 'stderr.log').read_text().strip()
            assert not list((case / 'snap').rglob('*.png'))
            text = (case / 'run.log').read_text()
            assert 'LUA ERROR' not in text and 'FAILED' not in text
            result = validate(text, fighter, side)
            for before, after in (('damage=322', 'damage=321'), ('cleanup=true', 'cleanup=false'), ('retired=true', 'retired=false')):
                corrupted = text.replace(before, after)
                try:
                    validate(corrupted, fighter, side)
                except AssertionError:
                    pass
                else:
                    raise AssertionError('Corruption gate did not reject ' + before)
            reports.append({'fighter': fighter, 'side': side, 'result': result, 'logSha256': sync.sha(case / 'run.log'), 'terminal': terminal})
    out.mkdir()
    (out / 'report.json').write_text(json.dumps({'finiteMechanicsPassed': True, 'visualAudioAcceptance': False, 'releaseAcceptance': False, 'cases': reports}, indent=2))
    print('PASS: four earned true-ID friendships, cleanup and actor retirement; visual/audio still open')


if __name__ == '__main__':
    main()
