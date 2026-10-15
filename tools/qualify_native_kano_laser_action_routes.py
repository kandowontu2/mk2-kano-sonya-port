"""Preserve the actual Friendship fallback discovered by whole initializer.

The prior new action source failed its preexisting-route guard before any
game build. Actual current HK is F9980 (Friendship -> first fatality -> HK),
not F5500 alone. Repair only the new action fallback; keep failed stages.
"""
import inspect
from pathlib import Path
import qualify_native_kano_laser_action as initial
import qualify_native_kano_laser_action_harness as harness_failure

ROOT=initial.ROOT
STAGE=ROOT/'source_native_kano_laser_action_routes'
OUT=ROOT/'audit_native_kano_laser_action_routes_source'


def main():
    initial.need(not OUT.exists(),'Fresh route-conserving successor')
    import json
    failure=json.loads((harness_failure.OUT/'native_exit.json').read_text())
    initial.need(failure['nativeExit']!=0 and 'existing true Kano first finish routes changed' in failure['stderr'],
                 'Actual preexisting-route source guard failure retained')
    old=(initial.STAGE/'midtunit_m.cpp').read_text();new=(STAGE/'midtunit_m.cpp').read_text()
    repairs=[('\tconstexpr unsigned kano_laser_parser=0xb0c80, kano_laser_entry=0xb0cc0;',
        '\tconstexpr unsigned kano_laser_parser=0xb0c80, kano_laser_entry=0xb0cc0;\n\tconstexpr unsigned kano_laser_previous_hk=0xf9980; // existing Friendship -> first finisher -> ordinary HK chain'),
        ('if (read32(0xff270+17*4)!=native_address(kano_finish_parser) ||',
         'if (read32(0xff270+17*4)!=native_address(kano_laser_previous_hk) ||'),
        ('leg_branch(0xc980,native_address(kano_finish_parser));',
         'leg_branch(0xc980,native_address(kano_laser_previous_hk));')]
    # The guarded source fragment also exists in the earlier Friendship
    # initializer. Limit repair/conservation checks to the new action block.
    at=old.index('// KANO_LASER_ACTION_BEGIN');prefix=old[:at];tail=old[at:]
    for before,after in repairs:
        initial.need(tail.count(before)==1,'Exact new action fallback repair only');tail=tail.replace(before,after)
    initial.need(prefix+tail==new,'Every previous action/source byte untouched')
    contract=inspect.getsource(initial.contract)
    before='a.jump(address(0xf5500),0xc980)'
    initial.need(contract.count(before)==1,'Expected independent fallback byte change')
    contract=contract.replace(before,'a.jump(address(0xf9980),0xc980)')
    code=inspect.getsource(initial.main)
    before="harness=old_harness.replace(anchor,anchor+'\\n'+block)"
    initial.need(code.count(before)==1,'Actual existing Kano action constant exposed to isolated harness')
    code=code.replace(before,"harness=old_harness.replace(anchor,anchor+'\\n\\tconstexpr unsigned kano_finish_action=0xf55c0;\\n'+block)")
    before='((0xff270+17*4,address(0xf5500))'
    initial.need(code.count(before)==1,'Restore actual prior complete Friendship HK chain for whole-guest hash')
    code=code.replace(before,'((0xff270+17*4,address(0xf9980))')
    inputs=[Path(initial.__file__),Path(harness_failure.__file__),*(initial.STAGE/f for f in ('midtunit_m.cpp','midtunit.cpp','midtunit.h'))]
    inputs.extend(folder/leaf for folder in (initial.OUT,harness_failure.OUT)
                  for leaf in ('failure.txt','compiler.log','failed_executed_sources.json.gz'))
    inputs.append(harness_failure.OUT/'native_exit.json')
    before='paths=[Path(__file__),accepted.OUT/'
    initial.need(code.count(before)==1,'Complete both failed source-checker provenances')
    code=code.replace(before,'paths=[Path(__file__),*failure_inputs,accepted.OUT/')
    code=code.replace('report=dict(passed=True,sourceOnlyAccepted=True,',
        'report=dict(passed=True,actualFriendshipFirstFatalityHKChainConserved=True,failedSourceGuardPreserved=True,sourceOnlyAccepted=True,')
    scope=dict(vars(initial),STAGE=STAGE,OUT=OUT,__file__=__file__,failure_inputs=inputs)
    exec(compile(contract,__file__+'::actual_chain_contract','exec'),scope)
    exec(compile(code,__file__+'::whole_source_qualification','exec'),scope)
    scope['main']()
    probe=harness_failure.OUT/'initializer_probe.exe'
    if probe.exists():
        initial.need(probe.parent.resolve()==harness_failure.OUT.resolve(),'Exact actual terminal failed guard probe');probe.unlink()


if __name__=='__main__':main()
