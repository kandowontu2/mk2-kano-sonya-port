"""Preserve failed checker; fix only native class WORD versus depth WORD.

The emitted source is correct: C0h class and adjacentD0h depth are WORDs.
A DWORD read wrongly combines51h and native depth1 into10051h. Preserve
every other semantic check and every actual generated opcode unchanged.
"""
import inspect
import json
from pathlib import Path

import qualify_native_kano_laser_emitters as prior

ROOT=prior.ROOT
OUT=ROOT/'audit_native_kano_laser_emitters_class_source'


def main():
    prior.need(not OUT.exists(),'Fresh successor, never overwrite executed failure/source')
    failure=prior.OUT/'failure.txt'
    prior.need('Exact facing-relative source position' in failure.read_text(),
               'Actual first failed particle class/position assertion preserved')
    units=inspect.getsource(prior.inspect_units)
    old='cpu.load(actor+0xc0,32)==0x51'
    new='cpu.load(actor+0xc0,16)==0x51 and cpu.load(actor+0xd0,16)==1'
    prior.need(units.count(old)==1,'Only native classWORD/depthWORD interpretation changes')
    units=units.replace(old,new)
    code=inspect.getsource(prior.main)
    old='paths=[Path(__file__),accepted.OUT/'
    new='paths=[Path(__file__),Path('+repr(str(Path(prior.__file__).resolve()))+'),ROOT/\'audit_native_kano_laser_emitters_source/failure.txt\',ROOT/\'audit_native_kano_laser_emitters_source/failed_executed_sources.json.gz\',ROOT/\'audit_native_kano_laser_emitters_source/compiler.log\',ROOT/\'audit_native_kano_laser_emitters_source/native_exit.json\',accepted.OUT/'
    prior.need(code.count(old)==1,'Exact preserved failed-check evidence paths')
    code=code.replace(old,new)
    code=code.replace('report=dict(passed=True,sourceOnlyAccepted=True,',
        'report=dict(passed=True,nativeEffectClassWordAndDepthWordReviewed=True,preservedPreviousCheckerFailure=True,sourceOnlyAccepted=True,')
    scope=dict(vars(prior),OUT=OUT,__file__=__file__)
    exec(compile(units,__file__+'::native_class_word','exec'),scope)
    exec(compile(code,__file__+'::complete_source_qualification','exec'),scope)
    scope['main']()
    original=json.loads((prior.OUT/'native_exit.json').read_text())
    prior.need(original['nativeExit']==0,'Original generated failed-check probe already terminal')
    probe=prior.OUT/'initializer_probe.exe'
    if probe.exists():
        prior.need(probe.parent.resolve()==prior.OUT.resolve(),'Exact terminal temporary probe only');probe.unlink()


if __name__=='__main__':main()
