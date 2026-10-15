"""Seal only terminal, state-qualified P2 campaign logs; preserve every byte."""
import json,subprocess
from pathlib import Path
import compact_current_tomb_logs_v3654 as storage
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v3760_guarded_p2_campaign_log_compression'
CASES=(('audit_v3745_guarded_kano_natural_p2_campaign','audit_v3748_guarded_p2_campaign_state_checked/report.json'),
       ('audit_v3745_guarded_sonya_natural_p2_campaign','audit_v3765_guarded_sonya_p2_capture_accounting_checked/report.json'))

def main():
    need(not OUT.exists(),'Immutable storage audit')
    pins={str(Path(__file__).resolve()):sha(__file__)};records=[]
    for leaf,proof in CASES:
        path=ROOT/proof;gate=json.loads(path.read_text())
        need(gate['passed']and len(gate['cases'])==1 and gate['cases'][0]['bounded_campaign_evidence_proven'],
          'Native state qualified; no false automatic-raster or full-clear acceptance')
        accepted=gate['cases'][0];pins[str(path)]=sha(path)
        folder=(ROOT/leaf).resolve();meta=folder/'result.json';terminal=json.loads(meta.read_text())
        need(folder.is_relative_to(ROOT.resolve())and terminal['exit_code']==0 and terminal['candidate']==current.NAME,
          'Only exact sealed terminal0 capture logs')
        pins[str(meta)]=sha(meta)
        for name in('run.log','stderr.log'):
            file=folder/name;digest=sha(file);logical=file.stat().st_size;before=storage.allocated(file)
            need(accepted['inputHashes'][str(file)]==digest,'Exact state-qualified evidence before compression')
            result=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/I','/Q',str(file)],capture_output=True,text=True)
            need(result.returncode==0 and sha(file)==digest and file.stat().st_size==logical,'Every logical source/evidence byte preserved')
            after=storage.allocated(file);need(after<=before,'No allocated size increase')
            records.append(dict(path=str(file),sha256=digest,logicalBytes=logical,allocatedBytesBefore=before,
              allocatedBytesAfter=after,reclaimedAllocatedBytes=before-after));pins[str(file)]=digest
    report=dict(passed=True,files=records,inputHashes=pins,deletedFiles=0,newBuilds=0,rawAudioFiles=0,
      logicalDiagnosticBytes=sum(r['logicalBytes']for r in records),allocatedBytesBefore=sum(r['allocatedBytesBefore']for r in records),
      allocatedBytesAfter=sum(r['allocatedBytesAfter']for r in records),reclaimedAllocatedBytes=sum(r['reclaimedAllocatedBytes']for r in records),
      automaticTimeoutRasterFailurePreserved=True,fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('files','inputHashes')},indent=2),flush=True)

if __name__=='__main__':main()
