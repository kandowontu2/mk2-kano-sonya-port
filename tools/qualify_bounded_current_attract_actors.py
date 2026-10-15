"""Qualify real actor identities in observed natural attract demo windows."""
import copy
import json
import re
from collections import defaultdict
import verify_native_source_sync as sync
from qualify_bounded_current_attract_bios import gate as bio_gate


def parse(text):
    return [(line.split()[0].removeprefix('MK2_LIGHT_ATTRACT_'),
             dict(re.findall(r'(\w+)=([^\s]+)', line)))
            for line in text.splitlines() if line.startswith('MK2_LIGHT_ATTRACT_')]


def gate(rows):
    bio_gate(rows)
    pairs = defaultdict(dict)
    active = defaultdict(list)
    missing = 0
    for tag, row in rows:
        assert row['writes'] == '0' and row['assistance'] == 'none'
        if tag not in ('DEMO_ACTOR', 'DEMO_MISSING'):
            continue
        frame, slot = int(row['frame']), int(row['slot'])
        assert slot in (1, 2) and slot not in pairs[frame]
        pairs[frame][slot] = (tag, row)
        if tag == 'DEMO_MISSING':
            # Publication/teardown records are retained, not active combat.
            assert row['actor'] == '00000000'
            missing += 1
            continue
        assert row['id'] == row['roster']
        assert row['owner'] == row['actor'] and row['state'] == '0'
        assert all(0x01000000 <= int(row[k], 16) < 0x01100000
                   for k in ('actor', 'main'))
        assert 0 <= int(row['hp']) <= 161
        active[(slot, int(row['roster']))].append(frame)
    expected = {(1, 10): (6320, 7092), (2, 18): (6320, 7092),
                (1, 17): (15420, 16192), (2, 2): (15420, 16192),
                (1, 18): (22534, 23306), (2, 4): (22534, 23306)}
    assert set(active) == set(expected)
    for key, (first, last) in expected.items():
        assert active[key] == list(range(first, last + 1))
    for pair in pairs.values():
        assert set(pair) == {1, 2}
        assert pair[1][0] == pair[2][0]
        assert any(int(row['roster']) in (17, 18) for _, row in pair.values())
    assert missing == 18428 and len(pairs) == 11533
    return [dict(slot=slot, character=ident, first=first, last=last,
                 continuousFrames=last-first+1)
            for (slot, ident), (first, last) in expected.items()]


def main():
    source = sync.verify()
    folder = sync.ROOT / 'audit_bounded_current_attract_actors_runtime'
    out = sync.ROOT / 'audit_bounded_current_attract_actors_checked'
    assert not out.exists()
    terminal = json.loads((folder / 'terminal.json').read_text())
    assert terminal['exitCode'] == 0 and terminal['limitReason'] is None
    assert terminal['peakWorkingSetBytes'] <= 320*1024*1024
    assert terminal['elapsedSeconds'] <= 90 and terminal['logBytes'] <= 10*1024*1024
    assert terminal['observerSha256'] == sync.sha(sync.ROOT / 'audit_bounded_current_attract_actors_preparation/attract.lua')
    assert not (folder / 'stderr.log').read_text().strip()
    assert not any(p.suffix.lower() in ('.png', '.bin', '.wav') for p in folder.rglob('*'))
    text = (folder / 'run.log').read_text()
    assert 'LUA ERROR' not in text
    prefix = 'MK2_LIGHT_ATTRACT_'
    original = (sync.ROOT / 'audit_bounded_current_attract_long_runtime/run.log').read_text()
    baseline = [l for l in original.splitlines() if l.startswith(prefix)]
    filtered = [l for l in text.splitlines() if l.startswith(prefix)
                and not l.startswith((prefix+'DEMO_ACTOR ', prefix+'DEMO_MISSING '))]
    assert filtered == baseline
    rows = parse(text)
    windows = gate(rows)
    bad = copy.deepcopy(rows)
    next(r for t, r in bad if t == 'DEMO_ACTOR' and r['roster'] == '17')['id'] = '0'
    try:
        gate(bad)
    except AssertionError:
        pass
    else:
        raise AssertionError('Proxy Kano identity accepted')
    bad = list(rows)
    bad.pop(next(i for i, (t, _) in enumerate(bad) if t == 'DEMO_ACTOR'))
    try:
        gate(bad)
    except AssertionError:
        pass
    else:
        raise AssertionError('Missing active paired field accepted')
    report = dict(passed=True, sourceSync=source, terminal=terminal,
                  windows=windows, baselineScalarTraceUnchanged=True,
                  proxyIdentityRejected=True, missingPairedFieldRejected=True,
                  logSHA256=sync.sha(folder / 'run.log'),
                  fullPortAcceptance=False,
                  scope='Three natural current-build CPU demos: continuous real roster/actor IDs and both actor/Main ownership pairs during every active frame. Null actor publication/teardown records retained separately. No full demo choreography, audio, raster, campaign or release acceptance.')
    out.mkdir()
    (out / 'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(passed=True, realKanoSonyaDemoActors=True,
                          activeDemoFrames=2319, fullPortAcceptance=False)))


if __name__ == '__main__':
    main()
