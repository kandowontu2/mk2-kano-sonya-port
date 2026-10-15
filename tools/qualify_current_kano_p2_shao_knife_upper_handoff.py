"""Verify actual native results, preserve preboss record prefix."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_shao_close_knife.py').read_text().replace('audit_current_kano_p2_shao_close_knife','audit_current_kano_p2_shao_knife_upper_handoff')
exec(compile(source,__file__+'::upper_handoff','exec'))
