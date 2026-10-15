"""Finite native pain-routing evidence; not waveform or listening acceptance."""
import copy
import json
import re
from pathlib import Path
import verify_native_source_sync as sync

ROOT = sync.ROOT
RX = re.compile(r'(\w+)=([^\s]+)')

def gate(rows, fighter):
    ident, route, entry, pc, commands = {
        'sonya': (18, 'female', 'FFA123B0', 'FFA123C0', [0x2DC, 0x2D5]),
        'kano': (17, 'male', 'FFA122D0', 'FFA122E0', [0x278, 0x26B]),
    }[fighter]
    branches = [(i, r) for i, (tag, r) in enumerate(rows) if tag.endswith('PAIN_BRANCH')]
    assert len(branches) == 2
    packets = []
    for (i, r), frame, command in zip(branches, (1424, 1487), commands):
        assert int(r['frame']) == frame and r['route'] == route
        assert r['entry'] == entry and r['pc'] == pc
        assert int(r['a2'], 16) == ident == int(r['id1'])
        assert r['a8'] == r['actor1'] and r['a13'] == r['main1']
        assert int(r['hp1']) == 121 and int(r['id2']) == 4 and int(r['hp2']) == 161
        pair = rows[i+1:i+3]
        assert len(pair) == 2 and all(tag.endswith('PAIN_SOUND') for tag, _ in pair)
        high, low = [x for _, x in pair]
        for p in (high, low):
            assert int(p['frame']) == frame and p['mask'] == 'FFFF'
            assert p['a8'] == r['actor1'] and p['a13'] == r['main1']
        assert high['pc'] == 'FFA13C90' and low['pc'] == 'FFA13D60'
        assert int(high['a0'], 16) == command
        assert int(high['data'], 16) == 0xFF00 | (command >> 8)
        assert int(low['data'], 16) == 0xFF00 | (command & 255)
        packets.append(dict(frame=frame, route=route, trueID=ident, command=f'{command:04X}'))
    channels = [r for tag, r in rows if tag.endswith('PAIN_CHANNEL')]
    assert len(channels) == 148
    assert {(int(r['frame']), int(r['channel'])) for r in channels} == {
        (frame, channel) for frame in range(1408, 1481, 2) for channel in range(10, 14)}
    assert all(r['length'] == '0' and float(r['pos']) == 0 and r['loop'] == '0'
               and r['paused'] == '0' for r in channels)
    return dict(packets=packets, idleSpecialChannelObservations=len(channels))

def main():
    out = ROOT/'audit_bounded_native_pain_voice_checked'
    assert not out.exists()
    cases = {}
    hashes = {str(Path(__file__)): sync.sha(Path(__file__))}
    for fighter in ('sonya', 'kano'):
        folder = ROOT/f'audit_bounded_{fighter}_native_pain_voice_runtime'
        terminal = json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode'] == 0 and terminal['limitReason'] is None
        assert terminal['peakWorkingSetBytes'] < 320*1024*1024
        assert terminal['observerSha256'] == '1AFDE0F32B55A515F297D1B6C50685A8C7ECFEBFF3640151ACEFCA64E20D3D75'
        assert not (folder/'stderr.log').read_text().strip()
        rows = []
        with (folder/'run.log').open() as stream:
            for line in stream:
                assert len(line) < 65536 and '[LUA ERROR]' not in line
                tag = line.split(' ', 1)[0]
                if 'PAIN_' in tag:
                    rows.append((tag, dict(RX.findall(line))))
        positive = gate(rows, fighter)
        faults = []
        for key, value in (('a2', '00000000'), ('a8', '00000000'), ('route', 'wrong')):
            bad = copy.deepcopy(rows)
            next(r for tag, r in bad if tag.endswith('PAIN_BRANCH'))[key] = value
            try:
                gate(bad, fighter)
            except AssertionError:
                faults.append(key)
            else:
                raise AssertionError('Fault accepted: '+key)
        bad = copy.deepcopy(rows)
        index = next(i for i, (tag, _) in enumerate(bad) if tag.endswith('PAIN_BRANCH'))
        bad[index+2][1]['data'] = 'FF00'
        try:
            gate(bad, fighter)
        except AssertionError:
            faults.append('wrong_low_packet')
        else:
            raise AssertionError('Wrong packet accepted')
        cases[fighter] = dict(**positive, rejectedFaults=faults, terminal=terminal)
        hashes[str(folder/'run.log')] = sync.sha(folder/'run.log')
    report = dict(passed=True, cases=cases, sourceSync=sync.verify(), hashes=hashes,
                  mixedWaveformAccepted=False, subjectiveAudioAccepted=False,
                  allAudioContextsAccepted=False, fullGoalComplete=False)
    out.mkdir()
    (out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(passed=True, cases=cases)))

if __name__ == '__main__':
    main()
