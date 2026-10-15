"""Current-build baby performer/victim checks, no raw-media sinks."""
import re
import verify_native_source_sync as sync

sync.verify()
out = sync.ROOT / 'audit_bounded_current_babalities_preparation'
assert not out.exists()
source = (sync.ROOT / 'mk2ks_native_babality_performer_probe_v738.lua').read_text()
source = '\n'.join(line for line in source.splitlines() if 'local raw=p:read_range(' not in line and 'local f=assert(io.open(' not in line) + '\n'
source = re.sub(r'screen:snapshot\([^)]*\)', '', source)
source = source.replace(' frame=frame+1\n', " frame=frame+1\n if frame>=5500 then log('HOST_BOUND','limit=5500');manager.machine:exit();return end\n", 1)
for banned in (':snapshot(', 'read_range(', 'io.open(', ':write_'):
    assert banned not in source, banned
out.mkdir()
lua = out / 'babalities.lua'
lua.write_text(source)
old = sync.ROOT / 'audit_bounded_current_friendships_preparation'
for fighter in ('kano', 'sonya'):
    for side in (1, 2):
        runner = (old / f'run_{fighter}_p{side}.ps1').read_text()
        runner = runner.replace(old.name + '/friendships.lua', out.name + '/babalities.lua')
        runner = runner.replace(sync.sha(old / 'friendships.lua'), sync.sha(lua))
        runner = runner.replace(f'audit_bounded_current_friendship_{fighter}_p{side}_runtime', f'audit_bounded_current_babality_{fighter}_p{side}_runtime')
        marker = "$env:MK2KS_CPU_PAIR_APPROACH='original'"
        victim = 'sonya' if fighter == 'kano' else 'kano'
        runner = runner.replace(marker, f"$env:MK2KS_BABY_WINNER='{fighter}'\n$env:MK2KS_BABY_WINNER_SIDE='{side}'\n$env:MK2KS_BABY_VICTIM='{victim}'\n$env:MK2KS_BABY_CASE='positive'\n" + marker)
        (out / f'run_{fighter}_p{side}.ps1').write_text(runner)
print('Prepared four media-free babality checks: ' + sync.sha(lua))
