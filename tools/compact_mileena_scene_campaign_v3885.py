"""Lossless compression of sealed3836 campaign/scene evidence, no deletions."""
import json,subprocess
from pathlib import Path
import compact_current_tomb_logs_v3654 as storage
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v3886_mileena_scene_campaign_compression'

def main():
    need(not OUT.exists(),'Fresh storage report')
    campaign=ROOT/'audit_v3871_mileena_fixed_sonya_campaign_checked/report.json'
    scene=ROOT/'audit_v3884_mileena_native_scene_fifo_checked/report.json'
    need(json.loads(campaign.read_text())['passed']and json.loads(scene.read_text())['passed'],'Actual sealed full campaign-state and four scene-context qualification')
    folders=[ROOT/'audit_v3851_mileena_fixed_sonya_p2_campaign',ROOT/'audit_v3867_mileena_kano_p1_native_scene_ram']
    folders.extend(ROOT/f'audit_v3878_mileena_{fighter}_p{side}_native_scene_ram'for fighter,side in(('kano',2),('sonya',1),('sonya',2)))
    pids=[json.loads((p/'process.json').read_text())['pid']for p in folders]
    check=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @('+','.join(map(str,pids))+') } | Select-Object -ExpandProperty ProcessId'],capture_output=True,text=True)
    need(check.returncode==0 and not check.stdout.strip(),'Every exact recorded capture handle missing now; unrelated builds left untouched')
    targets=[]
    for folder in folders:
        need(json.loads((folder/'result.json').read_text())['exit_code']==0,'Every actual capture terminal0')
        targets.extend(p for p in folder.iterdir()if p.is_file()and p.suffix in('.log','.json'))
    records=[];pins={str(Path(__file__).resolve()):sha(__file__),str(campaign):sha(campaign),str(scene):sha(scene)}
    for file in targets:
        file=file.resolve();need(file.is_relative_to(ROOT.resolve())and not file.is_symlink(),'Exact safe evidence leaf')
        before=storage.allocated(file);digest=sha(file);logical=file.stat().st_size
        result=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/I','/Q',str(file)],capture_output=True,text=True)
        need(result.returncode==0 and sha(file)==digest and file.stat().st_size==logical,'Every logical evidence byte and hash unchanged')
        after=storage.allocated(file);need(after<=before,'No allocated-byte increase')
        records.append(dict(path=str(file),sha256=digest,logicalBytes=logical,allocatedBefore=before,allocatedAfter=after,reclaimed=before-after));pins[str(file)]=digest
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Report compressed before write')
    value=dict(passed=True,files=records,inputHashes=pins,captureChildrenMissing=pids,deletedFiles=0,newPlayableCopies=0,
        reclaimedAllocatedBytes=sum(r['reclaimed']for r in records),allocatedBytesAfter=sum(r['allocatedAfter']for r in records),fullPortAcceptance=False)
    (OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n');print(json.dumps({k:v for k,v in value.items()if k not in('files','inputHashes')}))

if __name__=='__main__':main()
