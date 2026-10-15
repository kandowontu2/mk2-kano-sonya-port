"""Record the main agent's actual six-sheet /192-scene visual inspection."""
import json
import verify_stock_fire_display_v1201 as proof
ROOT=proof.ROOT;OUT=ROOT/'audit_v1204_stock_fire_visual_review';assert not OUT.exists()
path=ROOT/'audit_v1202_stock_fire_contacts/inventory.json';inventory=json.loads(path.read_text())
assert inventory['sceneCount']==192 and len(inventory['contacts'])==6
pins={str(path):proof.state.digest(path)}
for file,wanted in inventory['inputHashes'].items():
 assert proof.state.digest(file)==wanted; pins[file]=wanted
reports=[]
for name,side in (('control_kitana',1),('control_liu',2),('kano',1),('kano',2),('sonya',1),('sonya',2)):
 p=ROOT/f'audit_v1201_fire_{name}_p{side}_render_checked/report.json';r=json.loads(p.read_text());assert r['passed'];reports.append(r);pins[str(p)]=proof.state.digest(p)
controls={r['victimSlot']:r for r in reports if r['trueVictimID'] in (1,4)}
for r in reports:
 assert r['burnGeometry']==controls[r['victimSlot']]['burnGeometry'],'Every burn pose has exact stock-control vertical geometry'
record=dict(manualVisualReviewComplete=True,sceneCount=192,contacts=inventory['contacts'],
 observations=['All six unaltered actual contact sheets personally viewed by main agent.',
 'Kano/Sonya retain their own bodies and correct names through the original pre-burn dizzy phase.',
 'Original unmask, attached skull, fire breath, explosion, burning skeleton, scatter and win/fatality choreography appear in both directions.',
 'Early burn-body occlusion is original flame layering; full event-ordered replay validates the actual combined scenes.',
 'All seven burn-group vertical geometries equal the same-slot original control, despite different own standing floor origins.',
 'All six actual continue scenes are clear of fighter/selection portraits, poses and attached effects; winner/loser prompts occupy the correct slots.',
 'Original viewport edge clipping is retained; clipped pixels and unsampled fields are not accepted by inference.'],
 stockFireNormalDeadPoolSampledVisualReviewAccepted=True,currentContinueScreenVisuallyAccepted=True,
 allFatalityArtAccepted=False,alternateCostumesAccepted=False,audioAccepted=False,allArenasAccepted=False,
 allSelectionGraphicsAccepted=False,allFloorShadowsAccepted=False,fullPortAccepted=False,inputHashes=pins)
OUT.mkdir();(OUT/'review.json').write_text(json.dumps(record,indent=2)+'\n');print('192 actual scenes reviewed; same-slot burn geometry matched; full port remains incomplete')
