"""Preserve failed launcher; correct duplicated preparation path only."""
import verify_native_source_sync as sync

out=sync.ROOT/'audit_bounded_morphed_friendship_followthrough_preparation'
before='audit_bounded_morphed_friendship_followthrough_followthrough_preparation/friendships.lua'
after='audit_bounded_morphed_friendship_followthrough_preparation/friendships.lua'
for target in ('kano','sonya'):
    for side in (1,2):
        source=(out/f'run_{target}_p{side}.ps1').read_text()
        assert source.count(before)==1
        successor=out/f'run_{target}_p{side}_path_checked.ps1'
        assert not successor.exists()
        successor.write_text(source.replace(before,after))
print('Prepared corrected runner paths; observer and physical inputs unchanged')
