"""Whole native RGB digest reader, without waiving original gameplay rejection.

This capture's mirror-specific gameplay report is false for natural Sonya.
Rendering is bound to its terminal transport, exact pixels and positive PCM
inventory receipt, not reclassified as a gameplay pass.
"""
from pathlib import Path
source = Path(r'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port\tools\read_native_selector_special_frames_remote.py').read_text()
changes = (
    ("profile in('special','air')", "profile=='natural'"),
    ("root=sys.modules['__main__']if profile=='special'else sys.modules['capture_native_selector_square_contact_retained']",
     "root=sys.modules['capture_native_selector_cpu_projectile_pcm_natural']"),
    ("cases=root.RAM_CASES if profile=='special'else root.CONTACT_CASES", "cases=root.RAM_CASES"),
    ("handles=root.NATIVE_HANDLES if profile=='special'else root.CONTACT_HANDLES", "handles=root.NATIVE_HANDLES"),
    ("assert held['process'].poll()==0 and report['nativeExit']==0 and report['passed']",
     "receipt=json.loads((folder.parent.parent/'audit_native_selector_cpu_projectile_pcm_inventory_checked'/'report.json').read_text()); assert held['process'].poll()==0 and report['nativeExit']==0 and receipt['passed'] and receipt['actualNativeIdentity']==held['identity']; answer['originalGameplayPassed']=report['passed']"),
    ("rgb=images[f\"ui_{row['frame']:04d}.png\"]", "rgb=images[row['imageKey']]"))
for before, after in changes:
    assert source.count(before) == 1
    source = source.replace(before, after, 1)
exec(compile(source, __file__ + '::whole_original_pixel_reader', 'exec'))
