"""Original collision stores may publish unchanged HP; they are not damage.

Retain every store, full native opcode interval and complete health ledger.
This is the same distinction made by verify_morph_adversity_v3235, not a new
health mutation or a claim that a non-damaging store was a hit.
"""
import inspect,json,types
from pathlib import Path
import qualify_launch_challenger_transition_remaining as previous
original,corrected,faults=previous.original,previous.corrected,previous.faults
ROOT,need,sha=original.ROOT,original.need,original.sha

def physical_inventory(c):
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();a=(0xff836650-0xff800000)//8;b=(0xff836750-0xff800000)//8
 need(c['guest'][a:b]==stock[a:b],'Whole original collision arithmetic and HP-store interval, before relocated callback table operand')
 source=inspect.getsource(original.physical_inventory)
 before="0<=after<before<=161,'Actual native collision damage and saturation'"
 need(source.count(before)==1,'Exact original full health store contract distinguishes no-damage stores')
 source=source.replace(before,"0<=after<=before<=161,'Original native collision HP store: non-increasing, including unchanged HP'",1)
 scope=dict(vars(original));exec(compile(source,__file__+'::whole_native_health_ledger_including_no_damage_stores','exec'),scope)
 proof,by=scope['physical_inventory'](c)
 writes=[r for r in original.rows(c['text'],'MK2_INTERRUPT_HEALTH')if r['pc']=='FF836700']
 proof['actualDamagingCollisionStores']=sum(r['before']!=r['after']for r in writes)
 proof['actualNonDamagingCollisionStores']=[r for r in writes if r['before']==r['after']]
 return proof,by

def qualify(c):
 need(c['side']==2,'Remaining player-two contexts')
 try:original.physical_inventory(c)
 except ValueError as error:
  need(str(error)=='Actual native collision damage and saturation','Exact strict-damage checker rejection, not another ignored failure')
  out=ROOT/f"audit_launch_challenger_transition_no_damage_store_rejection_{c['move']}_p2";need(not out.exists(),'Retain original actual checker failure')
  out.mkdir();(out/'failure.json').write_text(json.dumps(dict(passed=False,nativeGameFailure=False,nativeTerminal=c['terminal'],error=str(error),executedSource=str(Path(previous.__file__).resolve()),executedSourceSHA256=sha(previous.__file__),originalPhysicalSourceSHA256=sha(original.__file__),newNativeBoots=0),indent=2)+'\n')
 source=inspect.getsource(original.qualify)
 before='for p in(Path(__file__),Path(prior.__file__),'
 need(source.count(before)==1,'Full original qualifier with actual corrected source pins')
 source=source.replace(before,'for p in(Path(__file__),Path(previous.__file__),Path(original.__file__),Path(corrected.__file__),Path(prior.__file__),',1)
 scope=dict(vars(original),__file__=__file__,previous=previous,original=original,corrected=corrected,packet_gate=corrected.packet_gate,physical_inventory=physical_inventory)
 exec(compile(source,__file__+'::whole_source_bound_same_terminal_qualification','exec'),scope)
 return scope['qualify'](c)

def check(c):
 source=inspect.getsource(faults.check)
 before="lambda r:tag!='MK2_MAUDIO_SOUND'or r['pc']=='FFA13C90'"
 need(source.count(before)==1,'Existing nonvacuous packet byte correction')
 source=source.replace(before,"lambda r:(tag!='MK2_MAUDIO_SOUND'or r['pc']=='FFA13C90')and r.get(key)!=value",1)
 before='Path(__file__),Path(mutations.__file__),'
 need(source.count(before)==1,'Pin whole executed fault model and original source')
 source=source.replace(before,'Path(__file__),Path(previous.__file__),Path(faults.__file__),Path(corrected.__file__),Path(mutations.__file__),',1)
 scope=dict(vars(faults),__file__=__file__,previous=previous,faults=faults,corrected=corrected,model=types.SimpleNamespace(**dict(vars(original),physical_inventory=physical_inventory)))
 exec(compile(source,__file__+'::same_capture_actual_counterexamples','exec'),scope)
 return scope['check'](c)
