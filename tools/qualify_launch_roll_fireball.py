"""Same terminal native low-fireball proof, both slots and actual fault suites.

The immutable guest oracle is independently reconstructed at both boundaries.
Every fault still compares the entire actual RAM guest to that oracle; cache
only the constant reconstruction, never runtime data or source-output samples.
"""
import inspect,types
import qualify_launch_fireball_faults as previous
import launch_roll_fireball_model as roll
ROOT,need,sha=roll.ROOT,roll.need,roll.sha

def static_guest_model(carrier):
    real=roll.model.current
    guest=real.expected()
    need(guest==carrier['guest'],'Whole actual guest matches complete independent constructor at admission')
    oracle=types.SimpleNamespace(**dict(vars(real),expected=lambda:guest))
    globals_=dict(roll.model.phase.__globals__,current=oracle)
    globals_['physical_gate']=types.FunctionType(roll.model.physical_gate.__code__,globals_,'physical_gate')
    phase=types.FunctionType(roll.model.phase.__code__,globals_,'phase')
    return types.SimpleNamespace(**dict(vars(roll.model),current=oracle,phase=phase))

inputs_source=inspect.getsource(previous.previous.inputs)
before="expected.append(dict(common,button='High_Punch'))"
need(inputs_source.count(before)==1,'Only original real low-button command differs')
inputs_source=inputs_source.replace(before,"expected.append(dict(common,button='Low_Punch'))",1)
scope=dict(previous.scope,model=roll.model)
exec(compile(inputs_source,__file__+'::entire_physical_schedule_actual_low_punch','exec'),scope)
inputs=scope['inputs']
source=previous.source
for before,after in [
 ('audit_launch_fireball_faults_checked_','audit_launch_roll_fireball_checked_'),
 ('def qualify(carrier):','def qualify(carrier):\n model=static_guest_model(carrier)'),
 (" need(all(sha(p)==h for p,h in pins.items()),'Source/evidence unchanged through complete qualification')",
  " need(roll.model.current.expected()==carrier['guest'],'Independent whole guest constructor restored at final boundary')\n need(all(sha(p)==h for p,h in pins.items()),'Source/evidence unchanged through complete qualification')"),
 ('Path(__file__),Path(previous.__file__)',"Path(__file__),ROOT/'tools/qualify_launch_fireball_faults.py',ROOT/'tools/launch_fireball_interruption_model.py',ROOT/'audit_launch_low_descriptor_scope_rejection/failure.json',Path(previous.__file__)"),
]:
    need(source.count(before)==1,'Only actual low-button/source-adapter pin or static-oracle boundary changed');source=source.replace(before,after,1)
scope=dict(previous.scope,__file__=__file__,model=roll.model,inputs=inputs,roll=roll,static_guest_model=static_guest_model)
exec(compile(source,__file__+'::whole_same_RAM_low_fireball_interruption_source_proof','exec'),scope)
qualify=scope['qualify']
