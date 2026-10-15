"""Confirm observer neutrality and report actual action transitions."""
import json
from collections import Counter
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_mirror_jump_action_trace_runtime'
terminal=json.loads((folder/'terminal.json').read_text())
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert terminal['elapsedSeconds']<90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_mirror_jump_action_trace_preparation/campaign.lua')
assert not (folder/'stderr.log').read_text().strip()
rows=chronology.load(folder/'run.log')
old=chronology.load(sync.ROOT/'audit_current_sonya_mirror_jumpkick_runtime/run.log')
assert rows['RESULT'][0]['frame']=='18500'
for tag in set(rows)|set(old):
    if tag in ('MIRROR_ACTION_CHANGE','RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue
    assert [r for r in rows.get(tag,[]) if int(r['frame'])<18500]==[r for r in old.get(tag,[]) if int(r['frame'])<18500],tag
events=rows['MIRROR_ACTION_CHANGE']
assert events and all(r['actor']==r['owner'] and r['id']==r['roster']=='18' for r in events)
counts={slot:dict(Counter(r['action'] for r in events if r['slot']==slot)) for slot in ('1','2')}
report=dict(passedObserverNeutrality=True,unchangedInputsThrough=18499,
 ownedActionChanges=len(events),actionCountsBySlot=counts,
 humanAirAttackCandidates=[r for r in events if r['slot']=='1' and int(r['action']) in (1024,1025)],
 cpuThrowEntries=sum(r['slot']=='2' and r['action']=='1287' for r in events),
 exactHitAttributionProven=False,fullPortAccepted=False,logSHA256=sync.sha(folder/'run.log'))
out=sync.ROOT/'audit_current_mirror_jump_action_trace_checked'
assert not out.exists();out.mkdir()
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
