"""Extend a progressing physical route; no controller/game-state changes."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_liu_standing_preparation'
out=sync.ROOT/'audit_current_kano_p2_campaign_32000_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
assert source.count('frame>=20000')==1
source=source.replace('frame>=20000','frame>=32000').replace('maximum_fields=20000','maximum_fields=32000')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_liu_standing_runtime','audit_current_kano_p2_campaign_32000_runtime')
assert "'-str','450'" in runner
runner=runner.replace("'-str','450'","'-str','700'")
(out/'run.ps1').write_text(runner)
print('Prepared unchanged physical controller through32000fields;90sec/320MiB/10MiB text/no media')
