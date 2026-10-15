"""Prepare finite, media-free physical-input friendship checks."""
import re
import verify_native_source_sync as sync

sync.verify()
out = sync.ROOT / 'audit_bounded_current_friendships_preparation'
assert not out.exists(), 'Preserve executed preparations'
source = (sync.ROOT / 'mk2ks_native_friendship_probe_v762.lua').read_text()
source = source.replace("  local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)\n", '')
source = source.replace("  local f=assert(io.open(assert(os.getenv('MK2KS_FRIEND_OUT'))..'/guest_maincpu.bin','wb'));f:write(raw);f:close()\n", '')
source = source.replace(";screen:snapshot('selection_p'..n..'.png')", '')
source = source.replace("  if action_age>=40 and action_age<=198 then screen:snapshot('native_field_'..action_age..'.png')end\n", '')
source = source.replace("  screen:snapshot('friendship_'..age..'.png')\n", '')
source = source.replace(' frame=frame+1\n', " frame=frame+1\n if frame>=5500 then log('HOST_BOUND','limit=5500');manager.machine:exit();return end\n", 1)
for banned in (':snapshot(', 'read_range(', 'io.open(', ':write_'):
    assert banned not in source, banned
out.mkdir()
lua = out / 'friendships.lua'
lua.write_text(source)
old = sync.ROOT / 'audit_bounded_own_finishers_dispatch_preparation'
for fighter in ('kano', 'sonya'):
    for side in (1, 2):
        runner = (old / f'run_{fighter}_p{side}.ps1').read_text()
        runner = runner.replace(old.name + '/finishers.lua', out.name + '/friendships.lua')
        runner = runner.replace(sync.sha(old / 'finishers.lua'), sync.sha(lua))
        runner = runner.replace(f'audit_bounded_own_finisher_dispatch_{fighter}_p{side}_runtime', f'audit_bounded_current_friendship_{fighter}_p{side}_runtime')
        marker = "$env:MK2KS_CPU_PAIR_APPROACH='original'"
        runner = runner.replace(marker, f"$env:MK2KS_FRIEND_WINNER='{fighter}'\n$env:MK2KS_FRIEND_SIDE='{side}'\n$env:MK2KS_FRIEND_CASE='positive'\n" + marker)
        (out / f'run_{fighter}_p{side}.ps1').write_text(runner)
print('Prepared four media-free cases; observer SHA256=' + sync.sha(lua))
