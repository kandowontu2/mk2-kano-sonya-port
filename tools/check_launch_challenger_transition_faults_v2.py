"""Use an actually different packet byte in the retained Sonya capture."""
import inspect,json
from pathlib import Path
import check_launch_challenger_transition_faults as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha

def check(c):
 out=ROOT/f"audit_launch_challenger_transition_vacuous_fault_rejection_{c['move']}_p{c['side']}"
 need(not out.exists(),'Fresh original nonvacuous-fault rejection receipt')
 out.mkdir();(out/'failure.json').write_text(json.dumps(dict(passed=False,nativeGameFailure=False,nativeTerminal=c['terminal'],error='Actually changed real evidence, no vacuous mutation',executedSource=str(Path(previous.__file__).resolve()),executedSourceSHA256=sha(previous.__file__),newNativeBoots=0),indent=2)+'\n')
 source=inspect.getsource(previous.check)
 before="lambda r:tag!='MK2_MAUDIO_SOUND'or r['pc']=='FFA13C90'"
 need(source.count(before)==1,'Only choose a native packet row with a different original value')
 source=source.replace(before,"lambda r:(tag!='MK2_MAUDIO_SOUND'or r['pc']=='FFA13C90')and r.get(key)!=value",1)
 before='Path(__file__),Path(mutations.__file__),'
 need(source.count(before)==1,'Retain executed original and corrected fault sources')
 source=source.replace(before,'Path(__file__),Path(previous.__file__),Path(mutations.__file__),',1)
 scope=dict(vars(previous),__file__=__file__,previous=previous)
 exec(compile(source,__file__+'::same_capture_nonvacuous_packet_faults','exec'),scope)
 return scope['check'](c)
