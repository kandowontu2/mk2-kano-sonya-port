"""Same native chronology, true identity, owned upper/throw gate."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_mileena_crouch_upper.py').read_text()
source=source.replace('audit_current_kano_p2_mileena_crouch_upper','audit_current_kano_p2_mileena_crouch_spacing')
exec(compile(source,__file__+'::native_spacing_gate','exec'))
