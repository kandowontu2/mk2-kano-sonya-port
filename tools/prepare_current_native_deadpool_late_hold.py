"""Fresh HP before held low buttons; observe uppercut/acid, assume neither."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_deadpool_joint_edge_preparation'
out=sync.ROOT/'audit_current_native_deadpool_late_hold_preparation';assert not out.exists()
source=(base/'stage.lua').read_text()
old="if age>=48 and age<64 then press(side,'Low Punch');press(side,'Low Kick')end"
assert source.count(old)==1
source=source.replace(old,"if age>=51 and age<90 then press(side,'Low Punch');press(side,'Low Kick')end")
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/stage.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua))
runner=runner.replace('audit_current_native_deadpool_joint_edge_kano_p1_runtime','audit_current_native_deadpool_late_hold_kano_p1_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared freshHP48 before heldLP/LK51..89; actual native outcome not assumed/no media')
