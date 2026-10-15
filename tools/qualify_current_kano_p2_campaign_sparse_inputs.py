"""Preserve actual gameplay record prefix; INPUT sink omission is not controller change."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_kitana_counter.py').read_text()
source=source.replace('audit_current_kano_p2_kitana_counter','audit_current_kano_p2_campaign_sparse_inputs')
source=source.replace('audit_current_kano_p2_early_knife_campaign_40000_runtime','audit_current_kano_p2_kitana_campaign_43000_runtime')
source=source.replace("('RESULT','HOST_BOUND')","('RESULT','HOST_BOUND','INPUT')")
source=source.replace("int(r['frame'])<34953","int(r['frame'])<43000")
source=source.replace('priorPrefixUnchangedThrough=34952','priorGameplayPrefixUnchangedThrough=42999')
source=source.replace("=='40000'","=='60000'").replace('completed40000','completed60000')
exec(compile(source,__file__+'::same_native_campaign_gate','exec'))
assert [r for r in rows.get('INPUT',[]) if int(r['frame'])<1690]==[r for r in old.get('INPUT',[]) if int(r['frame'])<1690]
assert not any(int(r['frame'])>=1690 for r in rows.get('INPUT',[]))
