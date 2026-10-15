"""Test settled crouch leg timing in the real stage5 mirror, no guest writes."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_mirror_prepared_uppercut_preparation'
out=sync.ROOT/'audit_current_sonya_mirror_settled_leg_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="if age>=13 and age<26 and gap<95 and age%6<3 then press('High Punch')end"
assert source.count(old)==1
source=source.replace(old,"if age>=13 and age<26 and gap<85 and age%6<3 then press('Low Punch');press('Block')end")
source=source.replace('MIRROR_PREPARED_UPPERCUT_ATTEMPT','MIRROR_SETTLED_LEG_ATTEMPT')
source=source.replace('0xff870dc0','0xfff80800').replace('0xff870dcf','0xfff8080f').replace('0xff870dd0','0xfff80810')
source=source.replace('MIRROR_NATIVE_UPPERCUT','MIRROR_NATIVE_LEG')
assert ':write_' not in source and 'snapshot(' not in source
out.mkdir()
lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_mirror_prepared_uppercut_runtime','audit_current_sonya_mirror_settled_leg_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared settled leg mirror controller,24000fields,90sec/320MiB,no media')
