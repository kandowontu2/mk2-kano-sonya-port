"""Original campaign gate with event-relative controller and actual outcomes."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_scorpion_jump.py').read_text()
source=source.replace('audit_current_kano_p2_scorpion_jump','audit_current_kano_p2_scorpion_event_jump')
exec(compile(source,__file__+'::native_campaign_gate','exec'))
