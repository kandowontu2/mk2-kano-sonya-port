"""Exact prefix before Cage, native contacts and paid-attempt evidence."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_cage_contact_trace.py').read_text().replace('audit_current_sonya_p2_cage_contact_trace','audit_current_sonya_p2_cage_early_retreat')
source=source.replace('cutoff=min(last(rows),last(reference))','cutoff=17315')
exec(compile(source,__file__+'::native_contacts','exec'))
detail=dict(passed=True,earnedStages=stages,
    ownCageWins=[r for r in rows['WIN'] if r['stage']=='2' and r['slot']=='2'],
    cagePaidLosses=[r for r in rows.get('LOSS',[]) if r['stage']=='2'],
    cageMatchCleared=3 in stages,fullCampaignAccepted=False,fullPortAccepted=False)
(out/'cage-progress.json').write_text(json.dumps(detail,indent=2)+'\n');print(json.dumps(detail))
