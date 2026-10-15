"""Retain earned secret controls/return, then release buttons for long idle."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_smoke_transition_batched_preparation'
out=sync.ROOT/'audit_current_sonya_smoke_long_idle_preparation'
assert not out.exists()
source=(base/'stage.lua').read_text()
source='local long_idle=false\n'+source
source=source.replace('frame>=28000','frame>=135000').replace('maximum_fields=28000','maximum_fields=135000')
old=' for n=1,2 do for _,field in pairs(buttons[n])do field:clear_value()end end'
assert source.count(old)==1
source=source.replace(old,old+'''
 if long_idle then
  if frame%600==0 then log('LONG_IDLE',string.format('mode=%d arena=%d counter=%d pc=%08X',p:read_u16(0x010601d0),p:read_u16(0x01061ac0),p:read_u16(0x01061ca0),cpu.PC.value))end
  return
 end
''')
old="if frame-returned>=180 then log('SECRET_RETURN_COMPLETE','start='..returned..' mode='..mode..' arena='..arena);manager.machine:exit()end"
assert source.count(old)==1
source=source.replace(old,"if frame-returned>=180 then log('SECRET_RETURN_COMPLETE','start='..returned..' mode='..mode..' arena='..arena);long_idle=true end")
# Preserve existing reset provenance; coarsen only post-return passive periodic data.
source=source.replace('if accepted and frame%120==0 then','if accepted and frame%(long_idle and 600 or 120)==0 then')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/stage.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua)).replace('audit_current_sonya_smoke_transition_batched_runtime','audit_current_sonya_smoke_long_idle_runtime').replace("'-frameskip','0'","'-frameskip','10'").replace("'-str','900'","'-str','2500'").replace('TotalSeconds -gt 90','TotalSeconds -gt 180')
(out/'run.ps1').write_text(runner)
print('EarnedSonyaSmoke then releasedidle;135000fields/180sec/320MiB/10MiB/no media')
