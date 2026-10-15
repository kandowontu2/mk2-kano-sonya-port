"""Explicit retained prefix and actual owned native upper/HP scope."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_shao_held_escape.py').read_text().replace('audit_current_kano_p2_shao_held_escape','audit_current_kano_p2_shao_crouch_upper_contact')
exec(compile(source,__file__+'::upper_contact_trial','exec'))
entries=[r for r in rows.get('BOSS_ACTION',[]) if r['stage']=='16' and r['after']=='263']
assert all(r['id']==r['roster']=='17' and r['actor']==r['owner'] for r in entries)
damage=rows.get('SHAO_UPPER_DAMAGE',[])
detail=dict(shaoObserved=any(r['stage']=='16' for r in rows['STAGE']),actualOwnedUpperStateEntries=entries,actualNativeDamage=damage,outgoingHP=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='1'),incomingHP=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='2'),fullPortAccepted=False)
(out/'upper-contact.json').write_text(json.dumps(detail,indent=2)+'\n');print(json.dumps(detail))
