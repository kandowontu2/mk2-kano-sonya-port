"""Actual native wins; not planned physical hit count."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_shao_close_knife.py').read_text().replace('audit_current_kano_p2_shao_close_knife','audit_current_kano_p2_shao_knife_upper_handoff20')
exec(compile(source,__file__+'::upper_handoff20','exec'))
