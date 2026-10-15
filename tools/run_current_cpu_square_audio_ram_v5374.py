"""Natural CPU Square: full launch waveform, native ownership and finite cleanup."""
import hashlib,json,os,re,subprocess,traceback,wave
from pathlib import Path
import numpy as np
from scipy.signal import fftconvolve
import current_payload_metadata_context_v5229 as current
import native_cpu_square_hit_contract_v3037 as phase
import verify_native_extended_cpu_v2946 as ledgers
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5376_current_cpu_square_audio_ram_checked'
LUA=ROOT/'mk2ks_cpu_square_audio_ram_v5374.lua'
ASSET=ROOT/'samples/mk2ks/sonya_square_launch.wav'
CHAIN=('mk2ks_physical_p2_cpu_continuation_v1997.lua','mk2ks_physical_p2_cpu_round_trace_v1998.lua',
 'mk2ks_physical_p2_cpu_overlap_trace_v1999.lua','mk2ks_physical_p2_cpu_choice_trace_v2035.lua',
 'mk2ks_physical_p2_cpu_square_trace_v2038.lua','mk2ks_native_cpu_square_boundary_v2993.lua',
 'mk2ks_native_cpu_square_locks_v3000.lua','mk2ks_cpu_bicycle_hit_audio_v3396.lua')
PREFIXES=('MK2_CPU_PAIR_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_','MK2_CPU_CHOICE_','MK2_SQUARE_NATIVE_','MK2_P2CPU_','MK2_SQUARE_BOUNDARY_','MK2_SQUARE_LOCK_')

def records(log,tag):
 result=[]
 for line in log.splitlines():
  if line.startswith('MK2_BBAUDIO_'+tag+' '):
   fields=re.findall(r'(\w+)=([^\s]+)',line);need(len(fields)==len(dict(fields)),'Unambiguous complete actual audio record');result.append(dict(fields))
 return result

def capture(enabled,guest):
 folder=ROOT/f'audit_v5375_current_cpu_square_audio_ram_{"samples"if enabled else"nosamples"}'
 need(not folder.exists(),'Fresh immutable physical audio capture')
 build=ROOT/current.NAME;meta=json.loads((build/'build-info.json').read_text(encoding='utf-8-sig'))
 scene_path=ROOT/'audit_v5371_current_cpu_square_scene_ram_checked/report.json'
 audio_path=ROOT/'audit_v5325_current_cpu_bicycle_ram_checked/report.json'
 scene=json.loads(scene_path.read_text());audio=json.loads(audio_path.read_text())
 need(scene['passed']and audio['passed'],'Original full physical Square and audio observer qualification')
 pins=dict(meta['input_hashes'])
 for name in CHAIN:
  path=ROOT/name;accepted=audio if name.endswith('v3396.lua')else scene
  need(sha(path)==accepted['inputHashes'][str(path)],'Every original actually executed observer source unchanged')
  need(not re.search(r':write_|write_[ui]\d+|\.value\s*=(?!=)|load_?state|:reset\(',path.read_text()),'No actor/state/HP/RNG/audio injection')
 for path in [*(ROOT/n for n in CHAIN),LUA,ASSET,Path(__file__),Path(current.__file__),scene_path,audio_path,
  build/'mkport_candidate.exe',build/'roms/mk2ks/mk2ks.mdata',build/'build-info.json',
  ROOT/'mame-mkp/src/emu/sound.cpp',ROOT/'mame-mkp/src/devices/sound/samples.cpp']:
  pins[str(path.resolve())]=sha(path)
 folder.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(folder)],capture_output=True).returncode==0,'Inherited trace compression')
 (folder/'input_hashes_before.json').write_text(json.dumps(pins,indent=2)+'\n')
 env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
 env.update(MK2KS_TEST_FIGHTER='kano',MK2KS_TEST_BOOT_FRAME='613',MK2KS_CPU_PAIR_APPROACH='guard_until_close',MK2KS_CPU_CONTINUATION_POLICY='jump_guard',MK2KS_CPU_PAIR_CONFIRM_AGE='264')
 command=[str(build/'mkport_candidate.exe'),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),'-samplepath',str(ROOT/'samples'),
  '-samples'if enabled else'-nosamples','-artpath',str(ROOT/'artwork'),'-skip_gameinfo','-nocheat','-inipath',str(folder),
  '-video','none','-sound','none','-samplerate','48000','-noautoframeskip','-frameskip','0','-nothrottle','-str','100',
  '-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),'-snapshot_directory',str(folder/'snap'),'-autoboot_script',str(LUA)]
 chunks=[];headers=[];guest_seen=False
 with(folder/'stderr.log').open('w',encoding='utf-8')as err,subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',errors='strict')as process:
  (folder/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command),indent=2)+'\n');print(folder.name+': actual native PID='+str(process.pid),flush=True)
  with(folder/'run.log').open('w',encoding='utf-8')as log:
   for line in process.stdout:
    if line.startswith(('MK2_BBAUDIO_PCM ','MK2_SQAUDIO_GUEST ')):
     fields=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(fields.pop('hex'));need(len(raw)==int(fields['bytes']),'Every raw native buffer complete')
     fields['sha256']=hashlib.sha256(raw).hexdigest().upper()
     if line.startswith('MK2_BBAUDIO_PCM '):need(len(raw)%4==0,'Whole stereo samples');chunks.append(raw);headers.append(fields)
     else:
      need(not guest_seen and fields['frame']=='1'and raw==guest,'Every actual initialized guest byte independently reconstructed');guest_seen=True
      (folder/'guest_memory_proof.json').write_text(json.dumps(fields,indent=2)+'\n')
     log.write(line.split()[0]+'_DIGEST '+' '.join(k+'='+str(v)for k,v in fields.items())+'\n')
    else:
     need('hex='not in line,'No raw audio/media persisted');log.write(line)
     if line.startswith(('MK2_P2CPU_COLD_LIVE ','MK2_CPU_PAIR_RESULT ','MK2_BBAUDIO_RESULT ')):print(line.strip(),flush=True)
  code=process.wait()
 log=(folder/'run.log').read_text();need(code==0 and guest_seen and (folder/'stderr.log').read_text()==''and not re.search(r'LUA ERROR|stack traceback|Fatal error|access violation',log,re.I),'Actual terminal0 and warning-free observation')
 need(headers and all(float(a['seconds'])<float(b['seconds'])for a,b in zip(headers,headers[1:]))and all(sha(p)==h for p,h in pins.items()),'Entire chronological PCM and stable actual inputs')
 pcm=b''.join(chunks)
 (folder/'result.json').write_text(json.dumps(dict(exit_code=code,candidate=current.NAME,input_hashes=pins,assistance='none',cheats_enabled=False,
  samples_enabled=enabled,wholeActualGuestComparedInRAM=True,rawGuestRGBPCMOrWAVFilesWritten=0,mixedPCMBytes=len(pcm),mixedPCMUpdates=len(headers),mixedPCMSHA256=hashlib.sha256(pcm).hexdigest().upper(),fullPortAcceptance=False),indent=2)+'\n')
 return folder,headers,np.frombuffer(pcm,dtype='<i2').reshape(-1,2).astype(np.float64)

def owner_contract(log,typed,enabled):
 entry=phase.native.rows(log,'MK2_SQUARE_BOUNDARY_ENTRY_STATE');own=next(r for r in entry if r['slot']==2)
 marks=[r for r in records(log,'SOUND')if r['word']in('6B00','6B01','6B02')]
 need(len(marks)==1 and marks[0]['word']=='6B00'and int(marks[0]['frame'])==typed['start']and marks[0]['mask']=='FFFF'and
  marks[0]['a8']==f"{own['actor']:08X}"and marks[0]['a13']==f"{own['main']:08X}"and marks[0]['writes']=='0'and marks[0]['assistance']=='none','Exactly real native owned CPU Square launch marker')
 frames=range(2200,2601);channels=records(log,'CHANNEL');owners=records(log,'OWNER')
 cb={(int(r['frame']),int(r['channel'])):r for r in channels};ob={(int(r['frame']),int(r['slot'])):r for r in owners}
 need(len(cb)==len(channels)==4*len(frames)and len(ob)==len(owners)==2*len(frames),'All actual finite channel/owner fields retained')
 for r in channels:need(r['writes']==r['loop']==r['paused']=='0','Unpaused nonlooping native channels, read-only')
 if not enabled:
  need(all(r['length']=='0'and float(r['pos'])==0 for r in channels),'Disabled-sample baseline has no loaded imported cue')
  need(all(r['actor']==r['main']=='00000000'and r['health']=='0'and r['writes']=='0'for r in owners),'Disabled imported cue has no stale owners')
  return dict(marker=marks[0],samplePlaybackDisabled=True)
 completed=None;first=typed['start']+1
 for channel in range(10,14):
  stream=[cb[f,channel]for f in frames]
  if channel!=12:need(all(r['length']=='0'and float(r['pos'])==0 for r in stream),'Human and second CPU channel never start')
  else:
   active=[r for r in stream if int(r['length'])>0]
   need(active and int(active[0]['frame'])==first and all(int(r['length'])==45512 and int(r['sample'])==13 for r in active),'Complete Square asset on actual CPU channel12/sample13')
   positions=[float(r['pos'])for r in active]
   need(all(a<=b for a,b in zip(positions,positions[1:]))and positions[-1]>=45512,'Actual finite cue reaches its end without reset or interruption')
   completed=next(int(r['frame'])for r in active if float(r['pos'])>=45512)
   need(all(cb[f,12]['length']=='0'and float(cb[f,12]['pos'])==0 for f in range(2200,first)),'No loaded cue before native launch')
 for f in frames:
  for slot in(1,2):
   r=ob[f,slot];need(r['writes']=='0','Read-only complete ownership ledger')
   if slot==2 and first<=f<completed:
    need((r['actor'],r['main'],int(r['health']))==(f"{own['actor']:08X}",f"{own['main']:08X}",own['hp']),'Whole actual playback bound to genuine native CPU Sonya')
   elif slot==1 or f<first or f>=completed+3:
    need(r['actor']==r['main']=='00000000'and r['health']=='0','Other owner clear and finite own owner cleanup')
   elif r['actor']!='00000000':need((r['actor'],r['main'],int(r['health']))==(f"{own['actor']:08X}",f"{own['main']:08X}",own['hp']),'Only genuine owner during final timer cleanup')
 return dict(marker=marks[0],completedFrame=completed,ownerCleanupByFrame=completed+3,ownerFields=len(owners),channelFields=len(channels),cueFrames=45512,channel=12,sample=13)

def waveform(headers,a,b,donor,marker):
 delta=a-b;need(np.array_equal(delta[:,0],delta[:,1]),'Actual cue contribution dual mono')
 signal=delta[:,0];offset=int(np.argmax(fftconvolve(signal,donor[::-1],mode='valid')));actual=signal[offset:offset+len(donor)]
 gain=float(np.dot(actual,donor)/np.dot(donor,donor));corr=float(np.dot(actual,donor)/(np.linalg.norm(actual)*np.linalg.norm(donor)))
 need(corr>.999 and .699<gain<.701,'Complete actual source launch waveform at compiled .70 route')
 need(not np.any(signal[:offset])and not np.any(signal[offset+len(donor)+2:]),'No premature or stale imported cue contribution')
 onset=float(headers[0]['seconds'])-int(headers[0]['bytes'])/4/48000+offset/48000
 need(abs(onset-float(marker['seconds']))<.0001,'Actual PCM launch synchronized with real native marker')
 return dict(correlation=corr,gain=gain,onsetSeconds=onset,markerSeconds=float(marker['seconds']),cueSamples=len(donor),offset=offset)

def run():
 guest=current.expected();enabled=capture(True,guest);disabled=capture(False,guest)
 folder,headers,a=enabled;baseline,oldheaders,b=disabled
 timeline=lambda hs:[{k:v for k,v in r.items()if k!='sha256'}for r in hs]
 need(timeline(headers)==timeline(oldheaders)and a.shape==b.shape,'Every enabled/disabled mixed sound update exactly aligned')
 log=(folder/'run.log').read_text();oldlog=(baseline/'run.log').read_text();prior=ROOT/'audit_v5370_current_cpu_square_scene_ram/run.log'
 select=lambda t:[s for s in t.splitlines()if s.startswith(PREFIXES)]
 need(select(log)==select(oldlog)==select(prior.read_text()),'Entire actual physical input/RNG/CPU/HP/state/contact/lock trajectory unchanged')
 typed=phase.verify(log,guest,'kano');typed2=phase.verify(oldlog,guest,'kano');need(typed==typed2,'Complete original native hit/drop/landing/individual recovery identical')
 health,by=ledgers.health_ledger(log,guest,'kano');state=ledgers.state_ledgers(log,guest,'kano',by)
 oldhealth,oldby=ledgers.health_ledger(oldlog,guest,'kano');oldstate=ledgers.state_ledgers(oldlog,guest,'kano',oldby)
 need(health==oldhealth and state==oldstate,'Entire native1800-field match health and states unchanged by imported playback')
 need(records(log,'SOUND')==records(oldlog,'SOUND'),'Entire actual native DCS and cue-command inventory unchanged')
 ownership=owner_contract(log,typed,True);disabled_owner=owner_contract(oldlog,typed,False)
 with wave.open(str(ASSET),'rb')as wav:
  need((wav.getnchannels(),wav.getsampwidth(),wav.getframerate(),wav.getnframes())==(1,2,48000,45512),'Whole exact retained Square launch asset format')
  donor=np.frombuffer(wav.readframes(wav.getnframes()),'<i2').astype(np.float64)
 audio=waveform(headers,a,b,donor,ownership['marker'])
 faults=[]
 mutations={'wrong_owner':log.replace('actor=010350A0 main=0106BF30 health=161 writes=0','actor=01000000 main=0106BF30 health=161 writes=0'),
  'missing_channel': '\n'.join(s for s in log.splitlines()if not s.startswith('MK2_BBAUDIO_CHANNEL ')),
  'missing_owner':'\n'.join(s for s in log.splitlines()if not s.startswith('MK2_BBAUDIO_OWNER ')),
  'looped_cue':log.replace('loop=0 paused=0','loop=1 paused=0'),
  'wrong_marker':log.replace('word=6B00','word=6B01'),
  'wrong_sample':log.replace('sample=13 length=45512','sample=14 length=45512')}
 for label,bad in mutations.items():
  need(bad!=log,'Effective real ledger corruption')
  try:owner_contract(bad,typed,True)
  except(ValueError,KeyError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Accepted corrupt actual playback ledger '+label)
 for label,changed,marker in [('wrong_gain',b+(a-b)*1.1,ownership['marker']),('wrong_onset',a,dict(ownership['marker'],seconds=str(float(ownership['marker']['seconds'])+.01)))]:
  try:waveform(headers,changed,b,donor,marker)
  except ValueError as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Accepted corrupt actual waveform '+label)
 pins={str(Path(__file__).resolve()):sha(__file__),str(prior):sha(prior)}
 for leaf in(folder,baseline):
  meta=json.loads((leaf/'result.json').read_text())
  for p,h in meta['input_hashes'].items():need(p not in pins or pins[p]==h,'Consistent actual executed inputs');pins[p]=h
  for p in leaf.rglob('*'):
   if p.is_file():pins[str(p)]=sha(p)
 for module in(phase,ledgers):pins[str(Path(module.__file__).resolve())]=sha(module.__file__)
 need(all(sha(p)==h for p,h in pins.items()),'All authoritative inputs and capture evidence stable')
 return dict(passed=True,candidate=current.NAME,cpuSlot=2,humanSlot=1,case=folder.name,baseline=baseline.name,phase=typed,
  wholeNativeHealth=health,wholeNativeState=state,ownership=ownership,disabledOwnership=disabled_owner,**audio,
  actualPhysicalTrajectoryRecords=len(select(log)),nativeSoundPortWrites=len(records(log,'SOUND')),mixedPCMUpdates=len(headers),mixedStereoSamples=len(a),
  actualPlaybackFaultsRejected=faults,fullCapturedNaturalCPUSquareLaunchPlaybackAndOwnershipAccepted=True,
  originalEntireNativeCPUHitPhaseAndMatchStateHealthContractRetained=True,fullNativeContactDCSWaveformAccepted=False,
  allCPUContextsArenasKOOverlapAudioAccepted=False,rawGuestRGBPCMOrWAVFilesWritten=0,newBuilds=0,fullPortAcceptance=False,inputHashes=pins)

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable actual CPU Square audio proof')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','wholeNativeHealth','wholeNativeState','phase')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
