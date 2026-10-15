"""Assemble unedited ACTUAL native scene captures for manual review.

No generated-art painting or simulated scene; original 400x254 pixels are
copied at 1:1 with captions outside them. This is not the runtime verifier.
"""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'audit_v1116_owned_split_actual_scene_contacts'
REPORT = ROOT/'audit_v1115_owned_native_split_checked/report.json'

if OUT.exists():
    raise ValueError('Preserve actual review evidence')
report = json.loads(REPORT.read_text())
assert report['passed'] and len(report['cases'])==4
OUT.mkdir()
pins = {str(REPORT):hashlib.sha256(REPORT.read_bytes()).hexdigest().upper()}
contacts = {}
for name,case in report['cases'].items():
    scenes = case['pixelMatches']
    assert len(scenes)==17
    scenes.sort(key=lambda row:(row['pose'],row['actor']))
    contact = Image.new('RGB',(1600,1370),(25,25,25))
    draw = ImageDraw.Draw(contact)
    for n,scene in enumerate(scenes):
        path = Path(scene['picture'])
        image = Image.open(path).convert('RGB')
        assert image.size==(400,254)
        x,y=(n%4)*400,(n//4)*274
        draw.text((x+3,y+3),f"{case['victim']} P{case['slot']} pose{scene['pose']} actor{scene['actor']} match{scene['score']:.3f}",fill='white')
        contact.paste(image,(x,y+20))
        pins[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest().upper()
    output = OUT/f"{case['victim']}-p{case['slot']}-actual-17-scenes.png"
    contact.save(output)
    contacts[name] = str(output)
    pins[str(output)] = hashlib.sha256(output.read_bytes()).hexdigest().upper()
(OUT/'inventory.json').write_text(json.dumps(dict(source= str(REPORT),sceneCount=68,contacts=contacts,
    actualScenePixelsChanged=False,manuallyReviewed=False,inputHashes=pins,
    scope='contact inventory only; viewport-edge clipping/actor and blood occlusion retained',
    alternateCostumesAccepted=False,fullPortAccepted=False),indent=2)+'\n')
print(json.dumps(contacts,indent=2))
