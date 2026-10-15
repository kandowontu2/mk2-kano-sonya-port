"""Bounded actual diagnostic, not waived all-state anchoring acceptance."""
from pathlib import Path
root=Path(__file__).resolve().parent.parent
source=(root/'tools/read_native_selector_ground_anchor_live.py').read_text()
source=source.replace('audit_native_selector_retained_ground_anchors_checked','audit_native_selector_retained_ground_anchors_diagnostic')
source=source.replace('tools/read_native_selector_ground_anchor_remote.py','tools/read_native_selector_ground_anchor_remote_diagnostic.py')
exec(compile(source,__file__+'::actual_exception_receiver','exec'))
