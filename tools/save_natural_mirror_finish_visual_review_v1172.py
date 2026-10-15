"""Main-agent review of four actual mirror finisher sheets; bounded evidence."""
import json
from pathlib import Path
import verify_natural_mirror_finish_v1169 as proof
OUT=proof.ROOT/'audit_v1172_natural_mirror_finish_visual_review'
assert not OUT.exists(),'Preserve visual review'
path=proof.ROOT/'audit_v1170_natural_mirror_finish_contacts/inventory.json'
inventory=json.loads(path.read_text());assert inventory['sceneCount']==124 and len(inventory['contacts'])==4
for filename,wanted in inventory['inputHashes'].items():assert proof.digest(Path(filename))==wanted,filename
record=dict(manualVisualReviewComplete=True,sceneCount=124,contacts=inventory['contacts'],
 reviewedBy='Main agent via view_image: all four actual contact sheets',
 findings=[
 'Kano normal red and natural alternate blue outfits remain distinct when each wins and when each is the extraction victim.',
 'Kano own windup, separate pulled skeleton and victim collapse appear in both facing directions, followed by native win and fatality text.',
 'Sonya green and natural alternate blue outfits remain distinct through own kiss/return-to-salute poses.',
 'Separate kiss orb launches, arcs and reaches the selected mirror victim; the burn and own salute/outro appear in both directions.',
 'KANO and SONYA remain in both lifebars and win text; no persistent selection portrait overlay is visible.',
 'Original viewport-edge clipping and occlusion are retained, so clipped victim/effect pixels are not fully visually accepted.',
 'The age-700 captures still show the fatality scene. Later native continue state is proved by runtime chronology, not by these selected images.',
 'Exact DMA/component/pixel binding, original-donor choreography, audio and all pose/arena floor shadows remain separate checks.',
 ],observedMirrorFinisherSequencesReviewed=True,allFatalityArtAccepted=False,
 continueScreenVisuallyAccepted=False,allFloorShadowsAccepted=False,allArenasAccepted=False,
 fullPortAccepted=False,inputHashes={**inventory['inputHashes'],str(path):proof.digest(path)})
OUT.mkdir();(OUT/'review.json').write_text(json.dumps(record,indent=2)+'\n')
print('Recorded 124 actual scenes; no all-art or visually displayed-continue claim')
