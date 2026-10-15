"""Lossless seal of three exact terminal captures, including retained failures.

No deletion and no gameplay acceptance. Never touch the live3971 matrix.
One pre-existing campaign guest dump is retained/compressed, not relabelled RAM.
"""
import json,subprocess
from pathlib import Path
import compact_current_tomb_logs_v3654 as storage
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v3979_terminal_split_campaign_compression'

def main():
    need(not OUT.exists(),'Fresh immutable compression evidence')
    pins={str(Path(__file__).resolve()):sha(__file__)}
    reports={}
    for leaf,passed in (('audit_v3951_sonya_close_leg_campaign_checked',True),('audit_v3962_kung_lao_split_native_scene_observed',False),('audit_v3968_kung_lao_split_native_scene_observed',False)):
        p=ROOT/leaf/'report.json';r=json.loads(p.read_text());need(r['passed']is passed and r.get('fullPortAcceptance')is False,'Exact honest terminal success/failure classification');reports[leaf]=r;pins[str(p)]=sha(p)
    campaign=reports['audit_v3951_sonya_close_leg_campaign_checked']['cases'][0]
    need(campaign['native_own_round_wins']==0 and campaign['paid_continue_losses']==144 and not campaign['unassisted_clear_proven'],'Loss result never accepted as clear')
    folders=[ROOT/'audit_v3948_sonya_close_leg_p2_campaign',ROOT/'audit_v3961_kung_lao_kano_p1_native_scene_ram',ROOT/'audit_v3967_kung_lao_kitana_p1_native_scene_ram']
    pids=[json.loads((p/'process.json').read_text())['pid']for p in folders]
    check=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @('+','.join(map(str,pids))+') } | Select-Object -ExpandProperty ProcessId'],capture_output=True,text=True)
    need(check.returncode==0 and not check.stdout.strip(),'All exact emulator processes missing now')
    records=[]
    for folder in folders:
        need(folder.resolve().is_relative_to(ROOT.resolve())and not folder.is_symlink(),'Exact safe evidence leaf')
        meta=json.loads((folder/'result.json').read_text());need(meta['exit_code']==0,'Emulator terminal0; semantic failures retained separately')
        for p in folder.iterdir():
            if not p.is_file()or p.suffix not in('.log','.json','.bin'):continue
            p=p.resolve();need(p.is_relative_to(folder.resolve())and not p.is_symlink(),'Exact existing log, metadata or diagnostic guest dump')
            digest=sha(p);logical=p.stat().st_size;before=storage.allocated(p)
            done=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/I','/Q',str(p)],capture_output=True,text=True)
            need(done.returncode==0 and sha(p)==digest and p.stat().st_size==logical,'Every byte/digest/size unchanged')
            after=storage.allocated(p);need(after<=before,'Allocated bytes do not grow')
            records.append(dict(path=str(p),sha256=digest,logicalBytes=logical,allocatedBefore=before,allocatedAfter=after,reclaimed=before-after));pins[str(p)]=digest
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed report before writes')
    r=dict(passed=True,captureFolders=3,files=records,inputHashes=pins,captureChildrenMissing=pids,deletedFiles=0,newPlayableCopies=0,reclaimedAllocatedBytes=sum(r['reclaimed']for r in records),allocatedBytesAfter=sum(r['allocatedAfter']for r in records),retainedSemanticFailureReports=2,retainedNativeCampaignGuestDumpFiles=1,excludedLiveMatrix='audit_v3971_*',gameplayAcceptance=False,fullPortAcceptance=False)
    (OUT/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items()if k not in('files','inputHashes')}),flush=True)

if __name__=='__main__':main()
