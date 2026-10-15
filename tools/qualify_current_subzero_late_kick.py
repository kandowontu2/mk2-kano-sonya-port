"""Same native chronology/identity gate; new timing policy, not assumed victory."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_subzero_release_jump.py').read_text()
source=source.replace('audit_current_sonya_p2_subzero_release_jump_runtime','audit_current_sonya_p2_subzero_late_kick_runtime')
source=source.replace('audit_current_subzero_release_jump_checked','audit_current_subzero_late_kick_checked')
old="if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue"
assert source.count(old)==1
source=source.replace(old,"if tag in ('AIR_TIMING','RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue")
exec(compile(source,__file__+'::native chronology','exec'))
