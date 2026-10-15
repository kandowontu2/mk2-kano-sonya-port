"""Same full native CSS/transition gate for batched output, no weaker target."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_smoke_transition_scoped.py').read_text()
source=source.replace('audit_current_sonya_smoke_transition_scoped_checked','audit_current_sonya_smoke_transition_batched_checked')
old="exec(compile(source,__file__+'::original_gate_with_native_css_scope','exec'))"
assert source.count(old)==1
source=source.replace(old,"""source=source.replace('audit_current_sonya_smoke_transition_runtime','audit_current_sonya_smoke_transition_batched_runtime')
source=source.replace('audit_current_sonya_smoke_transition_preparation','audit_current_sonya_smoke_transition_batched_preparation')
exec(compile(source,__file__+'::same_full_batched_transition_gate','exec'))""")
exec(compile(source,__file__+'::same_scoped_native_return_gate','exec'))
