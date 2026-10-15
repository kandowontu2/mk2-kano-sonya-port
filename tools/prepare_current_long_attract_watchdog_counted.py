"""Count routine executions without per-instruction log flooding."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_long_attract_watchdog_preparation'
out=sync.ROOT/'audit_current_long_attract_watchdog_counted_preparation'
assert not out.exists()
source=(base/'attract.lua').read_text()
start=source.index("taps[#taps+1]=p:install_read_tap(0xff904f80")
source=source[:start]+'''
local watchdog_count=0
taps[#taps+1]=p:install_read_tap(0xff904f80,0xff904f9f,'passive watchdog execution count',function(at,data,mask)
 if cpu.PC.value==0xff904f90 then watchdog_count=watchdog_count+1 end
end)
emu.register_frame_done(function()
 if frame%600==0 then log('WATCHDOG_COUNT','executions='..watchdog_count)end
end)
'''
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'attract.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/attract.lua',out.name+'/attract.lua').replace(sync.sha(base/'attract.lua'),sync.sha(lua)).replace('audit_current_long_attract_watchdog_runtime','audit_current_long_attract_watchdog_counted_runtime')
(out/'run.ps1').write_text(runner)
print('Countedobserver; same135000fields/180sec/320MiB/10MiB/no media')
