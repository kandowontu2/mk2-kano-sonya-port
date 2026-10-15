from pathlib import Path
code=Path(__file__).with_name('qualify_current_sonya_mirror_active_flag_guard.py').read_text().replace('sonya_mirror_active_flag_guard','sonya_mirror_standing_ready')
exec(compile(code,__file__,'exec'),{'__file__':__file__})
