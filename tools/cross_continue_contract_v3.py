"""Keep original SC row parser when reconstructing the full native loss gate."""
from pathlib import Path
import continue_viewport_contract_v6610 as original
import kano_ball_launch_context_v6642 as current
ROOT,need,sha=original.ROOT,original.need,original.sha
source=(ROOT/'tools/cross_continue_contract_v2.py').read_text()
before='scope=dict(original.namespace,origin=original.original.prior.current.origin,model=original.model)'
after='scope=dict(original.original.prior.current.executed.prior.original.__dict__,origin=original.original.prior.current.origin,model=original.model)'
need(source.count(before)==1,'Exact actual base parser namespace correction; no native replay')
source=source.replace(before,after,1)
exec(compile(source,__file__+'::whole_original_SC_parser_and_contract','exec'),globals())
DEPENDENCIES=[*DEPENDENCIES,ROOT/'tools/cross_continue_contract_v2.py']
