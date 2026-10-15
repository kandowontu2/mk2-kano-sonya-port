"""Exclude new passive timing records from old opening scalar comparison."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_subzero_release_jump.py').read_text()
old="if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue"
assert source.count(old)==1
source=source.replace(old,"if tag in ('AIR_TIMING','RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue")
source=source.replace("'audit_current_subzero_release_jump_checked'","'audit_current_subzero_release_jump_observer_prefix_checked'")
exec(compile(source,__file__+'::passive observer prefix','exec'))
