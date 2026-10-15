"""Preserve failed A8-victim assumption; HP slot identifies victim, not A8."""
from pathlib import Path
source=Path(__file__).with_name('audit_current_kano_p2_kintaro_round_contact.py').read_text()
source=source.replace('audit_current_kano_p2_kintaro_round_contact_checked','audit_current_kano_p2_kintaro_round_contact_v2_checked')
source=source.replace("assert all(r['a8']==r['cpuActor'] for r in outgoing)","# A8 is execution context, not assumed HP victim actor. Native HP slot1 is P1 Kintaro.\nassert all(r['cpuActor']==proof['proof']['kintaroFreshAttempt']['actors'].split(',')[1] for r in outgoing)")
source=source.replace('passedFiniteContactChecks=True,','passedFiniteContactChecks=True,a8VictimAssumptionRejected=True,')
exec(compile(source,__file__+'::corrected_register_scope','exec'))
