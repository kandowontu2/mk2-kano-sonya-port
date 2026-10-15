"""Bounded SHA-preserving miss-audio compression; retain failed startup too."""
import hashlib,json,subprocess
from pathlib import Path
from inventory_current_port_storage_v4200 import allocated
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'audit_v6431_current_cpu_ring_miss_audio_storage'

def need(value,message):
 if not value:raise ValueError(message)

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()

def main():
 need(not OUT.exists(),'Fresh finite source-audio storage record')
 proof=ROOT/'audit_v6429_current_cpu_ring_miss_audio_checked/report.json'
 report=json.loads(proof.read_text())
 need(report['passed'] and report['nativeTerminal']['nativeExit']==0 and not report['nativeTerminal']['hostDecodeErrors'],
      'Actual successful current source/native miss PCM/cue/retirement proof')
 pins=report['inputHashes']
 need(all(sha(p)==h for p,h in pins.items()),'All executed current/protected/source/capture evidence hashes intact')
 release=ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'
 release_hash='4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C'
 need(sha(release)==release_hash,'Existing portable ZIP unchanged, no replacement/copy')
 dirs=('audit_v6424_current_cpu_ring_miss_audio_ram','audit_v6427_current_cpu_ring_miss_audio_ram',
       'audit_v6429_current_cpu_ring_miss_audio_checked')
 files=[p for name in dirs for p in (ROOT/name).rglob('*')if p.is_file()]
 files+=[ROOT/name for name in('mk2ks_current_cpu_ring_miss_audio_v6422.lua','mk2ks_current_cpu_ring_miss_audio_v6425.lua')]
 files+=[ROOT/'tools'/name for name in('capture_current_cpu_ring_miss_audio_v6423.py',
  'capture_current_cpu_ring_miss_audio_v6426.py','verify_current_cpu_ring_miss_audio_v6428.py',Path(__file__).name)]
 need(len(files)==len(set(files)) and all(p.resolve().is_relative_to(ROOT)for p in files),'Only exact resolved finite evidence targets')
 rows=[]
 for p in files:
  need(p.suffix.lower()not in('.bin','.exe','.zip','.wav','.png'),'No raw media/guest/ROM/build retained in new evidence')
  h=sha(p);before=allocated(p)
  code=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True)
  need(code.returncode==0 and sha(p)==h,'Exact actual retained file losslessly compressed')
  rows.append(dict(path=str(p),sha256=h,logicalBytes=p.stat().st_size,beforeAllocatedBytes=before,allocatedBytes=allocated(p)))
 need(all(sha(p)==h for p,h in pins.items()) and sha(release)==release_hash,'All protected/current/release hashes unchanged after compression')
 query=subprocess.run(['powershell','-NoProfile','-Command',"Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'mkport_candidate.exe' -or $_.ProcessId -eq 170192 -or $_.ProcessId -eq 173684 } | Select-Object ProcessId,Name | ConvertTo-Json -Compress"],capture_output=True,text=True)
 need(query.returncode==0 and not query.stdout.strip(),'Actual native process census confirms both runs terminal')
 result=dict(passed=True,files=len(rows),logicalBytes=sum(r['logicalBytes']for r in rows),
  allocatedBytes=sum(r['allocatedBytes']for r in rows),beforeAllocatedBytes=sum(r['beforeAllocatedBytes']for r in rows),
  unchangedProtectedPins=len(pins),portableReleaseSHA256=release_hash,exactTargets=rows,
  failedStartupPreserved=True,noLiveNativeProcess=True,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
  deletedFiles=0,goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(result,indent=2)+'\n');h=sha(path)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==h,'Storage report losslessly compressed')
 print(json.dumps({k:v for k,v in result.items()if k!='exactTargets'}),flush=True)

if __name__=='__main__':main()
