"""Qualify bounded OS render admission independently of censored guest completion."""
import copy
import hashlib
import json
import re
from pathlib import Path

R = Path(__file__).resolve().parent.parent
case = R / 'audit_current_os_audio_admission_runtime'
out = R / 'audit_current_os_audio_admission_partial_checked'
assert not out.exists()
t = json.loads((case / 'terminal.json').read_text(encoding='utf-8-sig'))
rows = [json.loads(s) for s in (case / 'audio_sessions.jsonl').read_text().splitlines()]
log = (case / 'run.log').read_text()
assert t['limitReason'] == 'wall_limit' and t['elapsedSeconds'] <= 45.5
assert max(t['peakWorkingSetBytes'], t['hostPeakWorkingSetBytes']) <= 320 * 1024**2
assert t['logBytes'] < 10 * 1024**2 and t['osAudioSettingsModified'] is False
assert t['soundProvider'] == 'auto' and t['throttled'] is True
assert not (case / 'stderr.log').read_text().strip()
assert 'DirectSound: Primary buffer: 48000 Hz, 16 bits, 2 channels' in log
assert not re.search(r'failed to submit|Error creating|Error playing|LUA ERROR', log, re.I)
assert 'human=18:18 cpu=18:18' in log

def gate(records):
    assert records and len(records) <= 120
    accepted = []
    for row in records:
        assert row['pid'] == t['pid'] and row['birth'] == t['birth']
        assert 0 <= row['elapsedSeconds'] <= t['elapsedSeconds']
        for r in row['readings']:
            assert r['Pid'] == t['pid'] and not r.get('Error')
            assert all(0 <= r[k] <= 1 for k in ('Peak', 'SessionVolume', 'EndpointVolume'))
            if (r['State'] == 1 and r['Peak'] > 0.00001 and
                    not r['SessionMute'] and not r['EndpointMute'] and
                    r['SessionVolume'] > 0 and r['EndpointVolume'] > 0):
                accepted.append({'elapsedSeconds': row['elapsedSeconds'], 'reading': r})
    assert accepted
    return accepted

accepted = gate(rows)
faults = []
for kind in ('wrong_pid', 'wrong_birth', 'zero_peak', 'inactive', 'session_mute',
             'endpoint_mute', 'zero_session_volume', 'zero_endpoint_volume'):
    altered = copy.deepcopy(rows)
    for row in altered:
        if kind == 'wrong_pid': row['pid'] += 1
        if kind == 'wrong_birth': row['birth'] = 'not-the-observed-process-birth'
        for r in row['readings']:
            field = {'zero_peak': ('Peak', 0), 'inactive': ('State', 0),
                     'session_mute': ('SessionMute', True),
                     'endpoint_mute': ('EndpointMute', True),
                     'zero_session_volume': ('SessionVolume', 0),
                     'zero_endpoint_volume': ('EndpointVolume', 0)}.get(kind)
            if field: r[field[0]] = field[1]
    try:
        gate(altered)
    except AssertionError:
        faults.append(kind)
    else:
        raise AssertionError('Accepted fault ' + kind)

report = dict(actualOSNonzeroRenderAdmissionAccepted=True,
              scope='Exact launched PID/birth, active Windows render session, nontrivial peak, positive existing volumes and no mute; source getter-only observation. Not hardware hearing or mix-quality acceptance.',
              actualBackend='DirectSound 48000Hz 16bit stereo',
              readings=len(rows), qualifiedReadings=len(accepted),
              firstQualified=accepted[0], lastQualified=accepted[-1],
              maximumObservedPeak=max(x['reading']['Peak'] for x in accepted),
              effectiveFaultsRejected=faults, terminal=t,
              actualLastObservedFrame=max(map(int, re.findall(r' frame=(\d+)', log))),
              normalGuestCompletionAccepted=False, guest1850FieldsAccepted=False,
              reason='Wall-limited at last complete record; no natural exit code available.',
              heardMixAccepted=False, hardwareHearingAccepted=False,
              allAudioContextsAccepted=False, fullPortAccepted=False,
              hashes={name: hashlib.sha256((case/name).read_bytes()).hexdigest().upper()
                      for name in ('run.log', 'audio_sessions.jsonl', 'terminal.json')})
out.mkdir()
(out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report))
