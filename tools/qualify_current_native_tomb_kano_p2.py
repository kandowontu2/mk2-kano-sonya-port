"""Slot2 gate retains exact earned-damage/identity/scene/fault checks."""
from pathlib import Path
if __name__=='__main__':
    path=Path(__file__).with_name('qualify_current_native_tomb_case.py')
    code=path.read_text()
    replacements={
        "r['side']=='1'":"r['side']=='2'",
        'audit_current_native_tomb_kano_p1_runtime':'audit_current_native_tomb_kano_p2_runtime',
        'audit_current_native_tomb_kano_p1_checked':'audit_current_native_tomb_kano_p2_checked',
        'Current genuine KanoP1/SonyaP2':'Current genuine KanoP2/SonyaP1',
    }
    for old,new in replacements.items():
        assert old in code;code=code.replace(old,new)
    exec(compile(code,str(path)+' [Kano slot2]','exec'),{'__name__':'__main__','__file__':str(path)})
