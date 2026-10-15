"""Full original BGRX viewer; only the actual retained capture module changes."""
from pathlib import Path
source=Path(r'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port\tools\read_native_selector_cpu_guard_frames_remote.py').read_text()
before='capture_native_selector_cpu_guard_shadow'
assert source.count(before)==1
source=source.replace(before,'capture_native_selector_cpu_startup_guard',1)
exec(compile(source,'whole_original_BGRX_startup_guard_viewer','exec'))
