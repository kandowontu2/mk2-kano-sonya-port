"""Current actual displayed four-context UI plus paired full selection audio.

Reuse original full814 source/native-stock pixel and input/state gates and
817 reported-failure tests. Actual display/guest/GFX/PCM stays only in RAM.
No game edits, proxy actor/ID/HP/RNG writes, savestates or release promotion.
"""
import concurrent.futures,datetime,hashlib,io,json,os,re,struct,subprocess,traceback,unittest,wave
from pathlib import Path
import numpy as np
from scipy.signal import fftconvolve
import current_payload_metadata_context_v5229 as current
import verify_native_ui_flow_v814 as model
import test_current_native_ui_v817 as faults
import run_guarded_native_ui_qualified_ram_v3734 as qualified

ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v5426_current_morph_publication_progress/progress.json'
LUA=ROOT/'mk2ks_current_ui_audio_ram_v5427.lua'
BASE=ROOT/'audit_v5428_current_ui_audio_ram'
OUT=ROOT/'audit_v5429_current_ui_audio_progress'
RAM_CASES={};COMPLETED=[]

def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
def records(log,tag):return [dict(re.findall(r'(\w+)=([^\s]+)',line))for line in log.splitlines()if line.startswith('MK2_UA_'+tag+' ')]

def capture(fighter,side,enabled,guest,pins):
 key=f'{fighter}_p{side}_{"samples"if enabled else"nosamples"}';folder=BASE/key
 need(not folder.exists(),'Fresh immutable actual UI/audio leaf');folder.mkdir(parents=True)
 for name in('cfg','nvram','snap'):(folder/name).mkdir()
 save(folder/'input_hashes_before.json',pins)
 build=ROOT/current.NAME
 env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
 env.update(MK2KS_UI_FIGHTER=fighter,MK2KS_UI_SIDE=str(side),MK2KS_UI_BOOT='604')
 command=[str(build/'mkport_candidate.exe'),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),
  '-samplepath',str(ROOT/'samples'),'-samples'if enabled else'-nosamples','-artpath',str(ROOT/'artwork'),
  '-skip_gameinfo','-nocheat','-inipath',str(folder),'-video','none','-sound','none','-samplerate','48000',
  '-noautoframeskip','-frameskip','0','-nothrottle','-str','65','-snapsize','400x254',
  '-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),'-snapshot_directory',str(folder/'snap'),
  '-autoboot_script',str(LUA)]
 headers=[];images={};chunks=[];pcm_headers=[];guest_seen=False;rgb_hash=hashlib.sha256()
 with(folder/'stderr.log').open('w',encoding='utf-8')as err:
  proc=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW)
  save(folder/'process.json',dict(pid=proc.pid,command=command,env={k:v for k,v in env.items()if k.startswith('MK2KS_')}))
  print(key+' actual native PID='+str(proc.pid),flush=True)
  with(folder/'run.log').open('w',encoding='utf-8')as out:
   for line in proc.stdout:
    if line.startswith(('MK2_UA_RGB ','MK2_UA_GUEST ','MK2_UA_PCM ')):
     tag=line.split()[0];r=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(r.pop('hex'))
     need(len(raw)==int(r['bytes']),'Complete actual native RAM buffer');r['sha256']=hashlib.sha256(raw).hexdigest().upper()
     if tag=='MK2_UA_GUEST':
      need(not guest_seen and r['frame']=='1'and raw==guest,'Entire actual current guest byte-exact independent source reconstruction');guest_seen=True
     elif tag=='MK2_UA_RGB':
      need((r['width'],r['height'],len(raw))==('400','254',406400),'Whole actual native displayed 400x254 RGB32')
      rgb=np.frombuffer(raw,np.uint8).reshape(254,400,4)[:,:,2::-1].copy()
      need(r['filename']==f"ui_{int(r['frame']):04d}.png",'Exact original logical snapshot key')
      need(r['filename']not in images or np.array_equal(images[r['filename']],rgb),'Duplicate actual displayed snapshot identical')
      images[r['filename']]=rgb;headers.append(r);rgb_hash.update(rgb.tobytes())
     else:need(len(raw)%4==0,'Complete actual stereo signed16 PCM');chunks.append(raw);pcm_headers.append(r)
     out.write(tag+'_DIGEST '+' '.join(k+'='+str(v)for k,v in r.items())+'\n')
    else:
     need('hex='not in line,'No raw raster/guest/PCM persists in log');out.write(line)
   code=proc.wait()
 log=(folder/'run.log').read_text();error=(folder/'stderr.log').read_text()
 need(code==0 and guest_seen and not error and not re.search(r'LUA ERROR|stack traceback|Fatal error|access violation|WRONG CHECKSUMS|might not run correctly',log,re.I),
  'Actual current native warning-free terminal0 and complete guest')
 state=model.verify_log(log,fighter,side)
 need([r['file']for r in model.records(log,'SNAP')]==[r['filename']for r in headers],'All original native snapshots exactly transported, no skipped display targets')
 for row in model.records(log,'CODE'):
  first,last=model.h(row,'start'),model.h(row,'stop');raw=b''.join(struct.pack('<H',int(w,16))for w in row['words'].split(','))
  need(raw==guest[(first-0xff800000)//8:(last-0xff800000)//8],'All actual UI tables exactly current independently reconstructed guest')
 pixels=model.render(folder,log,fighter,side,load=lambda name:images[name])
 pcm=b''.join(chunks)
 result=dict(passed=True,candidate=current.NAME,fighter=fighter,side=side,samplesEnabled=enabled,nativePID=proc.pid,nativeExit=code,
  inputHashes=pins,assistance='none',cheatsEnabled=False,state=state,rendered=pixels,
  wholeActualGuestByteExactInRAM=True,actualDisplayedFrameCallbacks=len(headers),uniqueActualDisplayedFrames=len(images),
  actualDisplayedRGBStreamSHA256=rgb_hash.hexdigest().upper(),actualPCMUpdates=len(pcm_headers),actualPCMBytes=len(pcm),
  actualMixedPCMSHA256=hashlib.sha256(pcm).hexdigest().upper(),rawGuestRGBPCMOrWAVFilesWritten=0,fullPortAcceptance=False)
 save(folder/'result.json',result)
 compressed=subprocess.run(['compact.exe','/C','/EXE:LZX','/I','/Q',str(folder/'run.log')],capture_output=True,text=True)
 need(compressed.returncode==0,'Lossless retained text trace compression')
 print(key+' complete current selection/ladder/true match/name-shadow displayed pixels accepted',flush=True)
 return dict(folder=folder,log=log,headers=headers,images=images,pcm_headers=pcm_headers,
  pcm=np.frombuffer(pcm,'<i2').reshape(-1,2).astype(np.float64),result=result)

def audio_check(pair,fighter,side):
 a,b=pair;log,old=a['log'],b['log'];expected=0xfffc if fighter=='kano'else 0xfffb
 take=lambda text:[line for line in text.splitlines()if line.startswith('MK2_UI_')]
 need(take(log)==take(old),'Entire native UI/control/roster/ladder/fighter trajectory unchanged by announcements')
 clean=lambda rows:[{k:v for k,v in r.items()if k!='sha256'}for r in rows]
 need(clean(a['pcm_headers'])==clean(b['pcm_headers'])and a['pcm'].shape==b['pcm'].shape,'Every paired actual sound-update interval and stereo sample aligned')
 need(a['headers']==b['headers'],'Every entire actual displayed frame unchanged by enabled/disabled announcements')
 sounds=records(log,'SOUND');need(sounds==records(old,'SOUND'),'All actual native DCS/cue command writes identical, no sample-generated extra game command')
 markers=[r for r in sounds if 0xfffb<=int(r['word'],16)<=0xfffe]
 need(len(markers)==1 and int(markers[0]['word'],16)==expected and int(markers[0]['roster'])==17+(fighter=='sonya')and
  markers[0]['mask']=='FFFF'and markers[0]['writes']=='0'and markers[0]['assistance']=='none',
  'Exactly one actual native own selection-name marker, no wrong-character/winner/stale announcement')
 channels=records(log,'CHANNEL');baseline=records(old,'CHANNEL');terminal=a['result']['state']['terminal']
 cb={(int(r['frame']),int(r['channel'])):r for r in channels}
 need(len(cb)==len(channels)==14*terminal and set(cb)=={(f,c)for f in range(1,terminal+1)for c in range(14)},
  'All native announcement/effect/battle channel states every callback')
 need(all(r['loop']==r['paused']==r['writes']=='0'for r in channels+baseline),'Read-only native finite nonlooping channels')
 need(all(int(r['length'])==0 and float(r['pos'])==0 for r in baseline),'Disabled sample baseline has no loaded imported voice/effect')
 need(all(int(r['length'])==0 for r in channels if int(r['channel'])!=0),'Other imported voice/battle channels never acquire an unintended selection cue')
 asset=ROOT/'samples/mk2ks'/f'{fighter}_select.wav'
 with wave.open(str(asset),'rb')as wav:
  need((wav.getnchannels(),wav.getsampwidth(),wav.getframerate())==(1,2,48000),'Actual retained original selection voice asset format')
  donor=np.frombuffer(wav.readframes(wav.getnframes()),'<i2').astype(np.float64)
 active=[r for r in channels if int(r['channel'])==0 and int(r['length'])>0]
 need(active and all(int(r['length'])==len(donor)for r in active)and
  all(float(x['pos'])<=float(y['pos'])for x,y in zip(active,active[1:]))and float(active[-1]['pos'])>=len(donor),
  'Whole actual native selection channel source length, continuous progress and finite completion')
 signal=a['pcm']-b['pcm'];need(np.array_equal(signal[:,0],signal[:,1]),'Actual imported selection contribution dual mono')
 mono=signal[:,0];offset=int(np.argmax(fftconvolve(mono,donor[::-1],mode='valid')));actual=mono[offset:offset+len(donor)]
 gain=float(np.dot(actual,donor)/np.dot(donor,donor));corr=float(np.dot(actual,donor)/(np.linalg.norm(actual)*np.linalg.norm(donor)))
 need(corr>.999 and .209<gain<.211,'Whole actual native selection-name waveform at source-compiled .70 times .30 gain')
 need(not np.any(mono[:offset])and not np.any(mono[offset+len(donor)+2:]),'No premature/stale imported selection-name contribution')
 head=a['pcm_headers'][0];onset=float(head['seconds'])-int(head['bytes'])/4/48000+offset/48000
 need(abs(onset-float(markers[0]['seconds']))<.0001,'Actual native selection command and full PCM onset synchronized')
 return dict(passed=True,nativeNameMarker=markers[0],actualPCMUpdates=len(a['pcm_headers']),mixedStereoSamples=len(a['pcm']),
  originalSelectionAsset=str(asset),cueSamples=len(donor),correlation=corr,gain=gain,onsetSeconds=onset,
  allNativeSoundCommandsUnchanged=True,actualChannelFields=len(channels),noExtraOrPersistentImportedCue=True,
  nativeDCSCompleteWaveformAccepted=False,allAudioContextsAccepted=False)

def case(spec,guest,pins):
 fighter,side=spec;enabled=capture(fighter,side,True,guest,pins);disabled=capture(fighter,side,False,guest,pins)
 audio=audio_check((enabled,disabled),fighter,side);key=f'{fighter}_p{side}'
 RAM_CASES[key]=(enabled['folder'],enabled['log'],enabled['images'])
 result=dict(fighter=fighter,side=side,actual=enabled['result'],baseline=disabled['result'],audio=audio)
 COMPLETED.append(result);print(key+' paired full original name announcement/native channel cleanup accepted',flush=True)
 return result

def run():
 guest=current.expected();parent=json.loads(PARENT.read_text());need(parent['passed']and parent['goalStatus']=='active','Current morph ownership/scene progress accepted')
 pins=dict(parent['newInputHashes']);pins[str(PARENT)]=sha(PARENT)
 old_path=ROOT/'audit_v3736_guarded_native_ui_qualified_ram_checked/report.json';old=json.loads(old_path.read_text())
 need(old['passed']and old['currentBothSlotSelectionLadderFirstMatchPixelsAccepted'],'Original whole UI model and effective faults actually qualified')
 for p in(Path(model.__file__).resolve(),Path(faults.__file__).resolve(),ROOT/'mk2ks_native_ui_flow_v2_probe.lua'):
  need(sha(p)==old['inputHashes'][str(p)],'Original controller, UI semantic/pixel model and reported-failure tests unchanged')
 compiled=ROOT/current.NAME/'input_sources/mame-mkp/src/mame/midway'
 need('m_mk2ks_voices->set_volume(0, 0.30f);'in(compiled/'midtunit_m.cpp').read_text()and
  'm_mk2ks_voices->add_route(ALL_OUTPUTS, "mk2ksvoice", 0.70);'in(compiled/'midtunit.cpp').read_text(),
  'Current compiled native selection announcement output gain')
 for p in(LUA,Path(__file__).resolve(),Path(current.__file__),Path(model.__file__),Path(faults.__file__),Path(qualified.__file__),old_path,
  ROOT/'mk2ks_native_ui_flow_v2_probe.lua',ROOT/'roms/mk2ks/mk2ks.ui',ROOT/'samples/mk2ks/kano_select.wav',ROOT/'samples/mk2ks/sonya_select.wav',
  ROOT/'mame-mkp/src/emu/video.cpp',ROOT/'mame-mkp/src/emu/sound.cpp',ROOT/'mame-mkp/src/devices/sound/samples.cpp'):
  pins[str(p.resolve())]=sha(p)
 need(sha(ROOT/'roms/mk2ks/mk2ks.ui')==model.UI_SHA,'Original independent portrait/name source stable')
 need(all(sha(p)==h for p,h in pins.items()),'All current actual compiled/public/source/evidence stable before capture')
 with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:
  cases=list(pool.map(lambda spec:case(spec,guest,pins),faults.CASES))
 qualified.RAM_CASES=RAM_CASES
 stream=io.StringIO();qualification=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(qualified.ActualRAMFaults))
 print(stream.getvalue(),flush=True);need(qualification.wasSuccessful(),'All original reported-failure actual current state/pixel corruptions rejected with same-path positives')
 for p in BASE.rglob('*'):
  if p.is_file():need(p.suffix.lower()not in('.bin','.png','.wav','.rgb'),'No raw guest/raster/PCM/media file persisted');pins[str(p)]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All authoritative current/source/public bytes unchanged after full combined fixture')
 ps="Get-CimInstance Win32_Process -Filter \"Name = 'mkport_candidate.exe'\" | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',ps],capture_output=True,text=True);need(census.returncode==0,'Actual native process census')
 live=json.loads(census.stdout)if census.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 ids={c[k]['nativePID']for c in cases for k in('actual','baseline')};need(not any(r['ProcessId']in ids for r in live),'All eight actual native runs terminal')
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  remaining=parent['remaining'],parentAdditiveJournal=str(PARENT),cases=cases,previousGoalTurnClassification=parent['thisGoalTurnClassification'],
  thisGoalTurnClassification='progress: fresh current both-slot original full UI pixel/state regression plus actual paired whole selection-name waveform and finite channel ledger; whole actual guest source-exact; reported failure faults rerun against current displayed pixels',
  currentBothSlotSelectionLadderFirstMatchPixelsAccepted=True,wholeActualCurrentGuestAccepted=True,
  completeObservedNativeSelectionNamesAudioAccepted=True,actualCurrentRAMStatePixelQualificationMethods=qualification.testsRun,
  qualificationLog=stream.getvalue(),actualDisplayedFrameCallbacks=sum(c[k]['actualDisplayedFrameCallbacks']for c in cases for k in('actual','baseline')),
  actualNativeProcessCensus=live,newNativeBoots=8,newBuilds=0,newDeletedFiles=0,
  rawGuestRGBPCMOrWAVFilesWritten=0,publicPlayableChanged=False,refreshedReleaseZIP=False,
  fullLaddersAccepted=False,allCinematicsAccepted=False,allAudioContextsAccepted=False,fullPortAcceptance=False,newInputHashes=pins,
  nextAction='Use actual current combined UI/name-selection audio evidence alongside remaining native finisher/victim/arena/CPU/interrupt/KO/full-audio contexts; continue dependency-aware obsolete-folder cleanup and refresh the release only after all required combined acceptance. Every original unfinished scope group remains.')

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable combined current UI/audio checkpoint')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedCases=COMPLETED,goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();save(OUT/'progress.json',report)
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','completedCases','newInputHashes','remaining','qualificationLog')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
