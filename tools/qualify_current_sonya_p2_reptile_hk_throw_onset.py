"""Actual throw-initiation ownership/PC and preserved controller prefix."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_reptile_hk_ring.py').read_text().replace('audit_current_sonya_p2_reptile_hk_ring','audit_current_sonya_p2_reptile_hk_throw_onset')
exec(compile(source,__file__+'::native_context','exec'))
import collections
onsets=rows.get('REPTILE_THROW_START',[]);assert onsets
assert all(r['pc']=='FF8B6FA0' and r['a8']==r['cpu_actor'] and r['a13']==r['cpu_main'] and int(r['at'],16)==int(r['cpu_main'],16)+0x1f0 and r['human_actor']!=r['cpu_actor'] and r['human_main']!=r['cpu_main'] for r in onsets)
detail=dict(passedFiniteOnsetChecks=True,actualThrowStarts=len(onsets),catchGaps=sorted({int(r['gap']) for r in onsets}),humanActions=dict(collections.Counter(r['action'] for r in onsets)),hardwareWords=dict(collections.Counter(r['hardware'] for r in onsets)),kickAges=dict(collections.Counter(r['kick_age'] for r in onsets)),ringAges=dict(collections.Counter(r['ring_age'] for r in onsets)),fullPortAccepted=False)
(out/'throw-onset.json').write_text(json.dumps(detail,indent=2)+'\n');print(json.dumps(detail))
