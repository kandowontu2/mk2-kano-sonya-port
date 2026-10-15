"""Same true-ID/earned-opening/native-damage gate for standing HK response."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_subzero_crouch_counter.py').read_text()
source=source.replace('audit_current_kano_p2_subzero_crouch_counter','audit_current_kano_p2_subzero_standing')
source=source.replace("'KANO_P2_SUBZERO_COUNTER'","'KANO_P2_SUBZERO_STANDING'")
source=source.replace("== '263'","== '259'").replace('ownUppercutContacts','ownStandingKickContacts')
exec(compile(source,__file__+'::same_earned_native_gate','exec'))
