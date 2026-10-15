"""Complete1731/3643 cross earned contract; actual Pit12faults, no new admission.
Seven full-health two-KO matches, paid rematches, native own command/action,
801 consecutive states and1100cleanup remain mandatory. No visual/audio claim.
"""
import hashlib,inspect
import current_cross_tomb_state_v5836 as original
ROOT,need=original.ROOT,original.need
native=original.native
contract_source=original.contract_source
check_log=original.check_log
CONTRACT_SHA256=original.CONTRACT_SHA256
fault_source=original.fault_source
needle="check_log('\\n'.join(altered)+'\\n',fighter,side,1,guest=guest)"
need(fault_source.count(needle)==2,'Both entire original earned state counterexample gate calls')
fault_source=fault_source.replace(needle,needle.replace('side,1,','side,6,'),2)
need(fault_source.count("'FF8BDFE0'")==1,'One original native action omission target')
fault_source=fault_source.replace("'FF8BDFE0'","'FF8BDDE0'",1)
fault_scope=dict(vars(original.original_faults),check_log=check_log)
exec(compile(fault_source,__file__+'::whole4344_actual_Pit_earned_faults','exec'),fault_scope)
actual_faults=fault_scope['actual_faults']
FAULT_SHA256=hashlib.sha256(fault_source.encode()).hexdigest().upper()
