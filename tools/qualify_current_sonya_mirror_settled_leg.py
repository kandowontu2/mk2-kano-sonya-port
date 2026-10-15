"""Retain the same chronology and owned native entry gate for the leg successor."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_sonya_mirror_prepared_uppercut.py').read_text()
for old,new in (('mirror_prepared_uppercut','mirror_settled_leg'),('MIRROR_PREPARED_UPPERCUT_ATTEMPT','MIRROR_SETTLED_LEG_ATTEMPT'),('MIRROR_NATIVE_UPPERCUT','MIRROR_NATIVE_LEG'),('preparedUppercutRequests','settledLegRequests'),('nativeUppercutEntries','nativeLegEntries')):
    assert old in code
    code=code.replace(old,new)
exec(compile(code,__file__,'exec'),{'__file__':__file__})
