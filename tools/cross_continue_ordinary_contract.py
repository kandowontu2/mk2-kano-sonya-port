"""Original complete paid-loss/UI gates; actual immediate ordinary controls."""
import inspect, types
from pathlib import Path
import continue_viewport_contract_v6610 as original
import kano_ball_launch_context_v6642 as current
ROOT,need,sha,rows=original.ROOT,original.need,original.sha,original.rows


def compile_function(source,name,scope):
    namespace=dict(scope);exec(compile(source,__file__+'::'+name,'exec'),namespace)
    return namespace[name]


base_source=inspect.getsource(original.original.prior.current.executed.prior.original.gate)
for before,after in {
    "e['reLive']<int(q['frame'])<=terminal":"e['reLive']<=int(q['frame'])<terminal",
    "range(e['reLive']+1,terminal+1)":"range(e['reLive'],terminal)",
    "len(enemy)==1 and enemy[0]['state']=='0'and q['a8']==enemy[0]['actor']and q['a13']==enemy[0]['main']":"len(enemy)==1 and origin(q,enemy[0])",
    "selected=[q for q in rows(text,'SELECT')if int(q['origin'])==e['reselect']]":"selected=model.records(text,'SELECT')",
    "selected[-1]['roster']==selected[-1]['wanted']==str(IDS[target])":"selected[-1]['roster']==str(IDS[target]) and selected[-1]['fighter']==target and selected[-1]['side']==str(side)",
}.items():
    need(base_source.count(before)==1,'Whole original paid continue adaptation '+before);base_source=base_source.replace(before,after,1)
first=base_source.index(" need(len({q['x']");last=base_source.index(" health=rows(text,'HEALTH')",first)
base_source=base_source[:first]+""" controls=rows(text,'INPUT')
 for button,start,hold in [('Coin',20,5),('Coin',270,5),('Start',310,5)]:
  want=list(range(e['continue']+start,e['continue']+start+hold))
  need([int(q['frame'])for q in controls if q['button']==button and e['continue']+start<=int(q['frame'])<e['continue']+start+hold]==want,'Exact native paid continue input '+button)
"""+base_source[last:]
base_gate=compile_function(base_source,'gate',dict(original.original.prior.current.executed.prior.original.__dict__,origin=original.original.prior.current.origin,model=original.model))
ui_source=inspect.getsource(original.model.verify_log)
before="{n(r, 'frame') for r in inputs if r['button'] == 'Block'} == set(range(f, final+1))"
need(ui_source.count(before)==1,'Whole native UI contract, no Block policy in original ordinary tail')
ui_source=ui_source.replace(before,"not [r for r in inputs if r['button'] == 'Block']",1)
ui=types.SimpleNamespace(**dict(vars(original.model),verify_log=compile_function(ui_source,'verify_log',original.model.__dict__)))
_gate=compile_function(inspect.getsource(original.gate),'gate',dict(original.gate.__globals__,base_gate=base_gate,model=ui))
viewport=compile_function(inspect.getsource(original.viewport),'viewport',dict(original.viewport.__globals__,context=current))
render=compile_function(original.source,'render',dict(original.model.__dict__,viewport=viewport))
model=original.model


def gate(text,fighter,side,target):
    need(fighter!=target,'Actual cross-character continue')
    result=_gate(text,fighter,side,target);first=result['events']['reReady'];last=first+180
    fields={(int(r['frame']),int(r['slot'])):r for r in rows(text,'FIELD')};inputs=ui.records(text,'INPUT')
    for button,age,hold in (('Up',64,3),('High_Punch',128,3)):
        need([int(r['frame'])for r in inputs if r['button']==button and int(r['frame'])>=first]==list(range(first+age,first+age+hold)), 'Exact physical ordinary input '+button)
    walking=[r for r in inputs if r['button']in('Left','Right')and int(r['frame'])>=first]
    need([int(r['frame'])for r in walking]==list(range(first+12,first+36)),'Whole physical ordinary walk input')
    need(len({fields[f,side]['x']for f in range(first+12,first+56)})>1,'Actual post-continue walk')
    need(any(int(fields[f,side]['y'])<int(fields[f,side]['floor'])for f in range(first+65,first+116)),'Actual post-continue jump')
    need(any(fields[f,side]['action']=='257'for f in range(first+129,first+161)),'Actual post-continue ordinary punch')
    final=fields[last-1,side]
    need(final['id']==final['roster']==str({'kano':17,'sonya':18}[target])and final['y']==final['floor']and final['vy']==final['gravity']=='00000000'and int(final['flags'],16)&0x1c==0,'True continued fighter naturally grounded after ordinary controls')
    result.update(actualWalkJumpPunchAccepted=True,scope='current v6640 released-input cross-character CPU-earned paid continue, full native UI/viewport and actual ordinary walk/jump/punch; not all stages/audio/whole port')
    return result


DEPENDENCIES=[*original.DEPENDENCIES,Path(__file__),Path(current.__file__),ROOT/'mk2ks_cross_continue_v3.lua',ROOT/'mk2ks_cross_continue_ordinary_presentation.lua']
