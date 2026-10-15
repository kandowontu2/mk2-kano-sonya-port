"""Delay real physical HK until target gap below85 and actual height below90."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_scorpion_air_writers_preparation'
out=sync.ROOT/'audit_current_kano_p2_scorpion_close_air_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="if age>=8 and age<42 and age%6<3 then press('High Kick')end"
assert source.count(old)==1
source=source.replace(old,"if gap<85 and height<90 and age>=8 and age<48 and age%6<3 then press('High Kick')end")
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_scorpion_air_writers_runtime','audit_current_kano_p2_scorpion_close_air_runtime')
(out/'run.ps1').write_text(runner)
print('Closer physical HK gap<85/height<90;32000fields/90sec/320MiB/10MiB/no media')
