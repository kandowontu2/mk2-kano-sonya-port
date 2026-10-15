"""Record the main agent's actual visual review; no scene editing."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'audit_v1140_split_blood_actual_visual_review'
if OUT.exists():raise ValueError('Never replace reviewed evidence')
inventory_path=ROOT/'audit_v1137_actual_split_blood_pixels/report.json'
inventory=json.loads(inventory_path.read_text())
assert inventory['passed'] and inventory['sceneCount']==136 and len(inventory['contacts'])==8
for filename,wanted in inventory['inputHashes'].items():
 assert hashlib.sha256(Path(filename).read_bytes()).hexdigest().upper()==wanted,filename
record=dict(candidate='diagnostic_v1130_owned_split_invariant_blood',
 scope='136 actual normal and explicitly controlled alternate split scenes, Dead Pool only',
 reviewedBy='main agent: all eight unaltered 1:1 actual-scene contacts viewed in prior continuation; two alternate contacts rechecked in this continuation',
 sceneCount=136,contacts=inventory['contacts'],manualVisualReviewComplete=True,
 findings=[
  'Each true character retains its own costume, hair, attached arms and lower-body silhouette in the initial poses.',
  'Kano longitudinal cut blood stays red with both red normal trim and blue alternate trim.',
  'Sonya alternate blue costume retains native Sonya hair, boots and own half stream; her art was not changed by the Kano blood encoding.',
  'Both actors follow the original upright-to-outward fall sequence and opposing X mirror.',
  'Original native hat, blood spray and performer occlusion remain; no unseen cut pixels are asserted visible.',
  'Outward halves clip at the original viewport edge in some poses; these are not complete unclipped-body evidence.',
  'Separate native DMA/raster proofs cover the measured floor anchors; this does not establish all floor-shadow poses or arenas.',
 ],observedNormalAndControlledAlternateVisualReviewPassed=True,
 naturalAlternateSelectionAccepted=False,allStockFatalitiesAccepted=False,allArenasAccepted=False,fullPortAccepted=False,
 inputHashes={**inventory['inputHashes'],str(inventory_path):hashlib.sha256(inventory_path.read_bytes()).hexdigest().upper()})
OUT.mkdir();(OUT/'review.json').write_text(json.dumps(record,indent=2)+'\n')
print('Saved reviewed 136 actual split scenes; normal and explicitly controlled alternate only')
