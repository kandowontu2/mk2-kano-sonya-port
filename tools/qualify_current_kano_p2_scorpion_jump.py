"""Retain native campaign gate, prior prefix and actual Scorpion outcomes."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_scorpion_standing.py').read_text()
source=source.replace('audit_current_kano_p2_scorpion_standing','audit_current_kano_p2_scorpion_jump')
# The extra stage6 damage observer cannot affect the prior prefix but is absent in baseline.
source=source.replace("('HOST_BOUND','RESULT')","('HOST_BOUND','RESULT','KANO_P2_SCORPION_DAMAGE')")
exec(compile(source,__file__+'::native_campaign_gate','exec'))
