"""Lossless LZX seal: failed Jax phase assertion and qualified terminal campaign.

The Jax full renderer was exact649 fields; its original descriptor-as-pose
assertion failure remains false. No live scene leaves are compressed here.
"""
import json,subprocess
from pathlib import Path
import compact_current_tomb_logs_v3654 as storage
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v4043_jax_campaign_terminal_compression'

def main():
    need(not OUT.exists(),'Fresh immutable storage report')
    pins={str(Path(__file__).resolve()):sha(__file__)}
    for leaf in ('audit_v4010_sonya_zoning700_campaign_observed','audit_v4016_sonya_zoning700_campaign_checked'):
        p=ROOT/leaf/'report.json';r=json.loads(p.read_text());need(r['passed']and not r['fullPortAcceptance'],'Actual native matrix and independent state/FIFO qualification');pins[str(p)]=sha(p)
    failed=ROOT/'audit_v4022_jax_clap_native_scene_observed/report.json';f=json.loads(failed.read_text());need(not f['passed'],'Failed pose assertion remains failed');pins[str(failed)]=sha(failed)
    folders=[ROOT/'audit_v4009_sonya_zoning700_p2_campaign',ROOT/'audit_v4021_jax_clap_kano_p1_native_scene_ram']
    pids=[json.loads((p/'process.json').read_text())['pid']for p in folders]
    q=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @('+','.join(map(str,pids))+') } | Select-Object -ExpandProperty ProcessId'],capture_output=True,text=True)
    need(q.returncode==0 and not q.stdout.strip(),'Both exact native children terminal/missing now')
    files=[]
    for folder in folders:
        need(folder.resolve().is_relative_to(ROOT.resolve())and not folder.is_symlink(),'Exact bounded evidence leaf')
        r=json.loads((folder/'result.json').read_text());need(r['exit_code']==0,'Actual terminal capture')
        if 'jax_clap'in folder.name:need(not r['modelErrors']and r['observedRGBFields']==r['modelExactFields']==649,'Initial full native renderer exact; only later pose identity assertion failed')
        else:need(r['nativeGuestBytesVerifiedInRAM']==1048576 and r['guestDumpFilesWritten']==0,'Qualified actual campaign full-byte RAM guest comparison, no dump')
        for p in folder.iterdir():
            if not p.is_file()or p.suffix not in('.log','.json'):continue
            p=p.resolve();need(p.is_relative_to(folder.resolve())and not p.is_symlink(),'Exact existing metadata/log')
            digest=sha(p);logical=p.stat().st_size;before=storage.allocated(p)
            q=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/I','/Q',str(p)],capture_output=True,text=True)
            need(q.returncode==0 and sha(p)==digest and p.stat().st_size==logical,'Logical bytes/digests/sizes unchanged');after=storage.allocated(p);need(after<=before,'No allocation growth')
            files.append(dict(path=str(p),sha256=digest,logicalBytes=logical,allocatedBefore=before,allocatedAfter=after,reclaimed=before-after));pins[str(p)]=digest
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Report compressed before writes')
    r=dict(passed=True,captureFolders=2,files=files,inputHashes=pins,captureChildrenMissing=pids,deletedFiles=0,newPlayableCopies=0,reclaimedAllocatedBytes=sum(f['reclaimed']for f in files),allocatedBytesAfter=sum(f['allocatedAfter']for f in files),fullPortAcceptance=False)
    (OUT/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items()if k not in('files','inputHashes')}),flush=True)

if __name__=='__main__':main()
