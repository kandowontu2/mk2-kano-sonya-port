"""Record actual main-agent review; this is not full-port acceptance."""
import json
from pathlib import Path
import verify_native_hat_kill_v1158 as proof
ROOT=proof.ROOT
OUT=ROOT/'audit_v1162_native_hat_visual_review'
assert not OUT.exists(), 'Preserve prior evidence'
inventory_path=ROOT/'audit_v1161_native_hat_actual_contacts/inventory.json'
inventory=json.loads(inventory_path.read_text())
assert inventory['sceneCount']==128 and len(inventory['contacts'])==6
assert not inventory['actualScenePixelsChanged']
for filename,wanted in inventory['inputHashes'].items():
 assert proof.digest(Path(filename))==wanted, filename
report=json.loads((ROOT/'audit_v1158_native_hat_kill_checked/report.json').read_text())
assert report['passed'] and len(report['cases'])==6
record=dict(candidate=proof.split.CANDIDATE,sceneCount=128,
 contacts=inventory['contacts'],manualVisualReviewComplete=True,
 reviewedBy='Main agent viewed all four owned-character sheets and both original-control sheets using view_image',
 scope='50 source-bound own body/head samples and 78 selected normal Dead Pool timeline scenes; not every timeline field',
 findings=[
 'Physical steered hat reaches the neck and the native decapitation branch in both slots.',
 'Own Kano and Sonya headless costumes, limbs, boots and separate rotating/rolling heads remain identifiable; no Liu/Kitana body proxy.',
 'All seven own collapse poses progress through kneeling/falling to the floor under native timing.',
 'Original Kitana and Liu controls show the corresponding native hat, blood, body collapse and head roll.',
 'Actual native win, double-flawless, fatality and continue scenes appear; selection portraits are absent in these match captures.',
 'Native foreground blood, hat occlusion and viewport clipping remain; unseen or clipped pixels are not accepted.',
 'Sampled body grounding is consistent; all floor shadows, other arenas and natural alternate fatalities remain separate gates.',
 ],observedNativeHatVisualReviewPassed=True,alternateCostumesAccepted=False,
 allFloorShadowsAccepted=False,allArenasAccepted=False,fullPortAccepted=False,
 inputHashes={**inventory['inputHashes'],str(inventory_path):proof.digest(inventory_path)})
OUT.mkdir();(OUT/'review.json').write_text(json.dumps(record,indent=2)+'\n')
print('Reviewed 6 sheets / 128 actual scenes; bounded normal hat gate only')
