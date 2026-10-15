"""Retain original full earned progression and owned uppercut gates."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_kano_kitana_close_guard.py').read_text().replace('kano_kitana_close_guard','kano_kitana_tight_punish')
exec(compile(code,__file__,'exec'),{'__file__':__file__})
