"""Exact finite compound evidence compression; no new build/ROM/raw copies."""
import hashlib,json,subprocess
from pathlib import Path
from inventory_current_port_storage_v4200 import allocated
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'audit_v6441_current_cpu_compound_storage'


def need(value,message):
 if not value:raise ValueError(message)


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def main():
 need(not OUT.exists(),'Fresh exact-target finite storage proof')
 proof=ROOT/'audit_v6436_current_cpu_compound_render_checked/report.json';report=json.loads(proof.read_text())
 need(report['passed']and report['nativeTerminal']['exitCode']==0 and not report['nativeTerminal']['observationErrors'],
      'Actual current full compound/native shadow/raster qualification')
 pins=report['inputHashes'];need(all(sha(p)==h for p,h in pins.items()),'Every current/source/actual proof input unchanged')
 release=ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'
 release_hash='4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C'
 need(sha(release)==release_hash,'Existing portable playtest ZIP unchanged')
 dirs=('audit_v6434_current_cpu_compound_render_ram','audit_v6439_current_cpu_compound_render_ram','audit_v6436_current_cpu_compound_render_checked')
 files=[p for name in dirs for p in(ROOT/name).rglob('*')if p.is_file()]
 files+=[ROOT/name for name in('mk2ks_current_cpu_compound_render_ram_v6432.lua','mk2ks_current_cpu_compound_render_ram_v6437.lua')]
 files+=[ROOT/'tools'/name for name in('capture_current_cpu_compound_render_v6433.py','capture_current_cpu_compound_render_v6438.py',
                                    'verify_current_cpu_compound_render_v6435.py',Path(__file__).name)]
 need(len(files)==len(set(files))and all(p.resolve().is_relative_to(ROOT)for p in files),'Only exact resolved finite evidence targets')
 retained=[]
 for p in files:
  need(p.suffix.lower()not in('.exe','.bin','.zip','.wav','.png'),'No new build/ROM/raw medium retained')
  h=sha(p);before=allocated(p)
  result=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True)
  need(result.returncode==0 and sha(p)==h,'Exact lossless retained-file compression')
  retained.append(dict(path=str(p),sha256=h,logicalBytes=p.stat().st_size,beforeAllocatedBytes=before,allocatedBytes=allocated(p)))
 need(all(sha(p)==h for p,h in pins.items())and sha(release)==release_hash,'All protected/current/release logical hashes unchanged')
 query=subprocess.run(['powershell','-NoProfile','-Command',"Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'mkport_candidate.exe' -or $_.ProcessId -eq 157940 -or $_.ProcessId -eq 159440 } | Select-Object ProcessId,Name | ConvertTo-Json -Compress"],capture_output=True,text=True)
 need(query.returncode==0 and not query.stdout.strip(),'Both native processes actually terminal; no live emulator')
 result=dict(passed=True,files=len(retained),logicalBytes=sum(r['logicalBytes']for r in retained),
             beforeAllocatedBytes=sum(r['beforeAllocatedBytes']for r in retained),allocatedBytes=sum(r['allocatedBytes']for r in retained),
             unchangedProtectedPins=len(pins),exactTargets=retained,noLiveNativeProcess=True,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
             deletedFiles=0,portableReleaseSHA256=release_hash,goalStatus='active',fullPortAcceptance=False,
             previousGoalTurnClassification='no progress: acknowledgement only; authoritative current files and empty process census revalidated',
             thisGoalTurnClassification='progress: full naturally chained CPU leg/Square/ordinary source art, raster and absolute floor shadows qualified')
 OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(result,indent=2)+'\n');h=sha(path)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==h,'Exact storage manifest compressed')
 print(json.dumps({k:v for k,v in result.items()if k!='exactTargets'}),flush=True)


if __name__=='__main__':main()
