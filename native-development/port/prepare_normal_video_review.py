"""Bounded contact-frame sheets, explicitly not all-frame visual approval."""
import csv
import json
import shutil
import subprocess
from refresh_normal_videos import plan
from refresh_special_videos import BASE,PORT,FLAGS
from inspect_normal_runtime import sha

def sample_frame(label,rows,first,count):
    if label=='throw':sample=12
    else:
        drop=next(int(after['frame']) for before,after in zip(rows,rows[1:])
                  if int(after['p2hp'])<int(before['p2hp']))
        sample=drop-first
    assert 0<=sample<count
    return sample

def main():
    out=PORT/'generated_normal_review_2219';assert not out.exists(),'Never overwrite review artifacts'
    fixtures=plan('stock_wolf_2219_normal_video')
    assert all((BASE/name/'CAPTURED_NORMAL_QUALIFICATION.json').exists() for name,_,_,_ in fixtures)
    out.mkdir();ff=shutil.which('ffmpeg');assert ff
    records=[];indices={17:0,18:0}
    def command(args):subprocess.run(args,check=True,capture_output=True,timeout=30,creationflags=FLAGS)
    for name,actor,label,_ in fixtures:
        run=BASE/name;video=json.loads((run/'FINISHER_VIDEO.json').read_text())
        assert sha(run/'native_finisher_v2.mp4')==video['SHA256']
        with (run/'normals.csv').open() as stream:rows=list(csv.DictReader(stream))
        sample=sample_frame(label,rows,video['firstGuestFrame'],video['frames'])
        output=out/f'{actor}_{indices[actor]:02d}.png';indices[actor]+=1
        command([ff,'-v','error','-nostdin','-threads','1','-i',video['file'],'-vf',f'select=eq(n\\,{sample})',
                 '-frames:v','1','-threads','1','-n',str(output)])
        records.append(dict(actor=actor,label=label,sampleFrame=sample,file=str(output),sourceSHA256=video['SHA256']))
    for actor in (17,18):
        assert indices[actor]==17
        command([ff,'-v','error','-nostdin','-threads','1','-framerate','1','-i',str(out/f'{actor}_%02d.png'),
                 '-vf','tile=5x4','-frames:v','1','-threads','1','-n',str(out/f'{actor}_sheet.png')])
    (out/'SAMPLES.json').write_text(json.dumps(dict(scope='One sampled contact/throw pose per normal clip',
        cases=records,everyFrameVisualReviewPassed=False),indent=2)+'\n')
    print('34 bounded normal contact/throw samples extracted; no all-frame approval inferred.')

if __name__=='__main__':main()
