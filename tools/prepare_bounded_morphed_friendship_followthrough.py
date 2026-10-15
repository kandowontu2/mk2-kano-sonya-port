"""Observe actual action-relative retirement, not an earlier window deadline."""
import verify_native_source_sync as sync

sync.verify()
old=sync.ROOT/'audit_bounded_morphed_friendships_preparation'
out=sync.ROOT/'audit_bounded_morphed_friendship_followthrough_preparation'
assert not out.exists()
source=(old/'friendships.lua').read_text()
before=' if age>=720 then manager.machine:exit()end'
assert source.count(before)==1
source=source.replace(before,' if(action and frame-action>=650)or(not action and age>=720)then manager.machine:exit()end')
out.mkdir()
lua=out/'friendships.lua'
lua.write_text(source)
for target in ('kano','sonya'):
    for side in (1,2):
        runner=(old/f'run_{target}_p{side}.ps1').read_text()
        runner=runner.replace(old.name+'/friendships.lua',out.name+'/friendships.lua')
        runner=runner.replace(sync.sha(old/'friendships.lua'),sync.sha(lua))
        runner=runner.replace('audit_bounded_morphed_friendship_','audit_bounded_morphed_friendship_followthrough_')
        (out/f'run_{target}_p{side}.ps1').write_text(runner)
print('Prepared bounded action-relative retirement; inputs and punch counters unchanged')
