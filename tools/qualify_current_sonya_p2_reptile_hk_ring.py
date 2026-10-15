"""Actual native chronology/damage; not a command-count acceptance."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_reptile_leg_retreat.py').read_text().replace('audit_current_sonya_p2_reptile_leg_retreat','audit_current_sonya_p2_reptile_hk_ring')
exec(compile(source,__file__+'::native_context','exec'))
