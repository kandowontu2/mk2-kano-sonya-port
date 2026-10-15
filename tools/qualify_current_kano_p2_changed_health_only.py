"""Native/input prefix equivalence and explicit later campaign frontier."""
import json
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify()
root=sync.ROOT;case=root/'audit_current_kano_p2_changed_health_only_runtime'
prior=root/'audit_current_kano_p2_campaign_render_skip_runtime'
out=root/'audit_current_kano_p2_changed_health_only_checked'
assert not out.exists()
rows=load(case/'run.log');reference=load(prior/'run.log')
last=max(int(r['frame']) for records in rows.values() for r in records)
through=min(last,56421)
def prefix(items):
    result={}
    for tag,records in items.items():
        if tag=='HOST_BOUND':continue
        selected=[r for r in records if int(r['frame'])<=through and not(tag=='HEALTH' and int(r['frame'])>=1690 and r['before']==r['after'])]
        if selected:result[tag]=selected
    return result
assert prefix(rows)==prefix(reference)
terminal=json.loads((case/'terminal.json').read_text())
assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
later={tag:[r for r in rows.get(tag,[]) if int(r['frame'])>56421] for tag in ['STAGE','FIGHT','WIN','LOSS','PICTURE','TEXT','RESULT']}
report=dict(passedFinitePrefixChecks=True,unchangedActualInputsAndNativeEventsThrough=through,onlyUnchangedHealthRowsOmitted=True,lastLoggedField=last,laterCampaignEvidence=later,terminal=terminal,logSHA256=sync.sha(case/'run.log'),fullCampaignAccepted=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
