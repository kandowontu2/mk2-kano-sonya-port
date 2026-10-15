"""Unchanged current primary-finisher controller, reciprocal added victims."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_own_finishers_dispatch_preparation'
out=sync.ROOT/'audit_bounded_cross_primary_finishers_preparation'
assert not out.exists()
out.mkdir()
for fighter in ('kano','sonya'):
    victim='sonya' if fighter=='kano' else 'kano'
    for side in (1,2):
        runner=(old/f'run_{fighter}_p{side}.ps1').read_text()
        runner=runner.replace("$env:MK2KS_TEST_FIGHTER='kitana'",f"$env:MK2KS_TEST_FIGHTER='{victim}'")
        runner=runner.replace(f'audit_bounded_own_finisher_dispatch_{fighter}_p{side}_runtime',f'audit_bounded_cross_primary_finisher_{fighter}_p{side}_runtime')
        (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
print('Prepared four earned cross-primary fatalities, no new media/controller')
