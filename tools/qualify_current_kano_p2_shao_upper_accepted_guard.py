"""Compact check output, actual native accepted upper/HP records retained."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_shao_upper_recovery_guard.py').read_text().replace('audit_current_kano_p2_shao_upper_recovery_guard','audit_current_kano_p2_shao_upper_accepted_guard')
exec(compile(source,__file__+'::accepted_guard','exec'))
