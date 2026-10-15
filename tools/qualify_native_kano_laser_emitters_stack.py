"""Preserve both failed checkers; support actual non-yielding SP push.

ClassWORD/depthWORD correction stays. Add only decoded A20F (MOVE A0,
-*SP,1), already used by accepted native object/cache cleanup. No emitted
source/opcode repair and no weakened original ownership/stack checks.
"""
import inspect
import json
from pathlib import Path

import qualify_native_kano_laser_emitters as prior
import qualify_native_kano_laser_emitters_class as class_check

ROOT=prior.ROOT
OUT=ROOT/'audit_native_kano_laser_emitters_stack_source'


def main():
    prior.need(not OUT.exists(),'Fresh source successor; all executed failures preserved')
    prior.need('Unknown emitted word A20F' in (class_check.OUT/'failure.txt').read_text(),
               'Actual missing unit-model opcode failure preserved')
    model=inspect.getsource(prior.UnitCPU)
    old='elif op==0xa2ec:self.push(12,r[7])'
    new='elif op==0xa20f:self.push(15,r[0])\n            '+old
    prior.need(model.count(old)==1,'Only exact native A20F decoded push support added')
    model=model.replace(old,new)
    units=inspect.getsource(prior.inspect_units)
    old='cpu.load(actor+0xc0,32)==0x51'
    new='cpu.load(actor+0xc0,16)==0x51 and cpu.load(actor+0xd0,16)==1'
    prior.need(units.count(old)==1,'Keep exact native class/depth WORD checks')
    units=units.replace(old,new)
    code=inspect.getsource(prior.main)
    old='paths=[Path(__file__),accepted.OUT/'
    new='paths=[Path(__file__),Path('+repr(str(Path(prior.__file__).resolve()))+'),Path('+repr(str(Path(class_check.__file__).resolve()))+'),ROOT/\'audit_native_kano_laser_emitters_source/failure.txt\',ROOT/\'audit_native_kano_laser_emitters_source/failed_executed_sources.json.gz\',ROOT/\'audit_native_kano_laser_emitters_source/compiler.log\',ROOT/\'audit_native_kano_laser_emitters_source/native_exit.json\',ROOT/\'audit_native_kano_laser_emitters_class_source/failure.txt\',ROOT/\'audit_native_kano_laser_emitters_class_source/failed_executed_sources.json.gz\',ROOT/\'audit_native_kano_laser_emitters_class_source/compiler.log\',ROOT/\'audit_native_kano_laser_emitters_class_source/native_exit.json\',accepted.OUT/'
    prior.need(code.count(old)==1,'Complete actual failed source/model provenance')
    code=code.replace(old,new)
    code=code.replace('report=dict(passed=True,sourceOnlyAccepted=True,',
        'report=dict(passed=True,nativeEffectClassWordAndDepthWordReviewed=True,actualNativeA20FSupported=True,preservedBothCheckerFailures=True,sourceOnlyAccepted=True,')
    scope=dict(vars(prior),OUT=OUT,__file__=__file__)
    exec(compile(model,__file__+'::actual_stack_opcode','exec'),scope)
    exec(compile(units,__file__+'::native_class_word','exec'),scope)
    exec(compile(code,__file__+'::complete_source_qualification','exec'),scope)
    scope['main']()
    for folder in (prior.OUT,class_check.OUT):
        terminal=json.loads((folder/'native_exit.json').read_text())
        prior.need(terminal['nativeExit']==0,'Actual failed-check generated source probe terminal')
        probe=folder/'initializer_probe.exe'
        if probe.exists():
            prior.need(probe.parent.resolve()==folder.resolve(),'Exact terminal temporary probe only');probe.unlink()


if __name__=='__main__':main()
