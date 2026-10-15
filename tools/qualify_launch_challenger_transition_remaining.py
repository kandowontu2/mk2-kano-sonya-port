"""Apply the corrected whole contract to previously unstarted P2 cases."""
import inspect
import qualify_launch_challenger_transition as original
import qualify_launch_challenger_transition_v2 as corrected
import check_launch_challenger_transition_faults as faults
ROOT,need,sha=original.ROOT,original.need,original.sha

def qualify(c):
 need(c['side']==2,'Remaining native player-two contexts only')
 source=inspect.getsource(original.qualify)
 before='for p in(Path(__file__),Path(prior.__file__),'
 need(source.count(before)==1,'Retain original and corrected entire qualifier source pins')
 source=source.replace(before,'for p in(Path(__file__),Path(original.__file__),Path(corrected.__file__),Path(prior.__file__),',1)
 scope=dict(vars(original),__file__=__file__,original=original,corrected=corrected,packet_gate=corrected.packet_gate)
 exec(compile(source,__file__+'::whole_corrected_same_terminal_qualification','exec'),scope)
 return scope['qualify'](c)

def check(c):
 need(c['side']==2,'Remaining native player-two contexts only')
 source=inspect.getsource(faults.check)
 before="lambda r:tag!='MK2_MAUDIO_SOUND'or r['pc']=='FFA13C90'"
 need(source.count(before)==1,'Previously fixed nonvacuous native packet row selection')
 source=source.replace(before,"lambda r:(tag!='MK2_MAUDIO_SOUND'or r['pc']=='FFA13C90')and r.get(key)!=value",1)
 before='Path(__file__),Path(mutations.__file__),'
 need(source.count(before)==1,'All actually executed whole semantic checker sources')
 source=source.replace(before,'Path(__file__),Path(faults.__file__),Path(corrected.__file__),Path(mutations.__file__),',1)
 scope=dict(vars(faults),__file__=__file__,faults=faults,corrected=corrected)
 exec(compile(source,__file__+'::whole_same_terminal_actual_fault_checks','exec'),scope)
 return scope['check'](c)
