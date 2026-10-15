"""Extend passive attract beyond historical reset frontier, without scene writes."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_ending_scene_operands_preparation'
out=sync.ROOT/'audit_current_long_attract_watchdog_preparation'
assert not out.exists()
source=(base/'attract.lua').read_text()
assert source.count('frame>=700')==1
source=source.replace('frame>=700','frame>=135000').replace('maximum_fields=700','maximum_fields=135000').replace('frame%60==0','frame%600==0')
source+='''
taps[#taps+1]=p:install_read_tap(0xff904f80,0xff904f9f,'passive historical watchdog instruction',function(at,data,mask)
 if cpu.PC.value==0xff904f90 then
  log('WATCHDOG_FRONTIER',string.format('at=%08X pc=%08X mode=%d counter=%d',at,cpu.PC.value,p:read_u16(0x010601d0),p:read_u16(0x01061ca0)))
 end
end)
'''
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'attract.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/attract.lua',out.name+'/attract.lua').replace(sync.sha(base/'attract.lua'),sync.sha(lua)).replace('audit_current_ending_scene_operands_runtime','audit_current_long_attract_watchdog_runtime').replace("'-frameskip','0'","'-frameskip','10'").replace("'-str','400'","'-str','2500'").replace('TotalSeconds -gt 90','TotalSeconds -gt 180')
(out/'run.ps1').write_text(runner)
print('135000field attract;180sec/320MiB/10MiB/no media/guestwrites')
