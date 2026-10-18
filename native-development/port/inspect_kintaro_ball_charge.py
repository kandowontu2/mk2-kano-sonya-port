"""Physical charge continuity and sampled activation; not a win heuristic."""
import csv
import json
import subprocess
import sys
from inspect_normal_runtime import BASE, sha
from refresh_special_videos import PORT, FLAGS


def release_windows(rows):
    held = 0
    previous = None
    releases = []
    for row in rows:
        frame = int(row['frame'])
        if previous is None or frame != previous + 1:
            held = 0
        if row['phase'] == 'release':
            assert int(row['age']) >= 88 and row['lk'] == '0'
            assert row['height'] == '0' and int(row['action']) == 0x303
            assert int(row['flags']) & 0x1c == 0 and int(row['ownHP']) > 0
            releases.append(dict(frame=frame, consecutiveHeldFields=held,
                                 heldLongerThanNative80FieldGate=held > 80))
        held = held + 1 if row['lk'] == '1' else 0
        previous = frame
    return releases


def main(name):
    assert name and all(c.isalnum() or c in '_-' for c in name)
    run = BASE / name
    receipt = json.loads((run / 'execution.json').read_text())
    assert '--campaign-kano-kintaro-retreat-ball' in receipt['testArguments']
    subprocess.run([sys.executable, str(PORT / 'audit_campaign_run.py'), name],
                   check=True, stdout=subprocess.DEVNULL, creationflags=FLAGS)
    with (run / 'boss_ball_charge.csv').open() as stream:
        releases = release_windows(list(csv.DictReader(stream)))
    with (run / 'campaign.csv').open() as stream:
        campaign = list(csv.DictReader(stream))
    index = {int(r['frame']): r for r in campaign}
    for request in releases:
        frame = request['frame']
        request['nativeBallEntryWithin8Fields'] = next((f for f in range(frame, frame + 9)
            if f in index and index[f]['mode'] == '2' and index[f]['p1char'] == '17' and
            index[f]['p2char'] == '12' and int(index[f]['p1action']) == 0x20b), None)
    audit = json.loads((run / 'CAMPAIGN_AUDIT.json').read_text())
    rounds = [r for r in audit['rounds'] if r['opponent'] == 12]
    wins = [r for r in audit['nativeWinningRounds'] if r['opponent'] == 12]
    report = dict(scope='Logged physical charge continuity and sampled native Ball activation',
        releases=releases, requests=len(releases),
        continuousFullCharges=sum(r['heldLongerThanNative80FieldGate'] for r in releases),
        nativeBallEntries=sum(r['nativeBallEntryWithin8Fields'] is not None for r in releases),
        observedBossRounds=len(rounds), bestObservedBossHP=min(r['minimumCPUHP'] for r in rounds),
        nativeKintaroRoundWins=wins, fullPortVerified=False,
        pins={str(p): sha(p) for p in (run / 'execution.json', run / 'autoboot.lua',
            run / 'campaign.csv', run / 'boss_ball_charge.csv', run / 'CAMPAIGN_AUDIT.json')})
    (run / 'KINTARO_BALL_CHARGE_QUALIFICATION.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Releases', len(releases), 'continuous charges', report['continuousFullCharges'],
          'native Balls', report['nativeBallEntries'], 'native round wins', len(wins))


if __name__ == '__main__':
    assert len(sys.argv) == 2
    main(sys.argv[1])
