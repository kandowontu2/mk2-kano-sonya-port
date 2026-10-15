"""Actual native outgoing damage by action, without strategy rate claims."""
import json
from collections import Counter
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify()
root=sync.ROOT;log=root/'audit_current_sonya_p2_baraka_hk_spacing90_runtime/run.log'
out=root/'audit_current_sonya_baraka_spacing90_damage_checked';assert not out.exists()
rows=load(log);damage=rows['SONYA_BARAKA_DAMAGE'];outgoing=[r for r in damage if r['victim_slot']=='1']
assert outgoing and all(r['pc']=='FF836700' and r['ids']=='3,18' for r in outgoing)
values=Counter((r['human_action'],int(r['before'])-int(r['after'])) for r in outgoing)
report=dict(outgoingNativeDamageValues=[dict(humanAction=a,damage=d,events=n) for(a,d),n in values.items()],
    outgoingHP=sum(int(r['before'])-int(r['after']) for r in outgoing),
    logSHA256=sync.sha(log),fullPortAccepted=False,
    caveat='Action at HP callback is not necessarily the complete damage-source identity; projectile creator context remains required. No normalized strategy comparison.')
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
