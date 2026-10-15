"""Kintaro-only physical airkick timing; earlier matches unchanged."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p1_subzero_guard_ready_v2_preparation'
out=sync.ROOT/'audit_current_kano_p1_kintaro_late_kick_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old='     if kick_vy>=kick_vy_min and kick_vy<0x80000000 and frame%6<3 then press(\'High Kick\')end'
new="     if kick_vy>=(stage==15 and 0x20000 or kick_vy_min) and kick_vy<0x80000000 and(stage~=15 or height<=48) and frame%6<3 then press('High Kick')end"
assert source.count(old)==1;source=source.replace(old,new)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p1_subzero_guard_ready_v2_runtime','audit_current_kano_p1_kintaro_late_kick_runtime')
(out/'run.ps1').write_text(runner)
print('Kintaro-onlydescendingkickheight<=48;180sec/320MiB/10MiB/no media')
