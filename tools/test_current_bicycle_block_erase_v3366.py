"""Original eighteen native erase corruptions on each blocked human-slot capture."""
import inspect
import json
import traceback
from pathlib import Path
from types import SimpleNamespace
import verify_current_bicycle_block_render_v3362 as current
import test_current_bicycle_erase_v3331 as tests

ROOT=current.ROOT;OUT=ROOT/'audit_v3367_current_bicycle_block_erase_counterexamples';need=current.need

def run():
    expected=current.state.current.expected_current()
    current.state.current.assembly.NAME=current.state.current.current.CANDIDATE
    current.state.current.assembly.expected=lambda:expected
    cases=[];pins={}
    for side in (1,2):
        source=inspect.getsource(tests.run)
        substitutions=[
            ("    expected=current.current.expected_current()\n    current.current.assembly.NAME=current.current.current.CANDIDATE;current.current.assembly.expected=lambda:expected\n", ""),
            ("base=proof['erase'];", f"base=proof['cases'][{side-1}]['erase'];"),
            ("positive['continuousExactFlips']==109", "positive['continuousExactFlips']==67"),
        ]
        for before,after in substitutions:
            need(source.count(before)==1,'Exactly one declared expected-image/proof/fixture-length adaptation: '+before)
            source=source.replace(before,after)
        namespace=dict(vars(tests))
        namespace.update(expected=expected,model=current.erase,
                         current=SimpleNamespace(OUT=current.OUT,state=SimpleNamespace(CASE=f'audit_v3358_current_bicycle_block_display_p{side}_kano')))
        exec(compile(source,__file__+f'::original18_slot{side}','exec'),namespace)
        result=namespace['run']()
        need(result['passed'] and result['actualCounterexamplesRejected']==18 and
             result['sameMockedPathPositiveControlsAccepted'] and result['specificRejectionReasonsRequired'] and
             result['unrelatedMissingEventExceptionsNeverAccepted'] and result['actualCapturesUnmodified'],
             'All eighteen specifically qualified original erase corruptions per physical human slot')
        for file,digest in result['inputHashes'].items():
            need(file not in pins or pins[file]==digest,'Consistent immutable erase/source evidence');pins[file]=digest
        cases.append(dict(side=side,result=result))
        print('Completed original eighteen erase counterexamples for physical slot '+str(side),flush=True)
    pins[str(Path(__file__).resolve())]=current.state.current.assembly.sha(__file__)
    return dict(passed=True,physicalSlots=2,actualCounterexamplesRejected=36,cases=cases,inputHashes=pins,
                samePathPositiveControlsAccepted=True,specificRejectionReasonsRequired=True,
                unrelatedMissingEventExceptionsNeverAccepted=True,actualCapturesUnmodified=True,
                oneInitialBaseOnly=True,gameBytesChanged=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Never overwrite executed erase counterexamples')
    try:value=run()
    except Exception as error:value=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({k:v for k,v in value.items()if k not in ('cases','inputHashes')},indent=2),flush=True)
    raise SystemExit(0 if value['passed']else 1)
