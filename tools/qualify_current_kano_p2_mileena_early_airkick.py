"""Unchanged native chronology/identity and actual owned airkick evidence gates."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_mileena_air_release.py').read_text()
source=source.replace('audit_current_kano_p2_mileena_air_release','audit_current_kano_p2_mileena_early_airkick')
exec(compile(source,__file__+'::native_early_air_gate','exec'))
