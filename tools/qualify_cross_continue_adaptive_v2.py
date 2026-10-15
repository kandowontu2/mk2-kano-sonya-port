"""Source-exact original CPU damage fault predicate after context wrapping."""
from pathlib import Path
import qualify_cross_continue_adaptive as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
source=previous.source
before='contract.original.prior.loss_damage';need(source.count(before)==1,'Only actual original loss predicate namespace correction')
source=source.replace(before,'contract.original.original.prior.loss_damage',1)
source=source.replace('*contract.DEPENDENCIES,Path(__file__),','*contract.DEPENDENCIES,Path(__file__),ROOT/\'tools/qualify_cross_continue_adaptive.py\',',1)
scope=dict(previous.scope,__file__=__file__)
exec(compile(source,__file__+'::same_native_whole_original_loss_fault_predicate','exec'),scope)
qualify=scope['qualify']
