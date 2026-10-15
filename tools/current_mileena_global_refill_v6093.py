"""Complete6085 refill with the original global routine's P2 register context.

The routine writes both global lifebars and does not consult a winning actor.
Its retained A8 is the physical P2 actor; keep every writer/health/task/field.
"""
import inspect
import current_mileena_native_refill_v6085 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha

def refill(rows,side,guest):
 source=inspect.getsource(prior.refill)
 before="owner==action['actor']and 0x01000000<=task<0x01100000"
 after="owner==action['actor'if side==1 else'victim_actor']and 0x01000000<=task<0x01100000"
 need(source.count(before)==1,'One source-native physical P2 context assertion, no dropped global refill store')
 source=source.replace(before,after,1).replace('Actual native winning actor/refill task','Actual original global-refill P2 register context/task')
 scope=dict(prior.refill.__globals__)
 exec(compile(source,__file__+'::whole_original_global_refill','exec'),scope)
 report=scope['refill'](rows,side,guest);report['actorRegisterContextNotHealthOwnership']=True
 return report

def gate(rows,fighter,side,guest):
 source=inspect.getsource(prior.gate)
 scope=dict(prior.gate.__globals__,refill=refill,__file__=__file__)
 exec(compile(source,__file__+'::entire_original_Mileena_gate','exec'),scope)
 return scope['gate'](rows,fighter,side,guest)
