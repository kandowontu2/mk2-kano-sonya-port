"""Rendering skip must not alter observed gameplay or controller code."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_kunglao_hk_retreat.py').read_text().replace('audit_current_sonya_p2_kunglao_hk_retreat','audit_current_sonya_p2_campaign_render_skip')
exec(compile(source,__file__+'::native_context','exec'))
baseline=sync.ROOT/'audit_current_sonya_p2_kunglao_hk_retreat_preparation/campaign.lua'
candidate=sync.ROOT/'audit_current_sonya_p2_campaign_render_skip_preparation/campaign.lua'
assert candidate.read_text().replace("if frame>=60000 then log('HOST_BOUND','maximum_fields=60000 full_campaign_acceptance=false')","if frame>=40000 then log('HOST_BOUND','maximum_fields=40000 full_campaign_acceptance=false')")==baseline.read_text()
reference=chronology.load(sync.ROOT/'audit_current_sonya_p2_kunglao_hk_retreat_runtime/run.log')
cutoff=min(max(int(r['frame']) for group in rows.values() for r in group),40000)
for tag in set(rows)|set(reference):
    if tag not in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):
        assert [r for r in rows.get(tag,[]) if int(r['frame'])<cutoff]==[r for r in reference.get(tag,[]) if int(r['frame'])<cutoff],tag
(out/'render-neutrality.json').write_text(json.dumps(dict(passed=True,controllerUnchanged=True,completeGameplayPrefixIdenticalBefore=cutoff,visualAcceptance=False,fullCampaignAccepted=False,fullPortAccepted=False),indent=2)+'\n')
print('Render/control neutrality passed before field '+str(cutoff))
