"""Observer-neutral controller gate diagnosis; no inferred native rejection."""
import json
from collections import Counter
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
case=sync.ROOT/'audit_current_kano_p2_scorpion_readiness_trace_runtime'
out=sync.ROOT/'audit_current_kano_p2_scorpion_readiness_trace_checked'
assert not out.exists()
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_kano_p2_scorpion_readiness_trace_preparation/campaign.lua')
assert not (case/'stderr.log').read_text().strip()
rows=chronology.load(case/'run.log');old=chronology.load(sync.ROOT/'audit_current_kano_p2_scorpion_crouch_ready_runtime/run.log')
for tag in set(rows)|set(old):
    if tag!='SCORPION_READY':assert rows.get(tag,[])==old.get(tag,[]),tag
trace=rows['SCORPION_READY'];assert trace
for r in trace:
    ready=int(r['height'])==0 and int(r['flags'],16)&12==0 and int(r['body'],16)&12==0 and int(r['action']) in (770,771,772)
    assert int(r['ready'])==int(ready)
report=dict(passiveObserverNeutral=True,terminal=terminal,sampledGateFields=len(trace),
    gateStates=dict(Counter(r['ready'] for r in trace)),
    readyWithinRange=sum(r['ready']=='1' and int(r['gap'])<105 for r in trace),
    actualHPInputFields=sum(r['button']=='High_Punch' and int(r['frame'])>=21977 for r in rows['INPUT']),
    openingTrace=trace[:20],fullCampaignAccepted=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
