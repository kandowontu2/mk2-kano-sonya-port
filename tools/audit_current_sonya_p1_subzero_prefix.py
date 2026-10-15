"""Same native/physical history before stage11-only controller change."""
import json,re
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT;out=root/'audit_current_sonya_p1_subzero_prefix_checked';assert not out.exists()
old=root/'audit_current_sonya_p1_learned_campaign_runtime/run.log';new=root/'audit_current_sonya_p1_subzero_guard_ready_runtime/run.log'
def prefix(path):return [s for s in path.read_text().splitlines() if s.startswith('MK2_NAT_CAMPAIGN_') and int(re.search(r'\bframe=(\d+)',s)[1])<=73681]
assert prefix(old)==prefix(new)
out.mkdir();report=dict(nativeAndPhysicalPrefixExactlyPreservedThrough=73681,matchingRecords=len(prefix(old)),
    beforeSHA256=sync.sha(old),afterSHA256=sync.sha(new),fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
