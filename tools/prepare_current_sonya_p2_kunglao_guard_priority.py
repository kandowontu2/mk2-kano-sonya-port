"""Guard active native CPU0 before physical retreat; no game-state edits."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_kunglao_contact_trace_preparation'
out=sync.ROOT/'audit_current_sonya_p2_kunglao_guard_priority_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker='    if height<=8 and gap<((other.roster==2 or other.roster==0) and 100 or 90)'
assert source.count(marker)==1
source=source.replace(marker,"    if other.roster==0 and other.flags&0x10~=0 then\n     sh_start=nil;sr_start=nil;press('Down');press('Block')\n    elseif height<=8 and gap<((other.roster==2 or other.roster==0) and 100 or 90)")
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_kunglao_contact_trace_runtime','audit_current_sonya_p2_kunglao_guard_priority_runtime')
(out/'run.ps1').write_text(runner)
print('CPU0 physical guard-priority only;60k ceiling/90sec/320MiB/10MiB/no media')
