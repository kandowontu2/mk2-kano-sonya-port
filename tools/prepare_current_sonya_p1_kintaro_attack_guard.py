"""Unexecuted physical guard-before-grounded-jump experiment; no guest writes."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p1_boss_light_preparation'
fixed=sync.ROOT/'audit_current_sonya_p1_kintaro_close_retreat_preparation'
out=sync.ROOT/'audit_current_sonya_p1_kintaro_attack_guard_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker='    elseif escape and gap<preparation_gap then'
assert source.count(marker)==1
source=source.replace(marker,"    elseif stage==15 and other.flags&0x10~=0 then\n     boss_walk_last_x=nil;press('Down');press('Block')\n"+marker)
start=source.index('    if stage==16 then\n');end=source.index('    elseif quiet then',start)
correct=(fixed/'campaign.lua').read_text();cstart=correct.index('    if stage==16 then\n');cend=correct.index('    elseif quiet then',cstart)
source=source[:start]+correct[cstart:cend]+source[end:]
assert 'boss_jump_direction=forward;boss_walk_last_x=nil' in source
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p1_boss_light_runtime','audit_current_sonya_p1_kintaro_attack_guard_runtime')
(out/'run.ps1').write_text(runner)
print('PREPARED ONLY, NOT RUN: retain forwardjump; DownBlock before newgroundedjump whileCPUflag10; preservestomp/air; actualSonya ringstage16;180sec/320MiB/10MiB')
