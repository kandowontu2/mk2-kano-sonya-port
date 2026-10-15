"""Actual P2 performer, P1 loser paid rejoin, same error-free observer."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_secondary_rejoin_roster_ready_preparation'
out=sync.ROOT/'audit_bounded_secondary_rejoin_p2_preparation'
assert not out.exists()
out.mkdir()
for fighter in ('kano','sonya'):
    runner=(old/f'run_{fighter}.ps1').read_text()
    assert "$env:MK2KS_CAMPAIGN_SIDE='2'" in runner
    runner=runner.replace("$env:MK2KS_CAMPAIGN_SIDE='2'","$env:MK2KS_CAMPAIGN_SIDE='1'")
    runner=runner.replace(f'audit_bounded_secondary_rejoin_roster_ready_{fighter}_p1_runtime',f'audit_bounded_secondary_rejoin_roster_ready_{fighter}_p2_runtime')
    (out/f'run_{fighter}.ps1').write_text(runner)
