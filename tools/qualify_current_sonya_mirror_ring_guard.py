"""Same current identity/chronology/input-prefix gate for CPU-ring guard successor."""
from pathlib import Path
original=Path(__file__).with_name('qualify_current_sonya_mirror_ring_spacing.py')
code=original.read_text()
for old,new in (
    ('audit_current_sonya_mirror_ring_spacing_runtime','audit_current_sonya_mirror_ring_guard_runtime'),
    ('audit_current_sonya_mirror_ring_spacing_preparation','audit_current_sonya_mirror_ring_guard_preparation'),
    ('audit_current_sonya_mirror_ring_spacing_checked','audit_current_sonya_mirror_ring_guard_checked')):
    assert code.count(old)==1
    code=code.replace(old,new)
exec(compile(code,str(Path(__file__).resolve())+'::successor observation gate','exec'),{'__file__':__file__})
