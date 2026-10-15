"""Reversible exact-file storage probe on frozen accepted friendship evidence.

No media is created, edited or deleted. Logical source/evidence bytes are
hashed before and after, filenames remain, and live capture leaves are excluded.
"""
import json,subprocess
from pathlib import Path
import compact_current_tomb_logs_v3654 as storage
import run_mirror_guard_zoning_campaign_ram_v4187 as current

ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v4205_frozen_friendship_storage_sample'
FOLDER=ROOT/'audit_v2756_native_kano_friendship_palette_p2'

def main():
    need(not OUT.exists(),'Fresh immutable storage proof')
    need(json.loads((FOLDER/'result.json').read_text(encoding='utf-8-sig'))['exit_code']==0,'Exact original native capture terminal0')
    q=subprocess.run(['powershell.exe','-NoProfile','-Command',"Get-CimInstance Win32_Process -Filter \"Name='mkport_candidate.exe' OR Name='mkport.exe' OR Name='mame.exe' OR Name='hbmame.exe'\" | Where-Object { $_.CommandLine -like '*audit_v2756_native_kano_friendship_palette_p2*' } | Select-Object ProcessId,Name | ConvertTo-Json -Compress"],capture_output=True,text=True)
    need(q.returncode==0 and not q.stdout.strip(),'No live process owns this exact frozen evidence leaf')
    pins={str(Path(__file__).resolve()):sha(__file__),str(Path(storage.__file__).resolve()):sha(storage.__file__),str(FOLDER/'result.json'):sha(FOLDER/'result.json')}
    rows=[]
    for name in ('display_base.bin','display_vram_3692.bin','run.log'):
        p=FOLDER/name;need(p.is_file() and p.resolve().is_relative_to(ROOT.resolve()),'Exact present immutable file')
        for ancestor in (p,*p.parents):
            if ancestor.resolve()==ROOT.resolve():break
            need(not ancestor.lstat().st_file_attributes&0x400,'No reparse file or ancestor')
        stat=p.stat();need(stat.st_nlink==1,'No hardlink group or mutable source alias')
        digest,before=sha(p),storage.allocated(p)
        q=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/I','/Q',str(p)],capture_output=True)
        need(q.returncode==0 and sha(p)==digest and p.stat().st_size==stat.st_size,'All logical bytes and size unchanged')
        after=storage.allocated(p);need(after<=before,'No allocated growth')
        rows.append(dict(path=str(p.resolve()),logicalBytes=stat.st_size,sha256=digest,allocatedBefore=before,allocatedAfter=after,reclaimed=before-after));pins[str(p.resolve())]=digest
    report=dict(passed=True,files=rows,inputHashes=pins,reclaimedAllocatedBytes=sum(r['reclaimed'] for r in rows),deletedFiles=0,newMediaFiles=0,
      recovery='All original bytes remain readable at original paths. Native NTFS compact /U /EXE reverses this compression.',fullPortAcceptance=False,scope=__doc__)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writing report')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__':main()
