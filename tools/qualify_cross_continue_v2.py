"""Same terminal qualification; preserve original parser-namespace rejection."""
import inspect
from pathlib import Path
import qualify_continue_viewport_v6614 as previous
import cross_continue_contract_v3 as contract
ROOT,need,sha=contract.ROOT,contract.need,contract.sha
source=inspect.getsource(previous.qualify)
source=source.replace('audit_v6615_continue_viewport_checked_','audit_cross_continue_checked_',1)
source=source.replace('*contract.DEPENDENCIES,Path(__file__),','*contract.DEPENDENCIES,Path(__file__),Path(previous.__file__),ROOT/\'tools/qualify_cross_continue.py\',',1)
scope=dict(vars(previous),__file__=__file__,previous=previous,contract=contract)
exec(compile(source,__file__+'::same_native_whole_contract_correct_SC_namespace','exec'),scope)
qualify=scope['qualify']
