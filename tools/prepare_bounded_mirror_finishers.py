"""Eight earned same-ID primary/secondary contexts, physical selection only."""
import verify_native_source_sync as sync
sync.verify()
out=sync.ROOT/'audit_bounded_mirror_finishers_preparation'
assert not out.exists()
out.mkdir()
for kind in ('primary','secondary'):
    old=sync.ROOT/f'audit_bounded_cross_{kind}_finishers_preparation'
    for fighter in ('kano','sonya'):
        previous='sonya' if fighter=='kano' else 'kano'
        for side in (1,2):
            runner=(old/f'run_{fighter}_p{side}.ps1').read_text()
            marker=f"$env:MK2KS_TEST_FIGHTER='{previous}'"
            assert marker in runner
            runner=runner.replace(marker,f"$env:MK2KS_TEST_FIGHTER='{fighter}'")
            runner=runner.replace(f'audit_bounded_cross_{kind}_finisher_{fighter}_p{side}_runtime',f'audit_bounded_mirror_{kind}_finisher_{fighter}_p{side}_runtime')
            (out/f'run_{kind}_{fighter}_p{side}.ps1').write_text(runner)
print('Prepared eight bounded mirror-fatality cases')
