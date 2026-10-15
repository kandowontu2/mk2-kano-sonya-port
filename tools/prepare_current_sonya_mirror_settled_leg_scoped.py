"""Fix the preflight false positive on inert discard_snapshot calls."""
from pathlib import Path
code=Path(__file__).with_name('prepare_current_sonya_mirror_settled_leg.py').read_text()
old="assert ':write_' not in source and 'snapshot(' not in source"
assert code.count(old)==1
code=code.replace(old,"assert ':write_' not in source and ':snapshot(' not in source")
exec(compile(code,__file__,'exec'))
