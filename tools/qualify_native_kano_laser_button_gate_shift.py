"""Preserve the first checker failure; support actual native SLL immediate.

Source compiled and exact whole-byte contract passed. The unit model missed
SLL16's opcode range2600. Correct only that model boundary and model signed
LT from real subtraction N/V flags rather than unsigned carry equivalence.
"""
import inspect
import json
from pathlib import Path
import qualify_native_kano_laser_button_gate as failed

ROOT=failed.ROOT
OUT=ROOT/'audit_native_kano_laser_button_gate_shift_source'


def main():
    failed.need(not OUT.exists(),'Fresh successor; failed executed checker immutable')
    failed.need('Unsupported actual word 2607 at FF814BB0' in (failed.OUT/'failure.txt').read_text(),
                'Actual native ring-writer opcode failure preserved')
    cpu=inspect.getsource(failed.CPU)
    replacements=[
        ('op&0xfe10==0x2400','op&0xfc10==0x2400'),
        ('self.z=False;self.c=False;self.pc=0','self.z=False;self.c=False;self.n=False;self.v=False;self.pc=0'),
        ('def cmp(self,left,right):self.z=(left&0xffffffff)==(right&0xffffffff);self.c=(left&0xffffffff)<(right&0xffffffff)',
         'def cmp(self,left,right):\n        left&=0xffffffff;right&=0xffffffff;result=(left-right)&0xffffffff\n        self.z=result==0;self.c=left<right;self.n=bool(result&0x80000000)\n        self.v=bool((left^right)&(left^result)&0x80000000)'),
        ('4:self.c,8:self.c','4:self.n!=self.v,8:self.c')]
    for old,new in replacements:
        failed.need(cpu.count(old)==1,'Exact native-word model repair only');cpu=cpu.replace(old,new)
    inputs=[Path(failed.__file__),failed.OUT/'failure.txt',failed.OUT/'failed_executed_sources.json.gz',
            failed.OUT/'compiler.log',failed.OUT/'native_exit.json']
    code=inspect.getsource(failed.main)
    old='paths=[Path(__file__),accepted.OUT/'
    failed.need(code.count(old)==1,'Exact provenance extension')
    code=code.replace(old,'paths=[Path(__file__),*failure_inputs,accepted.OUT/')
    code=code.replace('report=dict(passed=True,sourceOnlyAccepted=True,',
        'report=dict(passed=True,actualNativeSLL16Supported=True,signedLTFlagsModeled=True,preservedFirstCheckerFailure=True,sourceOnlyAccepted=True,')
    scope=dict(vars(failed),OUT=OUT,__file__=__file__,failure_inputs=inputs)
    exec(compile(cpu,__file__+'::native_shift_model','exec'),scope)
    exec(compile(code,__file__+'::isolated_source_qualification','exec'),scope)
    scope['main']()
    terminal=json.loads((failed.OUT/'native_exit.json').read_text())
    failed.need(terminal['nativeExit']==0,'Actual failed-check initializer probe terminal')
    probe=failed.OUT/'initializer_probe.exe'
    if probe.exists():
        failed.need(probe.parent.resolve()==failed.OUT.resolve(),'Only exact terminal temporary probe');probe.unlink()


if __name__=='__main__':main()
