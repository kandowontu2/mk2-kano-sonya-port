"""Reuse native chronology/identity gates; never assume controller success."""
from pathlib import Path
import qualify_current_sonya_reptile_uppercut_campaign as base

def main():
    code=Path(base.__file__).read_text().replace("'12000'","'20000'")
    code=code.replace('audit_current_sonya_reptile_uppercut_runtime','audit_current_sonya_reptile_reactive_runtime')
    code=code.replace('audit_current_sonya_reptile_uppercut_checked','audit_current_sonya_reptile_reactive_checked')
    code=code.replace('audit_current_sonya_reptile_uppercut_preparation/campaign.lua','audit_current_sonya_reptile_reactive_preparation/campaign.lua')
    code=code.replace('existing physical approach/crouch+HP uppercuts','existing physical reactive jumpkick approach')
    exec(compile(code,str(Path(base.__file__))+' [reactive20k]','exec'),{'__name__':'__main__'})

if __name__=='__main__':main()
