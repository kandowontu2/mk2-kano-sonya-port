"""Earn Pit with ordinary HK inputs and paid rematches, unchanged native game."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_tomb_preparation'
out=sync.ROOT/'audit_current_native_pit_preparation';assert not out.exists()
source=(base/'stage.lua').read_text()
source=source.replace('frame>=12000','frame>=36000').replace('maximum_fields=12000','maximum_fields=36000')
old="   else press(side,'Down');if frame%22<4 then press(side,'Low Kick')end end"
assert source.count(old)==1
source=source.replace(old,"   else if frame%40<4 then press(side,'High Kick')end end")
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
runner=(base/'run_kano_p1.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/stage.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua))
runner=runner.replace('audit_current_native_tomb_kano_p1_runtime','audit_current_native_pit_kano_p1_runtime')
runner=runner.replace("MK2KS_STAGE_ARENA='1'","MK2KS_STAGE_ARENA='6'").replace("'-str','400'","'-str','900'")
(out/'run_kano_p1.ps1').write_text(runner)
print('Prepared physical HK/paid-rematch Pit attempt, no media;90sec/320MiB/10MiB limits retained')
