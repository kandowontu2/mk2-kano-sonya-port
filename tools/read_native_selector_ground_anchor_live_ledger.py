"""Fresh explicit-label successor; older observer failures remain immutable."""
from pathlib import Path
root=Path(__file__).resolve().parent.parent
source=(root/'tools/read_native_selector_ground_anchor_live.py').read_text()
source=source.replace('audit_native_selector_retained_ground_anchors_checked','audit_native_selector_retained_ground_anchors_ledger_checked')
source=source.replace('tools/read_native_selector_ground_anchor_remote.py','tools/read_native_selector_ground_anchor_remote_ledger.py')
exec(compile(source,__file__+'::explicit_remote_label_receiver','exec'))
