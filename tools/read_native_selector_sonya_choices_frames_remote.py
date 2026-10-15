"""Original distinct Sonya choice match; full native raster digest, RAM only."""
from pathlib import Path
path = Path(r'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port\tools\read_native_selector_startup_pcm_frames_remote.py')
source = path.read_text()
changes = (
    ('capture_native_selector_cpu_projectile_pcm_startup_direct', 'capture_native_selector_sonya_cpu_choices'),
    ('audit_native_selector_cpu_startup_ring_audio_checked', 'audit_native_selector_sonya_cpu_choices_checked'),
)
for before, after in changes:
    assert source.count(before) == 1
    source = source.replace(before, after, 1)
exec(compile(source, 'whole_original_sonya_choice_raster_reader', 'exec'))
