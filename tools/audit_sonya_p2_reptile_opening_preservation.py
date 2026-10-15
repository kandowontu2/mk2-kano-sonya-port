"""Prove preserved current cold opening, not a complete Reptile match."""
import json,re
import verify_native_source_sync as sync
sync.verify()
baseline=sync.ROOT/'audit_current_sonya_p2_liukang_leg_spacing_runtime/run.log'
current=sync.ROOT/'audit_current_sonya_p2_reptile_leg_spacing_runtime/run.log'
out=sync.ROOT/'audit_current_sonya_p2_reptile_opening_preservation_checked'
assert not out.exists()
def prefix(path):
    return [line for line in path.read_text().splitlines() if (m:=re.search(r' frame=(\d+) ',line)) and int(m[1])<44489]
old,new=prefix(baseline),prefix(current)
assert old and old==new
report=dict(passed=True,identicalNativeRecords=len(new),identicalThroughField=44488,baselineSHA256=sync.sha(baseline),currentSHA256=sync.sha(current),reptileMatchStillOpenAtObservedField46050=True,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
