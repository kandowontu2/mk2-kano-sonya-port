"""One explicitly user-approved180sec test; unchanged best physical controls."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_campaign_frontier_observer_preparation'
out=sync.ROOT/'audit_current_kano_p2_approved_180s_preparation'
assert not out.exists()
original=(base/'campaign.lua').read_text()
source=original.replace('frame>=80000','frame>=120000').replace('maximum_fields=80000','maximum_fields=120000')
assert source!=original and source.replace('frame>=120000','frame>=80000').replace('maximum_fields=120000','maximum_fields=80000')==original
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_campaign_frontier_observer_runtime','audit_current_kano_p2_approved_180s_runtime')
assert runner.count('TotalSeconds -gt 90')==1
runner=runner.replace('TotalSeconds -gt 90','TotalSeconds -gt 180').replace("'-str','1700'","'-str','2500'")
(out/'run.ps1').write_text(runner)
print('One approved180sec/320MiB/10MiB/no media/no guestwrites; physical controls unchanged')
