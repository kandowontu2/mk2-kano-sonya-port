"""Exact-target finite ball evidence compression; no build/ROM/archive mutation."""
import hashlib,json,subprocess
from pathlib import Path
from inventory_current_port_storage_v4200 import allocated
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'audit_v6457_current_cpu_ball_render_storage'


def need(value,message):
 if not value:raise ValueError(message)


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def main():
 need(not OUT.exists(),'Fresh finite ball storage proof')
 proof=ROOT/'audit_v6455_current_cpu_ball_render_checked/report.json';report=json.loads(proof.read_text())
 need(report['passed']and report['nativeTerminal']['naturalTerminal']and report['nativeTerminal']['exitCode']==0 and
      not report['nativeTerminal']['observationErrors'],'Actual current full native ball raster/body/shadow acceptance')
 pins=report['inputHashes'];need(all(sha(p)==h for p,h in pins.items()),'Every current/executed/proof input unchanged')
 release=ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'
 release_hash='4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C'
 need(sha(release)==release_hash,'Existing portable ZIP unchanged')
 query=subprocess.run(['powershell','-NoProfile','-Command',"Get-CimInstance Win32_Process -Filter \"Name = 'mkport_candidate.exe'\" | Select-Object ProcessId,Name | ConvertTo-Json -Compress"],capture_output=True,text=True)
 need(query.returncode==0 and not query.stdout.strip(),'Actual empty native process census')
 files=[p for leaf in('audit_v6453_current_cpu_ball_render_ram','audit_v6455_current_cpu_ball_render_checked')for p in(ROOT/leaf).rglob('*')if p.is_file()]
 files.append(ROOT/'mk2ks_current_cpu_ball_render_v6450.lua')
 files.extend(ROOT/'tools'/n for n in('current_cpu_ball_context_v6451.py','capture_current_cpu_ball_render_v6452.py',
                                   'verify_current_cpu_ball_render_v6454.py',Path(__file__).name))
 need(len(files)==len(set(files))and all(p.resolve().is_relative_to(ROOT)for p in files),'Exact resolved finite targets only')
 retained=[]
 for p in files:
  need(p.suffix.lower()not in('.exe','.bin','.wav','.png','.zip'),'No new raw media/build/ROM/archive')
  h=sha(p);before=allocated(p)
  result=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True)
  need(result.returncode==0 and sha(p)==h,'Lossless exact-file compression')
  retained.append(dict(path=str(p),sha256=h,logicalBytes=p.stat().st_size,beforeAllocatedBytes=before,allocatedBytes=allocated(p)))
 need(all(sha(p)==h for p,h in pins.items())and sha(release)==release_hash,'All protected/current/release logical bytes unchanged')
 result=dict(passed=True,files=len(retained),logicalBytes=sum(r['logicalBytes']for r in retained),
             allocatedBytes=sum(r['allocatedBytes']for r in retained),exactTargets=retained,unchangedProtectedPins=len(pins),
             nativePID=report['nativeTerminal']['pid'],completeScreens=report['completeContinuousRender']['fields'],
             noLiveNativeProcess=True,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,deletedFiles=0,
             portableReleaseSHA256=release_hash,goalStatus='active',fullPortAcceptance=False,
             previousGoalTurnClassification=report['previousGoalTurnClassification'],thisGoalTurnClassification=report['thisGoalTurnClassification'])
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(result,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Exact storage manifest compressed')
 print(json.dumps({k:v for k,v in result.items()if k!='exactTargets'}),flush=True)


if __name__=='__main__':main()
