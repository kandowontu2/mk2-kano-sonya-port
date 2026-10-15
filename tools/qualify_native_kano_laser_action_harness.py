"""Declare the two existing Kano constants in the isolated compile harness.

They are already in the actual game initializer. The preserved stand-alone
harness started after those declarations and only exposed Sonya's symbols.
No staged source/action or expected emitted bytes are changed.
"""
import inspect
import json
from pathlib import Path
import qualify_native_kano_laser_action as prior

ROOT=prior.ROOT
OUT=ROOT/'audit_native_kano_laser_action_harness_source'


def main():
    prior.need(not OUT.exists(),'Fresh source qualification successor')
    log=(prior.OUT/'compiler.log').read_text()
    prior.need("'kano_finish_parser' was not declared" in log and "'kano_finish_action' was not declared" in log,
               'Actual isolated-harness missing-symbol failure retained')
    source=(prior.STAGE/'midtunit_m.cpp').read_text()
    prior.need('constexpr unsigned kano_finish_parser=0xf5500, sonya_finish_parser=0xf5560;' in source and
               'constexpr unsigned kano_finish_action=0xf55c0, sonya_finish_action=0xf5640;' in source,
               'Both declarations genuinely present in real game source')
    code=inspect.getsource(prior.main)
    old="harness=old_harness.replace(anchor,anchor+'\\n'+block)"
    prior.need(code.count(old)==1,'Exact isolated harness append boundary')
    code=code.replace(old,"harness=old_harness.replace(anchor,anchor+'\\n\\tconstexpr unsigned kano_finish_parser=0xf5500, kano_finish_action=0xf55c0;\\n'+block)")
    inputs=[Path(prior.__file__),prior.OUT/'failure.txt',prior.OUT/'compiler.log',prior.OUT/'failed_executed_sources.json.gz']
    old='paths=[Path(__file__),accepted.OUT/'
    prior.need(code.count(old)==1,'Full prior executed failure provenance')
    code=code.replace(old,'paths=[Path(__file__),*failure_inputs,accepted.OUT/')
    code=code.replace('report=dict(passed=True,sourceOnlyAccepted=True,',
        'report=dict(passed=True,actualGameSourceAlreadyDeclaredKanoConstants=True,isolatedHarnessDeclarationsOnly=True,preservedCompileFailure=True,sourceOnlyAccepted=True,')
    scope=dict(vars(prior),OUT=OUT,__file__=__file__,failure_inputs=inputs)
    exec(compile(code,__file__+'::complete_isolated_source_qualification','exec'),scope)
    scope['main']()


if __name__=='__main__':main()
