"""Lossless sealed diagnostic-log compression; no deletion or game/build changes."""
import ctypes
import json
import subprocess
from pathlib import Path

import run_current_tomb_ram_matrix_v3648 as current

ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v3655_current_tomb_log_compression'


def allocated(path):
    api=ctypes.windll.kernel32.GetCompressedFileSizeW
    api.argtypes=[ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_ulong)];api.restype=ctypes.c_ulong
    high=ctypes.c_ulong();low=api(str(path.resolve()),ctypes.byref(high))
    need(low!=0xffffffff,'Actual exact diagnostic-file allocated size')
    return (high.value<<32)|low


def main():
    need(not OUT.exists(),'Fresh lossless compression audit')
    matrix_path=current.OUT/'report.json';matrix=json.loads(matrix_path.read_text())
    need(matrix['passed'],'All current diagnostic child runs terminal and checked before compression')
    targets=[]
    for fighter,side in current.CASES:
        folder,output=current.case_paths(fighter,side)
        report=json.loads((output/'report.json').read_text())
        terminal=json.loads((folder/'result.json').read_text())
        need(report['passed']and terminal['captureCompleted']and terminal['exit_code']==0,
             'Only completed sealed diagnostic log targets')
        file=folder/'run.log';targets.append((file,report['inputHashes'][str(file)]))
    prior=ROOT/'audit_v3635_current_native_tomb_ram_checked/report.json'
    old=json.loads(prior.read_text());file=ROOT/'audit_v3634_current_kano_tomb_p1_native_ram/run.log'
    need(old['passed'],'Prior accepted current Tomb capture remains sealed')
    targets.append((file,old['inputHashes'][str(file)]))
    records=[]
    for file,wanted in targets:
        file=file.resolve();need(file.is_relative_to(ROOT.resolve())and file.name=='run.log'and
                                sha(file)==wanted,'Exact in-workspace existing diagnostic log target')
        before=allocated(file);logical=file.stat().st_size
        result=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/I','/Q',str(file)],capture_output=True,text=True)
        need(result.returncode==0 and sha(file)==wanted and file.stat().st_size==logical,
             'Lossless compression preserves every logical byte/hash/size')
        after=allocated(file)
        need(after<=before,'No diagnostic allocated-size increase')
        records.append(dict(path=str(file),sha256=wanted,logicalBytes=logical,
                            allocatedBytesBefore=before,allocatedBytesAfter=after,
                            reclaimedAllocatedBytes=before-after,compactExitCode=result.returncode))
    pins={str(file):wanted for file,wanted in targets}
    for file in (matrix_path,prior,Path(__file__).resolve()):pins[str(file)]=sha(file)
    value=dict(passed=True,files=records,logicalDiagnosticBytes=sum(r['logicalBytes']for r in records),
               allocatedBytesBefore=sum(r['allocatedBytesBefore']for r in records),
               allocatedBytesAfter=sum(r['allocatedBytesAfter']for r in records),
               reclaimedAllocatedBytes=sum(r['reclaimedAllocatedBytes']for r in records),
               logicalHashesAndSizesUnchanged=True,deletedFiles=0,newBuildPixelVRAMAudioCopies=0,
               publicPlayableReleaseUnchanged=True,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)
    OUT.mkdir();file=OUT/'report.json';file.write_text(json.dumps(value,indent=2)+'\n')
    before=sha(file);result=subprocess.run(['compact.exe','/C','/I','/Q',str(file)],capture_output=True,text=True)
    need(result.returncode==0 and sha(file)==before,'Lossless compact storage audit')
    print(json.dumps({k:v for k,v in value.items()if k not in('files','inputHashes')},indent=2))


if __name__=='__main__':main()
