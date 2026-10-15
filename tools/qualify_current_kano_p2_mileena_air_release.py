"""Same actual native chronology, identity, contacts and air-state gates."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_mileena_air_counter.py').read_text()
source=source.replace('audit_current_kano_p2_mileena_air_counter','audit_current_kano_p2_mileena_air_release')
exec(compile(source,__file__+'::same_native_air_gate','exec'))
