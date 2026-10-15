"""Full current Sonya mirror Ring chip art/FIFO/shadow/erase qualification.

Every original6379 positive and real fault remains, plus6381's all-DMA
register binding. Only explicit actual physical human identity changes;
all source geometry, row cadence, ownership and cleanup rules are retained.
"""
import argparse,inspect,json,traceback
from pathlib import Path
from types import SimpleNamespace
import capture_current_cpu_ring_mirror_render_v6389 as capture
import verify_current_cpu_ring_render_v6379 as original
import verify_current_cpu_ring_render_v6381 as registers
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
CASE=capture.FOLDER
OUT=ROOT/'audit_v6392_current_cpu_ring_mirror_render_checked'


def native_gate(groups,*args):
 records,text,guest,payload,seq,timeline=args
 child=groups['FLOOR_CHILD_SPAWN'][0]['actor']
 publications=[];retirements=[]
 for index,line in enumerate(text.splitlines()):
  if not line.startswith(('MK2_NAT_CAMPAIGN_FLOOR_ALL_QUEUE ','MK2_NAT_CAMPAIGN_FLOOR_CHILD_RETIRE ')):continue
  tag,row=capture.model.parse(line)
  if row['actor']!=child:continue
  (publications if tag=='FLOOR_ALL_QUEUE'else retirements).append(index)
 need(len(retirements)==1 and publications and max(publications)<retirements[0],
      'Every actual child publication precedes retirement, including native same-field order')
 source=inspect.getsource(original.native_gate)
 for before,after in(('human=17','human=18'),('identities=(17,18)','identities=(18,18)')):
  need(source.count(before)==1,'Only true physical mirror identity differs in entire native source/geometry gate')
  source=source.replace(before,after,1)
 # The original observer keeps precisely max(recovery,retirement)+30. In
 # this branch retirement is later, with the last queued draw committed on
 # the following display field. Retain that complete original window; derive
 # its29 empty fields from actual DMA/publication and scanout, not a shortened
 # capture, guessed same-field clear or added idle fields solely for a count.
 before="    tail=[r for r in records if r['frame']>timeline['retirement']+1]\n    assert len(tail)>=30 and all(r['body']['3']['pixels']==0 for r in tail),'Complete actual post-retirement erase tail has no ring pixels'"
 after="""    last_child_dma=max(f for f,rows in by_draw.items()if any(q['slot']==3 for q in rows))
    assert last_child_dma<=timeline['retirement'], 'No child drawing issued after native retirement'
    committed=last_child_dma+1
    assert max(r['frame']for r in records if r['body']['3']['pixels']>0)==committed, 'Last visible child field binds its actual preceding native DMA'
    tail=[r for r in records if r['frame']>committed]
    assert [r['frame']for r in tail]==list(range(committed+1,timeline['lastScene']+1)) and tail and all(r['body']['3']['pixels']==0 for r in tail), 'Entire original recovery tail clears after the actual committed child draw'
""".rstrip()
 need(source.count(before)==1,'Only actual native publication/scanout retirement boundary replaces cross-branch idle-count assumption')
 source=source.replace(before,after,1)
 scope=dict(original.native_gate.__globals__,CASE=CASE)
 exec(compile(source,__file__+'::whole_original_native_Ring_FIFO_cache_projection_mirror','exec'),scope)
 register_scope=dict(registers.native_gate.__globals__,original=SimpleNamespace(native_gate=scope['native_gate']))
 exec(compile(inspect.getsource(registers.native_gate),__file__+'::whole_complete_DMA_register_binding','exec'),register_scope)
 return register_scope['native_gate'](groups,*args)


def shadow_gate(groups,buffers):
 source=inspect.getsource(original.shadow_gate)
 before='{(1,17),(2,18)}'
 need(source.count(before)==1,'Only actual two Sonya shadow identities differ')
 source=source.replace(before,'{(1,18),(2,18)}',1)
 scope=dict(original.shadow_gate.__globals__,CASE=CASE)
 exec(compile(source,__file__+'::whole_original_native_compressed_shadow_mirror','exec'),scope)
 return scope['shadow_gate'](groups,buffers)


def main(preflight=False):
 meta=json.loads((CASE/'result.json').read_text())
 timeline=meta['independentSemantics']['ring']['acceptedRings'][0]
 need(meta['passed'] and timeline['blocked'] and timeline['damage']==6 and timeline['victim']==18,
      'Actual current native Sonya mirror chip, never substituted Kano full hit')
 source=inspect.getsource(original.main)
 before='Path(__file__),Path(original.__file__),Path(shadows.__file__)'
 need(source.count(before)==1,'Pin every full source gate used by this successor')
 source=source.replace(before,'Path(__file__),Path(prior.__file__),Path(registers.__file__),Path(original.__file__),Path(shadows.__file__)',1)
 before='currentCPUFullRingHitRenderShadowAndEraseAccepted=True'
 need(source.count(before)==1,'Report the actual mirror-block branch, not full-hit acceptance')
 source=source.replace(before,'currentCPUBlockedMirrorRingRenderShadowAndEraseAccepted=True',1)
 before=" need(check(groups)==positive and shadow_gate(groups,buffers)==shadow,'Complete native positive restored after every actual fault')"
 after=""" child=groups['FLOOR_CHILD_SPAWN'][0]['actor']
 lines=text.splitlines()
 pubs=[i for i,s in enumerate(lines)if s.startswith('MK2_NAT_CAMPAIGN_FLOOR_ALL_QUEUE ')and capture.model.parse(s)[1]['actor']==child]
 dead=next(i for i,s in enumerate(lines)if s.startswith('MK2_NAT_CAMPAIGN_FLOOR_CHILD_RETIRE ')and capture.model.parse(s)[1]['actor']==child)
 bad=list(lines);pub=bad.pop(pubs[-1]);dead=next(i for i,s in enumerate(bad)if s.startswith('MK2_NAT_CAMPAIGN_FLOOR_CHILD_RETIRE '));bad.insert(dead+1,pub)
 changed='\\n'.join(bad)
 need(changed!=text,'Actual last publication reordered after same-field retirement')
 try:native_gate(groups,records,changed,guest,scene.payload,sequences['ring'],timeline)
 except(ValueError,AssertionError,KeyError)as error:rejected.append(dict(fault='child publication moved after same-field retirement',rejectedBy=str(error)))
 else:raise ValueError('Accepted actual same-field child retirement-order fault')
 need(check(groups)==positive and shadow_gate(groups,buffers)==shadow,'Complete native positive restored after every actual fault')
""".rstrip()
 need(source.count(before)==1,'Add real same-field ordering counterexample and retain every original fault/positive')
 source=source.replace(before,after,1)
 actual_capture=SimpleNamespace(**capture.__dict__,previous=capture.prior.previous)
 scope=dict(original.__dict__,__file__=__file__,OUT=OUT,CASE=CASE,capture=actual_capture,
            prior=original,registers=registers,native_gate=native_gate,shadow_gate=shadow_gate)
 exec(compile(inspect.getsource(original.observations),__file__+'::whole_original_hash_bound_GFX_observations','exec'),scope)
 exec(compile(source,__file__+'::whole_original_positive_and_actual_Ring_fault_matrix','exec'),scope)
 return scope['main'](preflight)


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');args=parser.parse_args()
 try:main(args.preflight)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if not args.preflight:OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
