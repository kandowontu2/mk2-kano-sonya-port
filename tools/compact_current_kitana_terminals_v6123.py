"""Force terminal-only LZX conversion; inherited NTFS compression skips without /F."""
import json,subprocess
from pathlib import Path
import checkpoint_current_kitana_scene_v6121 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v6124_current_kitana_terminal_storage_checked'

def run():
 proof=json.loads(prior.PROOF.read_text());need(proof['passed']and all(sha(p)==h for p,h in proof['inputHashes'].items()),'Complete current native matrix/evidence intact')
 exe=ROOT/prior.current.NAME/'mkport_candidate.exe'
 query="Get-CimInstance Win32_Process | Where-Object { $_.ExecutablePath -eq '"+str(exe).replace("'","''")+"' } | Select-Object ProcessId,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
 need(census.returncode==0 and not census.stdout.strip(),'Actual native emulator process census empty')
 targets=[]
 for c in proof['cases']:
  need(c['actualWindowsTerminal']['nativeExit']==0,'Each exact capture is natively terminal')
  folder=(ROOT/f"audit_v6114_current_kitana_{c['fighter']}_p{c['side']}_native_scene_ram").resolve()
  need(folder.parent==ROOT.resolve(),'Exact target within requested mk2port workspace')
  for p in folder.iterdir():
   if p.is_file():need(str(p.resolve())in proof['inputHashes']and p.suffix in('.json','.log'),'Already pinned terminal metadata/trace only');targets.append(p)
 before={str(p):prior.allocated(p)for p in targets}
 result=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',*[str(p)for p in targets]],capture_output=True,text=True)
 need(result.returncode==0 and all(sha(p)==h for p,h in proof['inputHashes'].items()),'Forced exact-file LZX preserves all executed/evidence logical bytes')
 after={str(p):prior.allocated(p)for p in targets}
 return dict(passed=True,files=len(targets),logicalBytes=sum(p.stat().st_size for p in targets),
      allocatedBytesBefore=sum(before.values()),allocatedBytesAfter=sum(after.values()),
      allocatedBytesReclaimed=sum(before.values())-sum(after.values()),actualBefore=before,actualAfter=after,
      compressionOutput=result.stdout,filesDeleted=0,newBuildCopies=0,nativeGameChanges=0,
      inputHashes={str(prior.PROOF):sha(prior.PROOF),str(Path(__file__).resolve()):sha(__file__)},
      fullPortAcceptance=False)

if __name__=='__main__':
 need(not OUT.exists(),'Fresh exact terminal storage audit')
 report=run();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualBefore','actualAfter','compressionOutput')},indent=2))
