"""Contact sheets of ACTUAL native snapshots; no artwork modification."""
import json
import re
from pathlib import Path
from PIL import Image, ImageDraw
import verify_native_inflation_art_v941 as proof

ROOT = proof.ROOT
OUT = ROOT / 'audit_v943_owned_inflation_visual_review'


def main():
    if OUT.exists():
        raise ValueError('Preserve review evidence')
    OUT.mkdir()
    report = {'scope': 'actual_400x254_native_display_frames_not_generated_mockups', 'cases': {}}
    for case in proof.CASES:
        directory = ROOT / case
        text = (directory / 'run.log').read_text(encoding='utf-8-sig')
        matches = re.findall(r'^MK2_INFLATION_ART_V938_POSE_SNAPSHOT frame=(\d+) .*?file=(\S+) source=(\S+) .*?queued_frame=(\d+)', text, re.M)
        assert len(matches) == 6
        sheet = Image.new('RGB', (1200, 560), (35, 35, 40))
        draw = ImageDraw.Draw(sheet)
        files = []
        for pose, (frame, filename, source, queued) in enumerate(matches):
            assert int(frame) == int(queued) + 1
            x, y = pose % 3 * 400, pose // 3 * 280
            draw.text((x + 3, y + 3), f'{case.split("kitana_")[1]} pose {pose} / field {frame}', fill='white')
            image = Image.open(directory / 'snap' / filename)
            assert image.size == (400, 254)
            sheet.paste(image, (x, y + 22))
            files.append(str(directory / 'snap' / filename))
        output = OUT / (case + '-native-six-poses.png')
        sheet.save(output)
        report['cases'][case] = {'contact_sheet': str(output), 'actual_snapshots': files}
    (OUT / 'sources.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'output': str(OUT), 'actual_runtime_frames': 24}))


if __name__ == '__main__':
    main()
