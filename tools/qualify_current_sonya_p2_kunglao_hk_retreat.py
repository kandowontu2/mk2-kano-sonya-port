"""Earned early route prefix and genuine native Kung Lao campaign observations."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_subzero_hk_ring.py').read_text().replace('audit_current_sonya_p2_subzero_hk_ring','audit_current_sonya_p2_kunglao_hk_retreat')
exec(compile(source,__file__+'::native_context','exec'))
reference=chronology.load(sync.ROOT/'audit_current_sonya_p2_cage_early_retreat_runtime/run.log')
for tag in set(rows)|set(reference):
    if tag not in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):
        assert [r for r in rows.get(tag,[]) if int(r['frame'])<23056]==[r for r in reference.get(tag,[]) if int(r['frame'])<23056],tag
fields=[r for r in rows['LIVE'] if r['stage']=='3'];assert fields
assert all(r['human']=='18:18' and r['cpu']=='0:0' and r['human_actor']!=r['cpu_actor'] and r['human_main']!=r['cpu_main'] for r in fields)
detail=dict(passed=True,earlierRecordsIdenticalThrough=23055,earnedStages=stages,nativeKungLaoPairFields=len(fields),
    ownKungLaoWins=[r for r in rows['WIN'] if r['stage']=='3' and r['slot']=='2'],
    kungLaoPaidLosses=[r for r in rows.get('LOSS',[]) if r['stage']=='3'],kungLaoMatchCleared=4 in stages,fullCampaignAccepted=False,fullPortAccepted=False)
(out/'kunglao-progress.json').write_text(json.dumps(detail,indent=2)+'\n');print(json.dumps(detail))
