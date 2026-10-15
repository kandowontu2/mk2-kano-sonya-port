"""Repair only original passive viewer exception-string quotation."""
from pathlib import Path
source=Path(r'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port\tools\read_native_selector_cpu_sonya_continuous_frames_remote.py').read_text()
begin=source.index('        assert report[\'error\']==')
end=source.index('\n',begin)
source=source[:begin]+'''        assert report['error']==repr(ValueError("invalid literal for int() with base 10: 'continuous_guard'"))'''+source[end:]
exec(compile(source,'whole_original_passive_viewer_error_repr_repair','exec'))
