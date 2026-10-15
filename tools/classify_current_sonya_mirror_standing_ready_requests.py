"""Did waiting for standing remove actual blocked high-kick requests?"""
from pathlib import Path
code=Path(__file__).with_name('classify_current_sonya_mirror_counter_readiness.py').read_text()
code=code.replace('audit_current_sonya_mirror_standing_counter_runtime','audit_current_sonya_mirror_standing_ready_runtime')
code=code.replace('audit_current_sonya_mirror_counter_readiness','audit_current_sonya_mirror_standing_ready_requests')
exec(compile(code,__file__,'exec'),{'__file__':__file__})
