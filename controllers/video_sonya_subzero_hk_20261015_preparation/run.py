"""Fresh, bounded, streaming smoke only. No historic imports or frame queues."""
import ctypes as C
from ctypes import wintypes as W
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import threading
import time

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'video_sonya_subzero_hk_20261015'
EXE=ROOT/'diagnostic_native_selector_layers_long/mkport_candidate.exe'
LUA=ROOT/'video_sonya_subzero_hk_20261015_preparation/campaign.lua'
EXPECTED_EXE='EBDFEB6CCA3617308F1448A4A0F6778E3E787420CACF3D11E9B4F40358C87F6A'
HIDDEN=0x08000000
RATE='8000000/146234'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest().upper()
def need(v,m):
 if not v:raise RuntimeError(m)

k=C.WinDLL('kernel32',use_last_error=True)
ps=C.WinDLL('psapi',use_last_error=True)
k.CreateNamedPipeW.argtypes=[W.LPCWSTR,W.DWORD,W.DWORD,W.DWORD,W.DWORD,W.DWORD,W.DWORD,C.c_void_p]
k.CreateNamedPipeW.restype=W.HANDLE
k.ConnectNamedPipe.argtypes=[W.HANDLE,C.c_void_p];k.ConnectNamedPipe.restype=W.BOOL
k.ReadFile.argtypes=[W.HANDLE,C.c_void_p,W.DWORD,C.POINTER(W.DWORD),C.c_void_p];k.ReadFile.restype=W.BOOL
k.CloseHandle.argtypes=[W.HANDLE];k.CloseHandle.restype=W.BOOL
k.OpenProcess.argtypes=[W.DWORD,W.BOOL,W.DWORD];k.OpenProcess.restype=W.HANDLE
k.GetCurrentProcess.restype=W.HANDLE
class Counters(C.Structure):
 _fields_=[('cb',W.DWORD),('PageFaultCount',W.DWORD),('PeakWorkingSetSize',C.c_size_t),('WorkingSetSize',C.c_size_t),('QuotaPeakPagedPoolUsage',C.c_size_t),('QuotaPagedPoolUsage',C.c_size_t),('QuotaPeakNonPagedPoolUsage',C.c_size_t),('QuotaNonPagedPoolUsage',C.c_size_t),('PagefileUsage',C.c_size_t),('PeakPagefileUsage',C.c_size_t),('PrivateUsage',C.c_size_t)]
ps.GetProcessMemoryInfo.argtypes=[W.HANDLE,C.c_void_p,W.DWORD];ps.GetProcessMemoryInfo.restype=W.BOOL
def memory(pid):
 h=k.OpenProcess(0x1000|0x10,False,pid)
 if not h:return 0
 try:
  c=Counters();c.cb=C.sizeof(c)
  return c.WorkingSetSize if ps.GetProcessMemoryInfo(h,C.byref(c),c.cb) else 0
 finally:k.CloseHandle(h)
def probe(ffprobe,path):
 p=subprocess.run([str(ffprobe),'-v','error','-show_streams','-show_format','-of','json',str(path)],capture_output=True,text=True,timeout=5,creationflags=HIDDEN,check=True)
 return json.loads(p.stdout)

def main():
 need(os.name=='nt','Windows namedpipe smoke')
 need(not OUT.exists(),'Never overwrite an executed smoke')
 need(sha(EXE)==EXPECTED_EXE,'Current executable changed')
 need(sha(LUA)=='D29AF0C4BA9EBE8BFA3C2BE4B8BF0DD94A354CFDB4DD2D916E053FF8F47EE42A','Prepared controller changed')
 ffmpeg=Path(shutil.which('ffmpeg') or '')
 ffprobe=ffmpeg.with_name('ffprobe.exe')
 need(ffmpeg.is_file() and ffprobe.is_file(),'Installed ffmpeg/ffprobe required')
 OUT.mkdir()
 for d in ['cfg','nvram','snap']:(OUT/d).mkdir()
 pipe_name=r'\\.\pipe\mk2ks_video_smoke_'+str(os.getpid())
 pipe=k.CreateNamedPipeW(pipe_name,1,0,1,65536,65536,0,None)
 need(pipe not in (None,C.c_void_p(-1).value),'CreateNamedPipe failed')
 video=OUT/'video.mp4';wav=OUT/'native_audio.wav';final=OUT/'Sonya_full_playthrough.mp4'
 start=time.monotonic();peaks={};limits=[];stream={'bytes':0,'errors':[]}
 encoder_args=[str(ffmpeg),'-hide_banner','-loglevel','warning','-nostdin','-f','rawvideo','-pixel_format','bgra','-video_size','400x254','-framerate',RATE,'-i','pipe:0','-an','-c:v','libx264','-preset','veryfast','-crf','20','-vf','setsar=127/150','-pix_fmt','yuv420p','-movflags','+faststart','-y',str(video)]
 processes=[]
 with (OUT/'encoder.stderr.log').open('wb') as enc_log,(OUT/'run.log').open('wb') as game_log,(OUT/'stderr.log').open('wb') as game_err:
  encoder=subprocess.Popen(encoder_args,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=enc_log,bufsize=0,creationflags=HIDDEN)
  processes.append(('ffmpeg',encoder,384*1024**2))
  def reader():
   try:
    if not k.ConnectNamedPipe(pipe,None):
     need(C.get_last_error()==535,'ConnectNamedPipe error '+str(C.get_last_error()))
    buffer=C.create_string_buffer(65536);got=W.DWORD()
    while True:
     if not k.ReadFile(pipe,buffer,len(buffer),C.byref(got),None):
      err=C.get_last_error()
      if err in (109,232):break
      raise OSError(err,'ReadFile')
     if not got.value:break
     data=memoryview(buffer.raw)[:got.value]
     while data:
      wrote=encoder.stdin.write(data)
      need(wrote and wrote>0,'Encoder pipe closed')
      stream['bytes']+=wrote;data=data[wrote:]
   except Exception as e:stream['errors'].append(repr(e))
   finally:
    try:encoder.stdin.close()
    except Exception:pass
  thread=threading.Thread(target=reader,daemon=True);thread.start()
  env={n:v for n,v in os.environ.items() if not n.startswith(('MK2KS_','MK2_TRACE_','MK2_RANGE_','MK2_P2_','MK2PORT_'))}
  env['MK2KS_VIDEO_PIPE']=pipe_name
  env.update(MK2KS_TEST_FIGHTER='sonya',MK2KS_CAMPAIGN_SIDE='2',MK2KS_CAMPAIGN_STRATEGY='guard_punish',MK2KS_TEST_BOOT_FRAME='600')
  build=EXE.parent
  args=[str(EXE),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),'-samplepath',str(build/'samples')+';'+str(ROOT/'samples'),'-artpath',str(ROOT/'artwork'),'-samples','-samplerate','48000','-skip_gameinfo','-nocheat','-inipath',str(OUT),'-video','none','-sound','none','-noautoframeskip','-frameskip','0','-nothrottle','-str','2500','-snapsize','400x254','-wavwrite',str(wav),'-cfg_directory',str(OUT/'cfg'),'-nvram_directory',str(OUT/'nvram'),'-snapshot_directory',str(OUT/'snap'),'-autoboot_script',str(LUA)]
  game=subprocess.Popen(args,cwd=ROOT,env=env,stdout=game_log,stderr=game_err,creationflags=HIDDEN)
  processes.append(('mame',game,320*1024**2))
  (OUT/'launch.json').write_text(json.dumps(dict(executableSHA256=sha(EXE),luaSHA256=sha(LUA),ffmpeg=str(ffmpeg),ffmpegSHA256=sha(ffmpeg),ffprobeSHA256=sha(ffprobe),mame=args,encoder=encoder_args,guestWrites=False,inputs='physical controller only'),indent=2))
  while any(p.poll() is None for _,p,_ in processes):
   for name,p,cap in processes:
    if p.poll() is None:
     peaks[name]=max(peaks.get(name,0),memory(p.pid))
     if peaks[name]>cap:limits.append(name+'_memory')
   peaks['host']=max(peaks.get('host',0),memory(os.getpid()))
   if peaks['host']>128*1024**2:limits.append('host_memory')
   if time.monotonic()-start>600:limits.append('wall600')
   if wav.exists() and wav.stat().st_size>450*1024**2:limits.append('wav450MiB')
   if video.exists() and video.stat().st_size>250*1024**2:limits.append('video250MiB')
   if game_log.tell()+game_err.tell()>20*1024**2:limits.append('text20MiB')
   if limits:
    for _,p,_ in processes:
     if p.poll() is None:p.kill()
    break
   time.sleep(.1)
  for _,p,_ in processes:p.wait(timeout=3)
  thread.join(timeout=2)
 k.CloseHandle(pipe)
 terminal=dict(elapsedSeconds=time.monotonic()-start,peaks=peaks,limits=limits,stream=stream,exitCodes={n:p.returncode for n,p,_ in processes},rawFramesStored=False,audioTemporary=str(wav),fullPlaythrough=False)
 (OUT/'terminal.json').write_text(json.dumps(terminal,indent=2))
 need(not limits and not stream['errors'] and stream['bytes']%406400==0,'Complete bounded frame stream')
 frames=stream['bytes']//406400
 need(0<frames<=120000,'Frame count bound')
 import re
 text=(OUT/'run.log').read_text()
 def rows(tag):
  return [dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in text.splitlines() if line.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]
 result=rows('RESULT');need(len(result)==1,'Actual controller result')
 r=result[0];need(int(r['ending'])>0 and int(r['ending_completed'])>int(r['ending']),'Actual earned ending completion')
 fights=rows('FIGHT');need({int(x['stage']) for x in fights}==set(range(13))|{14,15,16},'Entire native ladder and both bosses')
 need(all(x['human']=='18:18' for x in fights),'True Sonya throughout campaign')
 need({x['page'] for x in rows('PICTURE')}=={'1','2'} and {x['page'] for x in rows('TEXT')}=={'1','2'},'Both own ending pictures and text')
 need(any(x['stage']=='16' and x['winner']=='2' and x['health'].split(',')[0]=='0' and int(x['health'].split(',')[1])>0 for x in rows('ENDING_START')),'Native earned Shao KO enters own ending')
 need(sum(x['slot']=='2' and x['stage']=='15' for x in rows('WIN'))>=2,'Actual own Kintaro round wins')
 need('VIDEO_FULL_STOP frames='+str(frames) in text,'Stream/controller stop binding')
 need(all(p.returncode==0 for _,p,_ in processes),'Encoder/game success')
 need(not (OUT/'stderr.log').read_text().strip(),'Lua/game errors')
 v=probe(ffprobe,video);a=probe(ffprobe,wav)
 vs=next(s for s in v['streams'] if s['codec_type']=='video')
 aud=next(s for s in a['streams'] if s['codec_type']=='audio')
 need(int(vs['nb_frames'])==frames and int(vs['width'])==400 and int(vs['height'])==254,'Encoded frame geometry/count')
 expected=frames*146234/8000000
 need(abs(float(vs['duration'])-expected)<.04 and abs(float(aud['duration'])-expected)<.08,'Native audio/video durations')
 muxargs=[str(ffmpeg),'-hide_banner','-loglevel','warning','-nostdin','-i',str(video),'-i',str(wav),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','128k','-movflags','+faststart','-y',str(final)]
 # Mux is only2.2sec native audio. Apply same wall/memory/output limits.
 with (OUT/'mux.stderr.log').open('wb') as log:
  mux=subprocess.Popen(muxargs,stdout=subprocess.DEVNULL,stderr=log,creationflags=HIDDEN)
  while mux.poll() is None:
   peaks['mux']=max(peaks.get('mux',0),memory(mux.pid))
   if peaks['mux']>384*1024**2 or time.monotonic()-start>600 or (final.exists() and final.stat().st_size>250*1024**2):
    mux.kill();mux.wait();raise RuntimeError('Mux resource limit')
   time.sleep(.05)
  need(mux.returncode==0,'AAC mux success')
 final_probe=probe(ffprobe,final)
 need({s['codec_type'] for s in final_probe['streams']}=={'video','audio'},'Final nativeAV streams')
 need(next(s for s in final_probe['streams'] if s['codec_type']=='video')['nb_frames']==str(frames),'Final120frames')
 need(abs(float(final_probe['format']['duration'])-expected)<.10,'Final timing')
 # Exact validated fresh runtime child only; no glob deletion.
 need(wav.resolve().parent==OUT.resolve() and wav.name=='native_audio.wav','Exact temporaryWAV containment')
 wav.unlink()
 need(video.resolve().parent==OUT.resolve() and video.name=='video.mp4','Exact intermediate containment')
 video.unlink()
 (OUT/'verification.json').write_text(json.dumps(dict(passed=True,smokeOnly=False,videoProbe=v,audioProbe=a,finalProbe=final_probe,finalSHA256=sha(final),temporaryWAVDeleted=True,frameRate=RATE,streamedFrames=frames,encodedFrames=frames,captureBoundary='Every native frame through actual own two-page ending and300fields; all paid losses/continues retained. Native audio recorded; not edited into a win.',bgraVisualReviewPending=True,fullPlaythrough=True),indent=2))
 print(OUT)
if __name__=='__main__':main()
