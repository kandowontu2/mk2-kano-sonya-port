"""Record main-agent inspection of exact native full-render contact sheets."""
import json
from pathlib import Path
import verify_stock_secondary_display_v1234 as proof
ROOT=proof.ROOT;OUT=ROOT/'audit_v1239_secondary_native_visual_review';assert not OUT.exists()
inventory_path=ROOT/'audit_v1237_secondary_native_contacts/inventory.json';inventory=json.loads(inventory_path.read_text())
assert inventory['sceneCount']==72 and inventory['actualImagesAltered'] is False
pins={str(inventory_path):proof.util.digest(inventory_path)};cases=[];unique=set()
for record in inventory['cases']:
 sheet=Path(record['sheet']);assert proof.util.digest(sheet)==record['sha256'];pins[str(sheet)]=record['sha256']
 for scene in record['scenes']:
  path=Path(scene['path']);assert proof.util.digest(path)==scene['sha256'];pins[str(path)]=scene['sha256'];unique.add(str(path))
 report_path=Path(record['renderReport']);assert proof.util.digest(report_path)==record['renderReportSHA256']
 report=json.loads(report_path.read_text());assert report['passed'] and report['currentSecondarySampledFullNativeRenderAccepted'];pins[str(report_path)]=record['renderReportSHA256']
 cases.append(dict(case=record['case'],reviewer='main_agent_actual_view_image',sceneEntriesReviewed=12,
  findings=['Headed body remains the selected true character, not knife/ring art.',
   'Original spear/sever animation shows native-owned upper torso and lower stump in both physical slots.',
   'Native name rendering and blood/body appearance remain present; continue screen clears all fighter/effect art.',
   'Some nearest-field contact entries repeat. This manual review is bounded, not all-fields/arenas/audio or floor-shadow acceptance.']))
report=dict(passed=True,candidate=proof.physical.headed.CANDIDATE,manualReviewComplete=True,sceneEntriesReviewed=72,
 uniqueActualImagesReviewed=len(unique),cases=cases,inputHashes=pins,secondaryNormalDeadPoolAppearanceAccepted=True,
 allFatalityArtAccepted=False,allFloorShadowsAccepted=False,audioAccepted=False,allArenasAccepted=False,fullPortAccepted=False)
OUT.mkdir();(OUT/'review.json').write_text(json.dumps(report,indent=2)+'\n')
print('Six full-native contact sheets manually reviewed; unique images',len(unique),flush=True)
