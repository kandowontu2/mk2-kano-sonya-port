"""Player-one physical Sonya tactics; no native AI/character-state mutation."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_baraka_ring_finish20_preparation'
out=sync.ROOT/'audit_current_sonya_p1_learned_campaign_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
assert source.count("fighter=='sonya' and side==2")==1
source=source.replace("fighter=='sonya' and side==2","fighter=='sonya' and side==1")
assert source.count('(side==2 and other.roster==1)')==1
source=source.replace('(side==2 and other.roster==1)','(side==1 and other.roster==1)')
source=source.replace('sample(2),sample(1)','sample(side),sample(opponent)')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_baraka_ring_finish20_runtime','audit_current_sonya_p1_learned_campaign_runtime')
assert "$env:MK2KS_CAMPAIGN_SIDE='2'" in runner
runner=runner.replace("$env:MK2KS_CAMPAIGN_SIDE='2'","$env:MK2KS_CAMPAIGN_SIDE='1'")
(out/'run.ps1').write_text(runner)
print('SonyaP1physicaltactics;180sec/320MiB/10MiB/no media/guestwrites')
