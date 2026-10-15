"""Exact earned-opening prefix and genuine Cage campaign observations."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_subzero_close_retreat.py').read_text()
source=source.replace('audit_current_sonya_p2_subzero_close_retreat','audit_current_sonya_p2_cage_hk_retreat')
exec(compile(source,__file__+'::native_context','exec'))
reference=chronology.load(sync.ROOT/'audit_current_sonya_p2_subzero_close_retreat_runtime/run.log')
for tag in set(rows)|set(reference):
    if tag not in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):
        assert [r for r in rows.get(tag,[]) if int(r['frame'])<17315]==[r for r in reference.get(tag,[]) if int(r['frame'])<17315],tag
fields=[r for r in rows['LIVE'] if r['stage']=='2'];assert fields
assert all(r['human']=='18:18' and r['cpu']=='2:2' and r['human_actor']!=r['cpu_actor'] and r['human_main']!=r['cpu_main'] for r in fields)
detail=dict(passed=True,earlierRecordsIdenticalThrough=17314,earnedStages=stages,
    nativeCagePairFields=len(fields),
    ownCageWins=[r for r in rows['WIN'] if r['stage']=='2' and r['slot']=='2'],
    cagePaidLosses=[r for r in rows.get('LOSS',[]) if r['stage']=='2'],
    cageMatchCleared=3 in stages,fullCampaignAccepted=False,fullPortAccepted=False)
(out/'cage-progress.json').write_text(json.dumps(detail,indent=2)+'\n');print(json.dumps(detail))
