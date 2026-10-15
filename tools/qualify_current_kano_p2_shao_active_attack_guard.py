"""Qualify retained opening and actual contact, not planned commands."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_shao_upper_recovery_guard.py').read_text().replace('audit_current_kano_p2_shao_upper_recovery_guard','audit_current_kano_p2_shao_active_attack_guard')
exec(compile(source,__file__+'::active_attack_guard','exec'))
