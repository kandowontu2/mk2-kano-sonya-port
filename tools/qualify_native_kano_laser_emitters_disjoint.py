"""Keep actual source unchanged; repair disjoint synthetic unit pools.

The32taskfixture's mock pool20000..3F000 collided with mock victim30000,
not real native memory. Preserve failures; use90000..AF000 with explicit
nonoverlap and stronger victim conservation, keeping all opcode checks.
"""
import inspect
import json
from pathlib import Path

import qualify_native_kano_laser_emitters as prior
import qualify_native_kano_laser_emitters_class as class_check
import qualify_native_kano_laser_emitters_stack as stack_check

ROOT=prior.ROOT
OUT=ROOT/'audit_native_kano_laser_emitters_disjoint_source'


def main():
    prior.need(not OUT.exists(),'Fresh isolated successor; frozen actual source/failures')
    prior.need('Every real emitted bone task' in (stack_check.OUT/'failure.txt').read_text(),
               'Actual32taskfixture failure preserved')
    model=inspect.getsource(prior.UnitCPU)
    substitutions=[('elif op==0xa2ec:self.push(12,r[7])',
        'elif op==0xa20f:self.push(15,r[0])\n            elif op==0xa2ec:self.push(12,r[7])'),
        ('self.next_job=0x20000;self.next_actor=0x40000',
         "self.next_job=0x90000;self.next_actor=0x40000\n        need(self.next_job>self.base_sp and self.victim<self.next_actor<self.base_sp, 'Disjoint synthetic victim, actor, global SP and native-task pools')")]
    for old,new in substitutions:
        prior.need(model.count(old)==1,'Only exact preserved unit-model boundary changes')
        model=model.replace(old,new)
    units=inspect.getsource(prior.inspect_units)
    substitutions=[('cpu.load(actor+0xc0,32)==0x51',
        'cpu.load(actor+0xc0,16)==0x51 and cpu.load(actor+0xd0,16)==1'),
        ('cpu.done and len(jobs)==32 and cpu.regs[8:12]==original and cpu.regs[15]==cpu.base_sp,',
         'cpu.done and len(jobs)==32 and cpu.regs[8:12]==original and cpu.regs[15]==cpu.base_sp and all(cpu.mem[at]==value for at,value in cpu.original_victim.items()),')]
    for old,new in substitutions:
        prior.need(units.count(old)==1,'Exact width fix and stronger actual victim conservation')
        units=units.replace(old,new)
    failure_inputs=[Path(module.__file__).resolve() for module in (prior,class_check,stack_check)]
    failure_inputs.extend(folder/leaf for folder in (prior.OUT,class_check.OUT,stack_check.OUT)
        for leaf in ('failure.txt','failed_executed_sources.json.gz','compiler.log','native_exit.json'))
    code=inspect.getsource(prior.main)
    old='paths=[Path(__file__),accepted.OUT/'
    new='paths=[Path(__file__),*failure_inputs,accepted.OUT/'
    prior.need(code.count(old)==1,'Complete all actual failed model/source provenance')
    code=code.replace(old,new)
    code=code.replace('report=dict(passed=True,sourceOnlyAccepted=True,',
        'report=dict(passed=True,disjointSyntheticPoolsVerified=True,strongerTrueVictimConservation=True,nativeEffectClassWordAndDepthWordReviewed=True,actualNativeA20FSupported=True,preservedAllCheckerFailures=True,sourceOnlyAccepted=True,')
    scope=dict(vars(prior),OUT=OUT,__file__=__file__,failure_inputs=failure_inputs)
    exec(compile(model,__file__+'::disjoint_pool_model','exec'),scope)
    exec(compile(units,__file__+'::actual_semantic_checks','exec'),scope)
    exec(compile(code,__file__+'::complete_source_qualification','exec'),scope)
    scope['main']()
    for folder in (prior.OUT,class_check.OUT,stack_check.OUT):
        terminal=json.loads((folder/'native_exit.json').read_text())
        prior.need(terminal['nativeExit']==0,'Actual generated failed-check source probes terminal')
        probe=folder/'initializer_probe.exe'
        if probe.exists():
            prior.need(probe.parent.resolve()==folder.resolve(),'Exact terminal temporary probe only');probe.unlink()


if __name__=='__main__':main()
