"""Exact native history plus owned original charge-phase observations."""
import json,re
from collections import Counter
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT;case=root/'audit_current_kano_p2_shao_charge_observer_runtime'
out=root/'audit_current_kano_p2_shao_charge_observer_checked';assert not out.exists()
def load(path):
    rows=[]
    for line in path.open():
        assert 'LUA ERROR' not in line
        if line.startswith('MK2_NAT_CAMPAIGN_'):
            rows.append((line.split()[0].removeprefix('MK2_NAT_CAMPAIGN_'),dict(re.findall(r'(\w+)=([^\s]+)',line))))
    return rows
rows=load(case/'run.log');last=max(int(r['frame']) for _,r in rows)
prior=load(root/'audit_current_kano_p2_shao_recovered_knife_runtime/run.log')
assert [(t,r) for t,r in rows if t!='SHAO_CHARGE_TRACE']==[(t,r) for t,r in prior if int(r['frame'])<=last]
traces=[r for t,r in rows if t=='SHAO_CHARGE_TRACE']
assert traces and all(r['human_id']=='17' and r['cpu_id']=='13' and r['writes']=='0' and r['assistance']=='none' for r in traces)
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert not (case/'stderr.log').read_text().strip()
report=dict(nativeHistoryUnchangedThrough=last,ownedChargeTraceEvents=dict(Counter(r['entry'] for r in traces)),
    humanActionAtContactRecovery=dict(Counter(r['human_action'] for r in traces if r['entry']=='FF9D24C0')),
    humanActionAtMissRecovery=dict(Counter(r['human_action'] for r in traces if r['entry']=='FF9D26B0')),
    traces=traces,terminal=terminal,logSHA256=sync.sha(case/'run.log'),
    caveat='These are callback-time states, not pre-hit states. Contact path does not by itself distinguish hit from block. A winning counter or complete safe window is not proven.',
    winningControllerProved=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='traces'}))
