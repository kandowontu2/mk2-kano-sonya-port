from pathlib import Path
source=Path(__file__).with_name('audit_current_sonya_p1_kintaro_close_retreat_progress.py').read_text()
source=source.replace('audit_current_sonya_p1_kintaro_close_retreat_runtime','audit_current_sonya_p1_kintaro_attack_guard_runtime').replace('audit_current_sonya_p1_kintaro_close_retreat_progress_checked','audit_current_sonya_p1_kintaro_attack_guard_progress_checked')
exec(compile(source,__file__,'exec'))
