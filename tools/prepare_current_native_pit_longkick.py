"""Try native full-range high kicks; preserve the failed close-kick route."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_pit_preparation'
out=sync.ROOT/'audit_current_native_pit_longkick_preparation';assert not out.exists()
source=(base/'stage.lua').read_text()
old="   if math.abs(h.x-v.x)>62 then press(side,forward)\n   else if frame%40<4 then press(side,'High Kick')end end"
assert source.count(old)==1
source=source.replace(old,"   if math.abs(h.x-v.x)>100 then press(side,forward)\n   else if frame%32<4 then press(side,'High Kick')end end")
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
runner=(base/'run_kano_p1.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/stage.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua))
runner=runner.replace('audit_current_native_pit_kano_p1_runtime','audit_current_native_pit_longkick_kano_p1_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared physical full-range HK attempt; same native game,90sec/320MiB/10MiB caps, no media')
