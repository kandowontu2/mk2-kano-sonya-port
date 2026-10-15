"""Reuse identity, earned chronology, terminal/cap gates for actual mirror route."""
from pathlib import Path
import qualify_current_sonya_p2_native_start_campaign as base

if __name__=='__main__':
    code=Path(base.__file__).read_text()
    for suffix in ('runtime','checked'):
        code=code.replace('audit_current_sonya_p2_native_start_'+suffix,'audit_current_sonya_p2_mirror_guard_'+suffix)
    code=code.replace('audit_current_sonya_p2_native_start_preparation/campaign.lua','audit_current_sonya_p2_mirror_guard_preparation/campaign.lua')
    code=code.replace('existing leg-grab controls','historical mirror physical guard/released-Block leg sequence; existing leg controls elsewhere')
    exec(compile(code,__file__+'::mirror guarded','exec'),{'__name__':'__main__','gate':base.gate})
