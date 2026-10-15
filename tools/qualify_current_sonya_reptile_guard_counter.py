"""Bounded guarded-counter native chronology without an assumed clear."""
from pathlib import Path
import qualify_current_sonya_reptile_uppercut_campaign as base

def main():
    code=Path(base.__file__).read_text().replace("'12000'","'20000'")
    for suffix in ('runtime','checked'):
        code=code.replace('audit_current_sonya_reptile_uppercut_'+suffix,'audit_current_sonya_reptile_guard_counter_'+suffix)
    code=code.replace('audit_current_sonya_reptile_uppercut_preparation/campaign.lua','audit_current_sonya_reptile_guard_counter_preparation/campaign.lua')
    code=code.replace('existing physical approach/crouch+HP uppercuts','physical crouch-block and released-Block Down9/HP6..8 counters')
    exec(compile(code,str(Path(base.__file__))+' [guarded counter]','exec'),{'__name__':'__main__'})

if __name__=='__main__':main()
