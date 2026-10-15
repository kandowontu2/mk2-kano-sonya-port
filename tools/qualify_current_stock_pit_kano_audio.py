"""Actual KanoP2 winner lifetime, same gate as Sonya counterpart."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_stock_pit_sonya_audio.py').read_text()
old="(('sonya_p1_kitana','3','FFFD'),)"
assert code.count(old)==1
code=code.replace(old,"(('kano_p2_subzero','2','FFFE'),)")
code=code.replace('audit_current_stock_pit_sonya_audio_checked','audit_current_stock_pit_kano_audio_checked')
exec(compile(code,__file__,'exec'))
