"""Retire combat taps after verified return; preserve physical prefix."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_smoke_long_idle_preparation'
out=sync.ROOT/'audit_current_sonya_smoke_long_idle_detached_preparation'
assert not out.exists()
source=(base/'stage.lua').read_text()
old=";long_idle=true end"
assert source.count(old)==1
source=source.replace(old,";long_idle=true;for _,tap in ipairs(taps)do tap:remove()end;taps={};flush_log() end")
source=source.replace("cpu.PC.value))end\n  return","cpu.PC.value));flush_log()end\n  return")
source=source.replace('if accepted and frame%(long_idle and 600 or 120)==0 then','if not long_idle and accepted and frame%120==0 then')
source+='''
emu.register_start(function()
 if frame>1 then log('ACTUAL_RESET_NOTIFY',string.format('pc=%08X mode=%d',cpu.PC.value,p:read_u16(0x010601d0)));flush_log()end
end)
'''
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/stage.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua)).replace('audit_current_sonya_smoke_long_idle_runtime','audit_current_sonya_smoke_long_idle_detached_runtime')
(out/'run.ps1').write_text(runner)
print('Combat taps retire afterreturn;135000fields/180sec/320MiB/10MiB/no media')
