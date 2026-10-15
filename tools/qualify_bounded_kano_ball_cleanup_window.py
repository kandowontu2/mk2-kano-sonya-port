"""Use actual138 post-hit callback records; preserve end-of-clip duration gate."""
from pathlib import Path
source=Path(__file__).with_name('qualify_bounded_kano_ball_cleanup_direct.py').read_text()
source=source.replace("clip=sync.ROOT/'samples/mk2ks/kano_ball_launch.wav'","clip=sync.ROOT/'diagnostic_native_selector_layers_long/samples/mk2ks/kano_ball_launch.wav'")
old='assert len(cleared)>200 and'
assert source.count(old)==1
source=source.replace(old,'assert len(cleared)==138 and')
source=source.replace('audit_bounded_kano_ball_cleanup_direct_checked','audit_bounded_kano_ball_cleanup_window_checked')
exec(compile(source,__file__+'::actual observation window','exec'),{'__name__':'__main__'})
