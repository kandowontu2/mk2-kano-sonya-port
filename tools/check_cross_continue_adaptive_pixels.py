"""Same terminal own ladder portrait and complete original extra pixel faults."""
from pathlib import Path
import check_cross_continue_ordinary_pixels as previous
import cross_continue_adaptive_contract as contract
ROOT,need,sha=contract.ROOT,contract.need,contract.sha
source=previous.source.replace('audit_cross_continue_ordinary_checked_','audit_cross_continue_adaptive_checked_',1).replace('audit_cross_continue_ordinary_pixels_','audit_cross_continue_adaptive_pixels_',1)
scope=dict(previous.scope,__file__=__file__,contract=contract,previous=previous.previous)
exec(compile(source,__file__+'::whole_original_own_portrait_and_pixel_faults','exec'),scope)
check=scope['check']
