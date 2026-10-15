"""Lossless terminal-log seal and exact unwanted timeout PNG cleanup only.

Failed probe logs/results stay immutable and false. The original full campaign
qualifier is still pending; sealing logical bytes does not promote it.
"""
import json,subprocess
from pathlib import Path
import compact_current_tomb_logs_v3654 as storage
import run_current_clean_uppercut_ram_v4155 as current

ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v4173_terminal_ready_probe_log_seal'

def main():
    need(not OUT.exists(),'Fresh cleanup evidence')
    folders=[ROOT/'audit_v4146_sonya_guard_uppercut_ready_p2_campaign',ROOT/'audit_v4170_current_sonya_p2_block_release_uppercut_ram',ROOT/'audit_v4176_current_sonya_p2_block_release_uppercut_ready_ram']
    pids=[json.loads((p/'process.json').read_text())['pid'] for p in folders]
    q=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @('+','.join(map(str,pids))+') } | Select-Object -ExpandProperty ProcessId'],capture_output=True,text=True)
    need(q.returncode==0 and not q.stdout.strip(),'Exact native captures terminal now')
    pins={str(Path(__file__).resolve()):sha(__file__),str(Path(storage.__file__).resolve()):sha(storage.__file__)}
    for name in ('audit_v4147_sonya_guard_uppercut_ready_campaign_observed','audit_v4171_current_sonya_p2_block_release_uppercut_checked','audit_v4177_current_sonya_p2_block_release_uppercut_ready_checked'):
        p=ROOT/name/'report.json';report=json.loads(p.read_text())
        need(report['passed']==(name.startswith('audit_v4147')),'Correct bounded observer/failed readiness proof remains unchanged');pins[str(p)]=sha(p)
    screenshot=folders[1]/'snap/mk2ks/0000.png'
    need(screenshot.is_file() and screenshot.resolve().is_relative_to(folders[1].resolve()) and not screenshot.is_symlink(),'Exact unrequested default timeout PNG')
    deleted=dict(path=str(screenshot.resolve()),sha256=sha(screenshot),logicalBytes=screenshot.stat().st_size,allocatedBytes=storage.allocated(screenshot),reason='Unwanted automatic -str snapshot from failed no-command probe; no accepted art or gameplay evidence depended on it',recoverable=False)
    literal=str(screenshot.resolve()).replace("'","''");leaf=str(folders[1].resolve()).replace("'","''")
    command="$ErrorActionPreference='Stop'; $taskLeaf=Get-Item -LiteralPath '"+leaf+"'; $taskFile=Get-Item -LiteralPath '"+literal+"'; if($taskFile.FullName -ne '"+literal+"' -or -not $taskFile.FullName.StartsWith($taskLeaf.FullName+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Exact scoped target required'}; $taskParent=$taskFile; while($taskParent -and $taskParent.FullName.StartsWith($taskLeaf.FullName,[StringComparison]::OrdinalIgnoreCase)){if($taskParent.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'No reparse target'}; $taskParent=if($taskParent.PSIsContainer){$taskParent.Parent}else{$taskParent.Directory}}; Remove-Item -LiteralPath $taskFile.FullName; if(Test-Path -LiteralPath '"+literal+"'){throw 'Target remains'}"
    q=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True)
    need(q.returncode==0 and not screenshot.exists(),'Only exact unrequested screenshot removed')
    files=[]
    for folder in folders:
        need(folder.resolve().is_relative_to(ROOT.resolve()) and not folder.is_symlink(),'Exact bounded terminal leaf')
        need(json.loads((folder/'result.json').read_text())['exit_code']==0,'Native terminal0, no reinterpretation of failed proof')
        for p in folder.iterdir():
            if not p.is_file() or p.suffix not in ('.log','.json'):continue
            p=p.resolve();need(p.is_relative_to(folder.resolve()) and not p.is_symlink(),'Exact evidence file only')
            digest,logical,before=sha(p),p.stat().st_size,storage.allocated(p)
            q=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/I','/Q',str(p)],capture_output=True)
            need(q.returncode==0 and sha(p)==digest and p.stat().st_size==logical,'Every logical evidence byte unchanged')
            after=storage.allocated(p);need(after<=before,'No allocation growth')
            files.append(dict(path=str(p),sha256=digest,logicalBytes=logical,allocatedBefore=before,allocatedAfter=after,reclaimed=before-after));pins[str(p)]=digest
    report=dict(passed=True,files=files,inputHashes=pins,captureChildrenMissing=pids,deletedFiles=1,deletedUnwantedTimeoutScreenshot=deleted,
      reclaimedLogAllocatedBytes=sum(f['reclaimed'] for f in files),reclaimedAllocatedBytes=sum(f['reclaimed'] for f in files)+deleted['allocatedBytes'],
      pendingWholeCampaignProofAccepted=False,failedProbeAcceptance=False,newPlayableCopies=0,fullPortAcceptance=False)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Cleanup report compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('files','inputHashes')},indent=2),flush=True)

if __name__=='__main__':main()
