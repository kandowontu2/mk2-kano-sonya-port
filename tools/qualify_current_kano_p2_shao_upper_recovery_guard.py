"""Preserve native prefix and actual HP; keep console output compact."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_shao_crouch_upper_contact.py').read_text().replace('audit_current_kano_p2_shao_crouch_upper_contact','audit_current_kano_p2_shao_upper_recovery_guard')
namespace=dict(__file__=__file__,print=lambda *args,**kwargs:None)
exec(compile(source,__file__+'::upper_guard_trial','exec'),namespace)
detail=namespace['detail'];out=namespace['out'];rows=namespace['rows']
print(dict(shaoObserved=detail['shaoObserved'],actualUpperEntries=len(detail['actualOwnedUpperStateEntries']),outgoingHP=detail['outgoingHP'],incomingHP=detail['incomingHP'],ownedShaoRounds=[r for r in rows['WIN'] if r['stage']=='16' and r['slot']=='2'],fullPortAccepted=False))
