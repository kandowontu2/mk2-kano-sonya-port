"""Unchanged physical Kitana route, bounded next-round extension."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_kitana_counter_preparation'
out=sync.ROOT/'audit_current_kano_p2_kitana_campaign_43000_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
assert source.count('frame>=40000')==1
source=source.replace('frame>=40000','frame>=43000').replace('maximum_fields=40000','maximum_fields=43000')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_kitana_counter_runtime','audit_current_kano_p2_kitana_campaign_43000_runtime').replace("'-str','850'","'-str','950'")
(out/'run.ps1').write_text(runner)
print('Unchanged next-round extension43000fields;90sec/320MiB/10MiB/no media')
