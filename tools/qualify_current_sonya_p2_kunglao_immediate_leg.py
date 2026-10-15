"""Native pairs, earned chronology, damage and actual owned leg entries."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_kunglao_guard_priority.py').read_text().replace('audit_current_sonya_p2_kunglao_guard_priority','audit_current_sonya_p2_kunglao_immediate_leg')
exec(compile(source,__file__+'::native_context','exec'))
entries=[r for r in rows.get('SPECIAL',[]) if r['stage']=='3' and r['move']=='leg']
assert all(r['id']=='18' and r['roster']=='18' and r['a8']==r['actor'] and r['a13']==r['main'] for r in entries)
(out/'leg-policy.json').write_text(json.dumps(dict(passed=True,nativeOwnedLegEntries=len(entries),kungLaoMatchCleared=4 in stages,strictSameAttemptAdvanceRequired=4 in stages,fullCampaignAccepted=False,fullPortAccepted=False),indent=2)+'\n')
print('Native owned leg entries: '+str(len(entries)))
