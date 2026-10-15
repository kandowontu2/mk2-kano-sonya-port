"""Whole4772 RAM capture with only a new Sonya/Kitana physical controller.

No native AI, difficulty, state, identity, health, schedule or RNG writes.
Retains complete initialized-guest and all six RAM image sinks; no new build.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
text=(ROOT/'tools/run_current_p1_campaign_ram_v4772.py').read_text()
changes=[
 ('mk2ks_current_p1_campaign_ram_v4771.lua','mk2ks_sonya_p1_kitana_guard_ram_v4793.lua'),
 ('audit_v4774_current_p1_campaign_source_checked','audit_v4796_sonya_p1_kitana_guard_source_checked'),
 ('audit_v4775_{fighter}_current_p1_campaign_ram','audit_v4797_{fighter}_p1_kitana_guard_ram'),
 ('audit_v4775_{args.fighter}_current_p1_campaign_ram','audit_v4797_{args.fighter}_p1_kitana_guard_ram'),
 ('audit_v4776_{args.fighter}_current_p1_campaign_observed','audit_v4798_{args.fighter}_p1_kitana_guard_observed'),
 ('qualify_current_p1_campaign_source_v4773','qualify_sonya_p1_kitana_guard_source_v4795'),
 ('def capture(fighter):\n',"def capture(fighter):\n    need(fighter=='sonya','Only the actual Sonya P1 Kitana physical experiment')\n"),
 ("choices=('kano','sonya')","choices=('sonya',)")]
for before,after in changes:
    assert text.count(before)==1,before
    text=text.replace(before,after,1)
exec(compile(text,__file__+'::whole4772_only_physical_Kitana_context_and_fresh_leaves','exec'),globals())
