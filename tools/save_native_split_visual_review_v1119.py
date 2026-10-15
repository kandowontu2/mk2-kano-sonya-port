"""Record main-agent visual inspection of actual source-bound runtime scenes."""
import hashlib,json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'audit_v1119_owned_split_actual_visual_review'
if OUT.exists():
    raise ValueError('Preserve visual evidence')
inventory_path = ROOT/'audit_v1116_owned_split_actual_scene_contacts/inventory.json'
inventory = json.loads(inventory_path.read_text())
for path,wanted in inventory['inputHashes'].items():
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()==wanted
assert inventory['sceneCount']==68 and len(inventory['contacts'])==4
OUT.mkdir()
(OUT/'review.json').write_text(json.dumps(dict(
    candidate='diagnostic_v1110_owned_native_split',
    scope='All 68 actual normal Dead Pool source-bound actor/pose pictures, both characters and physical slots',
    reviewedBy='main agent via view_image of all four 1:1 diagnostic contact sheets and four selected original actual PNGs',
    contacts=inventory['contacts'],
    sceneCount=68,
    findings=[
        'Initial three poses retain each character\'s own costume, hair, arms and lower-body silhouette.',
        'Both native actors render the own longitudinal half stream with opposing X mirror, not original Liu/Kitana body sections.',
        'The original upright-to-outward-fall sequence is visible in both player slots.',
        'Measured native floor/raster anchors verified separately in v1115; no standing/falling body appears globally raised.',
        'Actual native hat, performer, blood spray and win presentation remain; their foreground occlusion is not removed.',
        'One outward half clips at the actual viewport edge in several stages; this is retained and not called complete unclipped-body evidence.',
        'Normal-costume visual review only. Known Kano alternate-costume cut/blood recolouring remains unfinished.'
    ],
    normalObservedVisualReviewPassed=True,
    invariantBloodColoursAccepted=False,
    naturalAlternateSelectionAccepted=False,
    allArenasAccepted=False,
    allStockFatalitiesAccepted=False,
    fullPortAccepted=False,
    inputHashes={**inventory['inputHashes'],str(inventory_path):hashlib.sha256(inventory_path.read_bytes()).hexdigest().upper()}
),indent=2)+'\n')
print('Saved manual review: 68 actual scenes, normal Dead Pool only; full port incomplete')
