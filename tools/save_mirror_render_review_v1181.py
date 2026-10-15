"""Bind prior actual-scene review to byte-identical current captures and continue."""
import json
from pathlib import Path
import verify_natural_mirror_finish_v1169 as proof
OUT=proof.ROOT/'audit_v1181_current_mirror_render_visual_review'
assert not OUT.exists(),'Preserve visual review'
earlier_path=proof.ROOT/'audit_v1172_natural_mirror_finish_visual_review/review.json'
earlier=json.loads(earlier_path.read_text());assert earlier['manualVisualReviewComplete'] and earlier['sceneCount']==124
pins={str(earlier_path):proof.digest(earlier_path)};mapped={};continues=[]
for filename,wanted in earlier['inputHashes'].items():
 path=Path(filename);assert proof.digest(path)==wanted
 if 'audit_v1167_' in filename and '/snap/' in filename.replace('\\','/'):
  current=Path(filename.replace('audit_v1167_','audit_v1177_'))
  assert proof.digest(current)==wanted,'Reviewed actual pixels changed'
  mapped[filename]=str(current);pins[str(current)]=wanted
assert len(mapped)==124
for name in ('kano','sonya'):
 for side in (1,2):
  report_path=proof.ROOT/f'audit_v1179_{name}_mirror_finish_p{side}_render_checked/report.json'
  report=json.loads(report_path.read_text());assert report['passed'] and report['replayed']['frames']==165
  scene=proof.ROOT/report['case']/'snap/display_4080.png'
  assert proof.digest(scene)==report['inputHashes'][str(scene)]
  pins[str(scene)]=proof.digest(scene);pins[str(report_path)]=proof.digest(report_path);continues.append(str(scene))
record=dict(sceneCount=128,byteIdenticalPreviouslyReviewedScenes=124,
 newlyViewedContinueScenes=continues,manualVisualReviewComplete=True,
 reviewedBy='Main agent: four earlier complete contact sheets, exact byte equality to current replays, and four current display_4080.png continue scenes via view_image',
 findings=earlier['findings']+[
 'All four newer continue captures show the correct winner preparing for the next challenge and the loser needing two credits to continue, with countdown8.',
 'No Kano/Sonya selection portrait, selection animation, skeleton or kiss orb remains over the current continue scenes.',
 'Earlier age-700 scenes alone did not visually prove continue; these later directly viewed captures close that specific visual gap.',
 ],currentContinueScreenVisuallyAccepted=True,allFatalityArtAccepted=False,
 donorChoreographyAccepted=False,audioAccepted=False,allFloorShadowsAccepted=False,
 allArenasAccepted=False,fullPortAccepted=False,inputHashes=pins)
OUT.mkdir();(OUT/'review.json').write_text(json.dumps(record,indent=2)+'\n')
print('124 byte-identical reviewed scenes plus4 newly viewed native continue scenes')
