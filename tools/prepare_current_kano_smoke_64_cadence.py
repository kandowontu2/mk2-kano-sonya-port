"""Only change the physical Portal uppercut pulse rhythm to64fields."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_smoke_104_cadence_preparation'
out=sync.ROOT/'audit_current_kano_smoke_64_cadence_preparation'
assert not out.exists()
source=(base/'stage.lua').read_text()
old="if frame%104>=16 and frame%104<20 then press(side,'High Punch')end"
assert source.count(old)==1
source=source.replace(old,"if frame%64>=16 and frame%64<20 then press(side,'High Punch')end")
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/stage.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua)).replace('audit_current_kano_smoke_104_cadence_runtime','audit_current_kano_smoke_64_cadence_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared only64-field physical HP cadence;28000fields/90sec/320MiB/no media')
