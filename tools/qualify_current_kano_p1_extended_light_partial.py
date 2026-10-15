"""Observer thinning preserves retained gameplay; wall-censored no new clear."""
import json,re
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load,check
sync.verify()
root=sync.ROOT;out=root/'audit_current_kano_p1_extended_light_partial_checked';assert not out.exists()
case=root/'audit_current_kano_p1_extended_light_runtime';path=case/'run.log'
rows=load(path);last=max(int(r['frame']) for values in rows.values() for r in values)
limit=min(last-1,119999)
def retained(path):
    found=[]
    for s in path.read_text().splitlines():
        if not s.startswith('MK2_NAT_CAMPAIGN_'):continue
        r=dict(re.findall(r'(\w+)=([^\s]+)',s));tag=s.split()[0].removeprefix('MK2_NAT_CAMPAIGN_')
        if int(r['frame'])>limit or tag in ('HOST_BOUND','RESULT') or(tag=='BOSS_ACTION' and r.get('stage')=='15'):continue
        found.append(s)
    return found
prior=root/'audit_current_kano_p1_subzero_guard_ready_v2_runtime/run.log'
assert retained(path)==retained(prior)
assert check(rows,1,17,list(range(13))+[14,15,16])[-1]==15
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'));assert terminal['limitReason']=='wall_limit'
earlier=root/'audit_current_kano_p1_extended_default_runtime'
first=json.loads((earlier/'terminal.json').read_text(encoding='utf-8-sig'));assert first['limitReason']=='wall_limit'
report=dict(retainedNativeGameplayRecordsExactlyPreservedThrough=limit,lastObservedFrame=last,
    omittedDiagnosticOnlyTag='BOSS_ACTION stage15',ownKintaroRounds=[r for r in rows['WIN'] if r['stage']=='15' and r['slot']=='1'],
    firstExtendedRunTerminal=first,lightRunTerminal=terminal,logSHA256=sync.sha(path),
    beyondPrior120000FieldFrontierReached=False,fullCampaignAccepted=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
