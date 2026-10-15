"""Whole original paid-continue/UI gates plus genuine ordinary tail, v6640."""
import inspect, types
from pathlib import Path
import continue_viewport_contract_v6610 as original
import kano_ball_launch_context_v6642 as current
ROOT, need, sha, rows = original.ROOT, original.need, original.sha, original.rows


def bind(fn, changes, scope):
    source=inspect.getsource(fn)
    for before,after in changes:
        need(source.count(before)==1,'Exact whole original controller/gate adaptation '+before)
        source=source.replace(before,after,1)
    space=dict(fn.__globals__, **scope)
    exec(compile(source,__file__+'::'+fn.__name__,'exec'),space)
    return space[fn.__name__]


verify_ui=bind(original.model.verify_log, (
    ('final == f+180','final == f+360'),
    ("set(range(f, final+1))", "set(range(f, f+180))"),
), {})
ui=types.SimpleNamespace(**dict(vars(original.model),verify_log=verify_ui))
base_gate=bind(original.base_gate, (("terminal==e['reReady']+180", "terminal==e['reReady']+360"),), {})
_gate=bind(original.gate, (("terminal=e['reReady']+180", "terminal=e['reReady']+360"),), dict(base_gate=base_gate,model=ui))
viewport=bind(original.viewport, (), dict(context=current))
render=bind(original.render, (), dict(viewport=viewport))


def gate(text,fighter,side,target):
    need(fighter!=target,'Explicit cross-character continue, not another same-character case')
    result=_gate(text,fighter,side,target);e=result['events'];first=e['reReady'];end=first+360
    fields={(int(r['frame']),int(r['slot'])):r for r in rows(text,'FIELD')}
    inputs=ui.records(text,'INPUT')
    for button,age,hold in (('Up',244,3),('High_Punch',308,3)):
        need([int(r['frame'])for r in inputs if r['button']==button and int(r['frame'])>=first]==list(range(first+age,first+age+hold)), 'Whole actual post-continue ordinary input '+button)
    walking=[r for r in inputs if r['button']in('Left','Right')and int(r['frame'])>=first]
    need([int(r['frame'])for r in walking]==list(range(first+192,first+216)),'Whole real post-continue walk input')
    need(len({fields[f,side]['x']for f in range(first+192,first+236)})>1,'Actually walks after cross-character continue')
    need(any(int(fields[f,side]['y'])<int(fields[f,side]['floor'])for f in range(first+245,first+296)),'Actually jumps after cross-character continue')
    need(any(fields[f,side]['action']=='257'for f in range(first+309,first+341)),'Actual original standing punch after cross-character continue')
    final=fields[end-1,side]
    need(final['id']==final['roster']==str({'kano':17,'sonya':18}[target])and final['y']==final['floor']and final['vy']==final['gravity']=='00000000'and int(final['flags'],16)&0x1c==0,'True new fighter returns naturally grounded after ordinary controls')
    result.update(actualWalkJumpPunchAccepted=True,ordinaryTailFields=360,scope='current v6640 released-input cross-character CPU-earned paid continue, original complete UI/viewport and actual walk/jump/punch; not all stages/audio/whole port')
    return result


DEPENDENCIES=[*original.DEPENDENCIES,Path(__file__),Path(current.__file__),
 ROOT/'mk2ks_cross_continue.lua',ROOT/'mk2ks_cross_continue_presentation.lua',
 ROOT/'source_v6636_kano_ball_launch/midtunit_m.cpp']
