"""Whole existing earned progression gate; strategy success not presumed."""
from pathlib import Path
code = Path(__file__).with_name('qualify_current_kano_kitana_confirmed_jump.py').read_text().replace('kano_kitana_confirmed_jump', 'kano_kitana_standing_counter')
code = code.replace("len(rows.get('KANO_KITANA_JUMP_ACCEPTED',[]))", "len([r for r in rows.get('KANO_STANDING_ACTION',[]) if r['action']=='259'])")
exec(compile(code, __file__, 'exec'), {'__file__': __file__})
