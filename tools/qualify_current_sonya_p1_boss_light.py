from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p1_liukang_short_leg.py').read_text()
source=source.replace('audit_current_sonya_p1_liukang_short_leg','audit_current_sonya_p1_boss_light')
exec(compile(source,__file__,'exec'))
