"""Actual throw entry and exact pre-60k physical-control/native-event prefix."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_baraka_hk_guard_ready.py').read_text().replace('audit_current_sonya_p2_baraka_hk_guard_ready','audit_current_sonya_p2_baraka_hk_throw_onset')
exec(compile(source,__file__+'::native_context','exec'))
import collections
onsets=rows.get('BARAKA_THROW_START',[]);assert onsets
assert all(r['pc']=='FF8B6FA0' and r['a8']==r['cpu_actor'] and r['a13']==r['cpu_main'] and int(r['at'],16)==int(r['cpu_main'],16)+0x1f0 and r['human_actor']!=r['cpu_actor'] and r['human_main']!=r['cpu_main'] for r in onsets)
reference=chronology.load(sync.ROOT/'audit_current_sonya_p2_baraka_hk_guard_ready_runtime/run.log')
limit=min(report['lastLoggedField'],60000)
for tag in set(rows)|set(reference):
    if tag not in ('BARAKA_THROW_START','HOST_BOUND','RESULT','INPUT_DIGEST_FINAL'):
        assert [r for r in rows.get(tag,[]) if int(r['frame'])<limit]==[r for r in reference.get(tag,[]) if int(r['frame'])<limit],tag
detail=dict(passedFiniteOnsetChecks=True,unchangedPhysicalDigestsAndNativeEventsThrough=limit-1,actualThrowStarts=len(onsets),catchGaps=sorted({int(r['gap']) for r in onsets}),humanActions=dict(collections.Counter(r['action'] for r in onsets)),hardwareWords=dict(collections.Counter(r['hardware'] for r in onsets)),kickAges=dict(collections.Counter(r['kick_age'] for r in onsets)),ringAges=dict(collections.Counter(r['ring_age'] for r in onsets)),fullPortAccepted=False)
(out/'baraka-throw-onset.json').write_text(json.dumps(detail,indent=2)+'\n');print(json.dumps(detail))
