"""Preserve5501 preflight; bind the retained qualified module in full-source scope."""
import json
from pathlib import Path
import verify_current_reptile_p2_overlap_v5499 as previous

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
failure=ROOT/'audit_v5501_current_reptile_overlap_progress/progress.json'
need(json.loads(failure.read_text())['error']=="NameError(\"name 'qualified' is not defined\")"and
     not previous.BASE.exists(),'Exact preserved preboot namespace failure; no native run restarted')
source=Path(previous.__file__).read_text()
changes={
 "BASE=ROOT/'audit_v5500_current_reptile_p2_overlap_ram'":"BASE=ROOT/'audit_v5503_current_reptile_p2_overlap_ram'",
 "OUT=ROOT/'audit_v5501_current_reptile_overlap_progress'":"OUT=ROOT/'audit_v5504_current_reptile_overlap_progress'",
 'corrected_physical_faults=corrected_physical_faults,preserved_cases=prior)':
 'corrected_physical_faults=corrected_physical_faults,preserved_cases=prior,qualified=qualified)',
}
for before,after in changes.items():
    need(source.count(before)==1,'Exact whole pending P2 qualification namespace/immutable output correction')
    source=source.replace(before,after)
exec(compile(source,__file__+'.whole5499_complete_retained_qualified_module_binding','exec'),globals())
