"""Prepare full capture from proven physical Lua and tested streaming host, as text."""
import ast
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'video_kano_full_20261015_preparation'
assert not OUT.exists()
source=ROOT/'audit_current_kano_p2_shao_backjump_charge_counter_preparation/campaign.lua'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
assert sha(source)=='7134EDA5CC19CC8C0C3D54E7BEEB195C10F9C459ACE7173AE0A67AB68FA43326'
old=source.read_text()
# All discarded snapshots were already no-ops. Remove these call lines, not inputs.
lua='\n'.join(line for line in old.splitlines() if 'discard_snapshot' not in line)+'\n'
assert 'screen:pixels' not in lua and ':write_' not in lua and 'read_block' not in lua
assert 'screen:snapshot' not in lua and 'loadstate' not in lua
lua=lua.replace('frame>=120000','frame>=80000').replace('maximum_fields=120000','maximum_fields=80000')
lua+='''
-- Stream every native video frame. Existing physical policy is unchanged.
local video_pipe=assert(io.open(assert(os.getenv('MK2KS_VIDEO_PIPE')),'wb'))
video_pipe:setvbuf('no')
local video_frames=0
emu.register_frame_done(function()
 local raw=screen:pixels();local w,h=screen.width,screen.height
 assert(w==400 and h==254 and #raw==406400)
 assert(video_pipe:write(raw));video_frames=video_frames+1
 if video_frames==1 or video_frames%3000==0 then
  print(string.format('VIDEO_FULL frames=%d controller_frame=%d guest_seconds=%.12f',video_frames,frame,manager.machine.time:as_double()))
 end
 assert(video_frames<=80000,'Video frame bound')
end)
emu.register_stop(function()
 if video_pipe then video_pipe:close();video_pipe=nil end
 print(string.format('VIDEO_FULL_STOP frames=%d controller_frame=%d ending=%d ending_completed=%d guestwrites=0',video_frames,frame,ending or-1,ending_completed or-1))
end)
'''
OUT.mkdir();(OUT/'campaign.lua').write_text(lua)
host=(ROOT/'tools/run_video_stream_smoke_20261015.py').read_text()
host=host.replace("OUT=ROOT/'audit_video_stream_smoke_20261015'", "OUT=ROOT/'video_kano_full_20261015'")
host=host.replace("LUA=ROOT/'tools/video_stream_smoke_20261015.lua'", "LUA=ROOT/'video_kano_full_20261015_preparation/campaign.lua'")
host=host.replace(" need(sha(EXE)==EXPECTED_EXE,'Current executable changed')", " need(sha(EXE)==EXPECTED_EXE,'Current executable changed')\n need(sha(LUA)=='"+sha(OUT/'campaign.lua')+"','Prepared controller changed')")
host=host.replace("'mk2ks_video_smoke_'", "'mk2ks_video_kano_full_'")
host=host.replace("final=OUT/'smoke.mp4'", "final=OUT/'Kano_full_playthrough.mp4'")
host=host.replace("  env['MK2KS_VIDEO_PIPE']=pipe_name", "  env['MK2KS_VIDEO_PIPE']=pipe_name\n  env.update(MK2KS_TEST_FIGHTER='kano',MK2KS_CAMPAIGN_SIDE='2',MK2KS_CAMPAIGN_STRATEGY='zoning',MK2KS_TEST_BOOT_FRAME='600')")
host=host.replace("'-str','5'", "'-str','2500'")
host=host.replace('>30:', '>600:').replace("'wall30'", "'wall600'")
oldcap="   if sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file())>64*1024**2:limits.append('output64MiB')"
assert oldcap in host
host=host.replace(oldcap,"""   if wav.exists() and wav.stat().st_size>350*1024**2:limits.append('wav350MiB')
   if video.exists() and video.stat().st_size>250*1024**2:limits.append('video250MiB')
   if game_log.tell()+game_err.tell()>20*1024**2:limits.append('text20MiB')""")
host=host.replace("need(not limits and not stream['errors'] and stream['bytes']==120*400*254*4,'Bounded complete120frame stream')", """need(not limits and not stream['errors'] and stream['bytes']%406400==0,'Complete bounded frame stream')
 frames=stream['bytes']//406400
 need(0<frames<=80000,'Frame count bound')
 import re
 text=(OUT/'run.log').read_text()
 def rows(tag):
  return [dict(re.findall(r'(\\w+)=([^\\s]+)',line)) for line in text.splitlines() if line.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]
 result=rows('RESULT');need(len(result)==1,'Actual controller result')
 r=result[0];need(int(r['ending'])>0 and int(r['ending_completed'])>int(r['ending']),'Actual earned ending completion')
 fights=rows('FIGHT');need({int(x['stage']) for x in fights}==set(range(13))|{14,15,16},'Entire native ladder and both bosses')
 need(all(x['human']=='17:17' for x in fights),'True Kano throughout campaign')
 need({x['page'] for x in rows('PICTURE')}=={'1','2'} and {x['page'] for x in rows('TEXT')}=={'1','2'},'Both own ending pictures and text')
 need(any(x['stage']=='16' and x['winner']=='2' and x['health'].split(',')[0]=='0' and int(x['health'].split(',')[1])>0 for x in rows('ENDING_START')),'Native earned Shao KO enters own ending')
 need(sum(x['slot']=='2' and x['stage']=='15' for x in rows('WIN'))>=2,'Actual own Kintaro round wins')
 need('VIDEO_FULL_STOP frames='+str(frames) in text,'Stream/controller stop binding')""")
host=host.replace("int(vs['nb_frames'])==120", "int(vs['nb_frames'])==frames")
host=host.replace('expected=120*146234/8000000','expected=frames*146234/8000000')
host=host.replace("['nb_frames']=='120'", "['nb_frames']==str(frames)")
host=host.replace("time.monotonic()-start>30 or sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file())>64*1024**2", "time.monotonic()-start>600 or (final.exists() and final.stat().st_size>250*1024**2)")
host=host.replace(' wav.unlink()', " wav.unlink()\n need(video.resolve().parent==OUT.resolve() and video.name=='video.mp4','Exact intermediate containment')\n video.unlink()")
host=host.replace('smokeOnly=True','smokeOnly=False').replace('streamedFrames=120,encodedFrames=120','streamedFrames=frames,encodedFrames=frames').replace('fullPlaythrough=False','fullPlaythrough=True')
host=host.replace("rawFramesStored=False,audioTemporary=str(wav),fullPlaythrough=True", "rawFramesStored=False,audioTemporary=str(wav),fullPlaythrough=False")
host=host.replace("inputs=False)", "inputs='physical controller only')")
host=host.replace("'First native frame_done to120th; exact field log times retained; hardware/audio quality not judged.'", "'Every native frame through actual own two-page ending and300fields; all paid losses/continues retained. Native audio recorded; not edited into a win.'")
host=host.replace("'Bounded complete120frame stream'", "'Complete frame stream'")
ast.parse(host)
assert '120*400*254' not in host and 'expected=120' not in host and '>30' not in host
(OUT/'run.py').write_text(host)
(OUT/'preparation.json').write_text(json.dumps(dict(preparedNotRun=True,controllerSource=str(source),controllerSHA256=sha(source),luaSHA256=sha(OUT/'campaign.lua'),runnerSHA256=sha(OUT/'run.py'),changes='Remove no-op snapshot lines; controllerbound120000to80000; append singleframe streaming observer only. All physical controls/native taps retained.',limits='80000frames/600sec/MAME320MiB/ffmpeg384MiB/host128MiB/WAV350MiB/video250MiB/text20MiB',authenticity='Actual currentcold earned full ladder/bosses/ownending required; no state writes or staged opponents. If controller fails, capturedvideo cannot be labelled successful fullplaythrough.',rawFrameDisk=False),indent=2))
print(OUT)
