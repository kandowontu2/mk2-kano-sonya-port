"""Same native campaign gate; independent native owned upper contacts."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_scorpion_close_air_scoped.py').read_text()
source=source.replace('audit_current_kano_p2_scorpion_close_air','audit_current_kano_p2_scorpion_upper')
source=source.replace("proof['ownedAirKickContacts']","proof['ownedUpperContacts']").replace("proof['ownedAirKickDamage']","proof['ownedUpperDamage']")
source=source.replace("r['actions'].split(',')[1]=='512'","r['actions'].split(',')[1]=='263'")
exec(compile(source,__file__+'::native_upper_contact_gate','exec'))
