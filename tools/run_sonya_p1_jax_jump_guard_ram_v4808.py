"""Whole4772 current P1 RAM pipeline; Kitana guard plus ordinary Jax evasion.

Original schedule/selection/continues/bosses/ending and all native game bytes
retained. Only physical controller and readonly native callback observations.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
text=(ROOT/'tools/run_current_p1_campaign_ram_v4772.py').read_text()
changes=[
 ('mk2ks_current_p1_campaign_ram_v4771.lua','mk2ks_sonya_p1_jax_jump_guard_ram_v4807.lua'),
 ('audit_v4774_current_p1_campaign_source_checked','audit_v4810_sonya_p1_jax_jump_guard_source_checked'),
 ('audit_v4775_{fighter}_current_p1_campaign_ram','audit_v4811_{fighter}_p1_jax_jump_guard_ram'),
 ('audit_v4775_{args.fighter}_current_p1_campaign_ram','audit_v4811_{args.fighter}_p1_jax_jump_guard_ram'),
 ('audit_v4776_{args.fighter}_current_p1_campaign_observed','audit_v4812_{args.fighter}_p1_jax_jump_guard_observed'),
 ('qualify_current_p1_campaign_source_v4773','qualify_sonya_p1_jax_jump_guard_source_v4809'),
 ('def capture(fighter):\n',"def capture(fighter):\n    need(fighter=='sonya','Only actual Sonya P1 Jax physical evasion')\n"),
 ("choices=('kano','sonya')","choices=('sonya',)")]
for before,after in changes:
    assert text.count(before)==1,before
    text=text.replace(before,after,1)
exec(compile(text,__file__+'::whole4772_only_Jax_physical_guard_and_unused_leaves','exec'),globals())
