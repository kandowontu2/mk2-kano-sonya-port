"""Owned upper activation and preceding native crouch loop; no hit claim."""
import json
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify()
root=sync.ROOT;log=root/'audit_current_kano_p2_shao_charge_settled_counter_runtime/run.log'
out=root/'audit_current_shao_settled_counter_activation_checked';assert not out.exists()
rows=load(log);entries=[r for r in rows['BOSS_ACTION'] if r['stage']=='16' and r['after']=='263']
assert len(entries)==46 and all(r['id']==r['roster']=='17' and r['actor']==r['owner']==r['a8'] and r['main']==r['a13'] for r in entries)
plans=[r for r in rows['BOSS_PLAN'] if r['move']=='shao_charge_recovery_upper_attempt']
loops=[r for r in rows['BOSS_ACTION'] if r['stage']=='16' and r['after']=='770' and r['pc']=='FF82FA80']
for r in plans:
    assert r['human_action']=='770'
    assert any(s['main']==r['human_main'] and 0<int(r['frame'])-int(s['frame'])<=2 for s in loops)
report=dict(ownedUpperStateEntries=len(entries),counterPlansAfterObservedCrouchLoop=len(plans),
    inputTransitionTimingCorrected=True,directHitCountProved=False,ownShaoMatchCleared=False,
    fullPortAccepted=False,logSHA256=sync.sha(log))
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
