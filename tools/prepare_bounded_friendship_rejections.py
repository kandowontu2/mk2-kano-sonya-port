"""Reuse unchanged bounded observer for real wrong-command/punch checks."""
import verify_native_source_sync as sync

sync.verify()
out = sync.ROOT/'audit_bounded_friendship_rejections_preparation'
assert not out.exists()
out.mkdir()
old = sync.ROOT/'audit_bounded_current_friendships_preparation'
for fighter in ('kano','sonya'):
    for side in (1,2):
        for case in ('wrong_command','punch_used'):
            runner = (old/f'run_{fighter}_p{side}.ps1').read_text()
            runner = runner.replace(f'audit_bounded_current_friendship_{fighter}_p{side}_runtime',f'audit_bounded_friendship_{case}_{fighter}_p{side}_runtime')
            runner = runner.replace("$env:MK2KS_FRIEND_CASE='positive'",f"$env:MK2KS_FRIEND_CASE='{case}'")
            (out/f'run_{case}_{fighter}_p{side}.ps1').write_text(runner)
print('Prepared eight media-free physical-input rejection cases')
