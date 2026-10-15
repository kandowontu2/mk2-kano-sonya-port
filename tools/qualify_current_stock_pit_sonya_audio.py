"""Retain actual winner sample lifetime gate and neutral-observer comparison."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_stock_tomb_audio.py').read_text()
changes={
 "(('kunglao','2','FFFE'),('jax_sonya_p2','3','FFFD'))":"(('sonya_p1_kitana','3','FFFD'),)",
 'audit_current_stock_tomb_audio_':'audit_current_stock_pit_other_sides_audio_',
 'audit_current_native_tomb_stock_':'audit_current_stock_pit_initialized_selector_',
}
for old,new in changes.items():
    assert old in code;code=code.replace(old,new)
code=code.replace('audit_current_stock_pit_other_sides_audio_checked','audit_current_stock_pit_sonya_audio_checked')
exec(compile(code,__file__,'exec'))
