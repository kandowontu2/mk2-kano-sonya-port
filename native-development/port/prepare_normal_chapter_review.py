"""Bounded, labeled three-sample review of every normal showcase chapter."""
import io
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw
from inspect_normal_runtime import PORT, sha
from refresh_special_videos import FLAGS


def main():
    folder = PORT / 'generated_showcases_2219_streamcopy'
    manifest = folder / 'SHOWCASES.json'
    output = folder / 'normal_chapter_review'
    assert not output.exists() or not any(output.iterdir()), 'Preserve existing review output'
    output.mkdir(exist_ok=True)
    report = dict(scope='Sparse decoded visual samples, not full animation or audio approval',
                  manifestSHA256=sha(manifest), cases=[])
    for case in json.loads(manifest.read_text())['cases']:
        video = Path(case['file'])
        assert sha(video) == case['SHA256']
        chapters = [c for c in case['chapters'] if c['sourceKey'].startswith('normal/')]
        assert len(chapters) == 17
        for begin in (0, 6, 12):
            group = chapters[begin:begin+6]
            sheet = Image.new('RGB', (1200, 274*len(group)), 'black')
            draw = ImageDraw.Draw(sheet)
            samples = []
            for row, chapter in enumerate(group):
                start = chapter['startMilliseconds'] / 1000
                duration = (chapter['endMilliseconds'] - chapter['startMilliseconds']) / 1000
                draw.text((4, row*274+2), chapter['title'], fill='white')
                for column, fraction in enumerate((0.15, 0.4, 0.75)):
                    when = start + duration*fraction
                    result = subprocess.run(['ffmpeg','-v','error','-threads','1',
                        '-ss',f'{when:.6f}','-i',video,'-frames:v','1','-threads','1',
                        '-f','image2pipe','-vcodec','png','pipe:1'],
                        capture_output=True,check=True,timeout=15,creationflags=FLAGS)
                    with Image.open(io.BytesIO(result.stdout)) as frame:
                        assert frame.size == (400,254)
                        sheet.paste(frame,(column*400,row*274+20))
                    samples.append(dict(title=chapter['title'],timeSeconds=when))
            path = output / f"actor{case['actor']}_normals_{begin+1}.png"
            sheet.save(path)
            report['cases'].append(dict(file=str(path),SHA256=sha(path),
                videoSHA256=case['SHA256'],samples=samples))
    (output/'SAMPLES.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Prepared102 labeled samples in6 sheets; no emulator or raw video dump')


if __name__ == '__main__':main()
