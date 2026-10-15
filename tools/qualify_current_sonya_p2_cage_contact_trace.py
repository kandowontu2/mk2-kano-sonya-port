"""Native contacts and exact gameplay neutrality; not full campaign proof."""
from pathlib import Path
import collections
source=Path(__file__).with_name('qualify_current_sonya_p2_subzero_hk_ring.py').read_text().replace('audit_current_sonya_p2_subzero_hk_ring','audit_current_sonya_p2_cage_contact_trace')
exec(compile(source,__file__+'::native_context','exec'))
reference=chronology.load(sync.ROOT/'audit_current_sonya_p2_cage_hk_retreat_runtime/run.log')
last=lambda data:max(int(r['frame']) for group in data.values() for r in group)
cutoff=min(last(rows),last(reference))
for tag in set(rows)|set(reference):
    if tag not in ('SONYA_CAGE_DAMAGE','RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):
        assert [r for r in rows.get(tag,[]) if int(r['frame'])<cutoff]==[r for r in reference.get(tag,[]) if int(r['frame'])<cutoff],tag
damage=rows['SONYA_CAGE_DAMAGE'];assert damage
def valid(r):
    return r['ids']=='2,18' and int(r['after'])<int(r['before'])<=161 and r['human_actor']!=r['cpu_actor'] and r['human_main']!=r['cpu_main'] and r['at']==('010602F0' if r['victim_slot']=='1' else '01060EC0')
assert all(valid(r) for r in damage)
for key in ('ids','at'):
    broken=dict(damage[0]);broken[key]='invalid';assert not valid(broken)
kicks=[r for r in damage if r['victim_slot']=='1' and r['human_action']=='259' and r['a8']==r['human_actor'] and r['a13']==r['human_main']]
incoming=collections.Counter()
for r in damage:
    if r['victim_slot']=='2':incoming[(r['cpu_action'],r['human_action'])]+=int(r['before'])-int(r['after'])
detail=dict(passed=True,allPriorRecordsIdenticalBefore=cutoff,ownedDirectHKContacts=len(kicks),ownedDirectHKDamage=sum(int(r['before'])-int(r['after']) for r in kicks),
    outgoingDamage=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='1'),
    incomingDamage=sum(incoming.values()),incomingActionPairs=[dict(cpuAction=k[0],humanAction=k[1],damage=v) for k,v in incoming.most_common()],
    observerFaultsRejected=2,fullCampaignAccepted=False,fullPortAccepted=False)
(out/'cage-contact.json').write_text(json.dumps(detail,indent=2)+'\n');print(json.dumps(detail))
