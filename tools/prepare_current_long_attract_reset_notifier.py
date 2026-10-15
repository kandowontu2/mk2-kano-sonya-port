"""Observe actual reset notification, not ordinary graphics-copy execution."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_long_attract_watchdog_preparation'
out=sync.ROOT/'audit_current_long_attract_reset_notifier_preparation'
assert not out.exists()
source=(base/'attract.lua').read_text()
start=source.index("taps[#taps+1]=p:install_read_tap(0xff904f80")
source=source[:start]+'''
local observed_resets=0
emu.register_start(function()
 observed_resets=observed_resets+1
 log('ACTUAL_RESET_NOTIFY',string.format('count=%d pc=%08X mode=%d',observed_resets,cpu.PC.value,p:read_u16(0x010601d0)))
end)
'''
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'attract.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/attract.lua',out.name+'/attract.lua').replace(sync.sha(base/'attract.lua'),sync.sha(lua)).replace('audit_current_long_attract_watchdog_runtime','audit_current_long_attract_reset_notifier_runtime')
(out/'run.ps1').write_text(runner)
print('Actualresetnotifier135000fields;180sec/320MiB/10MiB/no media/guestwrites')
