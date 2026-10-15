"""Verify unchanged earned chronology and group exact hit-time poses."""
import json
from collections import Counter
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_sonya_mirror_hit_pose_runtime'
out=sync.ROOT/'audit_current_sonya_mirror_hit_pose_checked'
assert not out.exists()
terminal=json.loads((folder/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason'] is None
baseline=chronology.load(sync.ROOT/'audit_current_sonya_mirror_neutral_recovery_runtime/run.log')
rows=chronology.load(folder/'run.log')
excluded={'HOST_BOUND','MIRROR_CPU_HIT_POSE'}
checked=[]
for tag,items in rows.items():
    if tag in excluded:continue
    actual=[r for r in items if int(r['frame'])<19500]
    expected=[r for r in baseline.get(tag,[]) if int(r['frame'])<19500]
    assert actual==expected,tag
    checked.append(tag)
for tag,items in baseline.items():
    if tag not in excluded and any(int(r['frame'])<19500 for r in items):assert tag in rows,tag
hits=rows['MIRROR_CPU_HIT_POSE']
assert hits
groups=Counter(r['cpu_pose'] for r in hits)
out.mkdir()
report=dict(passiveObservationPassed=True,unchangedPriorTags=checked,maximumFields=19500,
            hitCallbacks=len(hits),damage=sum(int(r['before'])-int(r['after']) for r in hits),
            poseCounts=dict(groups),hits=hits,logSHA256=sync.sha(folder/'run.log'),
            exactAttackSubtypeProven=False,fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:report[k] for k in ('hitCallbacks','damage','poseCounts')}))
