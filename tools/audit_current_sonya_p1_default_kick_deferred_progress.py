from pathlib import Path
source=Path(__file__).with_name('audit_current_sonya_p1_deferred_observers_progress.py').read_text()
source=source.replace('audit_current_sonya_p1_kintaro_deferred_observers_runtime','audit_current_sonya_p1_default_kick_deferred_runtime').replace('audit_current_sonya_p1_deferred_observers_progress_checked','audit_current_sonya_p1_default_kick_deferred_progress_checked')
exec(compile(source,__file__,'exec'))
