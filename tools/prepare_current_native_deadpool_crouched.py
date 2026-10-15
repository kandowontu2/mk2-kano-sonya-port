"""Crouch before LP/LK, recover before fresh HP; no native state changes."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_deadpool_actions_preparation'
out=sync.ROOT/'audit_current_native_deadpool_crouched_preparation';assert not out.exists()
source=(base/'stage.lua').read_text()
old="""     if age>=5 and age<44 then press(side,'Low Punch');press(side,'Low Kick')end
     if age>=16 and age<44 then press(side,'Down')end
     if age>=32 and age<36 then press(side,'High Punch')end
"""
assert source.count(old)==1
source=source.replace(old,"""     if age>=16 and age<64 then press(side,'Low Punch');press(side,'Low Kick')end
     if age>=0 and age<70 then press(side,'Down')end
     if age>=48 and age<52 then press(side,'High Punch')end
""")
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/stage.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua))
runner=runner.replace('audit_current_native_deadpool_actions_kano_p1_runtime','audit_current_native_deadpool_crouched_kano_p1_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared real Down before heldLP/LK, freshHP48..51; actual native outcome not assumed')
