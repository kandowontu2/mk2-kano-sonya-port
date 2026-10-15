"""Lossless LZX seal of16 terminal actual Jax native-audio leaves, no deletion."""
import json,subprocess
from pathlib import Path
import compact_current_tomb_logs_v3654 as storage
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v4070_jax_clap_audio_compression'

def main():
    need(not OUT.exists(),'Fresh immutable storage report')
    pins={str(Path(__file__).resolve()):sha(__file__)}
    for leaf in ('audit_v4056_jax_clap_native_audio_queue_observed','audit_v4061_jax_clap_native_audio_routes_observed','audit_v4067_jax_clap_native_audio_routes_checked'):
        p=ROOT/leaf/'report.json';r=json.loads(p.read_text());need(r['passed']and not r['fullPortAcceptance'],'Actual native matrix and independent state/FIFO qualification');pins[str(p)]=sha(p)
    folders=[ROOT/f'audit_v{version}_jax_clap_{f}_p{s}_audio_queue_{mode}'for version in(4055,4060)for f in('kano','sonya')for s in(1,2)for mode in('samples','nosamples')]
    pids=[json.loads((p/'process.json').read_text())['pid']for p in folders]
    q=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @('+','.join(map(str,pids))+') } | Select-Object -ExpandProperty ProcessId'],capture_output=True,text=True)
    need(q.returncode==0 and not q.stdout.strip(),'All16 exact native children terminal/missing now')
    files=[]
    for folder in folders:
        need(folder.resolve().is_relative_to(ROOT.resolve())and not folder.is_symlink(),'Exact bounded evidence leaf')
        r=json.loads((folder/'result.json').read_text());need(r['exit_code']==0 and r['mixedPCMBytesVerifiedInRAM']>0 and r['mixedPCMUpdates']>0 and r['rawAudioRasterVRAMROMCopiesWritten']==0,'Actual terminal whole PCM/guest RAM capture')
        for p in folder.iterdir():
            if not p.is_file()or p.suffix not in('.log','.json'):continue
            p=p.resolve();need(p.is_relative_to(folder.resolve())and not p.is_symlink(),'Exact existing metadata/log')
            digest=sha(p);logical=p.stat().st_size;before=storage.allocated(p)
            q=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/I','/Q',str(p)],capture_output=True,text=True)
            need(q.returncode==0 and sha(p)==digest and p.stat().st_size==logical,'Logical bytes/digests/sizes unchanged');after=storage.allocated(p);need(after<=before,'No allocation growth')
            files.append(dict(path=str(p),sha256=digest,logicalBytes=logical,allocatedBefore=before,allocatedAfter=after,reclaimed=before-after));pins[str(p)]=digest
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Report compressed before writes')
    r=dict(passed=True,captureFolders=16,files=files,inputHashes=pins,captureChildrenMissing=pids,deletedFiles=0,newPlayableCopies=0,reclaimedAllocatedBytes=sum(f['reclaimed']for f in files),allocatedBytesAfter=sum(f['allocatedAfter']for f in files),fullPortAcceptance=False)
    (OUT/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items()if k not in('files','inputHashes')}),flush=True)

if __name__=='__main__':main()
