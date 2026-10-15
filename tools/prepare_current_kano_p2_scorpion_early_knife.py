"""Earlier physical knife follow-up, no health/damage/state modifications."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_scorpion_ball_knife_preparation'
out=sync.ROOT/'audit_current_kano_p2_scorpion_early_knife_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
assert source.count('other.hp<=33 and ready')==1
source=source.replace('other.hp<=33 and ready','other.hp<=55 and ready')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_scorpion_ball_knife_runtime','audit_current_kano_p2_scorpion_early_knife_runtime')
(out/'run.ps1').write_text(runner)
print('Only physical knife follow-up threshold33to55;32000fields/90sec/320MiB/10MiB/no media')
