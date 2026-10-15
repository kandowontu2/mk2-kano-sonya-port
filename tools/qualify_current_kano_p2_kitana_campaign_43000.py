"""Same native campaign gate plus ALL prior40k records retained; cap scoped partial."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_kitana_counter.py').read_text()
source=source.replace('audit_current_kano_p2_kitana_counter','audit_current_kano_p2_kitana_campaign_43000')
source=source.replace('audit_current_kano_p2_early_knife_campaign_40000_runtime','audit_current_kano_p2_kitana_counter_runtime')
source=source.replace("int(r['frame'])<34953","int(r['frame'])<40000")
source=source.replace('priorPrefixUnchangedThrough=34952','priorPrefixUnchangedThrough=39999')
source=source.replace("=='40000'","=='43000'").replace('completed40000','completed43000')
exec(compile(source,__file__+'::same_native_campaign_gate','exec'))
