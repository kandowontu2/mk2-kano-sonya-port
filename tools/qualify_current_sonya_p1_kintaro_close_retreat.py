from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p1_boss_light.py').read_text()
source=source.replace('audit_current_sonya_p1_boss_light','audit_current_sonya_p1_kintaro_close_retreat')
exec(compile(source,__file__,'exec'))
