"""Freeze main-agent review of all six actual cold mirror contacts."""
import json
from pathlib import Path
import verify_natural_mirror_v1144 as proof
ROOT=proof.ROOT;OUT=ROOT/'audit_v1147_natural_mirror_actual_visual_review'
if OUT.exists():raise ValueError('Never replace visual review evidence')
inventory_path=ROOT/'audit_v1145_natural_mirror_actual_contacts/inventory.json'
inventory=json.loads(inventory_path.read_text())
assert inventory['sceneCount']==30 and len(inventory['contacts'])==6 and inventory['actualScenePixelsChanged'] is False
for filename,wanted in inventory['inputHashes'].items():assert proof.digest(Path(filename))==wanted
record=dict(candidate=proof.split.CANDIDATE,sceneCount=30,contacts=inventory['contacts'],
 reviewedBy='main agent via view_image original detail, all six actual-scene contact sheets, plus selected original PNGs',
 scope='Static selection and three live Dead Pool snapshots per natural mirror case; not all blink or ladder transition fields',
 findings=[
  'Kano versus Kano and Sonya versus Sonya actually render their own bodies, not Liu Kang proxies.',
  'Normal red Kano trim and green Sonya outfit are distinct from native alternate blue outfits in both confirmation orders.',
  'Both own top-row portraits and corresponding own selection poses are visible in sampled selection scenes.',
  'Overlapping native player numbers 1 and 2 are visible when both cursors occupy the same portrait, matching Liu Kang control behaviour.',
  'Actual match snapshots contain no persistent large selection portraits or selection pose overlays.',
  'Names read KANO and SONYA in both lifebars; neither changes to LIU KANG.',
  'Standing feet and ground shadows are visible in these sampled Dead Pool scenes; this is not all shadow shapes, animations or arenas acceptance.',
  'The five snapshots per case cannot prove cursor blinking cadence or immediate portrait cleanup before a ladder reveal; those remain separate final UI gates.',
 ],observedNaturalMirrorVisualReviewPassed=True,allSelectionGraphicsAccepted=False,
 allFloorShadowsAccepted=False,allArenasAccepted=False,naturalAlternateFatalitiesAccepted=False,fullPortAccepted=False,
 inputHashes={**inventory['inputHashes'],str(inventory_path):proof.digest(inventory_path)})
OUT.mkdir();(OUT/'review.json').write_text(json.dumps(record,indent=2)+'\n')
print('Saved review of 30 actual cold mirror scenes; full port incomplete')
