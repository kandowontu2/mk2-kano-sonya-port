"""Reclaim allocated space from exact terminal air traces without losing evidence.

No deletion, build, raw-media or recovery copies. Native terminal identities
and byte hashes are required before lossless Windows LZX compression. Failed
controller/test assumptions stay available and are never marked gameplay wins.
"""
import datetime,json,subprocess
from pathlib import Path
import current_payload_metadata_context_v5229 as current
from record_current_cross_tomb_audio_v5844 import allocated
from qualify_current_air_throw_roles_v6051 import MATRIX
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v6058_current_air_trace_storage_sealed'

def run():
 need(not OUT.exists(),'Fresh bounded terminal-trace storage seal')
 pairs=[('audit_v6041_air_kano_p1_kitana','audit_v6042_air_kano_p1_kitana_observed')]
 pairs.extend((f'audit_v6045_air_{f}_p{s}_{v}',f'audit_v6046_air_{f}_p{s}_{v}_observed')for f,s,v in
              (('kano',1,'kitana'),('kano',2,'kitana'),('kano',1,'sonya'),('sonya',1,'jax')))
 pairs.extend((f'audit_v6049_air_{f}_p{s}_{v}',f'audit_v6050_air_{f}_p{s}_{v}_observed')for f,s,v in MATRIX)
 census=subprocess.run(['powershell.exe','-NoProfile','-Command',
  "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'mkport*' } | Select-Object ProcessId,Name,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress"],capture_output=True,text=True)
 need(census.returncode==0,'Actual Windows native process census before storage operation')
 live=json.loads(census.stdout)if census.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 paths=[];images=[];processes=[]
 for index,(foldername,reportname)in enumerate(pairs):
  folder=ROOT/foldername;rp=ROOT/reportname/'report.json';process=json.loads((folder/'process.json').read_text())
  terminal=json.loads((folder/'native_terminal.json').read_text());report=json.loads(rp.read_text())
  need(terminal['nativeExit']==0 and terminal['pid']==process['pid']==process['actualWindowsIdentity']['ProcessId']and
       terminal['actualWindowsIdentity']==process['actualWindowsIdentity'],'Actual native terminal0 identity persisted even on failed postassertions')
  need(report['passed']==(index>=5),'Only eight full current captures passed; five real failed diagnostic assumptions preserved')
  need(not any(r['ProcessId']==process['pid']and r['Name']==process['actualWindowsIdentity']['Name']and
               r['CreationDate']==process['actualWindowsIdentity']['CreationDate']and
               r['ExecutablePath']==process['actualWindowsIdentity']['ExecutablePath']and
               r['CommandLine']==process['actualWindowsIdentity']['CommandLine']for r in live),
       'Exact captured PID/name/creation/executable/command confirmed terminal, no timeout/restart guess')
  processes.append(dict(folder=foldername,process=process,terminal=terminal,observerPassed=report['passed']))
  paths.extend(p for d in(folder,ROOT/reportname)for p in d.rglob('*')if p.is_file()and p.suffix.lower()in('.log','.json','.cfg','.txt'))
  images.extend(folder.rglob('*.png'))
 need(len(images)==68,'Only bounded declared rendered native PNGs and sheets, no final timeout duplicate/raw media')
 for name in('mk2ks_air_throw_roles_v6039.lua','mk2ks_air_native_ready_v6043.lua','mk2ks_air_native_dispatch_v6047.lua',
  'tools/capture_current_air_throw_roles_v6040.py','tools/capture_current_air_native_ready_v6044.py','tools/capture_current_air_native_dispatch_v6048.py',
  'tools/qualify_current_air_throw_roles_v6051.py','tools/qualify_current_air_followup_fault_v6053.py','tools/qualify_current_air_native_lookup_v6055.py'):
  paths.append(ROOT/name)
 paths.extend((ROOT/'audit_v6052_current_air_throw_roles_checked/report.json',ROOT/'audit_v6054_current_air_followup_fault_checked/report.json',Path(__file__).resolve()))
 paths=list(dict.fromkeys(p.resolve()for p in paths));pins={str(p):sha(p)for p in paths+images}
 for p in paths:need(p.is_relative_to(ROOT)and p.is_file(),'Exact existing completed workspace text target only')
 # Protect the current matched build and requested current ZIP; never rebuild.
 package=ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'
 artifacts={ROOT/current.NAME/'mkport_candidate.exe':current.EXE_SHA,
            ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata':current.PAYLOAD_SHA,
            package:'4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C'}
 need(all(sha(p)==v for p,v in artifacts.items()),'Matched current build/payload/requested ZIP intact before sealing')
 before=sum(allocated(p)for p in paths);logical=sum(p.stat().st_size for p in paths)
 for p in paths:
  result=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True)
  need(result.returncode==0 and sha(p)==pins[str(p)],'Every exact completed trace/source losslessly compressed, logical bytes unchanged')
 after=sum(allocated(p)for p in paths)
 need(all(sha(p)==v for p,v in pins.items())and all(sha(p)==v for p,v in artifacts.items()),'Every retained failed/success/native visual/build/package byte immutable')
 report=dict(passed=True,storageOnly=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
  goalStatus='active',fullPortAcceptance=False,sealedTextFiles=len(paths),sealedTextLogicalBytes=logical,
  allocatedBytesBefore=before,allocatedBytesAfter=after,allocatedBytesReclaimed=before-after,
  retainedNativeCaptureFolders=13,retainedPassingNativeCaptures=8,retainedFailedNativeDiagnostics=5,
  capturedNativeProcesses=processes,actualLiveNativeCensus=live,exactCapturedProcessesStillLive=[],
  boundedNativePNGArtifacts=68,boundedNativePNGBytes=sum(p.stat().st_size for p in images),
  inputHashes=pins,protectedMatchedArtifactHashes={str(p):v for p,v in artifacts.items()},
  newBuilds=0,newZIPs=0,newRawMediaOrRecoveryCopies=0,filesDeleted=0,recoverability='All logical files retained byte-identical; only NTFS allocated storage compressed.')
 OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(report,indent=2)+'\n');digest=sha(path)
 need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==digest,
      'Storage seal itself losslessly retained')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','capturedNativeProcesses')},indent=2),flush=True)

if __name__=='__main__':run()
