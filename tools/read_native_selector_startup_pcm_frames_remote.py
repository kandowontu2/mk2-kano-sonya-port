"""Original123 distinct startup PCM-game rasters, not a replay or media file."""
from pathlib import Path
path = Path(r'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port\tools\read_native_selector_special_frames_remote.py')
source = path.read_text()
changes = (
    ("profile in('special','air')", "profile=='startup'"),
    ("root=sys.modules['__main__']if profile=='special'else sys.modules['capture_native_selector_square_contact_retained']",
     "root=sys.modules['capture_native_selector_cpu_projectile_pcm_startup_direct']"),
    ("cases=root.RAM_CASES if profile=='special'else root.CONTACT_CASES", 'cases=root.RAM_CASES'),
    ("handles=root.NATIVE_HANDLES if profile=='special'else root.CONTACT_HANDLES", 'handles=root.NATIVE_HANDLES'),
    ("assert held['process'].poll()==0 and report['nativeExit']==0 and report['passed']",
     "receipt=json.loads((folder.parent.parent/'audit_native_selector_cpu_startup_ring_audio_checked'/'report.json').read_text()); assert held['process'].poll()==0 and report['nativeExit']==0 and report['passed'] and receipt['passed'] and receipt['actualNativeIdentity']==held['identity']; answer['fullNativeStateHealthRequalificationRequired']=True"),
    ("rgb=images[f\"ui_{row['frame']:04d}.png\"]", "rgb=images[row['imageKey']]"),
)
for before, after in changes:
    assert source.count(before) == 1
    source = source.replace(before, after, 1)
exec(compile(source, 'whole_original_startup_PCM_raster_reader_bound', 'exec'))
