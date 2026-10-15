"""Same event-window classifier, no new runtime or parser assumptions."""
from pathlib import Path
code=Path(__file__).with_name('classify_current_sonya_mirror_counter_readiness.py').read_text().replace('sonya_mirror_standing_counter_runtime','sonya_mirror_neutral_recovery_runtime').replace('audit_current_sonya_mirror_counter_readiness','audit_current_sonya_mirror_neutral_recovery_readiness')
exec(compile(code,__file__,'exec'),{'__file__':__file__})
