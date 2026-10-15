"""Separate literal victim-name provenance from FIRST_LIVE's victim pointer.

Whole physical gate retained. Correct only its ambiguous parsed-key use;
actual input/source/health/identity/wrap/retirement algorithms unchanged.
"""
import json
import subprocess
import traceback
from pathlib import Path
import qualify_original_mk2_baraka_bound_v5612 as previous

ROOT, need, sha = previous.ROOT, previous.need, previous.sha
FAILURE = previous.OUT / 'progress.json'
OUT = ROOT / 'audit_v5615_original_mk2_baraka_control_provenance_qualified'
source = previous.scope['physical_source']
before = """    need(not records('CACHE_OVERWRITE') and all(r['victim'] == 'cage' and r['side'] == '1'
         and r['killer'] == 'baraka' and r['writes'] == '0' and r['assistance'] == 'none'
         for tag in ('RESULT', 'ACTION', 'FIRST_LIVE', 'WRAP', 'HEALTH', 'INPUT') for r in records(tag)),
         'All original-reference records honest identity and passive provenance, no cache overrun')"""
after = """    prefixes=tuple('MK2_STOCK_HEAD_V921_'+tag+' ' for tag in ('RESULT','ACTION','FIRST_LIVE','WRAP','STATE','HEALTH','INPUT'))
    need(not records('CACHE_OVERWRITE') and all(re.match(
         r'^MK2_STOCK_HEAD_V921_(?:RESULT|ACTION|FIRST_LIVE|WRAP|STATE|HEALTH|INPUT) frame=\\d+ victim=cage side=1 killer=baraka writes=0 assistance=none(?: |$)',line)
         for line in log.splitlines() if line.startswith(prefixes)),
         'Every literal stock provenance header honest, separate from actor-pointer fields; no cache overrun')"""
need(source.count(before)==1, 'Only duplicate victim-name/pointer parser ambiguity corrected in whole physical gate')
source=source.replace(before,after,1)
scope=dict(previous.scope['scope'])
exec(compile(source,__file__+'.entire_original_native_physical_gate_literal_provenance_and_actor_pointer_distinct','exec'),scope)
previous.scope['physical']=scope['physical']

if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable full stock-control/source qualifier')
    failure=json.loads(FAILURE.read_text())
    need(not failure['passed'] and failure['error']=="ValueError('All original-reference records honest identity and passive provenance, no cache overrun')",
         'Actual duplicate parsed-key provenance failure retained')
    pins={str(p):sha(p) for p in (Path(__file__),Path(previous.__file__),FAILURE,previous.FAILURE)}
    try:
        report=previous.scope['run']()
    except Exception as error:
        report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
    need(all(sha(p)==h for p,h in pins.items()),'Original source/failures unchanged during qualification')
    report.update(preservedVerifierNamespaceFailure=str(previous.FAILURE),preservedParsedKeyAmbiguityFailure=str(FAILURE))
    report.setdefault('newInputHashes',{}).update(pins)
    OUT.mkdir()
    previous.original.original.save(OUT/'progress.json',report)
    paths=[OUT/'progress.json',Path(__file__)]
    frozen={str(p):sha(p) for p in paths}
    done=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',*[str(p) for p in paths]],capture_output=True)
    need(done.returncode==0 and all(sha(p)==h for p,h in frozen.items()),'New source/evidence losslessly compressed')
    print(json.dumps({k:report[k] for k in ('passed','error','originalNativeTerminal','originalPCMCallbacksObserved',
        'sourceQualifiedOriginalMixedWaveformAccepted') if k in report},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
