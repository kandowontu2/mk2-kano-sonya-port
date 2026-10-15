"""Same true native chronology and actual owned uppercut damage gate."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_scorpion_upper.py').read_text()
source=source.replace('audit_current_kano_p2_scorpion_upper','audit_current_kano_p2_scorpion_crouch_ready')
exec(compile(source,__file__+'::same_native_upper_gate','exec'))
