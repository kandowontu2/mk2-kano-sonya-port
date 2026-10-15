"""Preserve native-contact and actual round-win gate for the new observed case."""
from pathlib import Path
code=Path(__file__).with_name('classify_current_sonya_mirror_standing_counter.py').read_text().replace('sonya_mirror_standing_counter','sonya_mirror_neutral_recovery')
code=code.replace("'19008'","'19239'").replace("'28,0'","'8,0'")
exec(compile(code,__file__,'exec'),{'__file__':__file__})
