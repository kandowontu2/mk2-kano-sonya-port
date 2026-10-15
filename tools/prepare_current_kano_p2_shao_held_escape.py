"""Shao-only physical UpBack held through guard recovery;90sec cap restored."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_approved_180s_preparation'
out=sync.ROOT/'audit_current_kano_p2_shao_held_escape_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('    if stage==16 then\n')
end=source.index('    elseif quiet then\n',start)
branch=source[start:end]
old='     if projectile_start and frame-projectile_start<64 then\n'
assert branch.count(old)==1
new="     if frame-boss_last_jump<16 and height<=8 then\n      press('Up');press(boss_jump_direction)\n     elseif projectile_start and frame-projectile_start<64 then\n"
branch=branch.replace(old,new).replace('elseif frame-boss_last_jump<4 then','elseif frame-boss_last_jump<16 then')
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_approved_180s_runtime','audit_current_kano_p2_shao_held_escape_runtime')
assert runner.count('TotalSeconds -gt 180')==1
runner=runner.replace('TotalSeconds -gt 180','TotalSeconds -gt 90')
(out/'run.ps1').write_text(runner)
print('Shao only UpBack hold16vs4, unchanged earlierroute;90sec/320MiB/10MiB/no media')
