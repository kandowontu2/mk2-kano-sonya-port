"""Same bounded pending-continue observation gate; own native uppercut instead of HK."""
from pathlib import Path
code=Path(__file__).with_name('classify_current_kano_kunglao_spacing_counter.py').read_text()
code=code.replace('kano_kunglao_spacing_counter','kano_kunglao_crouch_counter')
code=code.replace("'259'","'263'")
code=code.replace('nativeStandingKickStarts','nativeUppercutStarts').replace('nativeOwnKickContacts','nativeOwnUppercutContacts').replace('standingKicks','uppercuts')
code=code.replace('23784','23710')
exec(compile(code,__file__,'exec'),{'__file__':__file__})
