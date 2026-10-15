"""Physical HP earlier after observed crouch, before prior native throw window."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_subzero_uppercut_edges_preparation'
out=sync.ROOT/'audit_current_sonya_subzero_early_uppercut_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="if age>=6 and age<9 then press('High Punch')end"
assert source.count(old)==1
source=source.replace(old,"if age>=2 and age<5 then press('High Punch')end")
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_subzero_uppercut_edges_runtime','audit_current_sonya_subzero_early_uppercut_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared unchanged9000fields with physical HP ages2..4 instead of6..8')
