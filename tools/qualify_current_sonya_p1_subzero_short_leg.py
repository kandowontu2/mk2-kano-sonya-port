from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p1_subzero_guard_release_leg.py').read_text()
source=source.replace('audit_current_sonya_p1_subzero_guard_release_leg','audit_current_sonya_p1_subzero_short_leg')
exec(compile(source,__file__,'exec'))
