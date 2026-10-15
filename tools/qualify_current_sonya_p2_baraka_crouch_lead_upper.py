"""Actual upper-entry receipt and retained native outcome checks."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_baraka_native_jumpkick.py').read_text()
source=source.replace('audit_current_sonya_p2_baraka_native_jumpkick','audit_current_sonya_p2_baraka_crouch_lead_upper')
exec(compile(source,__file__+'::bounded_context','exec'))
