"""Extend successful physical leg spacing to native LiuKang1 only."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_kunglao_leg_spacing_preparation'
out=sync.ROOT/'audit_current_sonya_p2_liukang_leg_spacing_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old='   elseif leg_tactic and other.roster==0 then\n'
assert source.count(old)==1
source=source.replace(old,'   elseif leg_tactic and (other.roster==0 or (side==2 and other.roster==1)) then\n')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_kunglao_leg_spacing_runtime','audit_current_sonya_p2_liukang_leg_spacing_runtime')
(out/'run.ps1').write_text(runner)
print('LiuKang1 physical leg spacing only;90sec/320MiB/10MiB/no media')
