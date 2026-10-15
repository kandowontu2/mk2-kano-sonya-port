"""Full retained native opening through qualified Reptile match admission."""
import json,re
import verify_native_source_sync as sync
sync.verify()
baseline=sync.ROOT/'audit_current_sonya_p2_reptile_hk_early_retreat_runtime/run.log'
current=sync.ROOT/'audit_current_sonya_p2_baraka_hk_ring_runtime/run.log'
out=sync.ROOT/'audit_current_sonya_p2_baraka_opening_preservation_checked'
assert not out.exists()
def prefix(path):
    return [line for line in path.read_text().splitlines() if (m:=re.search(r' frame=(\d+) ',line)) and int(m[1])<50238]
old,new=prefix(baseline),prefix(current)
assert old and old==new
out.mkdir();report=dict(passed=True,identicalNativeRecords=len(new),identicalThroughField=50237,baselineSHA256=sync.sha(baseline),currentSHA256=sync.sha(current),fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
