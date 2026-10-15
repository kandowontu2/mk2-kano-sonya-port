"""Preserve the previous full lifetime gate, apply it to the opposite slots."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_stock_tomb_audio.py').read_text()
replacements={
 "(('kunglao','2','FFFE'),('jax_sonya_p2','3','FFFD'))":"(('sonya_p1_kitana','3','FFFD'),('kano_p2_subzero','2','FFFE'))",
 "audit_current_stock_tomb_audio_":"audit_current_stock_tomb_other_sides_audio_",
 "audit_current_native_tomb_stock_":"audit_current_stock_tomb_",
}
for old,new in replacements.items():
    assert old in source
    source=source.replace(old,new)
exec(compile(source,str(Path(__file__)), 'exec'))
