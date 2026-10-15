"""Native CPU-earned idle losses then physical initialized reselect, four roles."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_continue_selection_preparation'
out=sync.ROOT/'audit_current_native_continue_roles_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old='if winner==0 and human.hp>0 and other.hp>0 then'
assert source.count(old)==1
source=source.replace(old,'if false and winner==0 and human.hp>0 and other.hp>0 then -- Idle physical player; native CPU earns loss.')
old='assert(own.roster==18 and own.id==18 and own.owner==own.actor)'
assert source.count(old)==1
source=source.replace(old,'assert(own.roster==identity and own.id==identity and own.owner==own.actor)')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace("$env:MK2KS_CAMPAIGN_STRATEGY='leg'","$env:MK2KS_CAMPAIGN_STRATEGY='zoning'")
for fighter in ('kano','sonya'):
 for side in (1,2):
  text=runner.replace('audit_current_sonya_continue_selection_runtime',f'audit_current_native_continue_{fighter}_p{side}_runtime')
  text=text.replace("$env:MK2KS_TEST_FIGHTER='sonya'",f"$env:MK2KS_TEST_FIGHTER='{fighter}'")
  text=text.replace("$env:MK2KS_CAMPAIGN_SIDE='2'",f"$env:MK2KS_CAMPAIGN_SIDE='{side}'")
  (out/f'run_{fighter}_p{side}.ps1').write_text(text)
print('Prepared four genuine idle-loss/paid-continue roles; no forced health/results or media')
