"""Complete original finite UI/state/fault gates on this current native run."""
import inspect
from pathlib import Path
import qualify_continue_viewport_v6614 as previous
import cross_continue_contract_v2 as contract
ROOT,need,sha=contract.ROOT,contract.need,contract.sha
source=inspect.getsource(previous.qualify)
before='audit_v6615_continue_viewport_checked_';need(source.count(before)==1,'Fresh current cross-character proof')
source=source.replace(before,'audit_cross_continue_checked_',1)
before='*contract.DEPENDENCIES,Path(__file__),';need(source.count(before)==1,'Whole original qualified source provenance')
source=source.replace(before,'*contract.DEPENDENCIES,Path(__file__),Path(previous.__file__),',1)
scope=dict(vars(previous),__file__=__file__,previous=previous,contract=contract)
exec(compile(source,__file__+'::whole_original_continue_UI_and_fault_qualification','exec'),scope)
qualify=scope['qualify']
