"""Make labelled, chaptered character showcases from verified real AV clips.

Labels live below the unchanged game picture. Source clips stay unaltered.
No fabricated gameplay, speed changes, synthesized sound, or resampled timing.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import time

ROOT=Path(__file__).resolve().parent.parent
sp=importlib.util.spec_from_file_location('video_helpers',ROOT/'video_sonya_subzero_hk_20261015_preparation/run.py')
h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
BASE=ROOT/'videos_showcase_20261015'
MOVES={
 'knife':('Knife Throw','D, B + HP'), 'blade':('Blade Swipe','D, F + HP - close'),
 'choke':('Choke','D, F + LP - close'), 'ball':('Cannonball','Hold LK about 1.5 seconds, then release'),
 'ring':('Energy Ring','D, F + LP'), 'bicycle':('Bicycle Kick','B, B, D + HK'),
 'leg':('Leg Grab','D + LP + Block - close'), 'square':('Square Wave','F, B + HP - airborne opponent'),
 'uppercut':('Uppercut','D + HP'), 'sweep':('Sweep','B + LK'),
 'roundhouse':('Roundhouse','B + HK'), 'throw':('Throw','F + LP - touching distance'),
 'standing_block':('Standing Block','Block'), 'crouching_block':('Crouching Block','D + Block'),
 'deadpool':('Dead Pool Stage Finish','Close uppercut, then hold LP + LK through launch'),
 'pit':('Pit II Stage Fatality',''), 'tomb':('Kombat Tomb Stage Fatality',''),
 'primary':('',''), 'secondary':('',''), 'friendship':('Friendship',''), 'babality':('Babality',''),
}

def sequence(fighter):
    basics=['uppercut','sweep','roundhouse','throw','standing_block','crouching_block']
    specials=['knife','blade','choke','ball'] if fighter=='kano' else ['ring','bicycle','leg','square']
    return basics+specials+['primary','secondary','friendship','babality','deadpool','tomb','pit','morph']

def label(fighter,move):
    if move=='morph':return 'Shang Tsung: Morph to '+fighter.title(), 'B, D, B + LK' if fighter=='kano' else 'D + LP + Block'
    title,command=MOVES[move]
    if move=='primary':title,command=('Skeleton Rip','B, D, F + HK - close') if fighter=='kano' else ('Kiss of Death','B, F, D, D + LP - close/mid')
    if move=='secondary':title,command=('Eye Laser','LP, Block, Block, HK - mid; release Block') if fighter=='kano' else ('Death Orb / Bubble','HOLD Block throughout U, U, B, D + HK - far')
    if move=='friendship':command='LK, Block, Block, HK - far; win using kicks only' if fighter=='kano' else 'B, F, B, D + Block - far; win using kicks only'
    if move=='babality':command='F, F, D, D + LK - win using kicks only' if fighter=='kano' else 'D, D, F + LK - win using kicks only'
    if move in ('pit','tomb'):command='U, U, B + LK - close' if fighter=='kano' else 'F, F, D + HP - close'
    return fighter.title()+' - '+title,command

def bounded(args,log,cap=384):
    with log.open('wb') as f:
        p=subprocess.Popen(args,stdout=subprocess.DEVNULL,stderr=f,creationflags=h.HIDDEN)
        begin=time.monotonic();peak=0
        while p.poll() is None:
            peak=max(peak,h.memory(p.pid))
            if peak>cap*1024**2 or time.monotonic()-begin>90:
                p.kill();p.wait();raise RuntimeError('Bounded assembly resource limit')
            time.sleep(.05)
        h.need(p.returncode==0,'Assembly: '+str(log))
    return peak

def main():
    pa=argparse.ArgumentParser();pa.add_argument('fighter',choices=['kano','sonya']);pa.add_argument('--finish-existing',action='store_true');a=pa.parse_args()
    out=BASE/(a.fighter+'_complete_showcase')
    h.need(not out.exists() if not a.finish_existing else out.is_dir() and not (out/'verification.json').exists(),'Never overwrite verified assembly')
    # Validate every expected chapter before creating/rendering anything.
    entries=[]
    for move in sequence(a.fighter):
        key='shang_'+a.fighter if move=='morph' else a.fighter+'_'+move
        folder=BASE/(key+'_v2' if key in ('kano_primary','kano_uppercut') else key)
        verification=json.loads((folder/'verification.json').read_text())
        h.need(verification['passed'] and not verification.get('fullPlaythrough',False),'Actual qualified showcase clip')
        clip=folder/(key+'.mp4');h.need(h.sha(clip)==verification['finalSHA256'],'Unchanged recorded source '+key)
        entries.append((move,key,clip,verification))
    if not a.finish_existing:out.mkdir()
    temp=out/'labelled_intermediates'
    if not a.finish_existing:temp.mkdir()
    ff=Path(shutil.which('ffmpeg'));fp=ff.with_name('ffprobe.exe')
    chapters=[];ms=0;maxmem=0
    for i,(move,key,clip,verification) in enumerate(entries):
        title,command=label(a.fighter,move)
        titlefile=temp/(str(i)+'_title.txt');titlefile.write_text(title)
        cmdfile=temp/(str(i)+'_command.txt');cmdfile.write_text(command)
        target=temp/(f'{i:02}.mp4')
        # Relative text filenames avoid Windows drive-colon filter escaping.
        titlepath=titlefile.relative_to(ROOT).as_posix();cmdpath=cmdfile.relative_to(ROOT).as_posix()
        vf=f"scale=800:600:flags=neighbor,setsar=1,pad=800:680:0:0:black,drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':textfile='{titlepath}':x=16:y=610:fontsize=26:fontcolor=white,drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':textfile='{cmdpath}':x=16:y=648:fontsize=19:fontcolor=yellow"
        cmd=[str(ff),'-hide_banner','-loglevel','warning','-nostdin','-i',str(clip),'-vf',vf,'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-ar','48000','-movflags','+faststart',str(target)]
        if a.finish_existing:
            h.need(target.is_file(),'Existing labelled segment')
        else:maxmem=max(maxmem,bounded(cmd,temp/(f'{i:02}.log')))
        probe=h.probe(fp,target)
        duration=float(probe['format']['duration']);end=ms+round(duration*1000)
        chapters.append(dict(key=key,title=title,command=command,startMilliseconds=ms,endMilliseconds=end,sourceSHA256=verification['finalSHA256'],nativeFirstFrame=verification['firstNativeFrame'],nativeLastFrame=verification['lastNativeFrame']))
        ms=end
    concat=temp/'concat.txt';concat.write_text(''.join("file '"+f'{i:02}.mp4'+"'\n" for i in range(len(entries))))
    metadata=temp/'chapters.ffmeta'
    metadata.write_text(';FFMETADATA1\ntitle='+a.fighter.title()+' - Complete Move Showcase\ncomment=Real current-build gameplay with native sound; F/B are opponent-relative. Labels are outside the game.\n'+''.join(f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={c['startMilliseconds']}\nEND={c['endMilliseconds']}\ntitle={c['title']}\n" for c in chapters))
    final=out/(a.fighter.title()+'_Complete_Moves_and_Finishers'+('_VERIFIED' if a.finish_existing else '')+'.mp4')
    h.need(not final.exists(),'Fresh mux output')
    cmd=[str(ff),'-hide_banner','-loglevel','warning','-nostdin','-f','concat','-safe','0','-i',str(concat),'-i',str(metadata),'-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1','-c:v','copy','-c:a','aac','-b:a','128k','-af','aresample=async=1:first_pts=0','-movflags','+faststart',str(final)]
    maxmem=max(maxmem,bounded(cmd,out/('assembly_verified.log' if a.finish_existing else 'assembly.log')))
    probe=json.loads(subprocess.run([str(fp),'-v','error','-show_streams','-show_format','-show_chapters','-of','json',str(final)],capture_output=True,text=True,check=True,timeout=10,creationflags=h.HIDDEN).stdout)
    types=[s['codec_type'] for s in probe['streams']]
    h.need(len(probe['chapters'])==len(entries) and types.count('video')==types.count('audio')==1 and all(t in ('video','audio','data') for t in types),'Every chapter and AV stream; MP4 chapter data track allowed')
    h.need(abs(float(probe['format']['duration'])-ms/1000)<.3 and final.stat().st_size<200*1024**2,'Final duration and size')
    report=dict(passed=True,fighter=a.fighter,chapters=chapters,finalSHA256=h.sha(final),finalBytes=final.stat().st_size,probe=probe,peakWorkingSetBytes=maxmem,gamePicture='400x254 native screen displayed at 4:3 inside800x600; labels only in added80pixel footer',frameRate=h.RATE,visualFinalReviewPending=True,scope='Every special, finisher, listed shared basic control and Shang morph in the included port movelist; not a full campaign')
    (out/'verification.json').write_text(json.dumps(report,indent=2))
    (out/'CHAPTERS.txt').write_text('\n'.join(f"{c['startMilliseconds']//60000:02}:{c['startMilliseconds']//1000%60:02}  {c['title']} | {c['command']}" for c in chapters)+'\n\nF = toward opponent; B = away. Native sound; no cheats or guest state writes.\n')
    # Only generated descendants, never the recording sources or game data.
    h.need(temp.resolve().parent==out.resolve() and temp.name=='labelled_intermediates' and not temp.is_symlink(),'Exact generated intermediates')
    for child in temp.iterdir():h.need(child.is_file() and not child.is_symlink(),'Only expected generated files')
    shutil.rmtree(temp)
    if a.finish_existing:
        rejected=out/(a.fighter.title()+'_Complete_Moves_and_Finishers.mp4')
        h.need(rejected.parent==out and rejected.is_file() and not rejected.is_symlink(),'Exact superseded unaccepted mux')
        rejected.unlink()
    print(final)

if __name__=='__main__':main()
