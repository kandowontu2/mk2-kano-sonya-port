"""Avoid formatting unchanged HP writes; retain best physical Kano campaign."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_campaign_render_skip_preparation'
out=sync.ROOT/'audit_current_kano_p2_changed_health_only_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old='  if mask==0xffff and first_live then\n'
new='  if mask==0xffff and first_live and (frame<1690 or p:read_u16(at)~=(data&0xffff)) then\n'
assert source.count(old)==1
source=source.replace(old,new)
assert source.replace(new,old)==(base/'campaign.lua').read_text()
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_campaign_render_skip_runtime','audit_current_kano_p2_changed_health_only_runtime')
(out/'run.ps1').write_text(runner)
print('Only skip unchangedHP observation formatting after1690; identical best inputs/90sec/320MiB/10MiB/no media')
