"""Same direct native campaign and owned-air-hit gate on new physical recovery."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_scorpion_close_air_scoped.py').read_text()
source=source.replace('audit_current_kano_p2_scorpion_close_air','audit_current_kano_p2_scorpion_release_air')
exec(compile(source,__file__+'::same_native_ownership_gate','exec'))
