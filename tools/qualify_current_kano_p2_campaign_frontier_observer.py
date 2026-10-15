"""Explicit reduced observation scope; physical/native retained prefix equality."""
import json
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify()
root=sync.ROOT;case=root/'audit_current_kano_p2_campaign_frontier_observer_runtime'
prior=root/'audit_current_kano_p2_changed_health_only_runtime'
out=root/'audit_current_kano_p2_campaign_frontier_observer_checked'
assert not out.exists()
rows=load(case/'run.log');reference=load(prior/'run.log')
last=max(int(r['frame']) for records in rows.values() for r in records);through=min(last,65763)
omitted={'HEALTH','BOSS_HANDLER','KANO_P2_SONYA_DAMAGE','KANO_P2_SUBZERO_DAMAGE','KANO_P2_LIU_DAMAGE','KANO_P2_SCORPION_DAMAGE','KANO_P2_KITANA_DAMAGE','KANO_P2_MILEENA_DAMAGE'}
def prefix(items):
    result={}
    for tag,records in items.items():
        if tag in omitted or tag=='HOST_BOUND':continue
        selected=[r for r in records if int(r['frame'])<=through and not(tag=='BOSS_FIELD' and int(r['frame'])%120!=0)]
        if selected:result[tag]=selected
    return result
assert prefix(rows)==prefix(reference)
terminal=json.loads((case/'terminal.json').read_text())
assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
later={tag:[r for r in rows.get(tag,[]) if int(r['frame'])>65763] for tag in ['STAGE','FIGHT','WIN','LOSS','PICTURE','TEXT','RESULT']}
report=dict(passedFinitePrefixChecks=True,unchangedPhysicalInputsAndRetainedNativeEventsThrough=through,omittedDiagnosticTags=sorted(omitted),denseDamageCoverageClaimed=False,lastLoggedField=last,laterCampaignEvidence=later,terminal=terminal,logSHA256=sync.sha(case/'run.log'),fullCampaignAccepted=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
