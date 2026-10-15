"""Preserve full original reader; use a literal debug compilation label."""
from pathlib import Path
path = Path(r'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port\tools\read_native_selector_cpu_projectile_pcm_frames_remote.py')
source = path.read_text()
before = "__file__ + '::whole_original_pixel_reader'"
assert source.count(before) == 1
source = source.replace(before, "'whole_original_pixel_reader_bound_remote'", 1)
exec(compile(source, str(path) + '::literal_debug_filename', 'exec'))
