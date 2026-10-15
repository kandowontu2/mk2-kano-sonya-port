"""Remote diagnostic contexts do not set __file__; bind the exact frozen path."""
from pathlib import Path
_anchor_remote_path='C:/Users/kando/Documents/Codex/2026-08-29/i-ha/work/mk2port/tools/read_live_shang_anchor_frames_remote.py'
_anchor_bound_source=Path(_anchor_remote_path).read_text()
assert _anchor_bound_source.count('__file__')==2
_anchor_bound_source=_anchor_bound_source.replace('__file__',repr(_anchor_remote_path))
exec(compile(_anchor_bound_source,_anchor_remote_path+'::explicit_read_only_callback_path','exec'))
