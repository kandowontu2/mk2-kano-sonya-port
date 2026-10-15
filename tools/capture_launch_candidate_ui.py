"""Whole native four-case UI regression on actual private launch candidate.

Physical original controller unchanged; full guest/GFX/RGB/PCM RAM only.
Drain each actual job after observer/transport errors, never timeout-reboot.
Entire original reported-failure state/pixel fault suite runs on current frames.
"""
import code,gzip,hashlib,io,json,os,re,subprocess,time,traceback,unittest
from pathlib import Path
import numpy as np
import kano_ball_launch_context_v6642 as current
import native_process_census_v6647 as identity
import verify_native_ui_flow_v814 as model
import test_current_native_ui_v817 as faults
import run_guarded_native_ui_qualified_ram_v3734 as qualified
ROOT,need,sha=current.ROOT,current.need,current.sha
BASE=ROOT/'audit_launch_candidate_ui_ram';OUT=ROOT/'audit_launch_candidate_ui_checked'
LUA=ROOT/'mk2ks_launch_candidate_ui.lua'
RAM_CASES={};COMPLETED=[]

def save(path,value):path.write_text(json.dumps(value,indent=2)+'\n')

def capture(fighter,side,guest,gfx,pins):
 key=f'{fighter}_p{side}';folder=BASE/key
 need(not folder.exists()and not identity.census(),'Fresh actual leaf, no native job replay')
 folder.mkdir(parents=True);build=ROOT/current.NAME
 env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK2PORT_ACCEPT_|MK2PORT_INTERRUPT_)',k)}
 env.update(MK2KS_UI_FIGHTER=fighter,MK2KS_UI_SIDE=str(side),MK2KS_UI_BOOT='604')
 command=[str(build/'mkport_candidate.exe'),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),
          '-samplepath',str(build/'samples')+';'+str(ROOT/'samples'),'-samples','-artpath',str(ROOT/'artwork'),
          '-skip_gameinfo','-nocheat','-inipath',str(folder),'-video','none','-sound','none','-samplerate','48000',
          '-noautoframeskip','-frameskip','0','-nothrottle','-str','65','-snapsize','400x254','-wavwrite','NUL',
          '-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),'-snapshot_directory',str(folder/'snap'),'-autoboot_script',str(LUA)]
 images={};headers=[];chunks=[];pcm_headers=[];errors=[];inventories={'MK2_UA_GUEST':0,'MK2_UA_GFX':0}
 with(folder/'stderr.log').open('w',encoding='utf-8')as err:
  started=time.time();job=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',errors='replace',creationflags=subprocess.CREATE_NO_WINDOW)
  actual=None
  try:
   for _ in range(100):
    actual=next((r for r in identity.census()if r['ProcessId']==job.pid),None)
    if actual or job.poll()is not None:break
    time.sleep(.02)
   need(actual and actual['ParentProcessId']==os.getpid()and actual['createdUnix']>=started-1 and
        Path(actual['ExecutablePath']).resolve()==(build/'mkport_candidate.exe').resolve()and str(folder)in actual['CommandLine'],'Actual kernel PID/parent/path/creation/full command')
  except Exception as error:errors.append(dict(stage='identity',error=repr(error)))
  save(folder/'process.json',dict(pid=job.pid,actualWindowsIdentity=actual,command=command))
  print(f'{key} actual native PID={job.pid}',flush=True)
  with gzip.open(folder/'run.log.gz','wt',encoding='utf-8')as log:
   for line in job.stdout:
    try:
     if ' hex='in line:
      tag=line.split()[0];pairs=re.findall(r'(\w+)=([^\s]+)',line);h=dict(pairs);need(len(pairs)==len(h),'Unique raw transport metadata')
      raw=bytes.fromhex(h.pop('hex'));need(len(raw)==int(h['bytes']),'Full actual native buffer');h['sha256']=hashlib.sha256(raw).hexdigest().upper()
      if tag in inventories:
       need(h['frame']=='1'and raw==(guest if tag=='MK2_UA_GUEST'else gfx),'Whole independent actual guest/GFX byte equality');inventories[tag]+=1
      elif tag=='MK2_UA_RGB':
       need(h['width']=='400'and h['height']=='254'and len(raw)==406400 and h['filename']==f"ui_{int(h['frame']):04d}.png",'Unscaled full actual native displayed frame')
       rgb=np.frombuffer(raw,np.uint8).reshape(254,400,4)[:,:,2::-1].copy()
       need(h['filename']not in images or np.array_equal(images[h['filename']],rgb),'Duplicate snapshot is byte-identical')
       images[h['filename']]=rgb;headers.append(h)
      elif tag=='MK2_UA_PCM':need(len(raw)%4==0,'Whole stereo PCM');chunks.append(raw);pcm_headers.append(h)
      else:raise ValueError('Unexpected actual raw transport '+tag)
      log.write(tag+'_DIGEST '+' '.join(k+'='+str(v)for k,v in h.items())+'\n')
     else:
      need('hex='not in line,'Raw media never persisted');log.write(line)
      if line.startswith(('MK2_UI_LIVE ','MK2_UI_RESULT ')):print(line.strip(),flush=True)
    except Exception as error:errors.append(dict(stage='decode',error=repr(error)))
   exitcode=job.wait()
 with gzip.open(folder/'run.log.gz','rt',encoding='utf-8')as log:text=log.read()
 terminal=dict(pid=job.pid,nativeExit=exitcode,actualWindowsIdentity=actual,hostDecodeErrors=errors)
 save(folder/'native_terminal.json',terminal)
 carrier=dict(folder=folder,log=text,images=images,headers=headers,pcm=chunks,pcmHeaders=pcm_headers,terminal=terminal,inputHashes=pins)
 RAM_CASES[key]=(folder,text,images)
 result=dict(passed=False,candidate=current.NAME,fighter=fighter,side=side,nativeTerminal=terminal,inputHashes=pins,fullPortAcceptance=False)
 try:
  need(exitcode==0 and not errors and not(folder/'stderr.log').read_text()and not re.search(r'LUA ERROR|stack traceback|fatal error|access violation|WRONG CHECKSUMS|might not run correctly',text,re.I),'Actual warning/error-free natural native terminal0')
  need(inventories=={'MK2_UA_GUEST':1,'MK2_UA_GFX':1},'Exactly one entire guest and source graphics inventory')
  state=model.verify_log(text,fighter,side)
  need([r['file']for r in model.records(text,'SNAP')]==[r['filename']for r in headers],'Every original physical displayed snapshot retained')
  for r in model.records(text,'CODE'):
   raw=b''.join(int(w,16).to_bytes(2,'little')for w in r['words'].split(','));need(raw==guest[(int(r['start'],16)-0xff800000)//8:(int(r['stop'],16)-0xff800000)//8],'Every observed original UI table matches independent actual guest')
  pixels=model.render(folder,text,fighter,side,load=lambda name:images[name])
  owner_rows=[dict(re.findall(r'(\w+)=([^\s]+)',s))for s in text.splitlines()if s.startswith('MK2_UA_OWNER ')]
  need(len(owner_rows)==2*state['terminal']and {(int(r['frame']),int(r['slot']))for r in owner_rows}=={(f,s)for f in range(1,state['terminal']+1)for s in(1,2)}and
       all(r['actor']==r['main']=='00000000'and r['id']==r['health']=='0'and r['writes']=='0'and r['assistance']=='none'for r in owner_rows),'Entire cold UI/ladder/first-match battle owner/ID/HP ledger clear')
  need(all(sha(p)==h for p,h in pins.items()),'Actual source/candidate unchanged')
  result.update(passed=True,state=state,rendered=pixels,actualDisplayedCallbacks=len(headers),actualUniqueDisplayedFrames=len(images),wholeActualGuestGFXAccepted=True,
                completeColdBattleOwnerFields=len(owner_rows),actualPCMCallbacks=len(chunks),rawMediaFilesWritten=0,audioAcceptance=False,fullRasterAcceptance=False)
 except Exception as error:result.update(error=repr(error),traceback=traceback.format_exc())
 save(folder/'result.json',result);carrier['result']=result;COMPLETED.append(result)
 print(json.dumps(dict(case=key,passed=result['passed'],displayedCallbacks=len(headers),error=result.get('error'))),flush=True)
 return carrier

def run():
 need(not BASE.exists()and not OUT.exists()and not identity.census(),'Fresh four-case current fixture')
 guest=current.expected();gfx=current.expected_gfx();build=ROOT/current.NAME
 pins=dict(json.loads((build/'build-info.json').read_text(encoding='utf-8-sig'))['input_hashes'])
 for p in(Path(__file__),Path(current.__file__),Path(identity.__file__),Path(model.__file__),Path(faults.__file__),Path(qualified.__file__),LUA,
          ROOT/'mk2ks_current_ui_audio_ram_v5430.lua',ROOT/'mk2ks_current_ui_audio_ram_v5427.lua',ROOT/'mk2ks_native_ui_flow_v2_probe.lua',
          ROOT/'roms/mk2ks/mk2ks.ui',ROOT/'mk2/mk2-maincpu.bin',build/'mkport_candidate.exe',build/'roms/mk2ks/mk2ks.mdata',build/'build-info.json'):
  pins[str(p.resolve())]=sha(p)
 need(sha(ROOT/'roms/mk2ks/mk2ks.ui')==model.UI_SHA and sha(ROOT/'mk2/mk2-maincpu.bin')==model.ORIGINAL_SHA,'Entire independent UI and original stock source')
 captures=[]
 for fighter,side in faults.CASES:
  capture_=capture(fighter,side,guest,gfx,pins);captures.append(capture_);need(capture_['result']['passed'],'Entire current positive control, do not dispatch later native jobs after rejection')
 qualified.RAM_CASES=RAM_CASES
 stream=io.StringIO();tests=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(qualified.ActualRAMFaults))
 print(stream.getvalue(),flush=True);need(tests.wasSuccessful(),'All entire original current state/pixel faults reject with restored positives')
 for p in BASE.rglob('*'):
  if p.is_file():need(p.suffix.lower()not in('.png','.wav','.bin','.exe','.zip'),'No raw media/build/ROM copies');pins[str(p.resolve())]=sha(p)
 need(not identity.census()and all(sha(p)==h for p,h in pins.items()),'All actual jobs terminal and executed input/evidence unchanged')
 report=dict(passed=True,candidate=current.NAME,cases=COMPLETED,originalStatePixelFaultMethods=tests.testsRun,qualificationLog=stream.getvalue(),inputHashes=pins,
             currentBothSlotSelectionLadderFirstMatchPixelsAccepted=True,wholeActualGuestGFXAccepted=True,allColdBattleOwnershipClear=True,
             newNativeBoots=4,newBuilds=0,newROMCopies=0,newZIPs=0,newRawMedia=0,audioAcceptance=False,fullRasterAcceptance=False,fullPortAcceptance=False,
             fullLaddersAccepted=False,allCinematicsAccepted=False,goalStatus='active',publicPlayableChanged=False)
 OUT.mkdir();save(OUT/'report.json',report)
 print(json.dumps(dict(passed=True,cases=len(COMPLETED),originalStatePixelFaultMethods=tests.testsRun)),flush=True)
 return report

if __name__=='__main__':
 try:accepted=run()
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedCases=COMPLETED,fullPortAcceptance=False)
  need(not OUT.exists(),'Never overwrite earlier executed report');OUT.mkdir();save(OUT/'failure.json',failure);print(json.dumps(dict(passed=False,error=repr(error))),flush=True)
 code.interact(banner='Same terminal UI captures remain RAM-only; no replay.',local=dict(module=__import__(__name__),captures=RAM_CASES))
