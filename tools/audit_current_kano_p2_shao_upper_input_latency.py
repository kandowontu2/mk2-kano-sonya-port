"""Measure actual upper entry latency, not intended HP pulse duration."""
import json
from collections import Counter
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify()
root=sync.ROOT;case=root/'audit_current_kano_p2_shao_upper_contact_bounded180_runtime'
out=root/'audit_current_kano_p2_shao_upper_input_latency_checked'
assert not out.exists()
rows=load(case/'run.log')
plans=[r for r in rows['BOSS_PLAN'] if r['stage']=='16' and r['move']=='shao_crouch_upper_attempt']
entries=[r for r in rows['BOSS_ACTION'] if r['stage']=='16' and r['after']=='263']
assert plans and entries
pairs=[]
for entry in entries:
    matching=[r for r in plans if r['human_actor']==entry['actor'] and r['human_main']==entry['main'] and 0<=int(entry['frame'])-int(r['frame'])<26]
    assert len(matching)==1
    plan=matching[0]
    pairs.append(dict(planFrame=int(plan['frame']),entryFrame=int(entry['frame']),latency=int(entry['frame'])-int(plan['frame']),planAction=int(plan['human_action']),planCpuAction=int(plan['cpu_action']),entryPc=entry['pc']))
assert len(pairs)==87
latencies=dict(Counter(r['latency'] for r in pairs))
assert all(r['latency']>3 for r in pairs)
report=dict(passedFiniteLatencyChecks=True,actualOwnedEntries=len(pairs),planToEntryFieldLatency=latencies,guardAtAgeThreePrecedesEveryMeasuredEntry=True,pairs=pairs,missingPlannedActivationsNotAutomaticallyGameBug=True,fullPortAccepted=False,logSHA256=sync.sha(case/'run.log'))
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='pairs'}))
