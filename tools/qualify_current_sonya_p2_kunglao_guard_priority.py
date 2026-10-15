"""Earned opening preservation, real native pairs and actual damage."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_kunglao_hk_retreat.py').read_text().replace('audit_current_sonya_p2_kunglao_hk_retreat','audit_current_sonya_p2_kunglao_guard_priority')
exec(compile(source,__file__+'::native_context','exec'))
damage=rows['SONYA_KUNGLAO_DAMAGE'];assert damage
assert all(r['ids']=='0,18' and int(r['after'])<int(r['before'])<=161 and r['human_actor']!=r['cpu_actor'] and r['human_main']!=r['cpu_main'] and r['at']==('010602F0' if r['victim_slot']=='1' else '01060EC0') for r in damage)
import collections
incoming=collections.Counter()
for r in damage:
    if r['victim_slot']=='2':incoming[(r['cpu_action'],r['human_action'])]+=int(r['before'])-int(r['after'])
detail=dict(passed=True,outgoingDamage=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='1'),incomingDamage=sum(incoming.values()),
    incomingActionPairs=[dict(cpuAction=k[0],humanAction=k[1],damage=v) for k,v in incoming.most_common()],
    fullCampaignAccepted=False,fullPortAccepted=False)
(out/'guard-contact.json').write_text(json.dumps(detail,indent=2)+'\n');print(json.dumps(detail))
