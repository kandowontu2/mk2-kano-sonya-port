"""Preserve5610's missing generated-function struct binding; fix namespace only."""
import json
import subprocess
import traceback
from pathlib import Path
import qualify_original_mk2_baraka_control_v5610 as original

ROOT, need, sha = original.ROOT, original.need, original.sha
FAILURE = original.OUT / 'progress.json'
OUT = ROOT / 'audit_v5613_original_mk2_baraka_bound_control_qualified'
source = Path(original.__file__).read_text()
edits = {
    'scope = dict(original.__dict__)': 'scope = dict(original.__dict__, struct=struct)',
    "OUT = ROOT / 'audit_v5611_original_mk2_baraka_control_qualified'":
        "OUT = ROOT / 'audit_v5613_original_mk2_baraka_bound_control_qualified'",
}
for before, after in edits.items():
    need(source.count(before)==1, 'Only fresh output and defining generated-function struct binding corrected')
    source=source.replace(before,after,1)
scope=dict(__name__='whole_stock_control5612_bound', __file__=__file__)
exec(compile(source,__file__+'.entire5610_physical_and_packet_qualification_struct_binding_only','exec'),scope)

if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable corrected control qualifier')
    failure=json.loads(FAILURE.read_text())
    need(not failure['passed'] and failure['error']=='''NameError("name 'struct' is not defined")''',
         'Actual prior verifier namespace failure retained')
    try:
        report=scope['run']()
    except Exception as error:
        report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
    report['preservedVerifierNamespaceFailure']=str(FAILURE)
    report.setdefault('newInputHashes',{}).update({str(FAILURE):sha(FAILURE),str(Path(original.__file__)):sha(original.__file__)})
    OUT.mkdir()
    original.original.save(OUT/'progress.json',report)
    paths=[OUT/'progress.json',Path(__file__)]
    frozen={str(p):sha(p) for p in paths}
    done=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',*[str(p) for p in paths]],capture_output=True)
    need(done.returncode==0 and all(sha(p)==h for p,h in frozen.items()),'New source/evidence compressed with all bytes preserved')
    print(json.dumps({k:report[k] for k in ('passed','error','originalNativeTerminal','originalPCMCallbacksObserved',
        'sourceQualifiedOriginalMixedWaveformAccepted') if k in report},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
