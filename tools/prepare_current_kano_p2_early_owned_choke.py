"""Physical own-ready choke extends from Cage2 to Kung0/Liu1, no game changes."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_cage_owned_choke_preparation'
out=sync.ROOT/'audit_current_kano_p2_early_owned_choke_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="(other.roster==5 or other.roster==2) then"
assert source.count(old)==1
source=source.replace(old,"(other.roster==5 or other.roster==2 or other.roster==0 or other.roster==1) then")
source=source.replace("other.roster==2 and 'CAGE_CHOKE_PLAN' or 'MILEENA_CHOKE_PLAN'","other.roster==2 and 'CAGE_CHOKE_PLAN' or other.roster==0 and 'KUNGLAO_CHOKE_PLAN' or other.roster==1 and 'LIUKANG_CHOKE_PLAN' or 'MILEENA_CHOKE_PLAN'")
source=source.replace("other.roster==2 and 'CAGE_CHOKE_LP_INPUT' or 'MILEENA_CHOKE_LP_INPUT'","other.roster==2 and 'CAGE_CHOKE_LP_INPUT' or other.roster==0 and 'KUNGLAO_CHOKE_LP_INPUT' or other.roster==1 and 'LIUKANG_CHOKE_LP_INPUT' or 'MILEENA_CHOKE_LP_INPUT'")
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_cage_owned_choke_runtime','audit_current_kano_p2_early_owned_choke_runtime')
(out/'run.ps1').write_text(runner)
print('PhysicalKung0/Liu1 choke extension;90sec/320MiB/10MiB/no media/no guestwrites')
