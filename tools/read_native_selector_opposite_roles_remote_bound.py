"""Diagnostic-hook globals do not supply __file__; bind exact original path."""
from pathlib import Path
path=Path(r'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port\tools\read_native_selector_opposite_roles_remote.py')
exec(compile(path.read_text(),str(path)+'::explicit_diagnostic_source_path','exec'),dict(globals(),__file__=str(path)))
