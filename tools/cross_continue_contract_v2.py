"""Recover whole generated gates from their retained source, not inspect lines."""
import inspect
from pathlib import Path
import continue_viewport_contract_v6610 as original
import kano_ball_launch_context_v6642 as current
ROOT,need,sha=original.ROOT,original.need,original.sha


def make_base():
    source=inspect.getsource(original.original.prior.current.executed.prior.original.gate)
    changes={
        "e['reLive']<int(q['frame'])<=terminal":"e['reLive']<=int(q['frame'])<terminal",
        "range(e['reLive']+1,terminal+1)":"range(e['reLive'],terminal)",
        "len(enemy)==1 and enemy[0]['state']=='0'and q['a8']==enemy[0]['actor']and q['a13']==enemy[0]['main']":"len(enemy)==1 and origin(q,enemy[0])",
        "selected=[q for q in rows(text,'SELECT')if int(q['origin'])==e['reselect']]":"selected=model.records(text,'SELECT')",
        "selected[-1]['roster']==selected[-1]['wanted']==str(IDS[target])":"selected[-1]['roster']==str(IDS[target]) and selected[-1]['fighter']==target and selected[-1]['side']==str(side)",
        "terminal==e['reReady']+180":"terminal==e['reReady']+360",
    }
    for before,after in changes.items():
        need(source.count(before)==1,'Whole original actual paid-loss/UI transport gate '+before);source=source.replace(before,after,1)
    first=source.index(" need(len({q['x']");last=source.index(" health=rows(text,'HEALTH')",first)
    source=source[:first]+""" controls=rows(text,'INPUT')
 for button,start,hold in [('Coin',20,5),('Coin',270,5),('Start',310,5)]:
  want=list(range(e['continue']+start,e['continue']+start+hold))
  need([int(q['frame'])for q in controls if q['button']==button and e['continue']+start<=int(q['frame'])<e['continue']+start+hold]==want,'Exact native paid continue input '+button)
"""+source[last:]
    scope=dict(original.namespace,origin=original.original.prior.current.origin,model=original.model)
    exec(compile(source,__file__+'::whole_original_base_gate','exec'),scope)
    return scope['gate']


def make_render():
    scope=dict(original.model.__dict__,viewport=viewport)
    exec(compile(original.source,__file__+'::whole_retained_original_renderer','exec'),scope)
    return scope['render']


source=(ROOT/'tools/cross_continue_contract.py').read_text()
before="base_gate=bind(original.base_gate, ((\"terminal==e['reReady']+180\", \"terminal==e['reReady']+360\"),), {})"
need(source.count(before)==1,'Exact inspected generated base-source retrieval correction')
source=source.replace(before,'base_gate=make_base()',1)
before='render=bind(original.render, (), dict(viewport=viewport))'
need(source.count(before)==1,'Exact generated whole renderer-source retrieval correction')
source=source.replace(before,'render=make_render()',1)
exec(compile(source,__file__+'::whole_extended_continue_contract','exec'),globals())
DEPENDENCIES=[*DEPENDENCIES,ROOT/'tools/cross_continue_contract.py']
