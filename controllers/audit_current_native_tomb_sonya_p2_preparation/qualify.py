"""Reciprocal Sonya gate retains complete earned/scene/fault checks."""
from pathlib import Path

if __name__=='__main__':
    path=Path(r'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port\tools\qualify_current_native_tomb_case.py')
    code=path.read_text()
    replacements={
        "r['side']=='1'":"r['side']=='2'",
        "r['winner']=='kano'":"r['winner']=='sonya'",
        "'17,18'":"'18,17'",
        "=='17'":"=='TEMP_OWN'",
        "=='18'":"=='17'",
        "=='TEMP_OWN'":"=='18'",
        'audit_current_native_tomb_kano_p1_runtime':'audit_current_native_tomb_sonya_p2_runtime',
        'audit_current_native_tomb_kano_p1_checked':'audit_current_native_tomb_sonya_p2_checked',
        'Proxy Kano accepted':'Proxy Sonya accepted',
        'Current genuine KanoP1/SonyaP2':'Current genuine SonyaP2/KanoP1',
    }
    for old,new in replacements.items():
        assert old in code
        code=code.replace(old,new)
    exec(compile(code,str(path)+' [reciprocal Sonya]','exec'),{'__name__':'__main__','__file__':str(path)})
