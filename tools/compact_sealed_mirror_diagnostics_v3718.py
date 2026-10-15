"""Losslessly seal completed mirror diagnostics; never touch active captures.

No deletion, rebuild or raw audio. Preserve every failed/positive evidence
byte while reclaiming allocated NTFS space from repetitive diagnostic logs.
"""
import json,subprocess
from pathlib import Path
import compact_current_tomb_logs_v3654 as storage
import run_natural_mirror_audio_ram_v3700 as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v3719_sealed_mirror_diagnostic_compression'
LEAVES=(
 'audit_v3701_kano_mirror_audio_p1_samples','audit_v3701_kano_mirror_audio_p1_nosamples',
 'audit_v3701_kano_mirror_audio_p2_samples','audit_v3701_kano_mirror_audio_p2_nosamples',
 'audit_v3706_kano_mirror_audio_p2_samples','audit_v3706_kano_mirror_audio_p2_nosamples',
 'audit_v3710_kano_mirror_audio_p1_samples','audit_v3710_kano_mirror_audio_p1_nosamples',
)

def main():
    need(not OUT.exists(),'Fresh lossless storage audit')
    records=[];pins={str(Path(__file__).resolve()):sha(__file__)}
    for leaf in LEAVES:
        folder=(ROOT/leaf).resolve();meta=folder/'result.json';terminal=json.loads(meta.read_text())
        need(folder.is_relative_to(ROOT.resolve())and terminal['exit_code']==0 and terminal['rawAudioFilesWritten']==0,'Exact sealed terminal capture only')
        pins[str(meta)]=sha(meta)
        for name in('run.log','error.log','stderr.log'):
            file=folder/name
            if not file.exists():continue
            digest=sha(file);logical=file.stat().st_size;before=storage.allocated(file)
            result=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/I','/Q',str(file)],capture_output=True,text=True)
            need(result.returncode==0 and sha(file)==digest and file.stat().st_size==logical,'Every logical evidence byte/size preserved')
            after=storage.allocated(file);need(after<=before,'No allocated diagnostic size increase')
            records.append(dict(path=str(file),sha256=digest,logicalBytes=logical,allocatedBytesBefore=before,allocatedBytesAfter=after,reclaimedAllocatedBytes=before-after))
            pins[str(file)]=digest
    report=dict(passed=True,files=records,inputHashes=pins,deletedFiles=0,newBuilds=0,rawAudioFiles=0,
      logicalDiagnosticBytes=sum(r['logicalBytes']for r in records),
      allocatedBytesBefore=sum(r['allocatedBytesBefore']for r in records),allocatedBytesAfter=sum(r['allocatedBytesAfter']for r in records),
      reclaimedAllocatedBytes=sum(r['reclaimedAllocatedBytes']for r in records),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('files','inputHashes')},indent=2),flush=True)

if __name__=='__main__':main()
