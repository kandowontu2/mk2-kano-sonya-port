"""Original isolated Kano group4 DCS asset oracle, six native jobs, RAM PCM.

Source0x0208503D implies channel variants0208..020C. Keep whole equal-clock
buffers, delivery delay and complete tail. Only0.70 output-route compensation;
no fade, gain fit, guest state writes, gameplay or port acceptance claim.
"""
import argparse,datetime,gzip,hashlib,json,os,re,subprocess,wave
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'audit_v6633_kano_launch_donor_oracle'
COMMANDS=['baseline',*['%04x'%i for i in range(0x208,0x20d)]]
def need(v,m):
 if not v:raise ValueError(m)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def run(command):
 out=OUT/command;need(not out.exists(),'Fresh native oracle command leaf, no restart/overwrite')
 exe=ROOT.parent/'hbmame/hbmame.exe';lua=ROOT/'mk3_cannonball_launch_isolated_ram_v6631.lua'
 paths=[exe,lua,ROOT/'mk3_friendship_isolated_time_v772.lua',ROOT/'mk3_isolated_sound_probe.lua',Path(__file__),
        ROOT/'mk3/mk3-maincpu.bin',*list((ROOT/'mk3').glob('*music_spch*'))]
 pins={str(p.resolve()):sha(p)for p in paths};out.mkdir(parents=True)
 env={k:v for k,v in os.environ.items()if not k.startswith('MK3_PROBE_')}
 env.update(MK3_PROBE_SOUND_U8='1',MK3_PROBE_SOUND_GAP_US='25',MK3_PROBE_TRACE_PORT='1')
 if command!='baseline':env['MK3_PROBE_SOUND_CMD']=command
 args=[str(exe),'mk3','-rompath',str(ROOT)+';'+str(ROOT.parent/'mame0289/roms'),'-nocheat','-skip_gameinfo',
  '-inipath',str(out),'-cfg_directory',str(out/'cfg'),'-nvram_directory',str(out/'nvram'),'-snapshot_directory',str(out/'snap'),
  '-video','none','-sound','none','-samplerate','48000','-nothrottle','-str','35','-autoboot_script',str(lua)]
 process=subprocess.Popen(args,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',errors='replace')
 print(command+' native donor PID='+str(process.pid),flush=True)
 (out/'process.json').write_text(json.dumps(dict(pid=process.pid,command=args,startedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2)+'\n')
 chunks=[];headers=[];text=[];errors=[]
 # Bound stdout collector owns the only raw PCM buffers, never writes them.
 with gzip.open(out/'run.log.gz','wt',encoding='utf-8')as log:
  for line in process.stdout:
   if line.startswith('MK3_LAUNCH_PCM '):
    q=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(q.pop('hex'))
    need(len(raw)==int(q['bytes'])and len(raw)%4==0,'Complete interleaved native16-bit stereo PCM')
    q['sha256']=hashlib.sha256(raw).hexdigest().upper();chunks.append(raw);headers.append(q)
    log.write('MK3_LAUNCH_PCM_DIGEST '+' '.join(k+'='+v for k,v in q.items())+'\n')
   else:log.write(line);text.append(line)
  stderr=process.stderr.read();exitcode=process.wait()
 (out/'stderr.log').write_text(stderr)
 result=dict(passed=False,command=command,nativeExit=exitcode,pid=process.pid,inputHashes=pins,
             hardwareOnlyNotGameplayAcceptance=True,guestRAMWrites=0,nativePCMHeaders=headers)
 try:
  need(exitcode==0 and not stderr.strip()and any(l.startswith('MK3_LAUNCH_ORACLE_TERMINAL frame=1500 ')for l in text),
       'Actual natural donor terminal, no str/deadline substitute or observer error')
  need(headers and all(q['bytes']=='3840'for q in headers)and all(sha(p)==h for p,h in pins.items()),'Whole consecutive native oracle and source inputs intact')
  need(not any(re.search(r'LUA ERROR|Lua error|stack traceback|fatal error',l,re.I)for l in text),'No original observer/runtime error')
  times=np.array([float(q['seconds'])for q in headers]);need(np.all(np.abs(np.diff(times)-.02)<1e-9),'All scheduled50Hz native audio callbacks, no skipped fields')
  result['passed']=True
 except Exception as error:result['error']=repr(error)
 (out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(command=command,passed=result['passed'],chunks=len(chunks),error=result.get('error'))),flush=True)
 need(result['passed'],'Preserve original isolated oracle rejection')
 return dict(report=result,text=''.join(text),raw=b''.join(chunks))

def main():
 need(not OUT.exists(),'Fresh complete donor asset oracle; no duplicate native jobs')
 OUT.mkdir();subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True,check=True)
 values={c:run(c)for c in COMMANDS};base=values['baseline'];rawbase=np.frombuffer(base['raw'],dtype='<i2').reshape(-1,2).astype(np.int32)
 rows=[];deltas={};first_time=None;pins={}
 for command,value in values.items():
  pins.update(value['report']['inputHashes'])
  need([(q['frame'],q['seconds'],q['bytes'])for q in value['report']['nativePCMHeaders']]==
       [(q['frame'],q['seconds'],q['bytes'])for q in base['report']['nativePCMHeaders']],
       'Every baseline/channel native audio callback clock/dimension matches, no fit/trim')
  if command=='baseline':continue
  records=re.findall(r'MK3_FRIEND_ISOLATED_TIME frame=\d+ seconds=([\d.]+) address=01680000 data=([\dA-F]{4}) mask=00FF',value['text'])
  need(len(records)==2 and [int(q[1],16)for q in records]==[int(command,16)>>8,int(command,16)&255],
       'Exactly original high/low command bytes at native hardware, no memory writes')
  seconds=float(records[0][0]);need(abs(float(records[1][0])-seconds-.000025)<1e-9,'Exact original25us hardware command interval')
  need(first_time is None or first_time==seconds,'Identical original delivery time for every channel');first_time=seconds
  samples=np.frombuffer(value['raw'],dtype='<i2').reshape(-1,2).astype(np.int32);delta=samples-rawbase
  start=round((seconds-(float(base['report']['nativePCMHeaders'][0]['seconds'])-.02))*48000)
  need(not np.any(delta[:start])and np.array_equal(delta[:,0],delta[:,1]),'No predelivery difference; native stereo cue is dual mono')
  deltas[command]=delta[:,0];rows.append(dict(command=command,seconds=seconds,pcmSHA256=hashlib.sha256(value['raw']).hexdigest().upper()))
 need(all(np.array_equal(deltas['0208'],deltas[c])for c in COMMANDS[2:]),'All5 original native launch channel variants exactly equal')
 delta=deltas['0208'];nz=np.flatnonzero(delta);need(len(nz)>0,'Actual original Kano launch waveform present')
 end=int(nz[-1])+3;need(end<len(delta)-48000 and not np.any(delta[end:]),'Complete original audio tail and at least1s verified silence')
 source=delta[start:end];scaled=np.rint(source/.70);need(np.max(np.abs(scaled))<32767 and np.max(np.abs(scaled*.70-source))<=.35+1e-8,'Lossless native0.70 route compensation within integer quantization, no clipping/creative gain')
 pcm=scaled.astype('<i2');asset=OUT/'kano_ball_launch.wav';need(not asset.exists(),'New staged authored audio asset')
 with wave.open(str(asset),'wb')as w:w.setparams((1,2,48000,0,'NONE','not compressed'));w.writeframes(pcm.tobytes())
 pins[str(asset)]=sha(asset)
 result=dict(passed=True,command=0x208,nativeChannelVariants=5,allVariantsExactlyEqual=True,frames=len(pcm),route=.70,
  firstPCMDelaySeconds=(int(nz[0])-start)/48000,wholeSourcePCM_SHA256=hashlib.sha256(source.astype('<i2').tobytes()).hexdigest().upper(),
  stagedAsset=str(asset),assetSHA256=sha(asset),actualNativeJobs=6,deliveryCases=rows,inputHashes=pins,
  hardwareOnlyNotGameplayAcceptance=True,fullPortAcceptance=False,newBuilds=0,newROMCopies=0,rawPCMTransportFiles=0)
 (OUT/'asset_report.json').write_text(json.dumps(result,indent=2)+'\n')
 for p in OUT.rglob('*'):
  if p.is_file():
   h=sha(p);subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True,check=True);need(sha(p)==h,'Lossless donor evidence compression')
 print(json.dumps({k:result[k]for k in ('passed','frames','firstPCMDelaySeconds','actualNativeJobs','assetSHA256','hardwareOnlyNotGameplayAcceptance')}),flush=True)
if __name__=='__main__':main()
