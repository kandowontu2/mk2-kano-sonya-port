"""Classify existing mirror damage, without running an emulator or recording RAM."""
import collections
import json
import re
import verify_native_source_sync as sync


def classify(lines):
    live = None
    events = []
    for line in lines:
        if '_LIVE ' in line:
            live = dict(re.findall(r'(\w+)=([^ ]+)', line.strip()))
        if '_HEALTH ' not in line or live is None:
            continue
        row = dict(re.findall(r'(\w+)=([^ ]+)', line.strip()))
        if live['stage'] != '5' or row['pc'] != 'FF836700':
            continue
        assert live['human'] == '18:18' and live['cpu'] == '18:18'
        before, after = int(row['before']), int(row['after'])
        if not 0 <= after < before <= 161:
            continue
        age = int(row['frame']) - int(live['frame'])
        assert 0 <= age < 30
        events.append(dict(frame=int(row['frame']), slot=int(row['slot']),
                           damage=before-after, sampledActions=live['actions'],
                           sampleAge=age, a8=row['a8'], a13=row['a13'],
                           humanActor=live['human_actor'], cpuActor=live['cpu_actor']))
    return events


def main():
    sync.verify()
    source = sync.ROOT/'audit_current_sonya_mirror_stance_guard_runtime/run.log'
    events = classify(source.read_text().splitlines())
    assert events
    # Mutation check: do not silently classify a proxy as a genuine mirror.
    corrupt = source.read_text().replace('human=18:18', 'human=18:0')
    try:
        classify(corrupt.splitlines())
    except AssertionError:
        pass
    else:
        raise AssertionError('Proxy mutation was not rejected')
    counts = collections.Counter((e['slot'], e['damage']) for e in events)
    throw_context = [e for e in events if e['slot'] == 1
                     and e['sampledActions'].split(',')[1] == '1287']
    report = dict(logSHA256=sync.sha(source), nativeDamageEvents=len(events),
                  damageCounts=[dict(slot=s, damage=d, count=n)
                                for (s,d),n in sorted(counts.items())],
                  humanDamageWithRecentCPUThrowSample=throw_context,
                  limitation='Actions are preceding 30-field samples, not exact hit-time actions. Victim-owned A8 during native throws is legitimate; this is not a proxy diagnosis.',
                  nextAction='Test physical throw avoidance/spacing only in the mirror branch; preserve the earned pre-mirror route.',
                  guestWrites=0, newEmulatorRuns=0, fullPortAccepted=False)
    out = sync.ROOT/'audit_current_sonya_mirror_damage_classification'
    assert not out.exists()
    out.mkdir()
    (out/'report.json').write_text(json.dumps(report, indent=2))
    print(json.dumps({k:v for k,v in report.items()
                      if k != 'humanDamageWithRecentCPUThrowSample'}, indent=2))
    print('Recent CPU-throw damage contexts:', len(throw_context))


if __name__ == '__main__':
    main()
