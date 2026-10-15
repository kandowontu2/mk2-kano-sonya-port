"""Same strict native/prefix gates for the observed-launch guard successor."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_kitana_ring_spacing.py').read_text()
source=source.replace('audit_current_sonya_p2_kitana_ring_spacing_runtime','audit_current_sonya_p2_kitana_projectile_guard_runtime')
source=source.replace('audit_current_sonya_p2_kitana_ring_spacing_checked','audit_current_sonya_p2_kitana_projectile_guard_checked')
source=source.replace("prior=load(root/'audit_current_sonya_p2_jax_standing_guard_runtime/run.log')", "prior=load(root/'audit_current_sonya_p2_kitana_ring_spacing_runtime/run.log')")
# Both experiments already contain the same passive Kitana context observers.
source=source.replace(" and t not in ('SONYA_KITANA_CPU_ACTION','SONYA_KITANA_DAMAGE')", '')
source=source.replace('One Kitana9-only physical policy.', 'One Kitana9-only observed-launch guard/recovered-ring physical policy. Exact shared passive context and all native/input prefix through104518 retained.')
exec(compile(source,__file__,'exec'))
