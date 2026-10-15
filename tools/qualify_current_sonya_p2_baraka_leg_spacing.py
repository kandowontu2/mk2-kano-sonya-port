"""Actual leg ownership, real damage and native campaign observations."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_baraka_hk_ring.py').read_text().replace('audit_current_sonya_p2_baraka_hk_ring','audit_current_sonya_p2_baraka_leg_spacing')
exec(compile(source,__file__+'::native_context','exec'))
entries=[r for r in rows.get('SPECIAL',[]) if r['stage']=='6' and r['move']=='leg']
assert all(r['id']=='18' and r['roster']=='18' and r['a8']==r['actor'] and r['a13']==r['main'] for r in entries)
(out/'leg-entries.json').write_text(json.dumps(dict(passed=True,nativeOwnedLegEntries=len(entries),fullPortAccepted=False),indent=2)+'\n')
print('Native Baraka-context owned leg entries: '+str(len(entries)))
