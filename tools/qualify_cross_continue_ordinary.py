"""Original18 state/raster counterexamples and complete current ordinary gate."""
import inspect
from pathlib import Path
import qualify_continue_viewport_v6614 as previous
import cross_continue_ordinary_contract as contract
ROOT,need,sha=contract.ROOT,contract.need,contract.sha
source=inspect.getsource(previous.qualify)
before='audit_v6615_continue_viewport_checked_';need(source.count(before)==1,'Fresh current proof, not historical runtime acceptance')
source=source.replace(before,'audit_cross_continue_ordinary_checked_',1)
source=source.replace('*contract.DEPENDENCIES,Path(__file__),','*contract.DEPENDENCIES,Path(__file__),Path(previous.__file__),',1)
scope=dict(vars(previous),__file__=__file__,previous=previous,contract=contract)
exec(compile(source,__file__+'::whole_original_current_native_fault_qualification','exec'),scope)
qualify=scope['qualify']
