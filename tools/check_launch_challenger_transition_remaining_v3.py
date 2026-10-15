"""Correct a checker alias shadowed by its own local faults list."""
import inspect,json,types
from pathlib import Path
import qualify_launch_challenger_transition_remaining_v2 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha

def check(c):
 need(c['move']=='square'and c['side']==2,'Exact already-qualified Sonya P2 capture')
 out=ROOT/'audit_launch_challenger_transition_fault_alias_rejection_square_p2';need(not out.exists(),'Retain actual original checker alias error')
 out.mkdir();(out/'failure.json').write_text(json.dumps(dict(passed=False,nativeGameFailure=False,nativeTerminal=c['terminal'],error="AttributeError: 'list' object has no attribute '__file__'",executedSourceSHA256=sha(previous.__file__),newNativeBoots=0),indent=2)+'\n')
 source=inspect.getsource(previous.faults.check)
 before="lambda r:tag!='MK2_MAUDIO_SOUND'or r['pc']=='FFA13C90'";need(source.count(before)==1,'Whole existing packet-fault correction')
 source=source.replace(before,"lambda r:(tag!='MK2_MAUDIO_SOUND'or r['pc']=='FFA13C90')and r.get(key)!=value",1)
 before='Path(__file__),Path(mutations.__file__),';need(source.count(before)==1,'Unshadowed actual source pin alias')
 source=source.replace(before,'Path(__file__),Path(previous.__file__),Path(fault_module.__file__),Path(mutations.__file__),',1)
 scope=dict(vars(previous.faults),__file__=__file__,previous=previous,fault_module=previous.faults,model=types.SimpleNamespace(**dict(vars(previous.original),physical_inventory=previous.physical_inventory)))
 exec(compile(source,__file__+'::same_terminal_unshadowed_fault_source_pins','exec'),scope)
 return scope['check'](c)
