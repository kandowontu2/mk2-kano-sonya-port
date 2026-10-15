"""Read native cue/voice ownership only; no PCM recorder or guest writes."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_current_friendships_preparation'
out=sync.ROOT/'audit_bounded_friendship_audio_dispatch_preparation'
assert not out.exists()
out.mkdir()
base=old/'friendships.lua'
observer=(sync.ROOT/'mk2ks_native_friendship_audio_v790.lua').read_text()
marker="dofile('mk2ks_native_friendship_probe_v784.lua')"
assert observer.count(marker)==1
source=base.read_text()+'\n'+observer.replace(marker,'-- controller included above')
assert ':snapshot(' not in source and 'io.open(' not in source and ':write_' not in source
lua=out/'audio.lua'
lua.write_text(source)
for fighter in ('kano','sonya'):
    for side in (1,2):
        runner=(old/f'run_{fighter}_p{side}.ps1').read_text()
        runner=runner.replace(old.name+'/friendships.lua',out.name+'/audio.lua').replace(sync.sha(base),sync.sha(lua))
        runner=runner.replace(f'audit_bounded_current_friendship_{fighter}_p{side}_runtime',f'audit_bounded_friendship_audio_dispatch_{fighter}_p{side}_runtime')
        (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
print('Prepared four scalar native audio-dispatch checks; no PCM recording')
