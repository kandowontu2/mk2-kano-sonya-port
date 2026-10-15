"""Same true native campaign gate; owned HK damage rather than intended inputs."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_mileena_ball_knife.py').read_text()
source=source.replace('audit_current_kano_p2_mileena_ball_knife','audit_current_kano_p2_mileena_standing')
source=source.replace("r['actions'].split(',')[1]=='523'","r['actions'].split(',')[1]=='259'")
source=source.replace('mileenaOwnedBallContacts','mileenaOwnedHKContacts').replace('mileenaOwnedBallDamage','mileenaOwnedHKDamage')
exec(compile(source,__file__+'::native_mileena_HK_gate','exec'))
