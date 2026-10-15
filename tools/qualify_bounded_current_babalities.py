"""Validate finite earned babality mechanics, not pixels or audio."""
import json
from qualify_bounded_current_friendships import fields
import verify_native_source_sync as sync


def validate(text, fighter, side):
    own = 17 if fighter == 'kano' else 18
    victim = 18 if own == 17 else 17
    rows = [(line.split()[0], fields(line)) for line in text.splitlines() if line.startswith('MK2_NATIVE_BABY_')]
    assert rows
    for _, row in rows:
        assert row['writes'] == '0' and row['assistance'] == 'none'
        assert int(row['winner_slot']) == side
    def select(tag):
        return [r for t, r in rows if t == 'MK2_NATIVE_BABY_' + tag]
    window = select('FINISH_WINDOW')
    assert len(window) == 1
    assert window[0]['native_kos'] == '2' and window[0]['damage'] == '322'
    assert window[0]['hp_counters'] == '0,0' and window[0]['lp_counters'] == '0,0'
    result = select('RESULT')
    assert len(result) == 1
    assert result[0]['wins'] == '2' and result[0]['damage'] == '322'
    assert result[0]['winner'] == fighter and result[0]['case'] == 'positive'
    assert int(result[0]['action']) > int(result[0]['window']) > 0
    constructed = select('CONSTRUCT')
    assert len(constructed) == 1 and int(constructed[0]['victim_id']) == victim
    baby = constructed[0]['actor']
    assert 0x01000000 <= int(baby, 16) < 0x01100000
    sampled = select('FIELD')
    handoffs = [r for r in sampled if int(r['slot']) == 3-side and r['owner'] == baby]
    assert handoffs and all(int(r['id']) == victim and int(r['roster']) == victim for r in handoffs)
    performers = [r for r in sampled if int(r['slot']) == side]
    assert performers and all(int(r['id']) == own and int(r['roster']) == own and r['actor'] == r['owner'] for r in performers)
    babies = select('BABY')
    assert babies and all(r['actor'] == baby and r['graphic'] == constructed[0]['frame_pointer'] for r in babies)
    assert any(r['actor'] == baby for r in select('BABY_REUSED'))
    retired = select('RETIRE')
    assert all(any(int(r['slot']) == n and r['value'] == '0000' for r in retired) for n in (1,2))
    assert not select('HOST_BOUND')
    return result[0]


def main():
    sync.verify()
    out = sync.ROOT / 'audit_bounded_current_babalities_checked'
    assert not out.exists()
    lua = sync.ROOT / 'audit_bounded_current_babalities_preparation/babalities.lua'
    reports = []
    for fighter in ('kano', 'sonya'):
        for side in (1,2):
            case = sync.ROOT / f'audit_bounded_current_babality_{fighter}_p{side}_runtime'
            terminal = json.loads((case / 'terminal.json').read_text(encoding='utf-8-sig'))
            assert terminal['exitCode'] == 0 and terminal['limitReason'] is None
            assert terminal['peakWorkingSetBytes'] <= 320*1024**2
            assert terminal['observerSha256'].lower() == sync.sha(lua).lower()
            assert not (case / 'stderr.log').read_text().strip()
            assert not list((case / 'snap').rglob('*.png'))
            text = (case / 'run.log').read_text()
            assert 'LUA ERROR' not in text and 'FAILED' not in text
            result = validate(text, fighter, side)
            for before, after in (('damage=322','damage=321'), ('native_kos=2','native_kos=1'), ('MK2_NATIVE_BABY_CONSTRUCT','REMOVED_CONSTRUCT'), ('MK2_NATIVE_BABY_BABY_REUSED','REMOVED_REUSE')):
                try:
                    validate(text.replace(before,after), fighter, side)
                except AssertionError:
                    pass
                else:
                    raise AssertionError('Corruption gate failed: '+before)
            reports.append({'fighter':fighter,'side':side,'result':result,'logSha256':sync.sha(case/'run.log'),'terminal':terminal})
    out.mkdir()
    (out/'report.json').write_text(json.dumps({'finiteMechanicsPassed':True,'visualAudioAcceptance':False,'releaseAcceptance':False,'cases':reports},indent=2))
    print('PASS: four earned true-ID babalities, baby handoff, actor retirement and reuse')


if __name__ == '__main__':
    main()
