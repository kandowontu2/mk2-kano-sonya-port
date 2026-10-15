"""Existing physical jump/counter policy, naturally scheduled mirror opponent."""
import json
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_campaign_progress_core_preparation'
out=sync.ROOT/'audit_bounded_sonya_mirror_jump_preparation';assert not out.exists();out.mkdir()
runner=(old/'run_sonya_p2.ps1').read_text()
assert runner.count("$env:MK2KS_CAMPAIGN_STRATEGY='defensive_leg'")==1
runner=runner.replace("$env:MK2KS_CAMPAIGN_STRATEGY='defensive_leg'","$env:MK2KS_CAMPAIGN_STRATEGY='jumpkick'")
runner=runner.replace('audit_bounded_campaign_progress_core_sonya_p2_runtime','audit_bounded_sonya_mirror_jump_runtime')
(out/'run.ps1').write_text(runner)
(out/'report.json').write_text(json.dumps(dict(prepared=True,onlyPhysicalControllerPolicyChanged=True,opponentForced=False,maximumFields=12000)))
