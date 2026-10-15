"""Whole earned campaign gate and actual native close-upper ownership."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_kano_kitana_confirmed_jump.py').read_text().replace('kano_kitana_confirmed_jump','kano_kitana_close_guard')
code=code.replace("len(rows.get('KANO_KITANA_JUMP_ACCEPTED',[]))","len(rows.get('KANO_CLOSE_NATIVE_UPPER',[]))")
code=code.replace("exec(compile(code,__file__,'exec'),", "assert all(r['actor']==r['owner'] and r['id']=='17' for r in rows.get('KANO_CLOSE_NATIVE_UPPER',[]))\nexec(compile(code,__file__,'exec'),")
exec(compile(code,__file__,'exec'),{'__file__':__file__})
