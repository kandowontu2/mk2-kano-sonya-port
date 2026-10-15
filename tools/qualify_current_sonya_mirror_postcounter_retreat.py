from pathlib import Path
code=Path(__file__).with_name('qualify_current_sonya_mirror_standing_counter.py').read_text().replace('sonya_mirror_standing_counter','sonya_mirror_postcounter_retreat')
exec(compile(code,__file__,'exec'),{'__file__':__file__})
