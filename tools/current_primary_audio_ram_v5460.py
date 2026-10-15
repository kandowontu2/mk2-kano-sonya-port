"""Actual current own mirror fatalities, complete voices/effects and native cleanup.

Original1166 controller, whole1674 physical/palette/FIFO and3715 audio models;
3713's actual state faults rerun with only RAM file transport. No game edit,
proxy, actor/HP/stage write, savestate, ROM/EXE build or public promotion.
"""
import concurrent.futures,datetime,hashlib,inspect,json,os,re,struct,subprocess,textwrap,traceback
from pathlib import Path
import numpy as np
import current_payload_metadata_context_v5229 as current
import run_natural_mirror_complete_audio_v3715 as original
import verify_natural_mirror_audio_state_faults_v3713 as original_faults
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v5459_current_babality_qualified_progress/progress.json'
BASE=ROOT/'audit_v5461_current_primary_audio_ram'
OUT=ROOT/'audit_v5462_current_primary_audio_progress'
LUA=ROOT/'mk2ks_current_primary_audio_ram_v5460.lua'
COMPLETED=[]
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
def digest(raw):return hashlib.sha256(raw).hexdigest().upper()

class RAMPath:
 """Only original logical guest/palette filenames; never pretend files exist."""
 def __init__(self,path,ram):self.path=Path(path);self.ram=ram
 def __truediv__(self,key):return RAMPath(self.path/key,self.ram)
 def __str__(self):return str(self.path)
 def read_bytes(self):return self.ram[self.path.name]

def state_faults():
 source=inspect.getsource(original_faults.run)
 first="        data=prior.prior.physical.rows(log)";last="        cases.append(dict(fighter=fighter"
 need(source.count(first)==source.count(last)==1,'Whole original40-state-fault boundary')
 body=textwrap.dedent(source[source.index(first):source.index(last)])
 function='def faults(log,fighter,side,folder,guest,contract):\n    positive=contract(log,fighter,side,folder,guest);faults=[]\n'+textwrap.indent(body,'    ')+'    return faults\n'
 scope=dict(original_faults.__dict__);exec(compile(function,__file__+'.entire_original3713_actual_state_faults','exec'),scope)
 return scope['faults'],digest(function.encode())

def capture(fighter,side,enabled,guest,pins):
 key=f'{fighter}_p{side}_{"samples"if enabled else"nosamples"}';folder=BASE/key
 need(not folder.exists(),'Fresh immutable current native primary context');folder.mkdir(parents=True)
 for name in('cfg','nvram','snap'):(folder/name).mkdir()
 save(folder/'input_hashes_before.json',pins)
 build=ROOT/current.NAME
 env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
 env.update(MK2KS_PORT_ROOT=str(ROOT),MK2KS_TEST_FIGHTER=fighter,MK2KS_MIRROR_WINNER=str(side),MK2KS_MIRROR_CONFIRM_FIRST='1',MK2KS_REPTILE_AUDIT_DIR=str(folder))
 command=[str(build/'mkport_candidate.exe'),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),'-samplepath',str(ROOT/'samples'),
  '-samples'if enabled else'-nosamples','-artpath',str(ROOT/'artwork'),'-skip_gameinfo','-nocheat','-log','-inipath',str(folder),
  '-video','none','-sound','none','-samplerate','48000','-noautoframeskip','-frameskip','0','-nothrottle','-str','110','-snapsize','400x254',
  '-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),'-snapshot_directory',str(folder/'snap'),'-autoboot_script',str(LUA)]
 ram={};images={};rgb_headers=[];pcm_headers=[];chunks=[]
 with(folder/'stderr.log').open('w',encoding='utf-8')as err:
  proc=subprocess.Popen(command,cwd=folder,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW)
  save(folder/'process.json',dict(pid=proc.pid,command=command,env={k:v for k,v in env.items()if k.startswith('MK2KS_')}))
  print(key+' actual native PID='+str(proc.pid),flush=True)
  with(folder/'run.log').open('w',encoding='utf-8')as out:
   for line in proc.stdout:
    if line.startswith(('MK2_PRIMARY_RAM_DATA ','MK2_PRIMARY_RAM_RGB ','MK2_BBAUDIO_PCM ')):
     tag=line.split()[0];r=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(r.pop('hex'));need(len(raw)==int(r['bytes']),'Complete actual native RAM buffer')
     r['sha256']=digest(raw)
     if tag=='MK2_PRIMARY_RAM_DATA':
      need(r['filename']not in ram,'Unique original logical RAM palette/guest key');ram[r['filename']]=raw
      if r['filename']=='guest_maincpu.bin':need(raw==guest,'Entire actual current initialized guest source-exact')
      else:need(len(raw)==256 and re.fullmatch(r'(mirror_palette_p[12]|finish_palette_p[12]_\d{3})\.bin',r['filename']),'Exact whole64-pen actual hardware palette')
     elif tag=='MK2_PRIMARY_RAM_RGB':
      need((r['width'],r['height'],len(raw))==('400','254',406400)and r['filename']not in images,'Whole unique actual displayed native raster')
      images[r['filename']]=np.frombuffer(raw,np.uint8).reshape(254,400,4)[:,:,2::-1].copy();rgb_headers.append(r)
     else:need(len(raw)%4==0,'Complete actual stereo signed16 PCM update');chunks.append(raw);pcm_headers.append(r)
     out.write(tag+'_DIGEST '+' '.join(k+'='+str(v)for k,v in r.items())+'\n')
    else:need('hex='not in line,'No raw capture persisted in text');out.write(line)
   code=proc.wait()
 log=(folder/'run.log').read_text();error=(folder/'stderr.log').read_text()
 need(code==0 and not error and ram.get('guest_maincpu.bin')==guest and
  not re.search(r'LUA ERROR|stack traceback|Fatal error|access violation|WRONG CHECKSUMS|might not run correctly',log,re.I),'Actual native warning-free terminal0 and entire current guest')
 contract,contract_sha=original.physical_contract();state=contract(log,fighter,side,RAMPath(folder,ram),guest)
 snapshots=[r['file']for tag,r in original.prior.physical.rows(log)if tag=='SNAPSHOT']
 need(snapshots==[r['filename']for r in rgb_headers],'Every original selection/live/finisher/continue display target transported')
 pcm=b''.join(chunks)
 result=dict(passed=True,candidate=current.NAME,fighter=fighter,side=side,samplesEnabled=enabled,nativePID=proc.pid,nativeExit=code,
  wholeActualGuestSourceExact=True,assistance='none',guestWrites=0,cheatsEnabled=False,physical=state,
  physicalContractSHA256=contract_sha,actualDisplayedFrameCallbacks=len(rgb_headers),actualPCMUpdates=len(pcm_headers),actualPCMBytes=len(pcm),
  actualMixedPCMSHA256=digest(pcm),allGuestPalettesImagesPCMOnlyInRAM=True,rawGuestRGBPCMOrWAVFilesWritten=0,inputHashes=pins,fullPortAcceptance=False)
 save(folder/'result.json',result)
 cp=subprocess.run(['compact.exe','/C','/EXE:LZX','/I','/Q',str(folder/'run.log')],capture_output=True,text=True);need(cp.returncode==0,'Lossless native text trace compression')
 print(key+' full original native physical/mirror costume/palette/FIFO/continue contract passed',flush=True)
 return dict(folder=folder,log=log,error=(folder/'error.log').read_text(),ram=ram,images=images,rgb_headers=rgb_headers,pcm_headers=pcm_headers,
  pcm=np.frombuffer(pcm,'<i2').reshape(-1,2).astype(np.float64),result=result)

def audio_check(pair,fighter,side):
 a,b=pair;log,old=a['log'],b['log'];state=a['result']['physical']
 selected=lambda s:[l for l in s.splitlines()if l.startswith('MK2_NATURAL_MIRROR_FINISH_V1166_')]
 need(selected(log)==selected(old),'Every original physical input/state/palette/FIFO/continue row unchanged by sample playback')
 need(a['ram']==b['ram']and a['rgb_headers']==b['rgb_headers'],'Entire actual native guest/each64-pen palette/each whole displayed frame unchanged by playback')
 timeline=lambda hs:[{k:v for k,v in h.items()if k!='sha256'}for h in hs]
 need(timeline(a['pcm_headers'])==timeline(b['pcm_headers'])and a['pcm'].shape==b['pcm'].shape,'Every actual native mixed interval and stereo sample aligned')
 rows=original.prior.rows
 need(rows(log,'SOUND')==rows(old,'SOUND')and rows(log,'REQUEST')==rows(old,'REQUEST'),'All genuine native DCS/direct/physical request command chronology identical')
 ends=rows(log,'CAPTURE_END');need(len(ends)==1 and ends==rows(old,'CAPTURE_END')and
  state['terminalFrame']==int(ends[0]['frame'])+1 and int(ends[0]['frame'])>=5198 and
  float(ends[0]['seconds'])>=float(ends[0]['not_before']),'Complete actual minimum95s/tail deadline and scheduled-exit final callback')
 model,events=original.cue_model(log,a['error'])
 select,win=(0xfffc,0xfffe)if fighter=='kano'else(0xfffb,0xfffd);effects=[0xfff9]if fighter=='kano'else[0xfffa,0xfff8,0xfff7]
 need([int(e['word'],16)for e in events]==[select,select,win,*effects,win],'All and only own selection/winner/individual-effect cues')
 need(all(state['action']<=int(e['frame'])<=state['wrap']for e in events if int(e['word'],16)in effects),'Every imported effect stays inside actual physical finisher choreography')
 delta=a['pcm']-b['pcm'];need(np.array_equal(delta[:,0],delta[:,1]),'Actual imported contribution dual mono')
 mixed=original.fit_all(delta[:,0],a['pcm_headers'],model)
 channels=rows(log,'CHANNEL');final=[r for r in channels if int(r['frame'])==state['terminalFrame']]
 need(len(final)==14 and all(int(r['sample'])==0xffffffff for r in final),'Every native imported voice/effect channel finite and inactive after full captured tails')
 need(all(r['loop']==r['paused']==r['writes']=='0'for r in channels),'All native14 channels finite/unpaused/read-only')
 need(all(r['length']=='0'for r in channels if 4<=int(r['channel'])<=9),'No unwanted Friendship/orphaned sample')
 need(all(int(r['sample'])==0xffffffff and r['length']=='0'for r in rows(old,'CHANNEL')),'No imported contribution in actual DCS-only baseline')
 owners=rows(log,'OWNER');terminal=[r for r in owners if int(r['frame'])==state['terminalFrame']]
 need(len(terminal)==2 and all(r['actor']==r['main']=='00000000'and r['health']=='0'for r in terminal),'Both actual launch owners cleared at terminal')
 for r in owners:
  if r['actor']=='00000000':need(r['main']=='00000000'and r['health']=='0','Complete cleared native owner tuple')
  else:need(any(m.get('request',{}).get('slot')==r['slot']and m['request']['actor']==r['actor']and m['request']['main']==r['main']and
   m['request']['health']==r['health']and int(m['event']['frame'])<int(r['frame'])for m in model),'Every active launch owner belongs to actual native Sonya request/marker')
 return dict(passed=True,mixedOriginalCueFidelity=mixed,cues=[{k:v for k,v in m.items()if k!='clip'}for m in model],
  subsequentOwnedLaunchCues=sum('request'in m for m in model),actualChannelFields=len(channels),actualOwnerFields=len(owners),nativeDCSCompleteWaveformAccepted=False)

def audio_faults(pair,fighter,side):
 positive=audio_check(pair,fighter,side);a,b=pair;out=[]
 def reject(label,changed):
  try:audio_check(changed,fighter,side)
  except ValueError as error:out.append(dict(label=label,rejectedBy=str(error)))
  else:raise ValueError('Actual audio counterexample accepted: '+label)
 delta=a['pcm']-b['pcm'];gain=dict(a,pcm=b['pcm']+delta*1.1);reject('actual full mixed imported gain increased10percent',(gain,b))
 delayed=np.zeros_like(delta);delayed[480:]=delta[:-480];reject('actual whole cue contribution delayed10ms',(dict(a,pcm=b['pcm']+delayed),b))
 stale=a['pcm'].copy();stale[-400:]+=1;reject('actual stale imported tail in final quiet samples',(dict(a,pcm=stale),b))
 muted=dict(a,pcm=b['pcm'].copy());reject('actual imported voice/effect mix muted',(muted,b))
 need(audio_check(pair,fighter,side)==positive,'Same actual audio positive restored after all effective counterexamples')
 return out

def case(spec,guest,pins):
 fighter,side=spec;a=capture(fighter,side,True,guest,pins);b=capture(fighter,side,False,guest,pins)
 audio=audio_check((a,b),fighter,side);contract,contract_sha=original.physical_contract();check,check_sha=state_faults()
 faults=check(a['log'],fighter,side,RAMPath(a['folder'],a['ram']),guest,contract)
 need(len(faults)==10,'All original ten actual native state/palette faults per context')
 afaults=audio_faults((a,b),fighter,side)
 result=dict(fighter=fighter,side=side,actual=a['result'],baseline=b['result'],audio=audio,
  originalStateFaultContractSHA256=check_sha,actualOriginalNativeStatePaletteFaults=faults,actualMixedAudioFaults=afaults,
  pairedEntireDisplayedFramesByteExact=True,allArenasAndVictimArtAccepted=False,fullPortAcceptance=False)
 COMPLETED.append(result);print(f'{fighter} P{side} actual full individual voices/effects/overlap/finite cleanup plus original native faults passed',flush=True)
 return result

def run():
 guest=current.expected();parent=json.loads(PARENT.read_text());need(parent['passed']and parent['goalStatus']=='active','Current22-context Babality checkpoint authoritative')
 pins=dict(parent['newInputHashes']);pins[str(PARENT)]=sha(PARENT)
 old_path=ROOT/'audit_v3717_natural_mirror_complete_audio_checked/report.json';old=json.loads(old_path.read_text())
 fault_path=ROOT/'audit_v3714_natural_mirror_audio_state_faults_checked/report.json';fault=json.loads(fault_path.read_text())
 need(old['passed']and fault['passed']and fault['totalQualifiedActualStatePaletteFaults']==40,'Original entire physical/audio models and effective fault set actually qualified')
 contract,code_sha=original.physical_contract();need(all(c['physicalContractSHA256']==code_sha for c in old['cases']),'Entire original physical/palette/FIFO/minimum-terminal contract unchanged')
 paths=[LUA,ROOT/'mk2ks_current_primary_controller_ram_v5460.lua',ROOT/'mk2ks_natural_mirror_finish_v1166.lua',ROOT/'mk2ks_natural_mirror_audio_ram_v3708.lua',
  Path(__file__).resolve(),Path(current.__file__).resolve(),Path(original.__file__).resolve(),Path(original.prior.__file__).resolve(),
  Path(original.prior.physical.__file__).resolve(),Path(original_faults.__file__).resolve(),ROOT/'tools/verify_native_friendship_audio_v791.py',old_path,fault_path]
 for p in paths:
  wanted=old['inputHashes'].get(str(p.resolve()))or fault['inputHashes'].get(str(p.resolve()))
  if wanted:need(sha(p)==wanted,'Original qualified model/controller/asset unchanged: '+str(p))
  pins[str(p)]=sha(p)
 for p in(ROOT/'samples/mk2ks').glob('*.wav'):pins[str(p)]=sha(p)
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();off=original.prior.physical.off
 for first,last in((0xff8953c0,0xff8954d0),(0xff8366c0,0xff836710),(0xff82bbb0,0xff82bc30)):
  need(guest[off(first):off(last)]==stock[off(first):off(last)],'Source-exact original native mirror assignment/damage/retirement')
 need(all(sha(p)==h for p,h in pins.items()),'Current/source/evidence/public stable before actual cold boots')
 first=case(('kano',1),guest,pins)
 with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:cases=[first]+list(pool.map(lambda spec:case(spec,guest,pins),[('kano',2),('sonya',1),('sonya',2)]))
 for p in BASE.rglob('*'):
  if p.is_file():need(p.suffix.lower()not in('.bin','.png','.wav','.rgb'),'All actual guest/palettes/raster/PCM remain RAM-only');pins[str(p)]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All authoritative current/source/public bytes unchanged after combined current primary matrix')
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',remaining=parent['remaining'],
  parentAdditiveJournal=str(PARENT),previousGoalTurnClassification=parent['thisGoalTurnClassification'],
  thisGoalTurnClassification='progress: actual current own fatalities both mirror costumes/player slots; original physical/parser/health/palette/FIFO/continue plus whole selection/winner/extract/kiss/fire/victim mix, finite owned subsequent launch cues and native cleanup; original40-state faults and16-audio faults against actual current RAM',
  cases=cases,currentBothSlotNaturalPrimaryMirrorsStateAndCompleteImportedAudioAccepted=True,effectiveOriginalActualStateFaults=40,effectiveActualMixedAudioFaults=16,
  actualPairedDisplayedFrameCallbacks=sum(c[k]['actualDisplayedFrameCallbacks']for c in cases for k in('actual','baseline')),
  newNativeBoots=8,newBuilds=0,newDeletedFiles=0,rawGuestRGBPCMOrWAVFilesWritten=0,publicPlayableChanged=False,refreshedReleaseZIP=False,
  allFinisherContextsAccepted=False,allArenasAccepted=False,allNativeDCSWaveformsAccepted=False,fullPortAcceptance=False,newInputHashes=pins,
  nextAction='Use actual current primary-fatality/mirror/full-imported-audio evidence alongside remaining victims/finisher/arena/nativeDCS/CPU/overlap/secret/cinematic contexts; dependency-aware obsolete-folder cleanup and release promotion still need complete applicable combined acceptance. Preserve all five original remaining groups.')

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable current primary fatality/audio checkpoint')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedCases=COMPLETED,goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();save(OUT/'progress.json',report)
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','completedCases','newInputHashes','remaining')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
