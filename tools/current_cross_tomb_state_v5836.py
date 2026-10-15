"""Original complete cross-character1731/3643 contract, not mirror admission."""
import hashlib,inspect
import native_tomb_drop_qualification_v3643 as native
import verify_tomb_mirror_contract_v4344 as original_faults
ROOT,need=native.ROOT,native.need
contract_source=native.source
drop_source=inspect.getsource(native.qualify_drop)
scope=native.scope
check_log=native.check_log
CONTRACT_SHA256=native.EXECUTED_CONTRACT_SHA256
DROP_SHA256=hashlib.sha256(drop_source.encode()).hexdigest().upper()
fault_source=inspect.getsource(original_faults.actual_faults)
fault_scope=dict(vars(original_faults),check_log=check_log)
exec(compile(fault_source,__file__+'::whole4344_real_faults_original_cross_contract','exec'),fault_scope)
actual_faults=fault_scope['actual_faults']
