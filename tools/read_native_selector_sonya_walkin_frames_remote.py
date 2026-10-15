"""Original whole-pixel reader bound to actual walk-in capture module."""
from pathlib import Path
path=Path(r'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port\tools\read_native_selector_sonya_throw_late_frames_remote.py')
source=path.read_text()
for before,after in (
    ('capture_native_selector_sonya_throw_late_views','capture_native_selector_sonya_walkin_kano_cpu'),
    ('audit_native_selector_sonya_throw_late_views_capture_checked','audit_native_selector_sonya_walkin_kano_cpu_capture_checked')):
    assert source.count(before)==1
    source=source.replace(before,after,1)
exec(compile(source,str(path)+'::same_full_native_walkin_raster_reader','exec'))
