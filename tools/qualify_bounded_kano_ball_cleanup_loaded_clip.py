"""Resolve clip from first actual current runtime sample-path, not root fallback."""
from pathlib import Path
source=Path(__file__).with_name('qualify_bounded_kano_ball_cleanup_direct.py').read_text()
old="clip=sync.ROOT/'samples/mk2ks/kano_ball_launch.wav'"
assert source.count(old)==1
source=source.replace(old,"clip=sync.ROOT/'diagnostic_native_selector_layers_long/samples/mk2ks/kano_ball_launch.wav'")
source=source.replace('audit_bounded_kano_ball_cleanup_direct_checked','audit_bounded_kano_ball_cleanup_loaded_clip_checked')
exec(compile(source,__file__+'::loaded clip','exec'),{'__name__':'__main__'})
