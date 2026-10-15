"""Stage chronology gate; native wins belong to the previous visited stage.

This helper never supplies a schedule: the caller must independently establish
the expected native sequence. Synthetic tests are not current campaign proof.
"""
import json
import re
from pathlib import Path


def check(rows, side, identity, expected_sequence):
    stages = rows['STAGE']
    actual = [int(row['stage']) for row in stages]
    assert actual and actual == list(expected_sequence[:len(actual)])
    assert len(actual) == len(set(actual))
    wins = [row for row in rows.get('WIN', []) if int(row['slot']) == side]
    for win in wins:
        health = [int(value) for value in win['health'].split(',')]
        assert int(win['id']) == identity and win['pc'] == 'FF8296B0'
        assert health[side - 1] > 0 and health[2 - side] == 0
    for previous, current in zip(stages, stages[1:]):
        earned = {int(win['frame']) for win in wins
                  if win['stage'] == previous['stage']
                  and int(previous['frame']) <= int(win['frame']) < int(current['frame'])}
        assert len(earned) >= 2
    return actual


def load(path):
    rows = {}
    for line in path.read_text().splitlines():
        assert '[LUA ERROR]' not in line
        if line.startswith('MK2_NAT_CAMPAIGN_'):
            rows.setdefault(line.split()[0][17:], []).append(
                dict(re.findall(r'(\w+)=([^\s]+)', line)))
    return rows


def self_test():
    rows = dict(STAGE=[dict(stage='12', frame='100'), dict(stage='14', frame='300')],
                WIN=[dict(stage='12', frame=str(frame), slot='1', id='17',
                          pc='FF8296B0', health='50,0') for frame in (150, 200)])
    assert check(rows, 1, 17, [12, 14]) == [12, 14]
    rejected = []
    for name, broken in (
        ('missing_round_win', dict(rows, WIN=rows['WIN'][:1])),
        ('wrong_preceding_stage', dict(rows, WIN=[dict(r, stage='13') for r in rows['WIN']])),
        ('wrong_health', dict(rows, WIN=[dict(r, health='50,1') for r in rows['WIN']])),
    ):
        try:
            check(broken, 1, 17, [12, 14])
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('Fault accepted: ' + name)
    return rejected


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    out = root / 'audit_campaign_stage_chronology_checked'
    assert not out.exists()
    rejected = self_test()
    results = {}
    for fighter, side, folder in (
        ('kano', 1, 'audit_bounded_compact_kano_campaign_p1_runtime'),
        ('sonya', 1, 'audit_bounded_campaign_progress_core_sonya_p1_runtime'),
        ('kano', 2, 'audit_bounded_campaign_progress_core_kano_p2_runtime'),
        ('sonya', 2, 'audit_bounded_campaign_progress_core_sonya_p2_runtime'),
    ):
        rows = load(root / folder / 'run.log')
        # Only already-observed early contiguous stages are qualified here.
        results[f'{fighter}P{side}'] = check(rows, side, 17 if fighter == 'kano' else 18, list(range(13)))
    report = dict(passed=True, observedEarlyStages=results, syntheticFaultsRejected=rejected,
                  currentLateStageSkipVerified=False, fullCampaignClear=False,
                  fullPortAcceptance=False, newGames=0, newBuilds=0,
                  scope='Previous-visited-stage victory accounting; current early logs and explicit synthetic 12-to-14 tests only. Caller must independently prove full native schedule.')
    out.mkdir()
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))
