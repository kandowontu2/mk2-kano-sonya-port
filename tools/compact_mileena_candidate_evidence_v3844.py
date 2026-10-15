"""Lossless compression of the two new candidates and stopped small logs."""
import json,subprocess
from pathlib import Path
import compact_current_tomb_logs_v3654 as storage
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v3845_mileena_candidate_compression'
def main():
    need(not OUT.exists(),'Fresh resource audit');files=[];pids=[]
    for build in ('diagnostic_v3822_native_mileena_victims','diagnostic_v3836_native_mileena_rom_identity'):
        need(json.loads((ROOT/build/'restoration.json').read_text(encoding='utf-8-sig'))['passed'],'Restored and stopped build')
        files.append(ROOT/build/'mkport_candidate.exe')
    for name in ('kano','sonya'):
        for side in (1,2):
            for prefix,suffix in (('audit_v3827','fixed'),('audit_v3838','rom_identity')):
                folder=ROOT/f'{prefix}_mileena_{name}_p{side}_{suffix}'
                need(json.loads((folder/'result.json').read_text())['terminalExitCode']==0,'Terminal actual capture')
                pids.append(json.loads((folder/'process.json').read_text())['pid']);files.extend(folder/n for n in ('run.log','stderr.log'))
    check=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @('+','.join(map(str,pids))+') } | Select-Object -ExpandProperty ProcessId'],capture_output=True,text=True)
    need(check.returncode==0 and not check.stdout.strip(),'Every recorded capture process missing now')
    records=[];pins={str(Path(__file__).resolve()):sha(__file__)}
    for file in files:
        file=file.resolve();need(file.is_relative_to(ROOT.resolve())and not file.is_symlink(),'Exact safe artifact leaf')
        before=storage.allocated(file);digest=sha(file);logical=file.stat().st_size
        result=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/I','/Q',str(file)],capture_output=True,text=True)
        need(result.returncode==0 and sha(file)==digest and file.stat().st_size==logical,'Every logical byte preserved')
        after=storage.allocated(file);need(after<=before,'No allocated-size increase')
        records.append(dict(path=str(file),sha256=digest,logicalBytes=logical,allocatedBefore=before,allocatedAfter=after,reclaimed=before-after));pins[str(file)]=digest
    OUT.mkdir();value=dict(passed=True,files=records,inputHashes=pins,captureChildrenMissing=pids,newCandidatesRetained=2,deletedFiles=0,reclaimedAllocatedBytes=sum(r['reclaimed']for r in records),allocatedBytesAfter=sum(r['allocatedAfter']for r in records),fullPortAcceptance=False)
    (OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n');print(json.dumps({k:v for k,v in value.items()if k not in ('files','inputHashes')}))
if __name__=='__main__':main()
