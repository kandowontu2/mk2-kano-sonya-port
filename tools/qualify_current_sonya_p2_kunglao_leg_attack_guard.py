"""Check native campaign results, not merely controller execution."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_kunglao_verified_leg.py').read_text().replace('audit_current_sonya_p2_kunglao_verified_leg','audit_current_sonya_p2_kunglao_leg_attack_guard')
source=source.replace('branch=original[start:end];assert current.count(branch)==1',"branch=original[start:end].replace('safe=safe and other.flags&0x0c==0','safe=safe and other.flags&0x1c==0');assert current.count(branch)==1")
source=source.replace('exactCurrentP1PhysicalPolicyReused=True','currentP1PolicyWithAttackFlagGuard=True')
exec(compile(source,__file__+'::native_context','exec'))
