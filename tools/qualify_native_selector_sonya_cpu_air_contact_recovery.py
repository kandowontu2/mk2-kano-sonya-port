"""Preserve first rejection; distinguish earlier Leg Grab from Bicycle cleanup."""
import json
from pathlib import Path
import qualify_native_selector_sonya_cpu_air_contact as rejected

failure=rejected.OUT/'failure.json'
rejected.need(json.loads(failure.read_text())['error']==
    "ValueError('Actual human cleanup action store, no synthesized victim ready event')",
    'Actual full contact proof rejected an earlier Leg Grab hurt-clear; preserve source and failure')
source=Path(rejected.__file__).read_text()
for before,after in (
    ("OUT=ROOT/'audit_native_selector_sonya_cpu_air_contact_checked'",
     "OUT=ROOT/'audit_native_selector_sonya_cpu_air_contact_recovery_checked'"),
    ("r['slot']==1 and r['kind']=='action' and r['before']==0x506 and r['after']==0",
     "hit<r['frame']<=clear and r['slot']==1 and r['kind']=='action' and r['before']==0x506 and r['after']==0"),
    ('for p in (Path(__file__),parent,Path(original.__file__),',
     'for p in (Path(__file__),Path(rejected.__file__),failure,parent,Path(original.__file__),'),
    ('actualContact=positive,effectiveFaultsRejected=faults,',
     'actualContact=positive,effectiveFaultsRejected=faults,earlierLegGrabCleanupScopeRejectionPreserved=True,')):
    rejected.need(source.count(before)==1,'Only exact chronological cleanup ownership/failure preservation boundary')
    source=source.replace(before,after,1)
exec(compile(source,__file__+'::whole_contact_actual_posthit_recovery','exec'))
