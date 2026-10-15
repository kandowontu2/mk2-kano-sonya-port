"""Extend progressing tied match only; physical controller unchanged."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_scorpion_ball_knife_preparation'
out=sync.ROOT/'audit_current_kano_p2_scorpion_ball_knife_40000_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
assert source.count('frame>=32000')==1
source=source.replace('frame>=32000','frame>=40000').replace('maximum_fields=32000','maximum_fields=40000')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_scorpion_ball_knife_runtime','audit_current_kano_p2_scorpion_ball_knife_40000_runtime').replace("'-str','700'","'-str','850'")
(out/'run.ps1').write_text(runner)
print('Unchanged physical tied-match extension40000fields;90sec/320MiB/10MiB/no media')
