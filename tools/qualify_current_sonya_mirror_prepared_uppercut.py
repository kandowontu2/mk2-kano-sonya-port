"""Preserve whole current campaign gate; observe actual owned native uppercuts."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_sonya_mirror_ring_spacing.py').read_text()
for old,new in (
    ('audit_current_sonya_mirror_ring_spacing_runtime','audit_current_sonya_mirror_prepared_uppercut_runtime'),
    ('audit_current_sonya_mirror_ring_spacing_preparation','audit_current_sonya_mirror_prepared_uppercut_preparation'),
    ('audit_current_sonya_mirror_ring_spacing_checked','audit_current_sonya_mirror_prepared_uppercut_checked'),
    ('MIRROR_RING_SPACING_ATTEMPT','MIRROR_PREPARED_UPPERCUT_ATTEMPT'),
    ("specials=[r for r in rows.get('SPECIAL',[]) if r['stage']=='5' and r['move']=='ring']","specials=rows.get('MIRROR_NATIVE_UPPERCUT',[])\nassert all(r['id']==r['roster']=='18' and r['actor']==r['owner'] for r in specials)"),
    ('ringSpacingRequests','preparedUppercutRequests'),
    ('nativeRingEntries','nativeUppercutEntries')):
    assert code.count(old)==1;code=code.replace(old,new)
exec(compile(code,__file__+'::native uppercut observation gate','exec'),{'__file__':__file__})
