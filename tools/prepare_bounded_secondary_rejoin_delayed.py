"""Reuse verified natural continue timing; retain earlier early-input failures."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_secondary_rejoin_state_preparation'
out=sync.ROOT/'audit_bounded_secondary_rejoin_delayed_preparation'
assert not out.exists()
out.mkdir()
source=(old/'rejoin.lua').read_text()
source=source.replace("request_age>=0 and request_age<4", "(request_age>=20 and request_age<25)or(request_age>=270 and request_age<275)")
source=source.replace('request_age>=18 and request_age<22','request_age>=310 and request_age<315')
source=source.replace(" if frame-wrap==300 then rejoin_snap('completed_scene')end",' -- No duplicate completion screenshot on this successor.')
source=source.replace('if age>=1600 then','if age>=1900 then')
lua=out/'rejoin.lua'
lua.write_text(source)
for fighter in ('kano','sonya'):
    runner=(old/f'run_{fighter}.ps1').read_text()
    runner=runner.replace(old.name+'/rejoin.lua',out.name+'/rejoin.lua').replace(sync.sha(old/'rejoin.lua'),sync.sha(lua))
    runner=runner.replace(f'audit_bounded_secondary_rejoin_state_{fighter}_p1_runtime',f'audit_bounded_secondary_rejoin_delayed_{fighter}_p1_runtime')
    runner=runner.replace("rawMedia='bounded_three_png'","rawMedia='bounded_two_png'")
    (out/f'run_{fighter}.ps1').write_text(runner)
