"""Same physical campaign; host render skip only, exact-prefix proof required."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_mileena_choke_counter_preparation'
out=sync.ROOT/'audit_current_kano_p2_campaign_render_skip_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
assert source.count('60000')==2
source=source.replace('60000','80000')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_mileena_choke_counter_runtime','audit_current_kano_p2_campaign_render_skip_runtime')
assert runner.count("'-frameskip','0'")==1
runner=runner.replace("'-frameskip','0'","'-frameskip','10'").replace("'-str','1250'","'-str','1700'")
(out/'run.ps1').write_text(runner)
print('Same physical controller;hostrender frameskip10;80000target/90sec/320MiB/10MiB/no media;must prove exactprefix')
