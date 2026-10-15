"""Earlier physical airkick window against CPU5, no native combat changes."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_mileena_air_release_preparation'
out=sync.ROOT/'audit_current_kano_p2_mileena_early_airkick_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="if gap<85 and height<90 and age>=8 and age<48 and age%6<3 then press('High Kick')end"
new="if gap<120 and height<120 and age>=4 and age<48 and age%6<3 then press('High Kick')end"
assert source.count(old)==1
source=source.replace(old,new)
assert source.replace(new,old)==(base/'campaign.lua').read_text()
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_mileena_air_release_runtime','audit_current_kano_p2_mileena_early_airkick_runtime')
(out/'run.ps1').write_text(runner)
print('CPU5-only earlier age4/gap120/height120 airkick;90sec/320MiB/10MiB/no media')
