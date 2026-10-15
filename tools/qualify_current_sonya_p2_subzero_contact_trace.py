"""Observer neutrality, native direct HK contacts and actual projectile links."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_subzero_hk_ring.py').read_text()
source=source.replace('audit_current_sonya_p2_subzero_hk_ring','audit_current_sonya_p2_subzero_contact_trace')
exec(compile(source,__file__+'::native_sonya_context_gate','exec'))
import collections
old=chronology.load(sync.ROOT/'audit_current_sonya_p2_subzero_hk_ring_runtime/run.log')
last=lambda data:max(int(r['frame']) for group in data.values() for r in group)
cutoff=min(last(rows),last(old))
for tag in set(rows)|set(old):
    if tag not in ('SONYA_SUBZERO_DAMAGE','HOST_BOUND','RESULT','INPUT_DIGEST_FINAL'):
        assert [r for r in rows.get(tag,[]) if int(r['frame'])<cutoff]==[r for r in old.get(tag,[]) if int(r['frame'])<cutoff],tag
damage=rows.get('SONYA_SUBZERO_DAMAGE',[]);assert damage
assert all(r['ids']=='8,18' and int(r['after'])<int(r['before'])<=161 and r['human_actor']!=r['cpu_actor'] and r['human_main']!=r['cpu_main'] for r in damage)
assert all(r['at']==('010602F0' if r['victim_slot']=='1' else '01060EC0') for r in damage)
kicks=[r for r in damage if r['victim_slot']=='1' and r['human_action']=='259' and r['a8']==r['human_actor'] and r['a13']==r['human_main']]
projectiles=[r for r in damage if r['victim_slot']=='1' and r['creator']==r['human_actor'] and r['a8']!=r['human_actor'] and r['a13']!=r['human_main']]
groups=collections.Counter()
for r in damage:
    if r['victim_slot']=='2':groups[(r['cpu_action'],r['human_action'])]+=int(r['before'])-int(r['after'])
detail=dict(passed=True,completeGameplayPrefixIdenticalBefore=cutoff,
    ownedDirectHKContacts=len(kicks),ownedDirectHKDamage=sum(int(r['before'])-int(r['after']) for r in kicks),
    hkContactGaps=[int(r['gap']) for r in kicks],linkedProjectileContacts=len(projectiles),
    linkedProjectileDamage=sum(int(r['before'])-int(r['after']) for r in projectiles),
    incomingActionPairs=[dict(cpuAction=k[0],humanAction=k[1],damage=v) for k,v in groups.most_common()],
    fullCampaignAccepted=False,fullPortAccepted=False)
(out/'native-contact.json').write_text(json.dumps(detail,indent=2)+'\n');print(json.dumps(detail))
