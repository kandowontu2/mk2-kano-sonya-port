"""Audit physical knife requests separately from actual native activation and wins."""
import csv
from collections import Counter
import json
import subprocess
import sys
from inspect_normal_runtime import BASE, sha
from refresh_special_videos import PORT, FLAGS
from campaign_rounds import split_rounds


def ready_request(row):
    return (row['phase'] == 'fire' and int(row['ownHP']) > 0 and
            int(row['ownAction']) == 0x303 and int(row['ownHeight']) == 0 and
            int(row['ownFlags']) & 0x1c == 0 and int(row['bodyHeight']) >= 120 and
            int(row['distance']) >= 175 and row['buttonTable'] == row['stanceTable'])


def main(name):
    assert name and all(c.isalnum() or c in '_-' for c in name)
    run = BASE / name
    receipt = json.loads((run / 'execution.json').read_text())
    hybrid = '--campaign-kano-kintaro-retreat-ball-finish-knife' in receipt['testArguments']
    assert hybrid or '--campaign-kano-kintaro-knife-ready' in receipt['testArguments']
    subprocess.run([sys.executable, str(PORT / 'audit_campaign_run.py'), name],
                   check=True, stdout=subprocess.DEVNULL, creationflags=FLAGS)
    log = (run / 'mame.log').read_text()
    assert 'Fatal error:' not in log and '[LUA ERROR]' not in log
    with (run / 'kintaro_knife_ready.csv').open() as stream:
        fired = [r for r in csv.DictReader(stream) if r['phase'] == 'fire']
    assert all(ready_request(r) for r in fired)
    if hybrid:
        assert '--campaign-kano-kintaro-retreat-ball' in receipt['testArguments']
        assert all(int(r['enemyHP'])<=50 for r in fired)
    else:
        assert fired
    with (run / 'campaign.csv').open() as stream:
        rows = list(csv.DictReader(stream))
    index = {int(r['frame']): r for r in rows}
    entries = set()
    missed = []
    missed_traces = []
    for request in fired:
        frame = int(request['frame'])
        entry = next((f for f in range(frame, frame + 25) if f in index and
                      index[f]['mode'] == '2' and index[f]['p1char'] == '17' and
                      index[f]['p2char'] == '12' and int(index[f]['p1action']) == 0x211), None)
        if entry is None:
            missed.append(frame)
            missed_traces.append(dict(requestFrame=frame, sampledStates=[
                dict(frame=f, action=int(index[f]['p1action']), hp=int(index[f]['p1hp']),
                     enemyAction=int(index[f]['p2action']))
                for f in range(frame, frame + 25) if f in index]))
        else:
            entries.add(entry)
    # Do not call temporally nearby damage a linked knife hit: this observer
    # lacks projectile identity/hitby. Preserve all boss damage as observations.
    drops = []
    for before, after in zip(rows, rows[1:]):
        if not (before['mode'] == after['mode'] == '2' and
                before['p2char'] == after['p2char'] == '12' and
                (before['attempt'], before['round']) == (after['attempt'], after['round'])):
            continue
        delta = int(before['p2hp']) - int(after['p2hp'])
        if delta > 0:
            drops.append(dict(frame=int(after['frame']), damage=delta))
    audit = json.loads((run / 'CAMPAIGN_AUDIT.json').read_text())
    wins = [r for r in audit['nativeWinningRounds'] if r['opponent'] == 12]
    fights = [r for r in rows if r['mode'] == '2' and r['p1char'] == '17' and
              r['p2char'] == '12' and int(r['p1hp']) > 0 and int(r['p2hp']) > 0]
    rounds = split_rounds(fights)
    report = dict(scope='Finite controller audit; damage is not attributed without projectile identity',
                  requests=len(fired), allRequestReadinessChecksPassed=True, lowHPHybrid=hybrid,
                  nativeKnifeEntriesWithin24Fields=len(entries), requestsWithoutObservedEntry=missed,
                  observedBossDamageWindows=drops, nativeKintaroRoundWins=wins,
                  sampledKintaroRounds=rounds,
                  bestObservedBossHP=min(r['minimumCPUHP'] for r in rounds),
                  bossDamageHistogram=dict(Counter(r['damage'] for r in drops)),
                  missedRequestTraces=missed_traces,
                  fullPortVerified=False, pins={str(p): sha(p) for p in
                  (run / 'execution.json', run / 'autoboot.lua', run / 'campaign.csv',
                   run / 'kintaro_knife_ready.csv')})
    (run / 'KINTARO_KNIFE_READY_QUALIFICATION.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Ready knife requests', len(fired), 'native entries', len(entries),
          'unattributed damage windows', len(drops), 'native round wins', len(wins))


if __name__ == '__main__':
    assert len(sys.argv) == 2
    main(sys.argv[1])
