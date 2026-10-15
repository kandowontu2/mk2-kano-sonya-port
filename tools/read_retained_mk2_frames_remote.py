"""Read-only bounded raster callback for the SAME terminal campaign host."""
import ast
from pathlib import Path

_retained_path=Path(r'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port\tools\read_live_shang_drain_frames_remote.py')
_retained_text=_retained_path.read_text()
_retained_function=next(n for n in ast.parse(_retained_text).body if isinstance(n,ast.FunctionDef))
_retained_source=ast.get_source_segment(_retained_text,_retained_function)
_retained_before="selected=[n for n in names if n in request and (n.startswith('shang_shrink_') or n.startswith('shang_victim_provenance_'))]"
assert _retained_source.count(_retained_before)==1
_retained_source=_retained_source.replace(_retained_before,"selected=[n for n in names if n in request]")
_retained_before="answer['nativePoll']=process.poll()"
assert _retained_source.count(_retained_before)==1
_retained_source=_retained_source.replace(_retained_before,_retained_before+"\n        assert answer['nativePoll']==0")
_retained_namespace={}
exec(compile(_retained_source,str(_retained_path)+'::same_original_terminal_host_read_only_rasters','exec'),_retained_namespace)
_retained_namespace['_mk2_drain_send_existing_rasters']()
