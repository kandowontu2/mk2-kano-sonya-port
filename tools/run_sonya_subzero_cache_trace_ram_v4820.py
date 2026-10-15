"""Fresh bounded readonly cursor/descriptor trace of the real native defect.

Entire original physical controller and initialized-guest/RGB RAM collector
retained. Host stops after the actual overrun; never whole-campaign acceptance.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
text=(ROOT/'tools/run_current_p1_campaign_ram_v4772.py').read_text()
changes=[
 ('mk2ks_current_p1_campaign_ram_v4771.lua','mk2ks_sonya_subzero_cache_trace_ram_v4819.lua'),
 ('audit_v4774_current_p1_campaign_source_checked','audit_v4822_sonya_subzero_cache_trace_source_checked'),
 ('audit_v4775_{fighter}_current_p1_campaign_ram','audit_v4823_{fighter}_subzero_cache_trace_ram'),
 ('audit_v4775_{args.fighter}_current_p1_campaign_ram','audit_v4823_{args.fighter}_subzero_cache_trace_ram'),
 ('audit_v4776_{args.fighter}_current_p1_campaign_observed','audit_v4824_{args.fighter}_subzero_cache_trace_observed'),
 ('qualify_current_p1_campaign_source_v4773','qualify_sonya_subzero_cache_trace_source_v4821'),
 ('def capture(fighter):\n',"def capture(fighter):\n    need(fighter=='sonya','Exact actual Sonya/Sub-Zero native defect probe')\n"),
 ("choices=('kano','sonya')","choices=('sonya',)"),
 ('return dict(passed=True,candidate=NAME','return dict(passed=True,diagnosticOnly=True,hostStoppedAfterActualDefect=True,candidate=NAME')]
for before,after in changes:
    assert text.count(before)==1,before
    text=text.replace(before,after,1)
exec(compile(text,__file__+'::whole4772_readonly_defect_probe_only','exec'),globals())
