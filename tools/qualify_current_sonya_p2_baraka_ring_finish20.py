"""Direct earlier-route and actual native damage/results checks."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_baraka_hk_spacing90_v2.py').read_text().replace('audit_current_sonya_p2_baraka_hk_spacing90_runtime','audit_current_sonya_p2_baraka_ring_finish20_runtime').replace('audit_current_sonya_p2_baraka_hk_spacing90_v2_checked','audit_current_sonya_p2_baraka_ring_finish20_checked')
exec(compile(source,__file__+'::ring_finish20','exec'))
