"""Exact native BGRX-digest verification using original callback image keys."""
from pathlib import Path
source=Path(r'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port\tools\read_native_selector_special_frames_remote.py').read_text()
changes=(("profile in('special','air')","profile=='guard'"),
    ("root=sys.modules['__main__']if profile=='special'else sys.modules['capture_native_selector_square_contact_retained']",
     "root=sys.modules['capture_native_selector_cpu_guard_shadow']"),
    ("cases=root.RAM_CASES if profile=='special'else root.CONTACT_CASES","cases=root.RAM_CASES"),
    ("handles=root.NATIVE_HANDLES if profile=='special'else root.CONTACT_HANDLES","handles=root.NATIVE_HANDLES"),
    ("rgb=images[f\"ui_{row['frame']:04d}.png\"]","rgb=images[row['imageKey']]"))
for before,after in changes:
    assert source.count(before)==1;source=source.replace(before,after,1)
exec(compile(source,'whole_original_BGRX_callback_distinct_guard_viewer','exec'))
