"""Full4387 physical both-Down contract, actual opposite-character victim."""
import hashlib,inspect
import current_cross_tomb_state_v5836 as cross
import verify_pressed_tomb_mirror_contract_v4387 as original
import assemble_current_pressed_tomb_full_scene_v5831 as writer_faults
ROOT,need=cross.ROOT,cross.need
native=original.native

def once(code,before,after):
 need(code.count(before)==1,'Exactly declared whole pressed cross adaptation '+before)
 return code.replace(before,after,1)

qualifier_source=once(inspect.getsource(original.qualify_pressed_drop),
 "own=17 if fighter=='kano'else 18","own=18 if fighter=='kano'else 17")
qualifier_scope=dict(vars(original))
exec(compile(qualifier_source,__file__+'::whole4387_actual_opposite_victim','exec'),qualifier_scope)
qualify_pressed_drop=qualifier_scope['qualify_pressed_drop'];qualify_pressed_drop.source=qualifier_source
contract_source=once(cross.contract_source,'qualify_drop(log,fighter,side,arena,case,guest)',
 'qualify_pressed_drop(log,fighter,side,arena,case,guest)')
scope=dict(cross.scope,qualify_pressed_drop=qualify_pressed_drop)
exec(compile(contract_source,__file__+'::whole1731_original_cross_with_physical_pressed_branch','exec'),scope)
full_check_log=scope['check_log']
check_source=inspect.getsource(original.check_log)
check_scope=dict(vars(original),full_check_log=full_check_log,qualify_pressed_drop=qualify_pressed_drop)
exec(compile(check_source,__file__+'::whole4387_full_earned_plus_pressed_admission','exec'),check_scope)
check_log=check_scope['check_log']
fault_source=original.fault_source
fault_scope=dict(original.fault_scope,check_log=check_log)
exec(compile(fault_source,__file__+'::whole4344_actual_earned_cross_faults','exec'),fault_scope)
actual_faults=fault_scope['actual_faults']
phase_fault_source=inspect.getsource(original.pressed_phase_faults)
phase_scope=dict(vars(original),qualify_pressed_drop=qualify_pressed_drop)
exec(compile(phase_fault_source,__file__+'::whole4387_actual269phase_faults','exec'),phase_scope)
pressed_phase_faults=phase_scope['pressed_phase_faults']
source_fault_source=inspect.getsource(writer_faults.actual_pressed_source_faults)
need(source_fault_source.count('runtime.native.qualify_pressed_drop')==3,'All original source/writer fault admission callsites retained')
source_fault_source=source_fault_source.replace('runtime.native.qualify_pressed_drop','qualify_pressed_drop')
source_fault_scope=dict(vars(writer_faults),qualify_pressed_drop=qualify_pressed_drop)
exec(compile(source_fault_source,__file__+'::whole5831_actual_source_writer_faults','exec'),source_fault_scope)
source_faults=source_fault_scope['actual_pressed_source_faults']
CONTRACT_SHA256=hashlib.sha256(contract_source.encode()).hexdigest().upper()
QUALIFIER_SHA256=hashlib.sha256(qualifier_source.encode()).hexdigest().upper()
