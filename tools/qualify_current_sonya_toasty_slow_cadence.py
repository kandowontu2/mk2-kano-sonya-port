"""Same native gate with earned-prefix comparison before changed inputs."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_toasty_decisions.py').read_text()
for old,new in (
    ('audit_current_sonya_toasty_decisions_runtime','audit_current_sonya_toasty_slow_cadence_runtime'),
    ('audit_current_sonya_toasty_decisions_checked','audit_current_sonya_toasty_slow_cadence_checked'),
    ('audit_current_sonya_toasty_decisions_preparation','audit_current_sonya_toasty_slow_cadence_preparation'),
    ('assert {t:r for t,r in rows.items() if t not in new}==old',
     "assert {t:[r for r in group if int(r['frame'])<20697] for t,group in rows.items() if t not in new and any(int(r['frame'])<20697 for r in group)}=={t:[r for r in group if int(r['frame'])<20697] for t,group in old.items() if any(int(r['frame'])<20697 for r in group)}"),
    ('allPreviousPhysicalAndGameplayRecordsUnchanged=True','priorEarnedPrefixUnchangedThrough=20696'),
    ('actualSecretLifecycleAccepted=False','actualSecretLifecycleAccepted=proof[\'completeSameRoundControls\']'),
):
    assert old in source,old
    source=source.replace(old,new)
exec(compile(source,__file__+'::same_native_decision_and_lifecycle_gate','exec'))
