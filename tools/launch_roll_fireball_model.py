"""Original low-fireball trajectory: both complete native animation descriptors.

Keep the complete projectile/physical/body/hurt/source-stop/audio contracts.
Only the exact additional original descriptor is admitted, never arbitrary
rectangles, pointers, owners, reaction constants or observer labels.
"""
import inspect,types
import launch_fireball_interruption_model as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
source=inspect.getsource(previous.projectile_gate)
changes=[
 ('(0xff8f3760,0xff8f37f0)','(0xff8f3760,0xff8f3880)'),
 ("    fields={(int(r['frame']),int(r['slot'])):r", "    need(struct.unpack_from('<9H',guest,at(0xff8f37f0))==(112,25,100,20,0x1110,0x1605,0,0,1), 'Entire additional original second-animation rectangle, reaction17 and22HP descriptor')\n    fields={(int(r['frame']),int(r['slot'])):r"),
 ("entry['a0']=='FF8F3760'","entry['a0']in('FF8F3760','FF8F37F0')"),
 ('Every original high-fireball descriptor and full branch outcome','Every exact original first/second fireball animation descriptor and complete native hit/miss outcome'),
]
for before,after in changes:
    need(source.count(before)==1,'Only exact original second descriptor/source scope admitted');source=source.replace(before,after,1)
scope=dict(vars(previous))
exec(compile(source,__file__+'::whole_native_projectile_gate_second_original_descriptor','exec'),scope)
gate=scope['projectile_gate']
binding=dict(vars(previous),projectile_gate=gate)
phase=types.FunctionType(previous.phase.__code__,binding,'phase')
model=types.SimpleNamespace(**dict(vars(previous),phase=phase,projectile_gate=gate,__file__=__file__))
