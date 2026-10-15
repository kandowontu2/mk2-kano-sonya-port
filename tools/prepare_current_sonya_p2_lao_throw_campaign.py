"""Change only ordinary controller tactics against native Kung Lao."""
import verify_native_source_sync as sync
sync.verify()
old = sync.ROOT / 'audit_current_sonya_p2_delayed_campaign_preparation'
out = sync.ROOT / 'audit_current_sonya_p2_lao_throw_campaign_preparation'
assert not out.exists()
source = (old / 'campaign.lua').read_text()
needle = '  if winner==0 and human.hp>0 and other.hp>0 then\n'
assert source.count(needle) == 1
source = source.replace(needle, needle + "   local strategy=other.roster==9 and 'throw' or strategy\n   local leg_tactic=strategy=='leg'or strategy=='defensive_leg'\n")
assert source.count('frame>=12000') == 1
source = source.replace('frame>=12000', 'frame>=20000').replace('maximum_fields=12000', 'maximum_fields=20000')
out.mkdir()
lua = out / 'campaign.lua'
lua.write_text(source)
runner = (sync.ROOT / 'audit_current_sonya_p2_leg_campaign_preparation/run.ps1').read_text()
runner = runner.replace(old.name+'/campaign.lua', out.name+'/campaign.lua').replace(sync.sha(old/'campaign.lua'), sync.sha(lua))
runner = runner.replace('audit_current_sonya_p2_leg_campaign_runtime', 'audit_current_sonya_p2_lao_throw_campaign_runtime')
runner = runner.replace("'-str','400'", "'-str','700'")
(out / 'run.ps1').write_text(runner)
print('Prepared physical leg approach, ordinary forward+LP throws against native Kung Lao only; 20000 fields, unchanged host caps, no media')
