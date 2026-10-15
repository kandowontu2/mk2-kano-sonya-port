"""Losslessly seal stopped cache-defect evidence; not successful gameplay."""
import json,subprocess
from pathlib import Path
import compact_current_tomb_logs_v3654 as storage
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v3796_mileena_cache_log_compression'
LEAVES=('audit_v3768_guarded_sonya_extended_p2_campaign','audit_v3778_campaign_cache_provenance',
 'audit_v3788_mileena_kano_p1_earned_cache','audit_v3788_mileena_kano_p2_earned_cache',
 'audit_v3788_mileena_sonya_p1_earned_cache','audit_v3786_mileena_earned_cache')

def main():
    need(not OUT.exists(),'Immutable storage audit')
    pins={str(Path(__file__).resolve()):sha(__file__)};records=[]
    path=ROOT/'audit_v3794_mileena_cache_cause_checked/report.json';gate=json.loads(path.read_text())
    need(gate['passed']and len(gate['cases'])==4 and not gate['stabilityFixAccepted'],'Actual defect proof, never successful gameplay')
    accepted=gate;pins[str(path)]=sha(path)
    for leaf in LEAVES:
        folder=(ROOT/leaf).resolve();meta=folder/'result.json';terminal=json.loads(meta.read_text())
        need(folder.is_relative_to(ROOT.resolve())and terminal.get('exit_code',terminal.get('terminalExitCode'))==0 and terminal['candidate']==current.NAME,
          'Only exact sealed terminal0 capture logs')
        pins[str(meta)]=sha(meta)
        for name in('run.log','stderr.log'):
            file=folder/name;digest=sha(file);logical=file.stat().st_size;before=storage.allocated(file)
            if name=='run.log':need(accepted['inputHashes'][str(file)]==digest,'Exact cause-qualified evidence before compression')
            result=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/I','/Q',str(file)],capture_output=True,text=True)
            need(result.returncode==0 and sha(file)==digest and file.stat().st_size==logical,'Every logical source/evidence byte preserved')
            after=storage.allocated(file);need(after<=before,'No allocated size increase')
            records.append(dict(path=str(file),sha256=digest,logicalBytes=logical,allocatedBytesBefore=before,
              allocatedBytesAfter=after,reclaimedAllocatedBytes=before-after));pins[str(file)]=digest
    report=dict(passed=True,files=records,inputHashes=pins,deletedFiles=0,newBuilds=0,rawAudioFiles=0,
      logicalDiagnosticBytes=sum(r['logicalBytes']for r in records),allocatedBytesBefore=sum(r['allocatedBytesBefore']for r in records),
      allocatedBytesAfter=sum(r['allocatedBytesAfter']for r in records),reclaimedAllocatedBytes=sum(r['reclaimedAllocatedBytes']for r in records),
      actualGameCorruptionEvidencePreserved=True,failedObserverEvidencePreserved=True,fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('files','inputHashes')},indent=2),flush=True)

if __name__=='__main__':main()
