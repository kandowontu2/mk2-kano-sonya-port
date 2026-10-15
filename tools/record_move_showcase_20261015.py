"""Bounded native AV clips using existing physical-input-only test controllers.

No historic capture imports, raw-frame files, RAM writes, or unbounded queues.
Each case is immutable after execution; evidence is retained even on failure.
"""
import argparse
import ctypes as C
from ctypes import wintypes as W
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import threading
import time

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('bounded_video_helpers', ROOT/'video_sonya_subzero_hk_20261015_preparation/run.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)  # Definitions only; main is explicitly guarded.


def plan(key):
    fighter, move = key.split('_', 1)
    h.need(fighter in ('kano', 'sonya', 'shang'), 'Known showcase fighter')
    if fighter == 'shang':
        h.need(move in ('kano', 'sonya'), 'Known morph')
        return 'audit_bounded_current_human_morphs_preparation/morph.lua', dict(MK2KS_HUMAN_SHANG_SIDE='1', MK2KS_HUMAN_SHANG_TARGET=move, MK2KS_HUMAN_SHANG_PROFILE='native'), 3100, 'morph'
    if move in ('knife','ball','blade','choke','ring','bicycle','leg','square'):
        h.need((move in ('knife','ball','blade','choke')) == (fighter == 'kano'), 'Character owns move')
        return 'audit_bounded_current_special_cycles_preparation/cycles.lua', dict(MK2KS_HUMAN_SPECIAL_MOVE=move, MK2KS_HUMAN_SPECIAL_SIDE='1', MK2KS_HUMAN_SPECIAL_VICTIM='kitana', MK2KS_HUMAN_SPECIAL_AIR='1' if move=='square' else '0'), 4400, 'special'
    if move in ('primary','secondary'):
        source = 'audit_bounded_own_finishers_dispatch_preparation/finishers.lua' if move=='primary' else 'audit_bounded_secondary_finishers_preparation/finishers.lua'
        command = fighter+'_own' if move=='primary' else ('kano_laser' if fighter=='kano' else 'sonya_orb')
        return source, dict(MK2KS_TEST_FIGHTER='kitana', MK2KS_CAMPAIGN_SIDE='2', MK2KS_STOCK_KILLER=fighter, MK2KS_STOCK_COMMAND=command, MK2KS_STOCK_GAP='64' if move=='primary' else '150' if fighter=='kano' else '250'), 5900, 'fatality'
    if move == 'friendship':
        return 'audit_bounded_current_friendships_preparation/friendships.lua', dict(MK2KS_FRIEND_SIDE='1', MK2KS_FRIEND_WINNER=fighter, MK2KS_FRIEND_CASE='positive'), 5600, 'friendship'
    if move == 'babality':
        return 'audit_bounded_current_babalities_preparation/babalities.lua', dict(MK2KS_BABY_WINNER_SIDE='1', MK2KS_BABY_WINNER=fighter, MK2KS_BABY_VICTIM='sonya' if fighter=='kano' else 'kano', MK2KS_BABY_CASE='positive'), 5600, 'babality'
    if move in ('pit','tomb','deadpool'):
        source={'pit':'audit_current_native_pit_longkick_preparation/stage.lua', 'tomb':'audit_current_native_tomb_preparation/stage.lua', 'deadpool':'audit_current_native_deadpool_stock_victim_preparation/stage.lua'}[move]
        return source,dict(MK2KS_STAGE_WINNER=fighter,MK2KS_STAGE_SIDE='1',MK2KS_STAGE_ARENA={'pit':'6','tomb':'1','deadpool':'0'}[move],MK2KS_STAGE_CASE='positive'),37000 if move=='pit' else 12100,'stage'
    if move in ('uppercut','sweep','roundhouse','throw','standing_block','crouching_block'):
        return 'audit_bounded_added_sweep_attack_preparation/prepared_observer.lua',dict(MK2KS_HUMAN_SPECIAL_MOVE='knife' if fighter=='kano' else 'ring',MK2KS_HUMAN_SPECIAL_SIDE='1',MK2KS_HUMAN_SPECIAL_VICTIM='kitana'),3100,'basic'
    raise ValueError(key)


def qualify(text, kind):
    def rows(tag):
        return [dict(re.findall(r'(\w+)=([^\s]+)', line)) for line in text.splitlines() if line.startswith(tag+' ')]
    if kind == 'special':
        r = rows('MK2_HSPECIAL_RESULT')[-1]
        h.need(r['completed']=='2' and int(r['entry'])>0 and int(r['recovered'])>int(r['entry']), 'Two genuine activations and recovery')
        commands=rows('MK2_HSPECIAL_COMMAND')
        damage=[x for x in rows('MK2_HSPECIAL_HEALTH') if x['slot']=='2' and int(x['after'])<int(x['before'])<=161]
        h.need(damage, 'Move must actually damage opponent, not merely activate')
        return max(0,int(commands[0]['frame'])-50),int(r['frame']),dict(result=r,damagingHits=damage)
    if kind == 'fatality':
        r=rows('MK2_STOCK_HEAD_V921_RESULT')[-1]
        h.need(int(r['damage'])>=322 and int(r['wins'])>=2 and int(r['action'])>0 and int(r['wrap'])>int(r['action']), 'Earned fatality with native common completion')
        h.need(not rows('MK2_STOCK_HEAD_V921_CACHE_OVERWRITE'), 'No body cache overwrite')
        return max(0,int(r['action'])-150),int(r['frame']),r
    if kind == 'friendship':
        r=rows('MK2_FRIEND_RESULT')[-1]
        h.need(r['kos']=='2' and int(r['damage'])>=322 and int(r['action'])>0 and r['cleanup']=='true', 'Earned friendship and cleanup')
        return max(0,int(r['action'])-160),int(r['frame']),r
    if kind == 'babality':
        r=rows('MK2_NATIVE_BABY_RESULT')[-1]
        h.need(int(r['wins'])>=2 and int(r['damage'])>=322 and int(r['action'])>0 and rows('MK2_NATIVE_BABY_CONSTRUCT') and rows('MK2_NATIVE_BABY_BABY'), 'Earned babality and visible native baby')
        return max(0,int(r['window'])-30),int(r['frame']),r
    if kind == 'stage':
        r=rows('MK2_STAGE_RESULT')[-1]
        h.need(r['kos']=='2' and int(r['damage'])>=322 and int(r['action'])>0 and int(r['frame'])-int(r['action'])>=1100,'Earned stage action and full followthrough')
        wanted=rows('MK2_STAGE_BOOT')[0]['target_arena']
        h.need(r['action_arena']==wanted,'Actual requested arena')
        fields=rows('MK2_STAGE_FIELD')
        h.need(any(x['own']=='00000000' and x['victim']=='00000000' for x in fields),'Actual native scene retirement')
        if wanted=='0':
            h.need(any(x['entry']=='FF8712A0' and x['arena']=='0' and x['finish']=='3' and x['a3']=='00000003' for x in rows('MK2_STAGE_ACID_GATE')),'Native acid stage action, not just uppercut')
        return max(0,int(r['command'])-100),int(r['frame']),r
    if kind == 'basic':
        ready=rows('MK2_HSPECIAL_READY')[0]
        end=rows('MK2_HSPECIAL_IDLE_TERMINAL')[0]
        fields=rows('MK2_HSPECIAL_FIELD')
        hits=[x for x in rows('MK2_HSPECIAL_CONTACT_HEALTH') if x['slot']=='2' and int(x['after'])<int(x['before'])<=161]
        return int(ready['frame'])+80,int(end['frame']),dict(ready=ready,end=end,damagingHits=hits,ownActions=sorted({int(x['action']) for x in fields if x['slot']=='1'}))
    r=rows('MK2_HUMAN_SHANG_RESULT')[-1]
    h.need(r['forms']=='1' and r['restores']=='1' and r['errors']=='0', 'Morph and native restoration')
    return int(r['match'])+60,int(r['frame']),r


def main():
    parser=argparse.ArgumentParser();parser.add_argument('case');parser.add_argument('--take',default='');args=parser.parse_args()
    source,extra,framecap,kind=plan(args.case)
    h.need(re.fullmatch(r'[a-z0-9_]*',args.take),'Safe take suffix')
    out=ROOT/'videos_showcase_20261015'/(args.case+args.take)
    h.need(not out.exists(), 'Never overwrite executed recording')
    h.need(h.sha(h.EXE)==h.EXPECTED_EXE, 'Current executable pin')
    original=(ROOT/source).read_text()
    if kind=='basic':
        move=args.case.split('_',1)[1]
        first=original.index("  if age>=8 and age<104 and math.abs(a.x-b.x)>85")
        last=original.index('\n  part(1,a);part(2,b)',first)
        gap={'uppercut':55,'sweep':75,'roundhouse':75,'throw':24,'standing_block':40,'crouching_block':40}[move]
        physical=f"  if age>=8 and age<104 and math.abs(a.x-b.x)>{gap} then input(1,a.x<b.x and 'Right' or 'Left')end\n"
        if move in ('sweep','roundhouse'):
            physical+="  if age>=108 and age<116 then input(1,a.x<b.x and 'Left' or 'Right')end\n"
            physical+="  if age>=112 and age<116 then input(1,'"+('Low Kick' if move=='sweep' else 'High Kick')+"')end\n"
        elif move=='uppercut':
            physical+="  if age>=108 and age<180 then input(1,'Down')end\n  if age>=150 and age<156 then input(1,'High Punch')end\n"
        elif move=='throw':
            physical+="  if age>=108 and age<116 then input(1,a.x<b.x and 'Right' or 'Left')end\n  if age>=112 and age<116 then input(1,'Low Punch')end\n"
        else:
            physical+="  if age>=108 and age<170 then input(1,'Block')end\n  if age>=135 and age<139 then input(2,'Low Kick')end\n"
            if move=='crouching_block':physical+="  if age>=108 and age<170 then input(1,'Down')end\n"
        original=original[:first]+physical+original[last:]
    if kind=='fatality' and args.case.endswith('secondary'):
        old='local action_addresses={p:read_u32(0xff8ba210+killer_id*32),p:read_u32(0xff8ba390+killer_id*32)}'
        new='local action_addresses={p:read_u32(p:read_u32(0xff876b50)+killer_id*32),p:read_u32(p:read_u32(0xff876b90)+killer_id*32)}'
        h.need(original.count(old)==1 or original.count(new)==1,'Current secondary native dispatch lookup')
        if old in original:original=original.replace(old,new,1)
    h.need(':write_' not in original and 'read_range' not in original and ':snapshot(' not in original, 'No guest writes or raw dump capture')
    out.mkdir(parents=True)
    for d in ('cfg','nvram','snap'):(out/d).mkdir()
    lua=out/'controller.lua'
    streamlua='''
local capture_screen=manager.machine.screens[':screen']
local capture_pipe=assert(io.open(assert(os.getenv('MK2KS_VIDEO_PIPE')),'wb'))
capture_pipe:setvbuf('no')
local capture_frames=0
emu.register_frame_done(function()
 local pixels=capture_screen:pixels()
 assert(capture_screen.width==400 and capture_screen.height==254 and #pixels==406400)
 assert(capture_pipe:write(pixels));capture_frames=capture_frames+1
 assert(capture_frames<=CAPTURE_BOUND,'Bounded showcase frame limit')
end)
emu.register_stop(function()
 capture_pipe:close()
 print('SHOWCASE_STREAM_STOP frames='..capture_frames..' writes=0')
end)
'''.replace('CAPTURE_BOUND',str(framecap))
    lua.write_text(original+'\n'+streamlua)
    ffmpeg=Path(shutil.which('ffmpeg'));ffprobe=ffmpeg.with_name('ffprobe.exe')
    video=out/'video.mp4';wav=out/'native_audio.wav';final=out/(args.case+'.mp4')
    pipe_name=r'\\.\pipe\mk2ks_showcase_'+str(os.getpid())
    pipe=h.k.CreateNamedPipeW(pipe_name,1,0,1,65536,65536,0,None)
    h.need(pipe not in (None,C.c_void_p(-1).value),'CreateNamedPipe')
    start=time.monotonic();peaks={};limits=[];stream={'bytes':0,'errors':[]}
    encargs=[str(ffmpeg),'-hide_banner','-loglevel','warning','-nostdin','-f','rawvideo','-pixel_format','bgra','-video_size','400x254','-framerate',h.RATE,'-i','pipe:0','-an','-c:v','libx264','-preset','veryfast','-crf','18','-vf','setsar=127/150','-pix_fmt','yuv420p','-y',str(video)]
    env={k:v for k,v in os.environ.items() if not k.startswith(('MK2KS_','MK2_TRACE_','MK2_RANGE_','MK2_P2_','MK2PORT_'))}
    env.update(extra);env['MK2KS_VIDEO_PIPE']=pipe_name
    build=h.EXE.parent
    gameargs=[str(h.EXE),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),'-samplepath',str(build/'samples')+';'+str(ROOT/'samples'),'-artpath',str(ROOT/'artwork'),'-samples','-samplerate','48000','-skip_gameinfo','-nocheat','-inipath',str(out),'-video','none','-sound','none','-noautoframeskip','-frameskip','0','-nothrottle','-str',str(int(framecap/54)+2),'-wavwrite',str(wav),'-cfg_directory',str(out/'cfg'),'-nvram_directory',str(out/'nvram'),'-snapshot_directory',str(out/'snap'),'-autoboot_script',str(lua)]
    with (out/'encoder.log').open('wb') as el,(out/'run.log').open('wb') as gl,(out/'stderr.log').open('wb') as ge:
        encoder=subprocess.Popen(encargs,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=el,bufsize=0,creationflags=h.HIDDEN)
        def reader():
            try:
                h.need(h.k.ConnectNamedPipe(pipe,None) or C.get_last_error()==535,'Pipe connection')
                buffer=C.create_string_buffer(65536);got=W.DWORD()
                while h.k.ReadFile(pipe,buffer,len(buffer),C.byref(got),None) and got.value:
                    data=memoryview(buffer.raw)[:got.value]
                    while data:
                        n=encoder.stdin.write(data);h.need(n and n>0,'Encoder closed');stream['bytes']+=n;data=data[n:]
            except Exception as e:stream['errors'].append(repr(e))
            finally:
                try:encoder.stdin.close()
                except Exception:pass
        thread=threading.Thread(target=reader,daemon=True);thread.start()
        game=subprocess.Popen(gameargs,cwd=ROOT,env=env,stdout=gl,stderr=ge,creationflags=h.HIDDEN)
        processes=[('mame',game,320),('encoder',encoder,384)]
        (out/'launch.json').write_text(json.dumps(dict(source=source,sourceSHA256=h.sha(ROOT/source),controllerSHA256=h.sha(lua),executableSHA256=h.sha(h.EXE),environment=extra,command=gameargs,pids={n:p.pid for n,p,_ in processes},physicalInputsOnly=True),indent=2))
        while any(p.poll() is None for _,p,_ in processes):
            if game.poll() is not None and stream['bytes']==0:
                limits.append('game_exit_before_video_pipe')
                # Release the reader's synchronous ConnectNamedPipe before
                # closing its handle if Lua failed before opening the pipe.
                try:
                    with open(pipe_name,'wb'):
                        pass
                except OSError:
                    pass
            for name,p,cap in processes:
                if p.poll() is None:
                    peaks[name]=max(peaks.get(name,0),h.memory(p.pid))
                    if peaks[name]>cap*1024**2:limits.append(name+'_memory')
            peaks['host']=max(peaks.get('host',0),h.memory(os.getpid()))
            if peaks['host']>128*1024**2:limits.append('host_memory')
            if time.monotonic()-start>240:limits.append('wall240')
            for path,cap in ((wav,140 if kind=='stage' else 24),(video,96 if kind=='stage' else 32),(out/'run.log',16)):
                if path.exists() and path.stat().st_size>cap*1024**2:limits.append(path.name+'_size')
            if limits:
                for _,p,_ in processes:
                    if p.poll() is None:p.kill()
                break
            time.sleep(.1)
        for _,p,_ in processes:p.wait(timeout=3)
        thread.join(timeout=2)
    h.k.CloseHandle(pipe)
    frames=stream['bytes']//406400
    (out/'terminal.json').write_text(json.dumps(dict(peaks=peaks,limits=limits,stream=stream,frames=frames,exitCodes={n:p.returncode for n,p,_ in processes},elapsedSeconds=time.monotonic()-start),indent=2))
    h.need(not limits and not stream['errors'] and stream['bytes']%406400==0 and 0<frames<=framecap,'Complete bounded native stream')
    h.need(all(p.returncode==0 for _,p,_ in processes) and not (out/'stderr.log').read_text().strip(),'Game and encoder success')
    text=(out/'run.log').read_text();first,last,evidence=qualify(text,kind)
    if kind=='basic':
        move=args.case.split('_',1)[1]
        if move.endswith('block'):
            h.need((1793 if move=='crouching_block' else 1792) in evidence['ownActions'],'Native correct guard action')
        else:h.need(evidence['damagingHits'],'Basic attack actually damages target')
    vp=h.probe(ffprobe,video);ap=h.probe(ffprobe,wav)
    v=next(s for s in vp['streams'] if s['codec_type']=='video');a=next(s for s in ap['streams'] if s['codec_type']=='audio')
    h.need(int(v['nb_frames'])==frames and abs(float(a['duration'])-frames*146234/8000000)<.09,'Native audio/video frame duration')
    offset=first*146234/8000000;duration=(min(last,frames)-first)*146234/8000000
    mux=[str(ffmpeg),'-hide_banner','-loglevel','warning','-nostdin','-ss',str(offset),'-i',str(video),'-ss',str(offset),'-i',str(wav),'-t',str(duration),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','veryfast','-crf','18','-vf','setsar=127/150','-c:a','aac','-b:a','128k','-movflags','+faststart',str(final)]
    subprocess.run(mux,check=True,capture_output=True,timeout=90,creationflags=h.HIDDEN)
    fp=h.probe(ffprobe,final)
    h.need({s['codec_type'] for s in fp['streams']}=={'audio','video'} and abs(float(fp['format']['duration'])-duration)<.1,'Final AV duration')
    (out/'verification.json').write_text(json.dumps(dict(passed=True,case=args.case,kind=kind,firstNativeFrame=first,lastNativeFrame=min(last,frames),nativeStreamFrames=frames,evidence=evidence,finalSHA256=h.sha(final),finalProbe=fp,visualReviewPending=True,temporaryMediaDeleted=True),indent=2))
    h.need(video.resolve().parent==out.resolve() and wav.resolve().parent==out.resolve(),'Exact intermediates')
    video.unlink();wav.unlink()
    print('RECORDED',args.case,final)


if __name__=='__main__':main()
