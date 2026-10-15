"""Prepared only: actual descending lower-height kick; native game remains unchanged."""
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT
base=root/'audit_current_sonya_p1_boss_light_preparation';fixed=root/'audit_current_sonya_p1_kintaro_attack_guard_preparation'
out=root/'audit_current_sonya_p1_kintaro_low_airkick_preparation';assert not out.exists()
source=(base/'campaign.lua').read_text()
old="if kick_vy>=kick_vy_min and kick_vy<0x80000000 and frame%6<3 then press('High Kick')end"
assert source.count(old)==1
source=source.replace(old,"if kick_vy>=kick_vy_min and kick_vy<0x80000000 and (stage~=15 or(height<=60 and gap<=100)) and frame%6<3 then press('High Kick')end")
start=source.index('    if stage==16 then\n');end=source.index('    elseif quiet then',start)
correct=(fixed/'campaign.lua').read_text();a=correct.index('    if stage==16 then\n');b=correct.index('    elseif quiet then',a)
source=source[:start]+correct[a:b]+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p1_boss_light_runtime','audit_current_sonya_p1_kintaro_low_airkick_runtime')
(out/'run.ps1').write_text(runner)
print('PREPARED ONLY/NOT RUN: stage15 descending HK height<=60/gap<=100; originalforwardjump; stage16correctSonyaRing;180sec/320MiB/10MiB')
