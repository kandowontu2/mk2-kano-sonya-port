"""Physical guard against CPU active flag; retain pre-mirror inputs."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_mirror_neutral_recovery_preparation'
out=sync.ROOT/'audit_current_sonya_mirror_active_flag_guard_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('   if leg_tactic and other.roster==18 then')
end=source.index('   elseif leg_tactic and other.roster==0 then',start)
branch=source[start:end]
assert branch.count('other.flags&0x0c==0')==1
branch=branch.replace('other.flags&0x0c==0','other.flags&0x1c==0')
old='    if ms_start and frame-ms_start<32 then'
assert branch.count(old)==1
branch=branch.replace(old,"    if other.flags&0x10~=0 then\n     ms_start=nil;press('Down');press('Block')\n    elseif ms_start and frame-ms_start<32 then")
source=source[:start]+branch+source[end:]
source=source.replace('frame>=24000','frame>=21000').replace('maximum_fields=24000','maximum_fields=21000')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_mirror_neutral_recovery_runtime','audit_current_sonya_mirror_active_flag_guard_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared21000fields; mirror-only physical active-flag guard; no media')
