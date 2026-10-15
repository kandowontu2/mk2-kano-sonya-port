"""Original sixteen raster corruptions, independently on each actual human slot."""
import builtins
import inspect
import json
import traceback
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import verify_current_bicycle_block_render_v3362 as current
import test_native_cpu_bicycle_round_render_v3136 as tests

ROOT=current.ROOT;OUT=ROOT/'audit_v3365_current_bicycle_block_render_counterexamples';need=current.need

def run():
    expected=current.state.current.expected_current()
    current.state.current.assembly.NAME=current.state.current.current.CANDIDATE
    current.state.current.assembly.expected=lambda:expected
    cases=[];pins={}
    for side in (1,2):
        source=inspect.getsource(tests.run)
        substitutions=[
            ("checked=ROOT/f'audit_v3131_native_cpu_bicycle_round_render_{player}_checked/report.json'", "checked=ROOT/'audit_v3363_current_bicycle_block_render_erase_checked/report.json'"),
            ("proof=json.loads(checked.read_text());", f"proof=json.loads(checked.read_text())['cases'][{side-1}]['scene'];"),
            ("q['slot']==2", f"q['slot']=={side}"),
            ("r['slot']==2", f"r['slot']=={side}"),
            ("condition=lines[-1].line or ''", "condition=model.render_condition(lines[-1])"),
        ]
        for before,after in substitutions:
            need(source.count(before)==1,'Exactly one declared actual-slot/proof/diagnostic routing change: '+before)
            source=source.replace(before,after)
        compiled={}
        def compile_capture(text,filename,*args,**kwargs):
            compiled[filename]=text.splitlines()
            return builtins.compile(text,filename,*args,**kwargs)
        def condition(frame):
            if frame.filename in compiled:return compiled[frame.filename][frame.lineno-1]
            return frame.line or ''
        bridge=SimpleNamespace(**vars(current.render.original))
        bridge.CASES={'current_p'+str(side):(f'audit_v3358_current_bicycle_block_display_p{side}_kano','new','kano')}
        bridge.bicycle=SimpleNamespace(INTRO=current.render.poses.INTRO)
        bridge.model=SimpleNamespace(capture=SimpleNamespace(assembly=current.state.current.assembly))
        bridge.verify=lambda key:current.render.verify(side)
        bridge.render_condition=condition
        namespace=dict(vars(tests));namespace['model']=bridge
        exec(compile(source,__file__+f'::original16_slot{side}','exec'),namespace)
        with patch.object(current.render,'compile',side_effect=compile_capture,create=True):
            result=namespace['run']()
        need(result['passed'] and result['actualCounterexamplesRejected']==16 and
             result['sameMockedPathPositiveControlAccepted'] and result['unrelatedMissingEventExceptionsNeverAccepted'] and
             result['originalCapturesUnchanged'],'All sixteen qualified original scene corruptions per physical human slot')
        for file,digest in result['inputHashes'].items():
            need(file not in pins or pins[file]==digest,'Consistent immutable scene/source evidence');pins[file]=digest
        cases.append(dict(side=side,result=result))
    pins[str(Path(__file__).resolve())]=current.state.current.assembly.sha(__file__)
    return dict(passed=True,physicalSlots=2,actualCounterexamplesRejected=32,cases=cases,inputHashes=pins,
                samePathPositiveControlsAccepted=True,specificRejectionReasonsRequired=True,
                unrelatedMissingEventExceptionsNeverAccepted=True,actualCapturesUnmodified=True,
                gameBytesChanged=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Never overwrite executed raster counterexamples')
    try:value=run()
    except Exception as error:value=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({k:v for k,v in value.items()if k not in ('cases','inputHashes')},indent=2),flush=True)
    raise SystemExit(0 if value['passed']else 1)
