"""Whole native RNG/PC/actor/Main/motion/voice gates for actual opposite victim."""
import inspect
import current_payload_metadata_context_v5229 as current
import current_cross_tomb_state_v5836 as state
import verify_tomb_mirror_native_branches_v4357 as original
import verify_native_tomb_scream_roles_v4394 as original_voice
ROOT,need,sha=current.ROOT,current.need,current.sha

def once(code,before,after):
 need(code.count(before)==1,'Only declared whole cross source replacement '+before)
 return code.replace(before,after,1)

branch_source=once(inspect.getsource(original.branch),'state=runtime.state','state=cross_state')
branch_source=once(branch_source,"own=17 if fighter=='kano'else 18","own=18 if fighter=='kano'else 17")
branch_scope=dict(vars(original),cross_state=state)
exec(compile(branch_source,__file__+'::whole4357_opposite_victim','exec'),branch_scope)
branch=branch_scope['branch'];branch.source=branch_source
fault_source=inspect.getsource(original.faults)
exec(compile(fault_source,__file__+'::whole4357_actual_cross_faults','exec'),branch_scope)
faults=branch_scope['faults']

def voice_models():
 code=once(inspect.getsource(original_voice.qualify_scream),
  "own=17 if fighter=='kano' else 18","own=18 if fighter=='kano' else 17")
 code=once(code,"'938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821'",repr(current.GUEST_SHA))
 namespace=dict(vars(original_voice))
 exec(compile(code,__file__+'::whole4394_actual_cross_voice','exec'),namespace)
 fn=namespace['qualify_scream'];fn.source=code
 exec(compile(inspect.getsource(original_voice.faults),__file__+'::whole4394_actual_cross_faults','exec'),namespace)
 return fn,namespace['faults']

def voice_proof(log,guest,fighter,side,phase):
 screams=[r for r in original_voice.native.rows(log,'ROUTE')if r['entry']=='FFA11FD0']
 if phase['nativeDrop']:
  need(len(screams)==1,'Exactly one original actual falling victim scream')
  gate,negative=voice_models()
  return gate(log,fighter,side,guest,screams[0]),negative(log,fighter,side,guest)
 need(not screams,'Native held branch must not emit a falling victim scream')
 return None,{}
