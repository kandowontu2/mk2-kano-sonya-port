"""Four real human mobility/ground/shadow cases on actual v6640, RAM only."""
import code,gzip,hashlib,json,os,re,subprocess,time,traceback
from pathlib import Path
import numpy as np
import kano_ball_launch_context_v6642 as current
import native_process_census_v6647 as identity
import launch_ground_model as model
ROOT,need,sha=current.ROOT,current.need,current.sha
BASE=ROOT/'audit_launch_ground_ram';OUT=ROOT/'audit_launch_ground_checked';LUA=ROOT/'mk2ks_launch_ground_ram.lua'
CAPTURES=[]
def save(path,v):path.write_text(json.dumps(v,indent=2)+'\n')

def capture(fighter,side,guest,gfx,pins):
 folder=BASE/f'{fighter}_p{side}';need(not folder.exists()and not identity.census(),'Fresh real mobility case; never replay a native handle')
 folder.mkdir(parents=True);build=ROOT/current.NAME
 carrier=dict(folder=folder,fighter=fighter,side=side,raw={},images={},gfx={},errors=[],inputHashes=pins);CAPTURES.append(carrier)
 env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK2PORT_)',k)}
 env.update(MK2KS_GROUND_FIGHTER=fighter,MK2KS_GROUND_SIDE=str(side),MK2KS_GROUND_BOOT='604',MK2KS_GROUND_OUT=str(folder))
 command=[str(build/'mkport_candidate.exe'),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),
          '-samplepath',str(build/'samples')+';'+str(ROOT/'samples'),'-samples','-artpath',str(ROOT/'artwork'),
          '-skip_gameinfo','-nocheat','-inipath',str(folder),'-video','none','-sound','none','-samplerate','48000',
          '-noautoframeskip','-frameskip','0','-nothrottle','-str','65','-snapsize','400x254','-wavwrite','NUL',
          '-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),'-snapshot_directory',str(folder/'snap'),'-autoboot_script',str(LUA)]
 guest_seen=0;memory_log=[]
 with(folder/'stderr.log').open('w',encoding='utf-8')as err:
  started=time.time();job=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',errors='replace',creationflags=subprocess.CREATE_NO_WINDOW)
  actual=None
  try:
   for _ in range(100):
    actual=next((r for r in identity.census()if r['ProcessId']==job.pid),None)
    if actual or job.poll()is not None:break
    time.sleep(.02)
   need(actual and actual['ParentProcessId']==os.getpid()and actual['createdUnix']>=started-1 and
        Path(actual['ExecutablePath']).resolve()==(build/'mkport_candidate.exe').resolve()and str(folder)in actual['CommandLine'],'Real kernel PID/parent/executable/creation/command')
  except Exception as error:carrier['errors'].append(dict(stage='identity',error=repr(error)))
  save(folder/'process.json',dict(pid=job.pid,command=command,actualWindowsIdentity=actual));print(f'{fighter} P{side} actual native PID={job.pid}',flush=True)
  with gzip.open(folder/'run.log.gz','wt',encoding='utf-8')as log:
   for line in job.stdout:
    try:
     if line.startswith('MK2_GROUND_RAW '):
      pairs=re.findall(r'(\w+)=([^\s]+)',line);r=dict(pairs);need(len(pairs)==len(r),'Unique exact raw transport metadata')
      raw=bytes.fromhex(r.pop('hex'));need(len(raw)==int(r['bytes']),'Entire declared native buffer');r['sha256']=hashlib.sha256(raw).hexdigest().upper()
      name,kind=r['filename'],r['kind']
      if kind=='GUEST':need(raw==guest and guest_seen==0,'Whole independently reconstructed actual current guest');guest_seen+=1
      elif kind=='RGB':
       need(len(raw)==406400 and name not in carrier['images'],'Whole unique native400x254 RGB32 frame')
       carrier['images'][name]=np.frombuffer(raw,np.uint8).reshape(254,400,4)[:,:,2::-1].copy()
      else:
       need(kind in('VRAM','VRAM_PRE','PALETTE')and len(raw)==(131072 if kind=='PALETTE'else 524288)and name not in carrier['raw'],'Whole unique native VRAM/palette buffer')
       carrier['raw'][name]=raw
      digest='MK2_GROUND_RAW_DIGEST '+' '.join(k+'='+str(v)for k,v in r.items())+'\n';log.write(digest);memory_log.append(digest)
     elif line.startswith('MK2_GROUND_GFX '):
      r=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(r['data']);first,size=int(r['first']),int(r['bytes'])
      need(len(raw)==size and raw==gfx[first:first+size]and r['key']not in carrier['gfx'],'Every complete actually drawn stock/imported source stream matches independently reconstructed compiled graphics')
      carrier['gfx'][r['key']]=r;memory_log.append(line)
      h=dict(r);h.pop('data');h['sha256']=hashlib.sha256(raw).hexdigest().upper();log.write('MK2_GROUND_GFX_DIGEST '+' '.join(k+'='+str(v)for k,v in h.items())+'\n')
     else:
      need('hex='not in line and 'data='not in line,'No raw media enters disk log');log.write(line);memory_log.append(line)
      if line.startswith(('MK2_GROUND_READY ','MK2_GROUND_RESULT ')):print(line.strip(),flush=True)
    except Exception as error:carrier['errors'].append(dict(stage='decode',error=repr(error)))
   exitcode=job.wait()
 carrier['text']=''.join(memory_log);terminal=dict(pid=job.pid,nativeExit=exitcode,actualWindowsIdentity=actual,hostDecodeErrors=carrier['errors']);carrier['terminal']=terminal;save(folder/'native_terminal.json',terminal)
 report=dict(passed=False,candidate=current.NAME,nativeTerminal=terminal,inputHashes=pins,fighter=fighter,side=side,newBuilds=0,newROMCopies=0,newZIPs=0,newRawMedia=0,fullPortAcceptance=False)
 try:
  need(exitcode==0 and not carrier['errors']and guest_seen==1 and not(folder/'stderr.log').read_text()and
       not re.search(r'LUA ERROR|stack traceback|fatal error|access violation|WRONG CHECKSUMS|INVALID',carrier['text'],re.I),'Actual clean naturally terminal native job with complete guest')
  results=model.original.rows(carrier['text'],'RESULT');fields=model.original.rows(carrier['text'],'FIELD')
  need(len(results)==1 and results[0]['terminalAge']==480 and len(fields)==962 and [(r['age'],r['slot'])for r in fields]==[(a,s)for a in range(481)for s in(1,2)],'Entire original real mobility window')
  for r in fields:
   wanted=17 if fighter=='kano'else 18
   if r['slot']!=side:wanted=4
   need(r['id']==r['roster']==wanted and r['owner']==r['actor']and r['state']==1 and r['hp']==161 and
        r['floor']==r['stageY']-{17:134,18:135,4:133}[wanted],'Every true actor/Main-owned physical field and source floor anchor')
  value=model.check(carrier)
  need(all(sha(p)==h for p,h in pins.items()),'Every actual candidate/source stable')
  report.update(passed=True,wholeGroundAndShadow=value,wholeActualGuestAccepted=True,completeSourceGraphicsStreams=len(carrier['gfx']),
                actualRGBFrames=len(carrier['images']),wholeRasterAcceptance=False,allArenaGroundAcceptance=False)
 except Exception as error:report.update(error=repr(error),traceback=traceback.format_exc())
 save(folder/'report.json',report);carrier['report']=report
 print(json.dumps(dict(case=f'{fighter}_p{side}',passed=report['passed'],error=report.get('error'))),flush=True)
 return carrier

def run():
 need(not BASE.exists()and not OUT.exists()and not identity.census(),'Fresh full current ground fixture')
 guest=current.expected();build=ROOT/current.NAME;pins=dict(json.loads((build/'build-info.json').read_text(encoding='utf-8-sig'))['input_hashes'])
 gfx=model.reconstruct(pins)
 for path in(Path(__file__),Path(current.__file__),Path(identity.__file__),Path(model.__file__),Path(model.original.__file__),Path(model.contract.__file__),
             Path(model.graphics.__file__),LUA,ROOT/'mk2ks_ground_shadow_v815_probe.lua',ROOT/'tools/inspect_natural_arena_floor_v602.py',ROOT/'tools/verify_native_floor_display_v602.py',
             ROOT/'tools/verify_native_idle_feet_v635.py',build/'mkport_candidate.exe',build/'build-info.json',build/'roms/mk2ks/mk2ks.mdata'):
  pins[str(path.resolve())]=sha(path)
 for fighter in('kano','sonya'):
  for side in(1,2):
   carrier=capture(fighter,side,guest,gfx,pins);need(carrier['report']['passed'],'Complete current positive, no dispatch after a rejected case')
 report=dict(passed=True,candidate=current.NAME,cases=[c['report']for c in CAPTURES],inputHashes=pins,
             currentBothSlotDeadPoolGroundAndShadowAccepted=True,newNativeBoots=4,newBuilds=0,newROMCopies=0,newZIPs=0,newRawMedia=0,
             allArenaGroundAcceptance=False,fullPortAcceptance=False,goalStatus='active',publicPlayableChanged=False)
 OUT.mkdir();save(OUT/'report.json',report);print(json.dumps(dict(passed=True,cases=4)),flush=True);return report

if __name__=='__main__':
 try:accepted=run()
 except Exception as error:
  need(not OUT.exists(),'Never overwrite actual executed failure');OUT.mkdir();save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedCases=[c.get('report')for c in CAPTURES],fullPortAcceptance=False));print(json.dumps(dict(passed=False,error=repr(error))),flush=True)
 code.interact(banner='Same native terminal mobility carriers remain RAM-only; no replay.',local=dict(module=__import__(__name__),captures=CAPTURES))
