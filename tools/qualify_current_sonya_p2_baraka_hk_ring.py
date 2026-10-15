"""Native unchanged opening/true actor identity/Baraka damage and round results."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_reptile_hk_early_retreat.py').read_text().replace('audit_current_sonya_p2_reptile_hk_early_retreat','audit_current_sonya_p2_baraka_hk_ring')
exec(compile(source,__file__+'::native_context','exec'))
import collections
damage=rows.get('SONYA_BARAKA_DAMAGE',[]);assert damage
assert all(r['ids']=='3,18' and int(r['after'])<int(r['before'])<=161 and r['human_actor']!=r['cpu_actor'] and r['human_main']!=r['cpu_main'] and r['at']==('010602F0' if r['victim_slot']=='1' else '01060EC0') for r in damage)
incoming=collections.Counter();outgoing=collections.Counter()
for r in damage:(incoming if r['victim_slot']=='2' else outgoing)[(r['cpu_action'],r['human_action'])]+=int(r['before'])-int(r['after'])
detail=dict(passedFiniteDamageChecks=True,incomingHP=sum(incoming.values()),outgoingHP=sum(outgoing.values()),incomingActionPairs=[dict(cpuAction=k[0],humanAction=k[1],damage=v) for k,v in incoming.most_common()],outgoingActionPairs=[dict(cpuAction=k[0],humanAction=k[1],damage=v) for k,v in outgoing.most_common()],ownBarakaRounds=[r for r in rows['WIN'] if r['stage']=='6' and r['slot']=='2'],nextStageObserved=7 in stages,strictAdvanceProofRequired=7 in stages,fullPortAccepted=False)
(out/'baraka-context.json').write_text(json.dumps(detail,indent=2)+'\n');print(json.dumps(detail))
