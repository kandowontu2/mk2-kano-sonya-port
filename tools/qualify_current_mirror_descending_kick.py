"""Preserve the earned identity/chronology gate for descending-kick successor."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_mirror_confirmed_jump.py').read_text()
for old,new in (('mirror_confirmed_jump','mirror_descending_kick'),('MIRROR_CONFIRMED_JUMP_ATTEMPT','MIRROR_DESCENDING_KICK_ATTEMPT')):
    assert old in code;code=code.replace(old,new)
exec(compile(code,__file__,'exec'),{'__file__':__file__})
