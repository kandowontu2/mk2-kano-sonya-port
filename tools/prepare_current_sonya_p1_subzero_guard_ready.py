"""Sonya stage11 only: recovered crouch/guard physical readiness."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p1_learned_campaign_preparation'
out=sync.ROOT/'audit_current_sonya_p1_subzero_guard_ready_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old='(other.roster==3 and (human.action==770 or human.action==1792 or human.action==1793))'
new='((other.roster==3 or(other.roster==8 and stage==11)) and (human.action==770 or human.action==1792 or human.action==1793))'
assert source.count(old)==1;source=source.replace(old,new)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p1_learned_campaign_runtime','audit_current_sonya_p1_subzero_guard_ready_runtime')
(out/'run.ps1').write_text(runner)
print('SonyaP1stage11physicalguardready;180sec/320MiB/10MiB/no media')
