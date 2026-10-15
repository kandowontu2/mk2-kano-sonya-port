"""Suppress repetitive general health log output; retain physical route/probes."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_campaign_render_skip_preparation'
out=sync.ROOT/'audit_current_kano_p2_campaign_slim_health_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker='local function log(tag,value)\n'
assert source.count(marker)==1
extra=" if tag=='HEALTH' and frame>=1690 then return end\n"
source=source.replace(marker,marker+extra)
assert source.replace(extra,'')==(base/'campaign.lua').read_text()
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_campaign_render_skip_runtime','audit_current_kano_p2_campaign_slim_health_runtime')
(out/'run.ps1').write_text(runner)
print('Only HEALTH text suppression after1690;native damage/ownership/win probes unchanged;80000target/90sec/320MiB/10MiB/no media')
