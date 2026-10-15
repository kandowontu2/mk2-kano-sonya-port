"""Retained pre-Kung route and actual later owned native evidence."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_cage_owned_choke.py').read_text().replace('audit_current_kano_p2_cage_owned_choke','audit_current_kano_p2_early_owned_choke')
source=source.replace("prior=root/'audit_current_kano_p2_changed_health_only_runtime'","prior=root/'audit_current_kano_p2_cage_owned_choke_runtime'").replace('8509','14045')
exec(compile(source,__file__+'::early_choke_extension','exec'))
