"""Actual taunt trace and observer-only native history comparison."""
import json,re
from collections import Counter
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT;case=root/'audit_current_kano_p2_shao_taunt_observer_runtime'
out=root/'audit_current_kano_p2_shao_taunt_observer_checked';assert not out.exists()
def load(path):
    rows=[]
    for line in path.open():
        assert 'LUA ERROR' not in line
        if line.startswith('MK2_NAT_CAMPAIGN_'):
            rows.append((line.split()[0].removeprefix('MK2_NAT_CAMPAIGN_'),dict(re.findall(r'(\w+)=([^\s]+)',line))))
    return rows
rows=load(case/'run.log');last=max(int(r['frame']) for _,r in rows)
prior=load(root/'audit_current_kano_p2_shao_recovered_knife_runtime/run.log')
assert [(t,r) for t,r in rows if t!='SHAO_TAUNT_TRACE']==[(t,r) for t,r in prior if int(r['frame'])<=last]
traces=[r for t,r in rows if t=='SHAO_TAUNT_TRACE']
assert all(r['writes']=='0' and r['assistance']=='none' and r['cpu_id']=='13' and r['human_id']=='17' for r in traces)
pairs=[];pending=None;starts=0;censored=0
for tag,r in rows:
    if tag=='FIGHT':
        if pending:censored+=1
        pending=None
    if tag!='SHAO_TAUNT_TRACE':continue
    if r['entry']=='FF9D0FD0':
        starts+=1
        if pending:censored+=1
        pending=r
    elif r['entry']=='FF9D12F0' and pending and pending['cpu_main']==r['cpu_main']:
        a,b=int(pending['frame']),int(r['frame'])
        knives=[s for t,s in rows if t=='SPECIAL' and s.get('stage')=='16' and s.get('move')=='knife' and a<=int(s['frame'])<=b]
        pairs.append(dict(start=a,end=b,observedFields=b-a,startGap=int(pending['gap']),endGap=int(r['gap']),
            knifeEntriesInsideObservedWindow=len(knives),cpuMain=r['cpu_main']))
        pending=None
if pending:censored+=1
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert not (case/'stderr.log').read_text().strip()
report=dict(nativeHistoryUnchangedThrough=last,actualTauntStarts=starts,pairedTauntTails=len(pairs),
    unmatchedStarts=censored,observedDurationFields=dict(Counter(r['observedFields'] for r in pairs)),pairs=pairs,
    terminal=terminal,logSHA256=sync.sha(case/'run.log'),winningTauntControllerProved=False,fullPortAccepted=False,
    caveat='Paired entry/tail only; unmatched starts may be interrupted/censored. No invulnerability or guaranteed attack opportunity inferred.')
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='pairs'}))
