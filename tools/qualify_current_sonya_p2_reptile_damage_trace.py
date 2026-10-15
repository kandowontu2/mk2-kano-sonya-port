"""Native actor-owned actual HP loss; preserve controller event prefix."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_reptile_slim_observation.py').read_text().replace('audit_current_sonya_p2_reptile_slim_observation','audit_current_sonya_p2_reptile_damage_trace')
source=source.replace("'INPUT_DIGEST_FINAL'):","'INPUT_DIGEST_FINAL','SONYA_REPTILE_DAMAGE'):")
exec(compile(source,__file__+'::native_context','exec'))
import collections
damage=rows.get('SONYA_REPTILE_DAMAGE',[])
assert damage
assert all(r['ids']=='9,18' and int(r['after'])<int(r['before'])<=161 and r['human_actor']!=r['cpu_actor'] and r['human_main']!=r['cpu_main'] and r['at']==('010602F0' if r['victim_slot']=='1' else '01060EC0') for r in damage)
incoming=collections.Counter();outgoing=collections.Counter()
for r in damage:
    (incoming if r['victim_slot']=='2' else outgoing)[(r['cpu_action'],r['human_action'])]+=int(r['before'])-int(r['after'])
detail=dict(passedFiniteDamageChecks=True,incomingHP=sum(incoming.values()),outgoingHP=sum(outgoing.values()),incomingActionPairs=[dict(cpuAction=k[0],humanAction=k[1],damage=v) for k,v in incoming.most_common()],outgoingActionPairs=[dict(cpuAction=k[0],humanAction=k[1],damage=v) for k,v in outgoing.most_common()],numericActionsAreContextSpecific=True,fullPortAccepted=False)
(out/'damage-context.json').write_text(json.dumps(detail,indent=2)+'\n');print(json.dumps(detail))
