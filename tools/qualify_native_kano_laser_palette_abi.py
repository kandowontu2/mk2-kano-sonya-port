"""Successor ABI check using actual native allocator operand/registers.

Preserve executed failed checker, failure and its complete initializer.
The game source does not change: FF80E280 stores A7..A12 through A2 and
saves type A1 by predecrement after the sleep word, not direct *A0(20).
"""
import inspect
import json
from pathlib import Path
import qualify_native_kano_laser_palette as prior

ROOT=prior.ROOT
OUT=ROOT/'audit_native_kano_laser_palette_abi_source'

def main():
    prior.need(not OUT.exists(),'Fresh immutable ABI qualification successor')
    failure=(prior.OUT/'failure.txt').read_text()
    prior.need('Actual native task context, word-cadence, queue record and MKII hardware palette contract' in failure and
               json.loads((prior.OUT/'native_exit.json').read_text())['nativeExit']==0,
               'Original successful initializer run and exact source-check failure preserved')
    code=inspect.getsource(prior.main)
    swaps=[("'MMTM   A0,A2,A7-A12'", "'MMTM   A2,A7-A12'"),
           ("'MOVE   A1,*A0(20h),0'", "'MOVE   A1,-*A2,0'"),
           ('paths=[Path(__file__),prior.OUT/',
            'paths=[Path(__file__),Path('+repr(str(Path(prior.__file__).resolve()))+'),ROOT/\'audit_native_kano_laser_palette_source/failure.txt\',ROOT/\'audit_native_kano_laser_palette_source/failed_executed_sources.json.gz\',prior.OUT/'),
           ('result=dict(passed=True,sourceOnlyAccepted=True,',
            "result=dict(passed=True,preservedOriginalCheckerFailure=True,actualAllocatorABIReviewed=True,sourceOnlyAccepted=True,")]
    for old,new in swaps:
        prior.need(code.count(old)==1,'Exact single ABI/provenance check boundary')
        code=code.replace(old,new)
    scope=dict(vars(prior),OUT=OUT,__file__=__file__)
    exec(compile(code,__file__+'::actual_allocator_abi','exec'),scope)
    scope['main']()
    probe=prior.OUT/'initializer_probe.exe'
    if probe.exists():
        prior.need(probe.parent.resolve()==prior.OUT.resolve(),'Exact terminal generated failed-check probe only')
        probe.unlink()

if __name__=='__main__':main()
