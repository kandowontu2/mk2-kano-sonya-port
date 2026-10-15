"""Verified Liu ready-HK/approach branch overrides range retreat for CPU5 only."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_mileena_standing_preparation'
out=sync.ROOT/'audit_current_kano_p2_mileena_approach_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old='other.roster==18 or other.roster==8 or other.roster==2'
assert source.count(old)==1
source=source.replace(old,old+' or other.roster==5')
old="or 'KANO_P2_LIU_STANDING'"
assert source.count(old)==1
source=source.replace(old,"or other.roster==2 and 'KANO_P2_LIU_STANDING' or 'KANO_P2_MILEENA_APPROACH'")
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_mileena_standing_runtime','audit_current_kano_p2_mileena_approach_runtime')
(out/'run.ps1').write_text(runner)
print('CPU5-only real-ready approach/HK2..6;60000target/90sec/320MiB/10MiB/no media')
