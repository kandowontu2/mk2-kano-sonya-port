"""Native campaign proof; historical input provenance is not gameplay transfer."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_kunglao_grounded_ring.py').read_text().replace('audit_current_sonya_p2_kunglao_grounded_ring','audit_current_sonya_p2_kunglao_historical_zoning')
exec(compile(source,__file__+'::native_context','exec'))
provenance=json.loads((sync.ROOT/'audit_current_sonya_p2_kunglao_historical_zoning_preparation/policy-provenance.json').read_text())
assert provenance['oldControllerSHA256']==sync.sha(provenance['oldController'])
(out/'historical-inputs.json').write_text(json.dumps(dict(passed=True,physicalPolicyProvenance=provenance,currentBuildActuallyTested=True,kungLaoMatchCleared=4 in stages,fullCampaignAccepted=False,fullPortAccepted=False),indent=2)+'\n')
