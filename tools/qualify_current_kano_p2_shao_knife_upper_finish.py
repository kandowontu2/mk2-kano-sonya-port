"""Actual native wins/unchanged early route, not input plans as success."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_shao_close_knife.py').read_text().replace('audit_current_kano_p2_shao_close_knife','audit_current_kano_p2_shao_knife_upper_finish')
exec(compile(source,__file__+'::upper_finish','exec'))
