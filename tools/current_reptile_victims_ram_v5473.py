"""Preserve5470 preflight; keep canonical helper binding across whole-source exec."""
import json
from pathlib import Path
import current_reptile_victims_ram_v5467 as canonical5467

failed=canonical5467.ROOT/'audit_v5472_current_reptile_victims_progress/progress.json'
status=json.loads(failed.read_text())
canonical5467.need(not status['passed']and status['error']=="AttributeError(\"module 'verify_native_death_grounding_v990' has no attribute 'independent_art'\")"and
                  not status['completedCases'],'Exact preserved module-binding preflight failure; no actual native runs')
base=Path(__file__).with_name('current_reptile_victims_ram_v5470.py')
source=base.read_text()
before='import current_reptile_victims_ram_v5467 as original'
canonical5467.need(source.count(before)==1,'One canonical helper import binding')
source=source.replace(before,'import current_reptile_victims_ram_v5467 as canonical5467')
canonical5467.need(source.count('original.')==7,'Every canonical helper reference, no native-controller adaptation')
source=source.replace('original.','canonical5467.')
changes={
 'audit_v5471_current_reptile_victims_ram':'audit_v5474_current_reptile_victims_ram',
 'audit_v5472_current_reptile_victims_progress':'audit_v5475_current_reptile_victims_progress',
 'ROOT/\'mk2ks_current_reptile_ram_v5467.lua\')':
 "ROOT/'mk2ks_current_reptile_ram_v5467.lua',ROOT/'tools/current_reptile_victims_ram_v5470.py',ROOT/'audit_v5472_current_reptile_victims_progress/progress.json')",
}
for before,after in changes.items():
    canonical5467.need(source.count(before)==1,'Exact fresh canonical-binding adaptation: '+before)
    source=source.replace(before,after)
exec(compile(source,__file__+'.whole5470_preserved_canonical5467_helper_binding','exec'),globals())
