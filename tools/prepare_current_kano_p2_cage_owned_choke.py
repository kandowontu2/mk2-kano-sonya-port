"""Apply verified physical own-ready choke controls to regular Cage2 only."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_campaign_frontier_observer_preparation'
out=sync.ROOT/'audit_current_kano_p2_cage_owned_choke_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="if fighter=='kano' and side==2 and other.roster==5 then"
assert source.count(old)==1
source=source.replace(old,"if fighter=='kano' and side==2 and (other.roster==5 or other.roster==2) then")
source=source.replace("log('MILEENA_CHOKE_PLAN',","log(other.roster==2 and 'CAGE_CHOKE_PLAN' or 'MILEENA_CHOKE_PLAN',").replace("log('MILEENA_CHOKE_LP_INPUT',","log(other.roster==2 and 'CAGE_CHOKE_LP_INPUT' or 'MILEENA_CHOKE_LP_INPUT',")
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_campaign_frontier_observer_runtime','audit_current_kano_p2_cage_owned_choke_runtime')
(out/'run.ps1').write_text(runner)
print('Cage2 ownreadychoke physicaltest;90sec/320MiB/10MiB/no media/no guestwrites')
