"""Stream sampled damage by round/action; adjacency is not causal attribution."""
import csv
import json
import sys
from collections import Counter
from inspect_normal_runtime import BASE, sha


def summarize(rows):
    rounds = {}
    previous = None
    damage = Counter()
    for row in rows:
        eligible = row['mode'] == '2' and row['p1char'] == '17' and row['p2char'] == '12'
        if not eligible:
            previous = None
            continue
        key = (row['attempt'], row['round'])
        result = rounds.setdefault(key, dict(attempt=int(key[0]), round=int(key[1]),
            firstFrame=int(row['frame']), lastFrame=0, playerDamage=0, bossDamage=0,
            minimumPlayerHP=int(row['p1hp']), minimumBossHP=int(row['p2hp']),
            playerDamageEvents=0, bossDamageEvents=0))
        result['lastFrame'] = int(row['frame'])
        result['minimumPlayerHP'] = min(result['minimumPlayerHP'], int(row['p1hp']))
        result['minimumBossHP'] = min(result['minimumBossHP'], int(row['p2hp']))
        if previous is not None and (previous['attempt'], previous['round']) == key:
            for target, field in (('player', 'p1hp'), ('boss', 'p2hp')):
                delta = int(previous[field]) - int(row[field])
                if delta > 0:
                    result[target + 'Damage'] += delta
                    result[target + 'DamageEvents'] += 1
                    # Preserve both sampled actions; hit/recovery can replace attack tags.
                    label = (target, previous['p1action'], previous['p2action'],
                             row['p1action'], row['p2action'], delta)
                    damage[label] += 1
        previous = row
    events = [dict(target=k[0], priorPlayerAction=int(k[1]), priorBossAction=int(k[2]),
                   playerAction=int(k[3]), bossAction=int(k[4]), damage=k[5], count=v)
              for k, v in sorted(damage.items(), key=lambda item: (-item[1], item[0]))]
    return dict(rounds=list(rounds.values()), sampledDamageGroups=events)


def main(name):
    assert name and all(c.isalnum() or c in '_-' for c in name)
    run = BASE / name
    execution = json.loads((run / 'execution.json').read_text())
    assert execution['exitCode'] == 0 and not execution['timedOut']
    path = run / 'campaign.csv'
    with path.open(newline='') as stream:
        report = summarize(csv.DictReader(stream))
    report.update(scope='Sampled HP deltas and action adjacency, not attack causality or match-win proof',
                  fullPortVerified=False, pins={str(p): sha(p) for p in
                      (path, run / 'execution.json', run / 'autoboot.lua')})
    (run / 'KINTARO_DAMAGE_DISTRIBUTION.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(rounds=len(report['rounds']),
        closestRounds=sorted(report['rounds'], key=lambda r:r['minimumBossHP'])[:5],
        mostFrequentSampledDamageGroups=report['sampledDamageGroups'][:8]), indent=2))


if __name__ == '__main__':
    assert len(sys.argv) == 2
    main(sys.argv[1])
