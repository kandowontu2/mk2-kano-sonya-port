"""Native STAGE/FIGHT may be published in the same callback field."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_kano_kitana_match_advance.py').read_text()
before="assert int(arrival['frame'])<int(fight['frame'])"
assert code.count(before)==1
code=code.replace(before,"assert int(arrival['frame'])<=int(fight['frame'])")
code=code.replace('audit_current_kano_kitana_match_advance_checked','audit_current_kano_kitana_match_advance_samefield_checked')
exec(compile(code,__file__,'exec'),{'__file__':__file__})
