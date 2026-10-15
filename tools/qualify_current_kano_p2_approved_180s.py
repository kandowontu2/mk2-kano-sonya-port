"""Retained physical/native prefix, explicit frontier for approved longer run."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_campaign_frontier_observer.py').read_text()
source=source.replace('audit_current_kano_p2_campaign_frontier_observer','audit_current_kano_p2_approved_180s')
exec(compile(source,__file__+'::approved_bounded_run','exec'))
