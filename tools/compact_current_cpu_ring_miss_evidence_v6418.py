"""Exact SHA-preserving finite missed-Ring evidence compression; no deletion."""
import hashlib,json,subprocess
from pathlib import Path
from inventory_current_port_storage_v4200 import allocated
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'audit_v6419_current_cpu_ring_miss_storage'

def need(value,message):
 if not value:raise ValueError(message)

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()

def main():
 need(not OUT.exists(),'Fresh finite storage inventory')
 proof=ROOT/'audit_v6415_current_cpu_ring_miss_render_checked/report.json'
 phase=ROOT/'audit_v6417_current_cpu_ring_miss_phase_checked/report.json'
 render=json.loads(proof.read_text());mechanics=json.loads(phase.read_text())
 need(render['passed'] and mechanics['passed'] and render['nativeTerminal']['exitCode']==0 and
      not render['nativeTerminal']['observationErrors'],'Actual current native miss rendering and phase terminal proofs')
 pins={**render['inputHashes'],**mechanics['inputHashes']}
 need(all(sha(p)==h for p,h in pins.items()),'All protected/current/source/capture hashes intact before compression')
 dirs=('audit_v6413_current_cpu_ring_miss_render_ram','audit_v6415_current_cpu_ring_miss_render_checked',
       'audit_v6417_current_cpu_ring_miss_phase_checked')
 files=[p for name in dirs for p in (ROOT/name).rglob('*')if p.is_file()]
 files+=[ROOT/'mk2ks_current_cpu_ring_miss_render_ram_v6410.lua']
 files+=[ROOT/'tools'/name for name in('current_cpu_ring_miss_phase_v6411.py',
  'capture_current_cpu_ring_miss_render_v6412.py','verify_current_cpu_ring_miss_render_v6414.py',
  'verify_current_cpu_ring_miss_phase_faults_v6416.py',Path(__file__).name)]
 need(len(files)==len(set(files)) and all(p.is_relative_to(ROOT) and p.is_file()for p in files),'Exact resolved finite targets only')
 rows=[]
 for p in files:
  need(p.suffix.lower()not in('.exe','.bin','.zip','.wav','.png'),'No build/ROM/raw-media copy retained')
  h=sha(p);before=allocated(p)
  code=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True)
  need(code.returncode==0 and sha(p)==h,'Exact file losslessly compressed')
  rows.append(dict(path=str(p),sha256=h,logicalBytes=p.stat().st_size,beforeAllocatedBytes=before,allocatedBytes=allocated(p)))
 need(all(sha(p)==h for p,h in pins.items()),'All current/protected logical hashes unchanged after compression')
 query=subprocess.run(['powershell','-NoProfile','-Command',"Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'mkport_candidate.exe' -or $_.ProcessId -eq 175204 } | Select-Object ProcessId,Name,ExecutablePath | ConvertTo-Json -Compress"],capture_output=True,text=True)
 need(query.returncode==0 and not query.stdout.strip(),'Actual native process census terminal/empty')
 result=dict(passed=True,files=len(rows),logicalBytes=sum(r['logicalBytes']for r in rows),
  allocatedBytes=sum(r['allocatedBytes']for r in rows),beforeAllocatedBytes=sum(r['beforeAllocatedBytes']for r in rows),
  unchangedProtectedPins=len(pins),exactTargets=rows,noNativeProcess=True,newBuilds=0,newROMCopies=0,newRawMedia=0,
  deletedFiles=0,goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(result,indent=2)+'\n');h=sha(path)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==h,'Storage manifest losslessly compressed')
 print(json.dumps({k:v for k,v in result.items()if k!='exactTargets'}),flush=True)

if __name__=='__main__':main()
