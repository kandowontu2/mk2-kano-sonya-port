"""Bind the repaired CPU into the successor unit function's own globals.

The preserved first successor repeated the original model failure because
its imported units function still referenced the old CPU class. Compile
that function in the same isolated namespace as the repaired model. No
source or emitted game byte changes; retain both actual failed receipts.
"""
import inspect
import json
from pathlib import Path
import qualify_native_kano_laser_button_gate_shift as prior

ROOT=prior.ROOT
OUT=ROOT/'audit_native_kano_laser_button_gate_bound_source'


def main():
    prior.failed.need(not OUT.exists(),'Fresh isolated successor')
    prior.failed.need('Unsupported actual word 2607 at FF814BB0' in (prior.OUT/'failure.txt').read_text(),
                      'Actual repeated namespace-model failure preserved')
    code=inspect.getsource(prior.main)
    old="exec(compile(cpu,__file__+'::native_shift_model','exec'),scope)"
    prior.failed.need(code.count(old)==1,'Exact isolated CPU namespace boundary')
    code=code.replace(old,old+"\n    exec(compile(inspect.getsource(failed.units),__file__+'::bound_units','exec'),scope)")
    old='inputs=[Path(failed.__file__)'
    prior.failed.need(code.count(old)==1,'Both actual failed-checker provenances')
    code=code.replace(old,"inputs=[Path(prior.__file__),prior.OUT/'failure.txt',prior.OUT/'failed_executed_sources.json.gz',prior.OUT/'compiler.log',prior.OUT/'native_exit.json',Path(failed.__file__)")
    scope=dict(vars(prior),OUT=OUT,prior=prior,__file__=__file__)
    exec(compile(code,__file__+'::isolated_bound_qualification','exec'),scope)
    scope['main']()
    terminal=json.loads((prior.OUT/'native_exit.json').read_text())
    prior.failed.need(terminal['nativeExit']==0,'Actual second failed-check source probe terminal')
    probe=prior.OUT/'initializer_probe.exe'
    if probe.exists():
        prior.failed.need(probe.parent.resolve()==prior.OUT.resolve(),'Only exact terminal temporary probe');probe.unlink()


if __name__=='__main__':main()
