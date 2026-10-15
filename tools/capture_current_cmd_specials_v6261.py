"""Actual canonical CMD -> physical selection -> two specials -> normal recovery.

No new binary, production configuration edit, forced guest state or raw media.
Drain the same native process even if host observation fails; terminal first.
The independent original semantic gate is retained, not a transport-only pass.
"""
import argparse,datetime,gzip,hashlib,json,os,re,subprocess,time,traceback
from pathlib import Path
from collections import defaultdict
import current_payload_metadata_context_v5229 as current
import verify_current_projectile_repeat_v5295 as context
import verify_special_repeat_v5115 as original
ROOT,need,sha=current.ROOT,current.need,current.sha
LUA=ROOT/'mk2ks_cmd_special_repeat_v6260.lua'
LAUNCHER=ROOT/'PLAY_MK2_KANO_SONYA.cmd'

def load_case(move,side):
 folder=ROOT/f'audit_v6262_current_cmd_special_{move}_p{side}'
 report_path=folder/'result.json'
 with gzip.open(folder/'run.log.gz','rt',encoding='utf-8')as reader:text=reader.read()
 rows=defaultdict(list)
 for line in text.splitlines():
  if line.startswith(('MK2_HSPECIAL_','MK2_HPHASE_')):
   rows[line.split()[0]].append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
 report=json.loads(report_path.read_text())
 frames={s['frame']for s in report['actualScenes']}
 entries={original.num(t,'frame')for t in rows['MK2_HSPECIAL_EVENT']if original.num(t,'entry')==original.SPECS[move][1]}
 for tag in('MK2_HPHASE_CANDIDATE','MK2_HPHASE_QUEUE'):
  rows[tag]=[t for t in rows[tag]if int(t['frame'])in frames-entries]
 need('hex='not in text and not re.search(r'LUA ERROR|stack traceback|fatal error|access violation|MK2_HSPECIAL_FAILED',text+(folder/'stderr.log').read_text(),re.I),'No runtime/observer failure or raw buffers persisted')
 return dict(move=move,side=side,folder=folder,report_path=report_path,report=report,rows=rows)

def census():
 command="Get-CimInstance Win32_Process -Filter \"Name='mkport_candidate.exe'\" | Select-Object ProcessId,ParentProcessId,ExecutablePath,CommandLine,@{Name='createdUnix';Expression={([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}} | ConvertTo-Json -Compress"
 r=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True)
 need(r.returncode==0,'Actual native process census')
 jobs=json.loads(r.stdout)if r.stdout.strip()else[]
 return[jobs]if isinstance(jobs,dict)else jobs

def capture(move,side):
 folder=ROOT/f'audit_v6262_current_cmd_special_{move}_p{side}'
 need(not folder.exists(),'Fresh capture; never restart a pending or failed job')
 guest=current.expected();gfx=current.expected_gfx();build=ROOT/current.NAME
 pins=dict(json.loads((build/'build-info.json').read_text(encoding='utf-8-sig'))['input_hashes'])
 for p in(LUA,LAUNCHER,ROOT/'PLAY_CURRENT_V5219_CHECKED.cmd',ROOT/'tools/check_current_playtest_v5975.ps1',ROOT/'mk2ks_special_repeat_v5099.lua',Path(__file__),Path(current.__file__),build/'mkport_candidate.exe',build/'build-info.json',build/'roms/mk2ks/mk2ks.mdata'):
  pins[str(p.resolve())]=sha(p)
 baseline=json.loads((ROOT/'audit_v5116_special_repeat_checked/report.json').read_text())
 need(sha(original.__file__)==baseline['inputHashes'][str(Path(original.__file__).resolve())],'Unchanged independently qualified semantic gate')
 for p in(Path(original.__file__),Path(context.__file__)):pins[str(p.resolve())]=sha(p)
 need(not census(),'No conflicting native job before this cold boot')
 folder.mkdir();env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK2PORT_ACCEPT_)',k)}
 env.update(MK2PORT_ACCEPT_MOVE=move,MK2PORT_ACCEPT_SIDE=str(side),MK2PORT_ACCEPT_AIR='0',MK2PORT_ACCEPT_VICTIM='sub_zero')
 args=[str(LAUNCHER),'-video','none','-sound','none','-noautoframeskip','-frameskip','0','-nothrottle','-str','100','-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),'-snapshot_directory',str(folder/'snap'),'-autoboot_script',str(LUA)]
 command=['cmd.exe','/d','/s','/c','"'+subprocess.list2cmdline(args)+'"']
 scenes=[];proofs={};errors=[];started=time.time();identity=None
 with(folder/'stderr.log').open('w',encoding='utf-8')as err:
  process=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',errors='replace')
  (folder/'process.json').write_text(json.dumps(dict(cmdPID=process.pid,command=command,startedUnix=started),indent=2)+'\n')
  print(f'{move} P{side}: canonical CMD pid={process.pid}',flush=True)
  try:
   time.sleep(2);jobs=census()
   (folder/'live_census.json').write_text(json.dumps(jobs,indent=2)+'\n')
   live=[j for j in jobs if j['ExecutablePath']and Path(j['ExecutablePath']).resolve()==(build/'mkport_candidate.exe').resolve()and j['ParentProcessId']==process.pid and j['createdUnix']>=started and str(folder)in(j['CommandLine']or'')]
   need(len(live)==1,'Exact native executable child of canonical CMD with isolated arguments')
   identity=live[0];(folder/'native_identity.json').write_text(json.dumps(identity,indent=2)+'\n')
  except Exception as error:errors.append(repr(error))
  with gzip.open(folder/'run.log.gz','wt',encoding='utf-8')as log:
   for line in process.stdout:
    try:
     if line.startswith(('MK2_HPHASE_GUEST ','MK2_HPHASE_GFX ','MK2_HPHASE_RGB ')):
      f=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(f.pop('hex'));digest=hashlib.sha256(raw).hexdigest().upper();tag=line.split()[0]
      if tag.endswith('_GUEST')or tag.endswith('_GFX'):
       kind='guest'if tag.endswith('_GUEST')else'gfx';expected=guest if kind=='guest'else gfx
       need(kind not in proofs and f==dict(frame='1',bytes=str(len(expected)))and raw==expected,'Complete independently reconstructed actual '+kind)
       proofs[kind]=dict(bytes=len(raw),sha256=digest,everyActualByteComparedInRAM=True)
      else:
       need(len(raw)==406400 and f['width']=='400'and f['height']=='254'and f['bytes']=='406400','Entire native RGB transport')
       scenes.append(dict(stage=f['stage'],attempt=int(f['attempt']),frame=int(f['frame']),width=400,height=254,bytes=len(raw),sha256=digest,rawMediaFilesWritten=0))
      log.write(tag+'_DIGEST '+' '.join(k+'='+str(v)for k,v in f.items())+' sha256='+digest+'\n')
     else:
      need('hex='not in line,'Never persist any raw buffer');log.write(line)
      if re.search(r'_(READY|COMMAND|RECOVERED|FINAL|FAILED|RESULT) ',line):print(line.strip(),flush=True)
    except Exception as error:errors.append(repr(error))
   exitcode=process.wait()
  terminal=dict(cmdPID=process.pid,nativePID=identity['ProcessId']if identity else None,exitCode=exitcode,naturalTerminal=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),observationErrors=errors)
  (folder/'native_terminal.json').write_text(json.dumps(terminal,indent=2)+'\n')
 need(not census(),'Native terminal confirmed by empty actual census')
 report=dict(passed=False,nativeExit=exitcode,move=move,side=side,victim='sub_zero',candidate=current.NAME,executableSHA256=current.EXE_SHA,guestSHA256=current.GUEST_SHA,payloadSHA256=current.PAYLOAD_SHA,inputHashes=pins,actualScenes=scenes,proofs=proofs,nativeStderrEmpty=not(folder/'stderr.log').read_text().strip(),canonicalCMDUsed=True,skipGameInfoUsed=False,rawGuestGFXRGBPCMOrWAVFilesWritten=0,newBuilds=0,fullPortAcceptance=False)
 try:
  need(exitcode==0 and identity and not errors and len(proofs)==2 and report['nativeStderrEmpty'],'Actual successful immutable native terminal, no host/runtime errors')
  need(all(sha(p)==h for p,h in pins.items()),'All executed inputs unchanged')
  with gzip.open(folder/'run.log.gz','rt',encoding='utf-8')as reader:log=reader.read()
  results=[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in log.splitlines()if line.startswith('MK2_HSPECIAL_RESULT ')]
  need(len(results)==1,'One natural physical controller terminal')
  report.update(passed=True,terminalResult=results[0]);(folder/'result.json').write_text(json.dumps(report,indent=2)+'\n')
  check,_,_=context.bindings();report['independentSemantics']=check(load_case(move,side),guest,(build/'roms/mk2ks/mk2ks.mdata').read_bytes())
 except Exception as error:report.update(passed=False,error=repr(error),traceback=traceback.format_exc())
 (folder/'result.json').write_text(json.dumps(report,indent=2)+'\n')
 for p in folder.rglob('*'):
  if p.is_file():need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0,'Compress exact terminal artifact')
 print(json.dumps(dict(move=move,side=side,passed=report['passed'],nativeExit=exitcode,error=report.get('error'),scenes=len(scenes))),flush=True)
 need(report['passed'],'Canonical-CMD physical regression failed; preserve actual failure')
 return report

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--move',choices=original.SPECS);parser.add_argument('--side',type=int,choices=(1,2));a=parser.parse_args()
 need(bool(a.move)==bool(a.side),'Specify both move/side, or the complete sixteen-case matrix')
 cases=[(a.move,a.side)]if a.move else[(m,s)for m in original.SPECS for s in(1,2)]
 for move,side in cases:capture(move,side)
