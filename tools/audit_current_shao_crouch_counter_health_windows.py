"""Same native health/cue scope on crouching-guard trial."""
from pathlib import Path
source=Path(__file__).with_name('audit_current_shao_counter_health_windows.py').read_text()
source=source.replace('audit_current_kano_p2_shao_charge_settled_counter_runtime','audit_current_kano_p2_shao_crouch_charge_counter_runtime').replace('audit_current_shao_counter_health_windows_checked','audit_current_shao_crouch_counter_health_windows_checked').replace('len(windows)==46','len(windows)==134')
exec(compile(source,__file__+'::crouch_guard_health_windows','exec'))
