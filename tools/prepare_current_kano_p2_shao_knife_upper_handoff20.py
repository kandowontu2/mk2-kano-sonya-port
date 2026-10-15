"""Use measured sub30HP handoff; physical inputs only."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_shao_knife_upper_handoff_preparation'
out=sync.ROOT/'audit_current_kano_p2_shao_knife_upper_handoff20_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
assert source.count('elseif other.hp<=35 and height==0 then')==1
source=source.replace('elseif other.hp<=35 and height==0 then','elseif other.hp<=20 and height==0 then')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_shao_knife_upper_handoff_runtime','audit_current_kano_p2_shao_knife_upper_handoff20_runtime')
(out/'run.ps1').write_text(runner)
print('Lowhealth20physicalhandoff;180sec/320MiB/10MiB/no media/guestwrites')
