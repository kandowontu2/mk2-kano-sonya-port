"""Small decoded review set and trace-derived chapter sidecars, no video reencode."""
import csv
import json
from pathlib import Path
import shutil
import subprocess
from campaign_video_chapters import chapter_plan, metadata
from inspect_normal_runtime import BASE, PORT, sha
from native_roster import verified_names
from refresh_special_videos import FLAGS


def main():
    out=PORT/'generated_sonya_campaign_2219'
    info=json.loads((out/'CAMPAIGN_VIDEO.json').read_text())
    assert info['earnedFullCampaignClearVerified']
    video=Path(info['file']);assert sha(video)==info['SHA256']
    run=BASE/'stock_wolf_2219_sonya_campaign_stream'
    clock=info['encoded'];clear=info['clear']
    review=out/'review_v2';assert not review.exists();review.mkdir()
    selection=ladder=combat=None
    with (run/'campaign.csv').open() as stream:
        for row in csv.DictReader(stream):
            if row['mode']=='2':
                combat=int(row['frame']);break
            if row['mode']=='4' and row['p1selected']=='18':selection=int(row['frame'])
            if row['mode']=='7' and ladder is None:ladder=int(row['frame'])
    assert selection and ladder and combat
    points=[('selection',selection),('ladder',ladder+90),('first_combat',combat+90),
        ('kahn_defeat',clear['finalBossClearFrame']+300),('congratulations',clear['finalBossClearFrame']+1140),
        ('story_1',clear['finalBossClearFrame']+1980),('story_2',clear['finalBossClearFrame']+2460),
        ('cast',clear['finalBossClearFrame']+4980),('credits',clear['finalBossClearFrame']+6060),
        ('game_over',clear['finalBossClearFrame']+8340),('last_field',clear['attractReturnFrame'])]
    ff=shutil.which('ffmpeg');assert ff
    samples=[]
    for label,frame in points:
        relative=frame-clock['firstGuestFrame'];assert 0<=relative<clock['frames']
        path=review/(label+'.png')
        subprocess.run([ff,'-v','error','-nostdin','-threads','1','-ss',f"{relative/clock['rate']:.9f}",
            '-i',str(video),'-vf','scale=400:300:flags=neighbor,setsar=1','-frames:v','1','-threads','1','-n',str(path)],
            check=True,capture_output=True,timeout=30,creationflags=FLAGS)
        samples.append(dict(label=label,requestedNativeFrame=frame,file=str(path),SHA256=sha(path)))
    audit=json.loads((run/'CAMPAIGN_AUDIT.json').read_text())
    winners={r['map']:r['successfulAttempt'] for r in audit['naturallyDefeatedOpponents']}
    winners[audit['maxMapPosition']]=clear['attempt']
    with (run/'campaign.csv').open() as source:
        chapters=chapter_plan(csv.DictReader(source),clock,verified_names(True),winners,clear['finalBossClearFrame'])
    (review/'SAMPLES.json').write_text(json.dumps(dict(scope='Sparse decoded campaign review, not every-frame visual approval',
        videoSHA256=info['SHA256'],samples=samples),indent=2)+'\n')
    plan=dict(cases=chapters,embeddedInVideo=False,videoSHA256=info['SHA256'])
    plan_path=out/'CHAPTER_PLAN.json'
    if plan_path.exists():assert json.loads(plan_path.read_text())==plan
    else:plan_path.write_text(json.dumps(plan,indent=2)+'\n')
    meta_path=out/'CHAPTERS.ffmetadata'
    if meta_path.exists():assert meta_path.read_text(encoding='utf-8')==metadata(chapters)
    else:meta_path.write_text(metadata(chapters),encoding='utf-8')
    print('Extracted',len(samples),'review images; prepared',len(chapters),'trace-derived chapter markers (sidecars only).')


if __name__=='__main__':main()
