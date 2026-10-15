"""Exact SHA-preserving NTFS compression of this finite mirror audio work.

No deletion, build, ROM/source copy or broad traversal. Measure actual disk
allocation with the existing Win32 inventory helper, not logical file size.
"""
import hashlib,json,subprocess
from pathlib import Path
from inventory_current_port_storage_v4200 import allocated

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'audit_v6409_current_cpu_ring_mirror_audio_storage'

def need(value,message):
 if not value:raise ValueError(message)

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()

def main():
 need(not OUT.exists(),'Fresh finite storage evidence')
 proof=ROOT/'audit_v6407_current_cpu_ring_mirror_audio_checked/report.json'
 report=json.loads(proof.read_text())
 need(report['passed'] and report['nativeTerminal']['nativeExit']==0,'Actual full waveform and independent mirror qualification')
 pins=report['inputHashes']
 need(all(sha(p)==h for p,h in pins.items()),'All current/protected/source/capture evidence intact before compression')
 dirs=[
  'audit_v6395_current_cpu_ring_mirror_audio_ram',
  'audit_v6398_preserved_first_video_boundary_failure',
  'audit_v6402_preserved_square_gain_failure',
  'audit_v6403_current_cpu_ring_mirror_audio_ram_checked',
  'audit_v6406_preserved_verifier_import_failure',
  'audit_v6407_current_cpu_ring_mirror_audio_checked',
 ]
 files=[p for name in dirs for p in (ROOT/name).iterdir()if p.is_file()]
 files+=[ROOT/'mk2ks_current_cpu_ring_mirror_audio_v6393.lua']
 files+=[ROOT/'tools'/name for name in(
  'capture_current_cpu_ring_mirror_audio_v6394.py',
  'finish_current_cpu_ring_mirror_audio_v6396.py',
  'finish_current_cpu_ring_mirror_audio_v6398.py',
  'finish_current_cpu_ring_mirror_audio_v6400.py',
  'finish_current_cpu_ring_mirror_audio_v6402.py',
  'verify_current_cpu_ring_mirror_audio_v6404.py',
  'verify_current_cpu_ring_mirror_audio_v6406.py',Path(__file__).name)]
 need(len(files)==len(set(files)) and all(p.is_relative_to(ROOT) and p.is_file()for p in files),'Only resolved exact finite targets')
 rows=[]
 for p in files:
  need(p.suffix.lower()not in('.exe','.bin','.zip','.wav','.png'),'No playable or raw-media copies among new evidence')
  h=sha(p);before=allocated(p)
  code=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True)
  need(code.returncode==0 and sha(p)==h,'Exact retained bytes losslessly compressed')
  rows.append(dict(path=str(p),sha256=h,logicalBytes=p.stat().st_size,beforeAllocatedBytes=before,allocatedBytes=allocated(p)))
 need(all(sha(p)==h for p,h in pins.items()),'All protected/capture/model hashes unchanged after compression')
 query=subprocess.run(['powershell','-NoProfile','-Command',"Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'mkport_candidate.exe' -or $_.ProcessId -eq 155308 } | Select-Object ProcessId,Name,ExecutablePath | ConvertTo-Json -Compress"],capture_output=True,text=True)
 need(query.returncode==0 and not query.stdout.strip(),'Actual native process census terminal/empty')
 result=dict(passed=True,files=len(rows),logicalBytes=sum(r['logicalBytes']for r in rows),
  allocatedBytes=sum(r['allocatedBytes']for r in rows),beforeAllocatedBytes=sum(r['beforeAllocatedBytes']for r in rows),
  unchangedProtectedPins=len(pins),exactTargets=rows,noNativeProcess=True,newBuilds=0,newROMCopies=0,newRawMedia=0,
  deletedFiles=0,goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(result,indent=2)+'\n');h=sha(path)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==h,'Storage manifest losslessly compressed')
 print(json.dumps({k:v for k,v in result.items()if k!='exactTargets'}),flush=True)

if __name__=='__main__':main()
