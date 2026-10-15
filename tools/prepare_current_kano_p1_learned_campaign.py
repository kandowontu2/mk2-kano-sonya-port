"""Adapt physical successful K2 tactics to P1; no native code/state changes."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_shao_backjump_charge_counter_preparation'
out=sync.ROOT/'audit_current_kano_p1_learned_campaign_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
assert source.count("fighter=='kano' and side==2")==4
source=source.replace("fighter=='kano' and side==2","fighter=='kano' and side==1")
source=source.replace('sample(2),sample(1)','sample(side),sample(opponent)').replace('KANO_P2_','KANO_P1_')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_shao_backjump_charge_counter_runtime','audit_current_kano_p1_learned_campaign_runtime')
assert "$env:MK2KS_CAMPAIGN_SIDE='2'" in runner
runner=runner.replace("$env:MK2KS_CAMPAIGN_SIDE='2'","$env:MK2KS_CAMPAIGN_SIDE='1'")
(out/'run.ps1').write_text(runner)
print('P1physicaltactics/relativeobserver adaptation;180sec/320MiB/10MiB/no media')
