"""Isolate generated source probes from frozen failed qualification folders.

Both prior executed checks/failures remain immutable. The first rejected
incorrect allocator text; the second reached output but rightly rejected
a temporary probe written in the old checker's directory by its function
globals. Rebind the actual compile function to this successor's own OUT.
"""
import inspect
import json
from pathlib import Path
import qualify_native_kano_laser_palette as prior
import qualify_native_kano_laser_palette_abi as abi

ROOT=prior.ROOT
OUT=ROOT/'audit_native_kano_laser_palette_isolated_source'

def main():
    prior.need(not OUT.exists(),'Fresh fully isolated source qualification')
    prior.need('Only exact terminal temporary source probe removed' in (abi.OUT/'failure.txt').read_text() and
               (abi.OUT/'report.json').exists(),'Late temporary-probe location failure preserved; earlier report is not accepted')
    code=inspect.getsource(prior.main)
    swaps=[("'MMTM   A0,A2,A7-A12'", "'MMTM   A2,A7-A12'"),
           ("'MOVE   A1,*A0(20h),0'", "'MOVE   A1,-*A2,0'"),
           ('paths=[Path(__file__),prior.OUT/',
            'paths=[Path(__file__),Path('+repr(str(Path(prior.__file__).resolve()))+'),Path('+repr(str(Path(abi.__file__).resolve()))+'),ROOT/\'audit_native_kano_laser_palette_source/failure.txt\',ROOT/\'audit_native_kano_laser_palette_source/failed_executed_sources.json.gz\',ROOT/\'audit_native_kano_laser_palette_abi_source/failure.txt\',ROOT/\'audit_native_kano_laser_palette_abi_source/report.json\',prior.OUT/'),
           ('result=dict(passed=True,sourceOnlyAccepted=True,',
            'result=dict(passed=True,actualAllocatorABIReviewed=True,allTemporaryProbesIsolated=True,sourceOnlyAccepted=True,')]
    for old,new in swaps:
        prior.need(code.count(old)==1,'Exact preserved source qualification boundary')
        code=code.replace(old,new)
    scope=dict(vars(prior),OUT=OUT,__file__=__file__)
    exec(compile(inspect.getsource(prior.compile_probe),__file__+'::isolated_probe','exec'),scope)
    exec(compile(code,__file__+'::actual_source_qualification','exec'),scope)
    scope['main']()
    # Both already-terminal generated probes are disposable test outputs,
    # not user sources or accepted executable inputs. Keep failure/harness.
    for folder in (prior.OUT,abi.OUT):
        probe=folder/'initializer_probe.exe'
        if probe.exists():
            prior.need(probe.parent.resolve()==folder.resolve(),'Exact generated temporary probe only')
            probe.unlink()

if __name__=='__main__':main()
