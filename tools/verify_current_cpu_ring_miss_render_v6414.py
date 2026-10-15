"""Full original FIFO/cache/geometry/shadow gates for actual missed Ring.

Keep complete source/art/register bindings. A miss has flight but no impact;
derive coverage from that actual branch and retain the whole recovery tail.
"""
import argparse,inspect,json
from pathlib import Path
from types import SimpleNamespace
import capture_current_cpu_ring_miss_render_v6412 as capture
import verify_current_cpu_ring_render_v6379 as original
import verify_current_cpu_ring_render_v6381 as registers

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
CASE=capture.FOLDER
OUT=ROOT/'audit_v6415_current_cpu_ring_miss_render_checked'


def native_gate(groups,*args):
 records,text,guest,payload,seq,timeline=args
 child=groups['FLOOR_CHILD_SPAWN'][0]['actor']
 pubs=[];dead=[]
 for index,line in enumerate(text.splitlines()):
  if not line.startswith(('MK2_NAT_CAMPAIGN_FLOOR_ALL_QUEUE ','MK2_NAT_CAMPAIGN_FLOOR_CHILD_RETIRE ')):continue
  tag,row=capture.original.model.parse(line)
  if row['actor']==child:(pubs if tag=='FLOOR_ALL_QUEUE'else dead).append(index)
 need(len(dead)==1 and pubs and max(pubs)<dead[0],'All actual missed-child publications precede native retirement')
 source=inspect.getsource(original.native_gate)
 before="block=block.replace(before,\"(ROOT/'mk2ks_physical_p2_cpu_continuation_v1997.lua')\",1)"
 after="""block=block.replace(before,"(ROOT/'mk2ks_physical_p2_cpu_continuation_v3300.lua')",1)
 before_draw='assert draws[1]>50 and draws[2]>50 and draws[3]>30'
 need(block.count(before_draw)==1,'Only hit-specific child draw-count assertion differs')
 block=block.replace(before_draw,"assert draws[1]>50 and draws[2]>50 and draws[3]>0, 'Complete miss owned FIFO/dispatch check has positive child draws'",1)"""
 need(source.count(before)==1,'Only actual physical driver location differs')
 source=source.replace(before,after,1)
 before="assert set(seq['body'])<=visible[2]and set(seq['impact'])<=visible[3], 'Every original release and seven impact poses actually visible'"
 after="assert set(seq['body'])<=visible[2] and set(seq['flight'])<=visible[3] and not any(q['slot']==3 and q['pose']in seq['impact']for q in queues.values()), 'Every original release and four flight poses visible; actual miss has no impact publications'"
 need(source.count(before)==1,'Actual miss replaces hit-only impact coverage, not omitted flight states')
 source=source.replace(before,after,1)
 source=source.replace('completeOriginalImpactPoses=len(seq[\'impact\'])','completeOriginalImpactPoses=0',1)
 scope=dict(original.native_gate.__globals__,CASE=CASE)
 exec(compile(source,__file__+'::whole_original_native_miss_FIFO_cache_projection','exec'),scope)
 register_scope=dict(registers.native_gate.__globals__,original=SimpleNamespace(native_gate=scope['native_gate']))
 exec(compile(inspect.getsource(registers.native_gate),__file__+'::whole_all_DMA_register_bindings','exec'),register_scope)
 return register_scope['native_gate'](groups,*args)


def main(preflight=False):
 meta=json.loads((CASE/'result.json').read_text())
 need(meta['passed'] and meta['wholeEarlierPhysicalTrajectoryIdentical'] and
      meta['independentSemantics']['ring']['acceptedRings'][0]['missed'],
      'Actual current missed Ring and unchanged whole original5324 physical trajectory')
 source=inspect.getsource(original.main)
 before='Path(__file__),Path(original.__file__),Path(shadows.__file__)'
 after='Path(__file__),Path(prior.__file__),Path(registers.__file__),Path(original.__file__),Path(shadows.__file__)'
 need(source.count(before)==1,'Pin complete executed source gates')
 source=source.replace(before,after,1)
 before='currentCPUFullRingHitRenderShadowAndEraseAccepted=True'
 need(source.count(before)==1,'Report true miss branch, not hit acceptance')
 source=source.replace(before,'currentCPUMissedRingRenderShadowAndEraseAccepted=True',1)
 before=" need(check(groups)==positive and shadow_gate(groups,buffers)==shadow,'Complete native positive restored after every actual fault')"
 after=""" child=groups['FLOOR_CHILD_SPAWN'][0]['actor']
 lines=text.splitlines()
 pubs=[i for i,s in enumerate(lines)if s.startswith('MK2_NAT_CAMPAIGN_FLOOR_ALL_QUEUE ')and capture.model.parse(s)[1]['actor']==child]
 changed=list(lines);pub=changed.pop(pubs[-1]);dead=next(i for i,s in enumerate(changed)if s.startswith('MK2_NAT_CAMPAIGN_FLOOR_CHILD_RETIRE '));changed.insert(dead+1,pub)
 changed='\\n'.join(changed)
 need(changed!=text,'Real last native miss publication reordered after retirement')
 try:native_gate(groups,records,changed,guest,scene.payload,sequences['ring'],timeline)
 except(ValueError,AssertionError,KeyError)as error:rejected.append(dict(fault='miss child published after native retirement',rejectedBy=str(error)))
 else:raise ValueError('Actual missed-child publication-order fault accepted')
 need(check(groups)==positive and shadow_gate(groups,buffers)==shadow,'Complete native positive restored after every actual fault')"""
 need(source.count(before)==1,'Retain all original faults plus real retirement order fault')
 source=source.replace(before,after,1)
 actual_capture=SimpleNamespace(**capture.__dict__,previous=capture.original.previous,model=capture.original.model,
                               init_model=capture.original.init_model)
 scope=dict(original.__dict__,__file__=__file__,OUT=OUT,CASE=CASE,capture=actual_capture,prior=original,
            registers=registers,native_gate=native_gate)
 exec(compile(inspect.getsource(original.observations),__file__+'::whole_original_GFX_digest_binding','exec'),scope)
 exec(compile(inspect.getsource(original.shadow_gate),__file__+'::whole_original_native_shadow_rows','exec'),scope)
 exec(compile(source,__file__+'::whole_miss_source_positive_and_record_faults','exec'),scope)
 return scope['main'](preflight)


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');args=parser.parse_args()
 main(args.preflight)
