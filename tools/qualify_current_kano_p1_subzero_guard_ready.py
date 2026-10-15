"""Reuse direct native chronology gate, preserve earlier P1 report."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p1_learned_campaign.py').read_text().replace('audit_current_kano_p1_learned_campaign_runtime','audit_current_kano_p1_subzero_guard_ready_runtime').replace('audit_current_kano_p1_learned_campaign_checked','audit_current_kano_p1_subzero_guard_ready_checked')
exec(compile(source,__file__+'::subzero_guard_ready','exec'))
