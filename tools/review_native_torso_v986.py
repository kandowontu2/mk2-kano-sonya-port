"""Contact sheets of ACTUAL native-rendered torso scenes, not sprite painting."""
import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit_v986_owned_torso_blood_visual_review'
if OUT.exists():
    raise ValueError('Preserve review evidence')
OUT.mkdir()
report = {}
for name in ('kano', 'sonya'):
    for side in (1, 2):
        case = f'audit_v979_cage_{name}_p{side}_owned_torso'
        start = 3090 if side == 1 else 3101
        ages = (0, 71, 75, 131, 135, 139 if side == 1 else 140, 200, 600)
        sheet = Image.new('RGB', (1600, 548), (35, 35, 40))
        draw = ImageDraw.Draw(sheet)
        files = []
        for index, age in enumerate(ages):
            # Exact first-source next-field images for the original native
            # poses, and unchanged periodic images for intact/late aftermath.
            if age in (0, 200, 600):
                path = ROOT / case / 'snap' / f'stock_head_{start}_{age:03d}.png'
            else:
                matches = list((ROOT / case / 'snap').glob(f'torso_pose_*_{start + age}.png'))
                physical = '01034E90' if side == 1 else '010350A0'
                path = next(p for p in matches if physical in p.name)
            image = Image.open(path).convert('RGB')
            assert image.size == (400, 254)
            x, y = index % 4 * 400, index // 4 * 274
            draw.text((x + 3, y + 3), f'{name} P{side}: native age {age}', fill='white')
            sheet.paste(image, (x, y + 20))
            files.append(str(path))
        sheet.save(OUT / f'{name}-p{side}-native-scenes.png')
        report[case] = files
(OUT / 'sources.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'actual_scene_images': 32, 'contact_sheets': 4, 'artworkAcceptance': False}))
