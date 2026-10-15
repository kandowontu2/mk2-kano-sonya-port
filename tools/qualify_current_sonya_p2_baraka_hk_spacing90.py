"""Use existing finite mechanics gate, no command-plan success claim."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_baraka_hk_ring.py').read_text().replace('audit_current_sonya_p2_baraka_hk_ring','audit_current_sonya_p2_baraka_hk_spacing90')
exec(compile(source,__file__+'::spacing90','exec'))
