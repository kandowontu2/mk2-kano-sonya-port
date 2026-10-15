"""Actual cold native queue/actor reset provenance, with one guest buffer in RAM."""
import datetime,hashlib,json,os,re,subprocess,time,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
FOLDER=ROOT/'audit_v5397_ko_queue_lifecycle'
OUT=ROOT/'audit_v5398_ko_queue_lifecycle_observed'
LUA=ROOT/'mk2ks_ko_queue_lifecycle_v5396.lua'

def run():
 guest=current.expected();parent=ROOT/'audit_v5395_current_ko_round_body_shadow_progress/progress.json'
 journal=json.loads(parent.read_text());need(journal['passed']and journal['goalStatus']=='active','Actual transition prerequisite active')
 pins=dict(journal['newInputHashes']);pins[str(parent)]=sha(parent)
 for p in(LUA,Path(__file__).resolve()):pins[str(p)]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All authoritative compiled, original physical and current observer sources stable')
 for name in('mk2ks_cpu_square_shadow_v5341.lua','mk2ks_cpu_choke_shadow_v5328.lua','mk2ks_special_shadow_v5131.lua'):
  p=ROOT/name;pins[str(p)]=sha(p)
 need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|:reset\(',LUA.read_text()),'Queue observer never changes guest/state/CPU/registers')
 old=ROOT/'audit_v5351_current_cpu_sonya_square_human_kano';process=json.loads((old/'process.json').read_text());command=process['command'][:]
 for i,value in enumerate(command):
  if str(old)in value:command[i]=value.replace(str(old),str(FOLDER))
 command[command.index('-autoboot_script')+1]=str(LUA)
 env=os.environ.copy()
 for key in tuple(env):
  if key.startswith('MK2KS_'):env.pop(key)
 env.update(MK2KS_TEST_FIGHTER='kano',MK2KS_TEST_BOOT_FRAME='613',MK2KS_CPU_PAIR_APPROACH='guard_until_close',
  MK2KS_CPU_PAIR_CONFIRM_AGE='264',MK2KS_CPU_CONTINUATION_POLICY='jump_guard')
 need(not FOLDER.exists(),'Fresh native runtime directory')
 FOLDER.mkdir()
 (FOLDER/'input_hashes_before.json').write_text(json.dumps(pins,indent=2)+'\n')
 for name in('cfg','nvram','snap'):(FOLDER/name).mkdir()
 captured=None;start=time.time()
 with (FOLDER/'stderr.log').open('w',encoding='utf-8')as stderr,(FOLDER/'run.log').open('w',encoding='utf-8')as output:
  proc=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=stderr,text=True,encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW)
  (FOLDER/'process.json').write_text(json.dumps(dict(pid=proc.pid,command=command,env={k:v for k,v in env.items()if k.startswith('MK2KS_')}),indent=2)+'\n')
  print('Native queue lifecycle PID '+str(proc.pid),flush=True)
  for line in proc.stdout:
   if line.startswith('MK2_QUEUE_LIFECYCLE_GUEST '):
    need(captured is None,'Exactly one actual entire initialized guest buffer')
    raw=bytes.fromhex(re.search(r'hex=([0-9a-fA-F]+)',line)[1]);need(raw==guest,'Whole actual initialized guest equals independent current source')
    captured=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest().upper());del raw
    output.write('MK2_QUEUE_LIFECYCLE_GUEST frame=1 bytes=1048576 sha256='+captured['sha256']+'\n')
   else:
    need('hex='not in line,'No old RAM/body/RGB/GFX/media observer loaded');output.write(line)
  exit_code=proc.wait()
 log=(FOLDER/'run.log').read_text();need(exit_code==0 and captured and (FOLDER/'stderr.log').read_text()==''and
  not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',log,re.I),'Actual warning-free native terminal0')
 prefixes=('MK2_CPU_PAIR_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_','MK2_CPU_CHOICE_','MK2_SQUARE_NATIVE_','MK2_P2CPU_','MK2_SQUARE_BOUNDARY_','MK2_SQUARE_LOCK_')
 select=lambda text:[line for line in text.splitlines()if line.startswith(prefixes)]
 need(select(log)==select((old/'run.log').read_text())and len(select(log))==8848,'Entire actual native physical input/state/HP/choices trajectory unchanged, including earned KO/reset')
 need('MK2_QUEUE_LIFECYCLE_CODE frame=3208'in log and 'MK2_QUEUE_LIFECYCLE_STOP frame=3623'in log,'Actual round lifecycle observed and original terminal retained')
 need(all(sha(p)==h for p,h in pins.items()),'Executed sources/evidence stable at actual native terminal')
 before=sha(FOLDER/'run.log');compressed=subprocess.run(['compact.exe','/C','/EXE:LZX','/I','/Q',str(FOLDER/'run.log')],capture_output=True)
 need(compressed.returncode==0 and sha(FOLDER/'run.log')==before,'Compress exact native text without changing evidence')
 report=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),candidate=current.NAME,nativeExit=exit_code,
  nativePID=proc.pid,seconds=time.time()-start,actualGuestMemoryProof=captured,originalWholePhysicalTrajectoryUnchanged=True,
  actualPhysicalTrajectoryRecords=8848,newNativeBoots=1,newBuilds=0,rawMediaFilesWritten=0,inputHashes=pins,
  sourceQueueLifecycleAcceptancePending=True,fullPortAcceptance=False)
 (FOLDER/'result.json').write_text(json.dumps(report,indent=2)+'\n')
 return report

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable native queue lifecycle observation')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
