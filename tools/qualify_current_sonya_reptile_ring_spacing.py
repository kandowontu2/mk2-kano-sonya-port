"""Keep unchanged Baraka and health-qualified natural advancement checks."""
from pathlib import Path
import qualify_current_sonya_reptile_uppercut_campaign as base

def main():
    code=Path(base.__file__).read_text().replace("'12000'","'20000'")
    code=code.replace('audit_current_sonya_reptile_uppercut_runtime','audit_current_sonya_reptile_ring_spacing_runtime')
    code=code.replace('audit_current_sonya_reptile_uppercut_checked','audit_current_sonya_reptile_ring_spacing_checked')
    code=code.replace('audit_current_sonya_reptile_uppercut_preparation/campaign.lua','audit_current_sonya_reptile_ring_spacing_preparation/campaign.lua')
    code=code.replace('existing physical approach/crouch+HP uppercuts','historical physical D,F,LP ring and early back-jump retry spacing')
    exec(compile(code,str(Path(base.__file__))+' [ring spacing20k]','exec'),{'__name__':'__main__'})

if __name__=='__main__':main()
