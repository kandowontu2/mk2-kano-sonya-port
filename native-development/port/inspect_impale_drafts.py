"""Record provenance and alpha bounds; never equate a draft with runtime acceptance."""
import json
from PIL import Image
from generate_head_sources import PORT, sha

folder = PORT / 'assets/impale_draft'
actors = []
for actor, reference in [('kano', '../nut_draft/kano-nut-draft-v1.png'),
                         ('sonya', '../backbreak_draft/sonya-backbreak-draft-v1.png')]:
    path = folder / f'{actor}-impale-draft-v1.png'
    frames = []
    with Image.open(path) as image:
        assert image.mode == 'RGBA'
        width, height = image.size
        for phase in range(3):
            rectangle = [phase*width//3, 0, (phase+1)*width//3, height]
            cell = image.crop(rectangle)
            box = cell.getchannel('A').point(lambda a: 255 if a >= 128 else 0).getbbox()
            assert box
            frames.append(dict(phase=phase, cell=rectangle, alpha128Bounds=box,
                touchesCellEdge=box[0] == 0 or box[1] == 0 or box[2] == cell.width or box[3] == height))
    prompt = folder / f'{actor.upper()}_PROMPT.txt'
    actors.append(dict(actor=actor, asset=path.name, SHA256=sha(path.read_bytes()),
        promptFile=prompt.name, promptSHA256=sha(prompt.read_bytes()), referenceAsset=reference,
        frames=frames))
report = dict(format='MK2KS-IMPALE-DRAFT-1', generationMode='built-in image_gen', actors=actors,
    visualAcceptance=False, runtimeVerified=False, fullPortVerified=False)
(folder/'DRAFT_MANIFEST.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report))
