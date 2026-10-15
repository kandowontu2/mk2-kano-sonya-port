"""Stage15 physical retreating jump; keep native timing and prior route."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p1_subzero_guard_ready_v2_preparation'
out=sync.ROOT/'audit_current_kano_p1_kintaro_retreat_jump_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="      boss_last_jump=frame;boss_jump_direction=forward;boss_walk_last_x=nil\n      decision('close_pressure_jumpkick_attempt',boss_jump_direction)\n      press('Up');press(boss_jump_direction)"
new="      boss_last_jump=frame;boss_jump_direction=stage==15 and back or forward;boss_walk_last_x=nil\n      decision('close_pressure_jumpkick_attempt',boss_jump_direction)\n      press('Up');press(boss_jump_direction)"
assert source.count(old)==1;source=source.replace(old,new)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p1_subzero_guard_ready_v2_runtime','audit_current_kano_p1_kintaro_retreat_jump_runtime')
(out/'run.ps1').write_text(runner)
print('Kintaro-onlyphysicalretreatjump;180sec/320MiB/10MiB/no media/guestwrites')
