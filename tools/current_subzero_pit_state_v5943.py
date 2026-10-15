"""Full1731/3643 own performer gates with explicitly selected real Sub-Zero8.

Pit only. No proxy or generic victim admission: all own17/18, stock8, full
health/paid selection/command/action/801fields/retirement gates stay intact.
All original12actual state/identity/input/action faults remain mandatory.
"""
import hashlib
import current_cross_pit_earned_state_v5893 as original
ROOT,need=original.ROOT,original.need
native=original.native
contract_source=original.contract_source
before='victim = 18 if own == 17 else 17'
need(contract_source.count(before)==1,'One exact opponent expectation, not any own ID or action change')
contract_source=contract_source.replace(before,"victim = 8\n    need(arena==6 and case=='positive','Explicit physically selected original Sub-Zero8 Pit context only')",1)
scope=dict(original.check_log.__globals__)
exec(compile(contract_source,__file__+'::whole1731_3643_real_SubZero8_Pit_opponent','exec'),scope)
check_log=scope['check_log']
CONTRACT_SHA256=hashlib.sha256(contract_source.encode()).hexdigest().upper()
fault_source=original.fault_source
fault_scope=dict(original.actual_faults.__globals__,check_log=check_log)
exec(compile(fault_source,__file__+'::whole12actual_Pit_earned_identity_command_cleanup_faults','exec'),fault_scope)
actual_faults=fault_scope['actual_faults']
FAULT_SHA256=hashlib.sha256(fault_source.encode()).hexdigest().upper()
