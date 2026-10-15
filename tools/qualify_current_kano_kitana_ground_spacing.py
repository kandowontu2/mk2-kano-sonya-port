"""Same full earned route/identity gate, distinct physical ground-spacing policy."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_kano_kitana_confirmed_jump.py').read_text().replace('kano_kitana_confirmed_jump','kano_kitana_ground_spacing')
code=code.replace("len(rows.get('KANO_KITANA_JUMP_ACCEPTED',[]))","len(rows.get('KANO_KITANA_SPACING_KNIFE',[]))")
exec(compile(code,__file__,'exec'),{'__file__':__file__})
