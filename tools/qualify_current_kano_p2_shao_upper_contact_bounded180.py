"""Actual owned upper state and direct HP changes, not script intentions."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_shao_crouch_upper_contact.py').read_text().replace('audit_current_kano_p2_shao_crouch_upper_contact','audit_current_kano_p2_shao_upper_contact_bounded180')
exec(compile(source,__file__+'::bounded_contact_probe','exec'))
