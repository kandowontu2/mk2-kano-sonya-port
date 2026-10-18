"""Decode early punch/kick motion at 50ms intervals, bounded one sheet at a time."""
import io
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw
from inspect_normal_runtime import PORT, sha
from refresh_special_videos import FLAGS


def main():
    folder=PORT/'generated_showcases_2219_streamcopy'
    output=folder/'short_attack_review'
    assert not output.exists(), 'Preserve existing samples'
    output.mkdir()
    report=[]
    for case in json.loads((folder/'SHOWCASES.json').read_text())['cases']:
        video=Path(case['file']);assert sha(video)==case['SHA256']
        for chapter in case['chapters']:
            if chapter['title'] not in ('High Punch','Low Punch','Vertical Jump Kick'):continue
            sheet=Image.new('RGB',(1600,6*274),'black');draw=ImageDraw.Draw(sheet)
            for index in range(24):
                offset=index*.05
                when=chapter['startMilliseconds']/1000+offset
                r=subprocess.run(['ffmpeg','-v','error','-threads','1','-ss',f'{when:.6f}',
                    '-i',str(video),'-frames:v','1','-threads','1','-f','image2pipe',
                    '-vcodec','png','pipe:1'],capture_output=True,check=True,
                    timeout=15,creationflags=FLAGS)
                x=(index%4)*400;y=(index//4)*274
                draw.text((x+3,y+2),f"{chapter['title']} +{offset:.2f}s",fill='white')
                with Image.open(io.BytesIO(r.stdout)) as frame:
                    assert frame.size==(400,254)
                    sheet.paste(frame,(x,y+20))
            path=output/f"actor{case['actor']}_{chapter['sourceKey'].split('/')[-1]}.png"
            sheet.save(path)
            report.append(dict(file=str(path),SHA256=sha(path),videoSHA256=case['SHA256'],
                chapter=chapter['title'],startMilliseconds=chapter['startMilliseconds'],
                offsetsSeconds=[i*.05 for i in range(24)]))
    (output/'SAMPLES.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Prepared144 samples in6 sheets; not full-motion approval')


if __name__=='__main__':main()
