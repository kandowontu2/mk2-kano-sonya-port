"""Whole5725 hardware proof with original P2 validation namespace bound.

The original model exposes context validation through its qualified parent,
not through the P1 adapter's convenience alias. No native ledger gate changes.
"""
from pathlib import Path
import current_payload_metadata_context_v5229 as current

old=current.ROOT/'tools/verify_current_p2_native_ending_hardware_v5725.py'
source=old.read_text()
for before,after in [('validate_context=p1.validate_context',
                      'validate_context=p1.previous.previous.validate_context'),
                     ('audit_v5726_','audit_v5728_')]:
 current.need(source.count(before)==1,'Whole actual P2 ledger namespace binding '+before)
 source=source.replace(before,after,1)
exec(compile(source,__file__+'::whole_original_P2_hardware_validator','exec'),globals())
