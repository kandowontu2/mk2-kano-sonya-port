"""Actual native wins and unchanged preboss opening."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_shao_close_knife.py').read_text().replace('audit_current_kano_p2_shao_close_knife','audit_current_kano_p2_shao_recovered_knife')
exec(compile(source,__file__+'::recovered_knife','exec'))
