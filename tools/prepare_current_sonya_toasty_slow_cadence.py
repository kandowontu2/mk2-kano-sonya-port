"""Original 104-field physical uppercut cadence; no RNG/state assistance."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_toasty_decisions_preparation'
out=sync.ROOT/'audit_current_sonya_toasty_slow_cadence_preparation'
assert not out.exists()
source=(base/'stage.lua').read_text()
old="if frame%48>=13 and frame%48<26 and frame%6<3 then press(side,'High Punch')end"
assert source.count(old)==1
source=source.replace(old,"if frame%104>=16 and frame%104<20 then press(side,'High Punch')end")
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/stage.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua)).replace('audit_current_sonya_toasty_decisions_runtime','audit_current_sonya_toasty_slow_cadence_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared only104-field physical Portal HP cadence; unchanged native RNG;28000fields/90sec/no media')
