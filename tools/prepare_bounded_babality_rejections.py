"""Prepare real wrong-direction/punch-use checks without new media."""
import verify_native_source_sync as sync

sync.verify()
out=sync.ROOT/'audit_bounded_babality_rejections_preparation'
assert not out.exists()
out.mkdir()
old=sync.ROOT/'audit_bounded_current_babalities_preparation'
for fighter in ('kano','sonya'):
    for side in (1,2):
        for case in ('wrong_direction','punch_used'):
            runner=(old/f'run_{fighter}_p{side}.ps1').read_text()
            runner=runner.replace(f'audit_bounded_current_babality_{fighter}_p{side}_runtime',f'audit_bounded_babality_{case}_{fighter}_p{side}_runtime')
            runner=runner.replace("$env:MK2KS_BABY_CASE='positive'",f"$env:MK2KS_BABY_CASE='{case}'")
            (out/f'run_{case}_{fighter}_p{side}.ps1').write_text(runner)
print('Prepared eight bounded babality rejection cases')
