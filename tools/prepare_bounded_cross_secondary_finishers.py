"""Same earned secondary controller, reciprocal added victims."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_secondary_finishers_preparation'
out=sync.ROOT/'audit_bounded_cross_secondary_finishers_preparation'
assert not out.exists()
out.mkdir()
for fighter in ('kano','sonya'):
    victim='sonya' if fighter=='kano' else 'kano'
    for side in (1,2):
        runner=(old/f'run_{fighter}_p{side}.ps1').read_text()
        assert "$env:MK2KS_TEST_FIGHTER='kitana'" in runner
        runner=runner.replace("$env:MK2KS_TEST_FIGHTER='kitana'",f"$env:MK2KS_TEST_FIGHTER='{victim}'")
        runner=runner.replace(f'audit_bounded_secondary_finisher_{fighter}_p{side}_runtime',f'audit_bounded_cross_secondary_finisher_{fighter}_p{side}_runtime')
        (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
print('Prepared four earned cross-secondary fatality cases')
