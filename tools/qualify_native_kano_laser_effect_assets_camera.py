"""Successor for the preserved camera disassembler-spacing mismatch.

Original JRLT is four letters, native JRC three; retain full instruction
and operand equality while matching the native mnemonic's padding. The
executed checker, failure and source stay frozen. No game/source repair.
"""
import inspect
import json
from pathlib import Path

import qualify_native_kano_laser_effect_assets as prior

ROOT=prior.ROOT
OUT=ROOT/'audit_native_kano_laser_effect_assets_camera_source'


def main():
    prior.need(not OUT.exists(),'Fresh successor output; failed checker/source immutable')
    failure=prior.OUT/'failure.txt'
    prior.need('Entire original/native tracking routines map' in failure.read_text(),
               'Original full tracking comparison failure preserved')
    camera=inspect.getsource(prior.camera_contract)
    old=".replace('JRLT','JRC')"
    new=".replace('JRLT   ','JRC    ')"
    prior.need(camera.count(old)==1,'Only exact native JRC mnemonic alignment changes')
    camera=camera.replace(old,new)
    code=inspect.getsource(prior.main)
    old_paths='paths=[Path(__file__),Path(prior.__file__),'
    new_paths='paths=[Path(__file__),Path('+repr(str(Path(prior.__file__).resolve()))+'),ROOT/\'audit_native_kano_laser_effect_assets_source/failure.txt\',ROOT/\'audit_native_kano_laser_effect_assets_source/failed_executed_sources.json.gz\',ROOT/\'audit_native_kano_laser_effect_assets_source/compiler.log\',ROOT/\'audit_native_kano_laser_effect_assets_source/native_exit.json\',Path(prior.__file__),'
    prior.need(code.count(old_paths)==1,'Exact full evidence path boundary')
    code=code.replace(old_paths,new_paths)
    code=code.replace('report=dict(passed=True,sourceOnlyAccepted=True,',
                      'report=dict(passed=True,preservedCameraSpacingFailure=True,fullInstructionEqualityRetained=True,sourceOnlyAccepted=True,')
    scope=dict(vars(prior),OUT=OUT,__file__=__file__)
    exec(compile(camera,__file__+'::camera_alignment','exec'),scope)
    exec(compile(code,__file__+'::whole_source_check','exec'),scope)
    scope['main']()
    # Native exit0 proves this failed run's generated source probe is already
    # terminal. Preserve all actual executed source/compiler/failure evidence.
    terminal=json.loads((prior.OUT/'native_exit.json').read_text())
    prior.need(terminal['nativeExit']==0,'Original temporary source probe terminal')
    probe=prior.OUT/'initializer_probe.exe'
    if probe.exists():
        prior.need(probe.parent.resolve()==prior.OUT.resolve(),'Exact disposable failed-check source probe only')
        probe.unlink()


if __name__=='__main__':main()
