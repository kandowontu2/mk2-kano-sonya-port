"""Lossless LZX seal of terminal native inflation/campaign logs; no deletions."""
import json,subprocess
from pathlib import Path
import compact_current_tomb_logs_v3654 as storage
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v3936_inflation_campaign_compression'

def main():
    need(not OUT.exists(),'Fresh immutable compression report')
    reports=[ROOT/p/'report.json'for p in('audit_v3922_kitana_inflation_native_scene_observed','audit_v3925_kitana_inflation_native_fifo_checked','audit_v3934_kitana_inflation_earned_state_checked','audit_v3929_sonya_later_start_campaign_checked')]
    pins={str(Path(__file__).resolve()):sha(__file__)}
    for path in reports:
        value=json.loads(path.read_text());need(value['passed'],'Actual terminal capture and independent source/state qualification');pins[str(path)]=sha(path)
    folders=[ROOT/'audit_v3911_sonya_zoning_later_start_p2_campaign']
    for fighter,side in(('kano',1),('kano',2),('sonya',1),('sonya',2)):
        folders.append(ROOT/f'audit_v3921_kitana_{fighter}_p{side}_native_scene_ram')
    pids=[json.loads((folder/'process.json').read_text())['pid']for folder in folders]
    command='Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @('+','.join(map(str,pids))+') } | Select-Object -ExpandProperty ProcessId'
    check=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True)
    need(check.returncode==0 and not check.stdout.strip(),'Only exact recorded terminal capture PIDs missing now; leave live3931 and unrelated processes alone')
    records=[]
    for folder in folders:
        need(folder.resolve().is_relative_to(ROOT.resolve())and not folder.is_symlink(),'Exact named safe evidence leaf')
        need(json.loads((folder/'result.json').read_text())['exit_code']==0,'Actual emulator terminal0')
        for path in folder.iterdir():
            if not path.is_file()or path.suffix not in('.log','.json'):continue
            path=path.resolve();need(path.is_relative_to(folder.resolve())and not path.is_symlink(),'Exact existing log/metadata file')
            logical=path.stat().st_size;digest=sha(path);before=storage.allocated(path)
            done=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/I','/Q',str(path)],capture_output=True,text=True)
            need(done.returncode==0 and sha(path)==digest and path.stat().st_size==logical,'All logical bytes/hashes/sizes unchanged')
            after=storage.allocated(path);need(after<=before,'No allocated-byte increase')
            records.append(dict(path=str(path),sha256=digest,logicalBytes=logical,allocatedBefore=before,allocatedAfter=after,reclaimed=before-after));pins[str(path)]=digest
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compression inherited before report writes')
    value=dict(passed=True,captureFolders=len(folders),files=records,inputHashes=pins,captureChildrenMissing=pids,
        deletedFiles=0,newPlayableCopies=0,reclaimedAllocatedBytes=sum(r['reclaimed']for r in records),allocatedBytesAfter=sum(r['allocatedAfter']for r in records),
        excludedLiveCampaign='audit_v3931_sonya_leg_later_start_p2_campaign',fullPortAcceptance=False)
    (OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n');print(json.dumps({k:v for k,v in value.items()if k not in('files','inputHashes')}))

if __name__=='__main__':main()
