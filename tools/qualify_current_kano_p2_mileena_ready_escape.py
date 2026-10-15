"""Same native chronology, owned special and air-state proof gates."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_mileena_knife_escape.py').read_text()
source=source.replace('audit_current_kano_p2_mileena_knife_escape','audit_current_kano_p2_mileena_ready_escape')
exec(compile(source,__file__+'::native_ready_escape_gate','exec'))
