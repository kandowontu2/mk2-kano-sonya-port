"""Two chaptered demonstrations from58 verified native clips, no new gameplay."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
from collect_native_videos import PORT,sha

NORMAL_LABELS=(('hp','High Punch'),('lp','Low Punch'),('hk','High Kick'),('lk','Low Kick'),
    ('roundhouse','Roundhouse'),('sweep','Sweep'),('uppercut','Uppercut'),
    ('duckpunch','Crouching Punch'),('duckhighkick','Crouching High Kick'),('ducklowkick','Crouching Low Kick'),
    ('jumpkick','Vertical Jump Kick'),('jumppunch','Vertical Jump Punch'),
    ('flyingkick','Diagonal Jump Kick'),('flyingpunch','Diagonal Jump Punch'),
    ('knee','Knee'),('elbow','Elbow'),('throw','Throw'))

def plan(actor):
    assert actor in (17,18)
    entries=[(f'normal/{actor}/{key}',label) for key,label in NORMAL_LABELS]
    specials=(('ball','Ball'),('knife','Knife'),('blade','Blade'),('choke','Choke')) if actor==17 else (
        ('ring','Ring'),('bike','Bicycle Kick'),('square','Square Wave'),('leg','Leg Grab'))
    entries += [('special/'+key,label) for key,label in specials]
    entries += [('lethal/'+key,label) for key,label in (
        (('extract','Skeleton Extract'),('laser','Eye Laser')) if actor==17 else (('kiss','Flame Kiss'),('bubble','Death Orb')))]
    entries += [(f'friend/{actor}','Friendship'),(f'baby/{actor}','Babality'),
                (f'deadpool/{actor}','Dead Pool'),(f'tomb/{actor}','Kombat Tomb'),
                (f'pit/{actor}','Pit II'),(f'morph/{actor}','Shang Tsung Morph and Return')]
    assert len(entries)==len({key for key,_ in entries})==29
    return entries

def main(stream_copy=False):
    catalog=PORT/'NATIVE_VIDEO_CATALOG_FULL_2219.json'
    data=json.loads(catalog.read_text());clips={r['key']:r for r in data['cases']}
    assert len(clips)==58 and data['allCurrent26ROMBytesVerified']
    assert {key for actor in (17,18) for key,_ in plan(actor)}==set(clips)
    # Validate every input before creating output, including source frame counts.
    for clip in clips.values():assert sha(Path(clip['file']))==clip['SHA256']
    out=PORT/('generated_showcases_2219_streamcopy' if stream_copy else 'generated_showcases_2219');assert not out.exists(),'Never overwrite generated media'
    out.mkdir()
    ff=shutil.which('ffmpeg');fp=shutil.which('ffprobe');assert ff and fp
    flags=getattr(subprocess,'CREATE_NO_WINDOW',0)|getattr(subprocess,'BELOW_NORMAL_PRIORITY_CLASS',0)
    def command(args):
        return subprocess.run(args,check=True,capture_output=True,text=True,timeout=180,creationflags=flags)
    results=[]
    for actor in (17,18):
        name='KANO' if actor==17 else 'SONYA'
        concat=['ffconcat version 1.0'];metadata=[';FFMETADATA1',f'title=MKII {name} - Native Move Demonstrations']
        chapters=[];elapsed=0.0;expected=0
        for key,label in plan(actor):
            clip=clips[key];path=Path(clip['file'])
            source=json.loads((path.parent/'FINISHER_VIDEO.json').read_text())
            assert source['SHA256']==clip['SHA256'] and source['frames']==clip['frames']
            duration=source['frames']/source['rate'];expected+=source['frames']
            assert "'" not in path.as_posix()
            concat += [f"file '{path.as_posix()}'",f'duration {duration:.12f}']
            start=round(elapsed*1000);elapsed+=duration;end=round(elapsed*1000)
            metadata += ['[CHAPTER]','TIMEBASE=1/1000',f'START={start}',f'END={end}',f'title={label}']
            chapters.append(dict(title=label,startMilliseconds=start,endMilliseconds=end,sourceKey=key,SHA256=clip['SHA256']))
        listing=out/f'{name}.ffconcat';listing.write_text('\n'.join(concat)+'\n',encoding='utf-8')
        meta=out/f'{name}.ffmetadata';meta.write_text('\n'.join(metadata)+'\n',encoding='utf-8')
        output=out/f'MKII_{name}_MOVES.mp4'
        command([ff,'-v','error','-nostdin','-threads','2','-safe','0','-f','concat','-i',str(listing),
                 '-f','ffmetadata','-i',str(meta),'-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1',
                 *(['-c:v','copy'] if stream_copy else ['-vf','setsar=127/150:max=1000','-fps_mode','passthrough','-c:v','libx264','-threads','2',
                 '-preset','veryfast','-crf','18','-pix_fmt','yuv420p']),'-af','aresample=async=1:first_pts=0',
                 '-c:a','aac','-b:a','192k','-movflags','+faststart','-n',str(output)])
        probe=json.loads(command([fp,'-v','error','-count_frames','-show_streams','-show_chapters','-of','json',str(output)]).stdout)
        video=next(s for s in probe['streams'] if s['codec_type']=='video')
        assert int(video['nb_read_frames'])==expected and video['display_aspect_ratio']=='4:3'
        assert any(s['codec_type']=='audio' for s in probe['streams']) and len(probe['chapters'])==29
        command([ff,'-v','error','-xerror','-nostdin','-threads','2','-i',str(output),'-f','null','NUL'])
        results.append(dict(actor=actor,file=str(output),SHA256=sha(output),bytes=output.stat().st_size,
            sourceFramesPreserved=expected,chapters=chapters,fullDecodePassed=True,exactAudioSyncQualified=False))
        print('ENCODED_SHOWCASE',name,expected,'frames',flush=True)
    (out/'SHOWCASES.json').write_text(json.dumps(dict(cases=results,catalogSHA256=sha(catalog),
        videoStreamCopiedWithoutReencoding=stream_copy,
        fullCampaignVideos=False,everyFrameVisualReviewPassed=False,fullPortVerified=False,releaseReady=False),indent=2)+'\n')

if __name__=='__main__':
    assert sys.argv[1:] in ([],['--stream-copy'])
    main('--stream-copy' in sys.argv)
