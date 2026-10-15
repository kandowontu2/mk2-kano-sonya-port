"""Actual native leg entries and campaign outcomes, not input plan counts."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_baraka_leg_spacing.py').read_text().replace('audit_current_sonya_p2_baraka_leg_spacing','audit_current_sonya_p2_baraka_own_ready_leg')
exec(compile(source,__file__+'::native_context','exec'))
