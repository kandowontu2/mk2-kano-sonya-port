"""Bind the two actual HP observer schemas without inventing absent operands.

The paired tap records frame/slot/value/PC/executing actor+Main. The complete
child tap independently records store address/mask/all registers and ownership.
Match their entire common schema, then validate the richer native operands.
Preserve the preceding real KeyError as a schema-binding failure, not gameplay.
"""
import inspect
import json
from pathlib import Path
import verify_native_kano_laser_cpu_leg_children_owned as prior

ROOT,need,sha,once,base=prior.ROOT,prior.need,prior.sha,prior.once,prior.base
OUT=ROOT/'audit_native_kano_laser_cpu_leg_children_health_checked'


def health_binding():
    source=inspect.getsource(prior.whole_health_with_child)
    source=once(source,"keys=('frame','slot','at','before','after','mask','pc','a8','a13','a10')",
                "keys=('frame','cycle','slot','before','after','pc','a8','a13')")
    source=once(source,
        "need(all(h[k]==c[k]for k in keys),'Same actual HP store, instruction, operands and execution order')",
        """need(all(h[k]==c[k]for k in keys),'Entire common native HP store schema agrees, in the same actual execution order')
        need(c['at']=={1:0x010602f0,2:0x01060ec0}[h['slot']] and c['mask']==65535 and
             c['writes']==0 and c['assistance']=='none',
             'Independent full native address/mask/register tap targets the exact actual physical lifebar')""")
    source=once(source,"h['before']-h['after']==h['a10']==accepted['damage']",
                "h['before']-h['after']==c['a10']==accepted['damage']")
    scope=dict(vars(prior))
    exec(compile(source,__file__+'::whole_child_owned_health_two_real_observer_schemas','exec'),scope)
    return scope['whole_health_with_child']


def execute(actual):
    failed=json.loads((prior.OUT/'failure.json').read_text())
    need(not failed['passed'] and failed['error']=="KeyError('at')",
         'Preserve actually executed missing-schema failure, not a false gameplay failure')
    scope=dict(vars(prior),OUT=OUT,__file__=__file__,whole_health_with_child=health_binding())
    exec(compile(inspect.getsource(prior.physical_binding),
                 __file__+'::whole_original_physical_binding_actual_health_schemas','exec'),scope)
    # Pin this adapter and the preserved failure in the same report.
    run_source=inspect.getsource(prior.run)
    run_source=once(run_source,'Path(__file__),Path(owned.__file__),Path(repeated_ring.__file__),',
                    'Path(__file__),Path(prior_file),prior_failure,Path(owned.__file__),Path(repeated_ring.__file__),')
    scope.update(prior_file=prior.__file__,prior_failure=prior.OUT/'failure.json')
    exec(compile(run_source,__file__+'::whole_original_child_owned_trace_faults','exec'),scope)
    exec(compile(inspect.getsource(prior.execute),__file__+'::immutable_actual_successor_result','exec'),scope)
    scope['execute'](actual)
