"""Native campaign chronology and contacts; controller change is not game fix."""
from pathlib import Path
import collections
source=Path(__file__).with_name('qualify_current_sonya_p2_subzero_hk_ring.py').read_text()
source=source.replace('audit_current_sonya_p2_subzero_hk_ring','audit_current_sonya_p2_subzero_close_retreat')
exec(compile(source,__file__+'::native_context','exec'))
damage=rows.get('SONYA_SUBZERO_DAMAGE',[])
assert damage and all(r['ids']=='8,18' and int(r['after'])<int(r['before'])<=161 for r in damage)
assert all(r['at']==('010602F0' if r['victim_slot']=='1' else '01060EC0') for r in damage)
starts=rows.get('SUBZERO_THROW_START',[])
assert all(r['a8']==r['cpu_actor'] and r['a13']==r['cpu_main'] and int(r['at'],16)==int(r['cpu_main'],16)+0x1f0 and r['pc']=='FF8B6FA0' for r in starts)
detail=dict(passed=True,throwStarts=len(starts),
    outgoingDamage=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='1'),
    incomingDamage=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='2'),
    ownedDirectHKContacts=sum(r['victim_slot']=='1' and r['human_action']=='259' and r['a8']==r['human_actor'] and r['a13']==r['human_main'] for r in damage),
    subzeroMatchCleared=2 in stages,fullCampaignAccepted=False,fullPortAccepted=False)
(out/'contact-summary.json').write_text(json.dumps(detail,indent=2)+'\n');print(json.dumps(detail))
