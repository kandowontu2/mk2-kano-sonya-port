"""Same native ID/chronology gate; exact prior route until first earned round."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_baraka_choke_route.py').read_text()
source=source.replace('audit_current_kano_p2_baraka_choke_route','audit_current_kano_p2_baraka_mixed_route')
source=source.replace('audit_current_kano_p2_campaign_slim_health_runtime','audit_current_kano_p2_baraka_choke_route_runtime')
source=source.replace("<21977","<22766").replace('priorPrefixUnchangedThrough=21976','priorPrefixUnchangedThrough=22765')
exec(compile(source,__file__+'::native_mixed_route_gate','exec'))
