"""Physical close retreat jump variant; native game decides collision and damage."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p1_boss_light_preparation'
out=sync.ROOT/'audit_current_sonya_p1_kintaro_close_retreat_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old='boss_last_jump=frame;boss_jump_direction=forward;boss_walk_last_x=nil'
assert source.count(old)==1
source=source.replace(old,'boss_last_jump=frame;boss_jump_direction=(stage==15 and gap<95)and back or forward;boss_walk_last_x=nil')
start=source.index('    if stage==16 then\n')
end=source.index('    elseif quiet then',start)
branch=source[start:end]
assert branch.count("if age>=8 and age<12 then press('High Punch')end")==1
branch=branch.replace("if age>=8 and age<12 then press('High Punch')end","if age>=8 and age<12 then press(fighter=='sonya'and'Low Punch'or'High Punch')end")
branch=branch.replace('projectile_start=frame;projectile_direction=back',"projectile_start=frame;projectile_direction=fighter=='sonya'and forward or back")
branch=branch.replace("decision('shao_knife_command_attempt',back)","decision(fighter=='sonya'and'shao_ring_command_attempt'or'shao_knife_command_attempt',projectile_direction)")
branch=branch.replace('-- Genuine Kano D,B,HP command, with ordinary retreat at close range.','-- Genuine Sonya D,F,LP ring / Kano D,B,HP knife, with ordinary retreat.')
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p1_boss_light_runtime','audit_current_sonya_p1_kintaro_close_retreat_runtime')
(out/'run.ps1').write_text(runner)
print('Stage15 gap<95 backwardjump / widerforwardjump; stage16actualSonya ringD,F,LP;140000ceiling/180sec/320MiB/10MiB/no media')
