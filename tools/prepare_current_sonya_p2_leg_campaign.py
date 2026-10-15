"""Reuse the bounded cold campaign with the already implemented physical leg tactic."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_current_sonya_p2_delayed_campaign_preparation'
out=sync.ROOT/'audit_current_sonya_p2_leg_campaign_preparation'
assert not out.exists()
runner=(old/'run.ps1').read_text()
before="MK2KS_CAMPAIGN_STRATEGY='zoning'";assert runner.count(before)==1
runner=runner.replace(before,"MK2KS_CAMPAIGN_STRATEGY='leg'")
runner=runner.replace('audit_current_sonya_p2_delayed_campaign_runtime','audit_current_sonya_p2_leg_campaign_runtime')
out.mkdir();(out/'run.ps1').write_text(runner)
print('Prepared unchanged12000field cold campaign, only physical tactic switched to leg')
