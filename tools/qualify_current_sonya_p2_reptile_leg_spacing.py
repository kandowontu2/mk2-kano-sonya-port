"""Native Reptile-context entries and round observations, not full acceptance."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_liukang_leg_spacing.py').read_text().replace('audit_current_sonya_p2_liukang_leg_spacing','audit_current_sonya_p2_reptile_leg_spacing')
exec(compile(source,__file__+'::native_context','exec'))
entries=[r for r in rows.get('SPECIAL',[]) if r['stage']=='5' and r['move']=='leg']
assert all(r['id']=='18' and r['roster']=='18' and r['a8']==r['actor'] and r['a13']==r['main'] for r in entries)
wins=[r for r in rows.get('WIN',[]) if r['stage']=='5' and r['slot']=='2']
assert all(r['id']=='18' and r['entry']=='FFFEFA40' and r['pc']=='FF8296B0' for r in wins)
(out/'reptile-policy.json').write_text(json.dumps(dict(passedFiniteChecks=True,nativeOwnedLegEntries=len(entries),ownReptileRounds=wins,nextStageObserved=6 in stages,strictSameAttemptAdvanceRequired=6 in stages,fullCampaignAccepted=False,fullPortAccepted=False),indent=2)+'\n')
print('Reptile native leg entries: '+str(len(entries))+'; own rounds: '+str(len(wins)))
