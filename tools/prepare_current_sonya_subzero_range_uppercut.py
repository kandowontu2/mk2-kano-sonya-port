"""Only issue HP after crouch settlement and actual range approaches contact."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_subzero_crouch_settle_preparation'
out=sync.ROOT/'audit_current_sonya_subzero_range_uppercut_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="if age>=13 and age<18 then press('High Punch')end"
assert source.count(old)==1
source=source.replace(old,"if age>=13 and age<26 and gap<95 and age%6<3 then press('High Punch')end")
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_subzero_crouch_settle_runtime','audit_current_sonya_subzero_range_uppercut_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared physical HP only after13crouchfields and actual gap<95, same bounded run')
