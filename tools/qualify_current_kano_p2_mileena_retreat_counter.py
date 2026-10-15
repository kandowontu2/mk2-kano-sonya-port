"""Same true native campaign/owned HK gate, separate guarded range response."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_mileena_approach.py').read_text()
source=source.replace('audit_current_kano_p2_mileena_approach','audit_current_kano_p2_mileena_retreat_counter')
exec(compile(source,__file__+'::same_native_HK_gate','exec'))
