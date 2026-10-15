"""Same7 actual twoKO/selection/return mutations for realKano17."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_smoke_return_faults.py').read_text()
for old,new in (
    ('audit_current_sonya_smoke_transition_batched_runtime','audit_current_kano_smoke_64_cadence_runtime'),
    ('audit_current_sonya_smoke_transition_batched_checked','audit_current_kano_smoke_64_cadence_checked'),
    ('audit_current_sonya_smoke_return_faults_checked','audit_current_kano_smoke_return_faults_checked'),
    ("'18,4'","'17,4'"),("{'1':'18','2':'4'}","{'1':'17','2':'4'}"),
    ('currentNaturalSonyaSmokeReturnPassed','currentNaturalKanoSmokeReturnPassed'),
):
    assert old in source,old
    source=source.replace(old,new)
start=source.index("old=load(sync.ROOT/'audit_current_sonya_smoke_transition_runtime/run.log')")
finish=source.index('def gate(records):',start)
source=source[:start]+source[finish:]
source=source.replace('batchingPreservesEveryPriorRecordThrough=through,','physicalCadence=64,')
exec(compile(source,__file__+'::same_actual_Kano_return_faults','exec'))
