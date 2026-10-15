"""Whole player-one4772 capture after actual preboot Lua return-value failure.

Only corrected wrapper, source proof and unused result leaves change. Native
controls, initialized guest/RGB transport and gameplay remain unchanged.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
text=(ROOT/'tools/run_current_p1_campaign_ram_v4772.py').read_text()
changes=[
 ('mk2ks_current_p1_campaign_ram_v4771.lua','mk2ks_current_p1_campaign_ram_v4781.lua'),
 ('audit_v4774_current_p1_campaign_source_checked','audit_v4784_current_p1_campaign_source_checked'),
 ('audit_v4775_{fighter}_current_p1_campaign_ram','audit_v4785_{fighter}_current_p1_campaign_ram'),
 ('audit_v4775_{args.fighter}_current_p1_campaign_ram','audit_v4785_{args.fighter}_current_p1_campaign_ram'),
 ('audit_v4776_{args.fighter}_current_p1_campaign_observed','audit_v4786_{args.fighter}_current_p1_campaign_observed'),
 ('qualify_current_p1_campaign_source_v4773','qualify_current_p1_campaign_source_v4783')]
for before,after in changes:
    assert text.count(before)==1,before
    text=text.replace(before,after,1)
exec(compile(text,__file__+'::whole4772_corrected_exact_wrapper','exec'),globals())
