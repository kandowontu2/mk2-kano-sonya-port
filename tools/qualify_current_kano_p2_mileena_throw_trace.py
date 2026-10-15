"""Finite passive throw trace; compare all complete earlier gameplay records."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
runtime = root / 'audit_current_kano_p2_mileena_throw_trace_runtime'
baseline = root / 'audit_current_kano_p2_mileena_retreat_counter_runtime'
prefix = 'MK2_NAT_CAMPAIGN_'

def records(path):
    result = []
    for line in path.read_text().splitlines():
        if not line.startswith(prefix):
            continue
        parts = line.split()
        fields = dict(part.split('=', 1) for part in parts[1:] if '=' in part)
        result.append((parts[0][len(prefix):], fields, line))
    return result

rows = records(runtime / 'run.log')
old = records(baseline / 'run.log')
terminal = json.loads((runtime / 'terminal.json').read_text())
assert terminal['exitCode'] == -1 and terminal['limitReason'] == 'wall_limit'
assert terminal['peakWorkingSetBytes'] <= 320 * 1024 * 1024
assert terminal['logBytes'] <= 10 * 1024 * 1024
assert terminal['elapsedSeconds'] < 92
assert not (runtime / 'stderr.log').read_bytes()
lua = root / 'audit_current_kano_p2_mileena_throw_trace_preparation/campaign.lua'
assert hashlib.sha256(lua.read_bytes()).hexdigest().upper() == terminal['observerSha256']
last = max(int(fields['frame']) for _, fields, _ in rows)
excluded = {'MILEENA_THROW_START', 'HOST_BOUND', 'RESULT'}
def complete(sequence):
    return [line for tag, fields, line in sequence
            if tag not in excluded and int(fields['frame']) < last]
assert complete(rows) == complete(old), 'Passive observer changed complete gameplay prefix'
throws = [fields for tag, fields, _ in rows if tag == 'MILEENA_THROW_START']
assert throws
for fields in throws:
    assert fields['stage'] == '10' if 'stage' in fields else True
    assert fields['writes'] == '0' and fields['assistance'] == 'none'
    assert fields['a8'] == fields['cpu_actor']
    assert fields['a13'] == fields['cpu_main']
    assert int(fields['at'], 16) == int(fields['cpu_main'], 16) + 0x1f0
    assert fields['cpu_actor'] != fields['human_actor']
    assert fields['cpu_main'] != fields['human_main']
    assert fields['pc'] == 'FF8B6FA0'
report = dict(finiteEvidenceVerified=True, fullCampaignAccepted=False,
              fullPortAccepted=False, completed60000=False,
              completeGameplayPrefixUnchangedBefore=last,
              actualNativeThrowStarts=len(throws),
              startsOutsideGap70=sum(int(f['gap']) >= 70 for f in throws),
              gaps=[int(f['gap']) for f in throws], terminal=terminal)
out = root / 'audit_current_kano_p2_mileena_throw_trace_checked'
out.mkdir(exist_ok=False)
(out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report))
