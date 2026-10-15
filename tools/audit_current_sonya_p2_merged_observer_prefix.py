"""Full per-tag native/damage/control prefix equality to best retained trial."""
import json
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify()
root=sync.ROOT
case=root/'audit_current_sonya_p2_baraka_merged_damage_observer_runtime'
reference=root/'audit_current_sonya_p2_baraka_hk_guard_ready_runtime'
out=root/'audit_current_sonya_p2_merged_observer_prefix_checked'
assert not out.exists()
actual=load(case/'run.log');prior=load(reference/'run.log')
last=min(max(int(r['frame']) for records in actual.values() for r in records),59999)
assert last>50238
def prefix(rows):
    return {tag:[r for r in records if int(r['frame'])<=last] for tag,records in rows.items() if tag!='HOST_BOUND' and any(int(r['frame'])<=last for r in records)}
a,b=prefix(actual),prefix(prior)
assert a==b,'Passive observer merger changed observed prefix'
report=dict(passedFiniteChecks=True,allObservedTagsIdenticalThrough=last,comparedRows=sum(len(v) for v in a.values()),comparedTags=sorted(a),referenceLogSHA256=sync.sha(reference/'run.log'),actualLogSHA256=sync.sha(case/'run.log'),physicalInputsAndNativeEventsPreserved=True,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
