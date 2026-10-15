"""Full native UI plus the whole existing actual-response/survival contract."""
import inspect,types
from pathlib import Path
import cross_continue_ordinary_contract as previous
import single_continue_controls_v6580 as controls
ROOT,need,sha,rows=previous.ROOT,previous.need,previous.sha,previous.rows
original,current,model=previous.original,previous.current,previous.model
compile_function=previous.compile_function
base_source=previous.base_source
before="terminal==e['reReady']+180";need(base_source.count(before)==1,'Only terminal derives from real recovered control')
base_source=base_source.replace(before,"terminal==int(r['recover'])+180",1)
base_gate=compile_function(base_source,'gate',dict(previous.base_gate.__globals__))
ui_source=previous.ui_source
before='final == f+180';need(ui_source.count(before)==1,'Whole UI ends at real adaptive terminal, never invented field')
ui_source=ui_source.replace(before,'final >= f+180',1)
ui=types.SimpleNamespace(**dict(vars(model),verify_log=compile_function(ui_source,'verify_log',model.__dict__)))
gate_source=inspect.getsource(original.gate)
before="terminal=e['reReady']+180";need(gate_source.count(before)==1,'Actual control recovery sets shared UI/physical terminal')
gate_source=gate_source.replace(before,"terminal=int(rows(text,'RESULT')[0]['recover'])+180",1)
_gate=compile_function(gate_source,'gate',dict(original.gate.__globals__,base_gate=base_gate,model=ui))
render=previous.render


def gate(text,fighter,side,target):
    need(fighter!=target,'Actual cross-character continue')
    result=_gate(text,fighter,side,target);events=result['events'];terminal=int(rows(text,'RESULT')[0]['frame'])
    controls.actual_controls(text,events,rows(text,'FIELD'),side,terminal)
    result.update(actualWalkJumpPunchAccepted=True,scope='current v6640 released startup/paid cross-character continue, full native selection/viewport/teardown/name pixels and whole actual-response walk/jump/punch/recovery/180 survival; not all stages/audio/whole port')
    return result


DEPENDENCIES=[*previous.DEPENDENCIES,Path(__file__),ROOT/'tools/cross_continue_ordinary_contract.py',Path(controls.__file__),ROOT/'mk2ks_single_continue_controls_v6579.lua',ROOT/'mk2ks_cross_continue_adaptive.lua']
