"""Same best controls, original damage outcomes; new passive merger scope."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_baraka_hk_guard_ready.py').read_text()
source=source.replace('audit_current_sonya_p2_baraka_hk_guard_ready','audit_current_sonya_p2_baraka_merged_damage_observer')
exec(compile(source,__file__+'::bounded_context','exec'))
