"""Correct stock-interval scope, retain executed broad-kernel rejection.

Entire current guest remains independently reconstructed. Explicit original
air-kick and observed HP-writer intervals are compared in full; other port
relocations are not falsely claimed stock-identical or silently excluded.
"""
import inspect
import qualify_launch_jump_interruption_v6696 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
before="""lo=(0xff830000-0xff800000)//8;hi=(0xff880000-0xff800000)//8
  need(guest[lo:hi]==stock[lo:hi],'Entire original collision, movement, hurt and stock attack kernel remains unchanged')"""
after="""for a,z in((0xff871d00,0xff872700),(0xff836640,0xff836720)):
   lo=(a-0xff800000)//8;hi=(z-0xff800000)//8
   need(guest[lo:hi]==stock[lo:hi],'Entire explicit original air-kick or actual health-writer source interval unchanged')
  need(guest==current.expected(),'Every other actual guest byte matches independent current port reconstruction, including legitimate relocations')"""
need(original.code.count(before)==1,'Only erroneous broad stock-identical interval changed; full current guest gate retained')
code=original.code.replace(before,after,1)
scope=dict(vars(original.previous_model))
exec(compile(code,__file__+'::whole_jump_phase_explicit_native_kernel_scope','exec'),scope)
model=original.Model();model.__dict__.update(original.model.__dict__);model.phase=scope['phase']
source=original.source
before='Path(__file__),Path(original.__file__),Path(model.__file__)'
after="Path(__file__),Path(original.__file__),ROOT/'tools/qualify_launch_interruption_v6691.py',ROOT/'audit_v6698_jump_kernel_scope_rejection/failure.json',Path(model.__file__)"
need(source.count(before)==1,'Both actual executed qualifiers and preserved kernel-scope failure pinned')
source=source.replace(before,after,1)
scope=dict(vars(original.original),__file__=__file__,original=original,model=model,inputs=original.inputs)
exec(compile(source,__file__+'::whole_same_RAM_jump_proof_correct_stock_scope','exec'),scope)
qualify=scope['qualify']
