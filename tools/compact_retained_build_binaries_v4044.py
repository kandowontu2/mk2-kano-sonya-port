"""Losslessly compress exact retained historical EXEs, never delete evidence.

Preserve every logical byte, digest, build provenance and launch path. Skip
any executable actually loaded now. Do not touch3836, installed mkport.exe,
dirty source checkout, release ZIPs, recovery archives or unrelated projects.
"""
import json,subprocess
from pathlib import Path
import compact_current_tomb_logs_v3654 as storage
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v4045_retained_build_binary_compression'
NAMES=('diagnostic_v3822_native_mileena_victims','diagnostic_v3172_native_morph_shadow','diagnostic_v2753_native_friendship_palette','diagnostic_v3680_native_sound_packet_guard','diagnostic_v1836_ball_register_boundary','diagnostic_v1597_native_ground_throw','diagnostic_v1110_owned_native_split','diagnostic_v1130_owned_split_invariant_blood','diagnostic_v1250_native_correct_rom_metadata')

def active():
    q=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process | Select-Object ProcessId,ExecutablePath | ConvertTo-Json -Compress'],capture_output=True,text=True)
    need(q.returncode==0 and q.stdout.strip(),'Actual process inventory before bounded executable compression')
    rows=json.loads(q.stdout);rows=[rows]if isinstance(rows,dict)else rows
    return {str(Path(r['ExecutablePath']).resolve()).lower():r['ProcessId']for r in rows if r.get('ExecutablePath')}

def main():
    need(not OUT.exists(),'Fresh immutable binary-storage report')
    pins={str(Path(__file__).resolve()):sha(__file__)};records=[];skipped=[]
    for name in NAMES:
        folder=(ROOT/name).resolve();path=(folder/'mkport_candidate.exe').resolve();build_path=folder/'build-info.json'
        need(folder.parent==ROOT.resolve()and path.parent==folder and path.is_file()and not folder.is_symlink()and not path.is_symlink(),'Exact inspected bounded retained executable')
        live=active()
        if str(path).lower()in live:
            skipped.append(dict(path=str(path),actualLivePID=live[str(path).lower()]));continue
        build=json.loads(build_path.read_text(encoding='utf-8-sig'));digest=sha(path)
        need(digest==build['executable_sha256'],'Actual retained build provenance before compression')
        pins[str(build_path)]=sha(build_path);logical=path.stat().st_size;before=storage.allocated(path)
        q=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/I','/Q',str(path)],capture_output=True,text=True)
        need(q.returncode==0 and sha(path)==digest and path.stat().st_size==logical,'Executable compression preserves every logical byte/hash/size and path')
        after=storage.allocated(path);need(after<=before,'No allocation growth')
        pins[str(path)]=digest;records.append(dict(path=str(path),sha256=digest,logicalBytes=logical,allocatedBefore=before,allocatedAfter=after,reclaimed=before-after))
        print(name+' reclaimed='+str(before-after)+' logical_bytes_unchanged=true',flush=True)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Report compressed before writes')
    r=dict(passed=True,files=records,skippedActuallyLoadedEXEs=skipped,inputHashes=pins,reclaimedAllocatedBytes=sum(f['reclaimed']for f in records),allocatedBytesAfter=sum(f['allocatedAfter']for f in records),deletedFiles=0,newBuildCopies=0,allLogicalExecutableBytesAndLaunchPathsUnchanged=True,fullPortAcceptance=False,scope=__doc__)
    (OUT/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items()if k not in('files','inputHashes')},indent=2),flush=True)

if __name__=='__main__':main()
