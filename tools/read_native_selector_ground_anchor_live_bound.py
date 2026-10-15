"""Preserve first passive observer namespace failure; use fresh bound ledger."""
from pathlib import Path
root=Path(__file__).resolve().parent.parent
source=(root/'tools/read_native_selector_ground_anchor_live.py').read_text()
for old,new in (
    ('audit_native_selector_retained_ground_anchors_checked','audit_native_selector_retained_ground_anchors_bound_checked'),
    ('tools/read_native_selector_ground_anchor_remote.py','tools/read_native_selector_ground_anchor_remote_bound.py'),
):
    assert source.count(old)>=1
    source=source.replace(old,new)
exec(compile(source,__file__+'::actual_retained_ledger_receiver','exec'))
