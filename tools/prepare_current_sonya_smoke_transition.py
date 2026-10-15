"""Extend the earned secret controls, then release inputs for native match end."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_toasty_72_cadence_preparation'
out=sync.ROOT/'audit_current_sonya_smoke_transition_preparation'
assert not out.exists()
source=(base/'stage.lua').read_text()
def change(old,new):
    global source
    assert source.count(old)==1,old
    source=source.replace(old,new)
change('local walked,jumped,punched=false,false,false','local walked,jumped,punched=false,false,false\nlocal controls_done,returned=nil,nil')
change(' if accepted then\n  if mode~=2 then',' if accepted then\n  if not controls_done then\n  if mode~=2 then')
change("log('SECRET_COMPLETE','epoch='..epoch..' recovered='..recovered..' human='..h.id..' cpu='..v.id..' arena='..arena);manager.machine:exit()",
       "log('SECRET_COMPLETE','epoch='..epoch..' recovered='..recovered..' human='..h.id..' cpu='..v.id..' arena='..arena);controls_done=frame")
change("  if h and v then log('SECRET_FIELD'", "  end\n  if h and v then log('SECRET_FIELD'")
change(' if not accepted and mode==2 and pending', ''' if controls_done and arena~=9 and mode==2 and h and v then
  if not returned then
   returned=frame;log('SECRET_RETURN',string.format('mode=%d arena=%d ids=%d,%d rosters=%d,%d states=%d,%d actors=%08X,%08X owners=%08X,%08X mains=%08X,%08X hp=%d,%d',
    mode,arena,h.id,v.id,h.roster,v.roster,h.state,v.state,h.actor,v.actor,h.owner,v.owner,h.main,v.main,h.hp,v.hp))
  end
  if frame-returned>=180 then log('SECRET_RETURN_COMPLETE','start='..returned..' mode='..mode..' arena='..arena);manager.machine:exit()end
 end
 if not accepted and mode==2 and pending''')
source+='''
local watchdog_time,watchdog_pc=emu.time(),0
local decoder_observed=false
taps[#taps+1]=p:install_write_tap(0x01d81060,0x01d8107f,'passive native watchdog provenance',function(at,data,mask)
 watchdog_time,watchdog_pc=emu.time(),cpu.PC.value
 if accepted and cpu.PC.value==0xff904f80 and not decoder_observed then
  decoder_observed=true
  log('SECRET_DECODER_WATCHDOG',string.format('pc=%08X a1=%08X a2=%08X a3=%08X a7=%08X a11=%08X stack=%08X task=%08X',cpu.PC.value,cpu.A1.value,cpu.A2.value,cpu.A3.value,cpu.A7.value,cpu.A11.value,cpu.A12.value,cpu.A13.value))
 end
end)
emu.register_prestart(function()
 if frame>1 then log('SECRET_NATIVE_RESET',string.format('pc=%08X mode=%d watchdogPC=%08X elapsed=%.9f',cpu.PC.value,p:read_u16(0x010601d0),watchdog_pc,emu.time()-watchdog_time))end
end)
emu.register_frame_done(function()
 if accepted and frame%120==0 then log('SECRET_POST_STATE',string.format('mode=%d arena=%d rosters=%d,%d states=%d,%d hp=%d,%d pc=%08X watchdogPC=%08X watchdogElapsed=%.9f',
  p:read_u16(0x010601d0),p:read_u16(0x01061ac0),p:read_u16(slots[1].roster),p:read_u16(slots[2].roster),p:read_u16(slots[1].state),p:read_u16(slots[2].state),p:read_u16(slots[1].hp),p:read_u16(slots[2].hp),cpu.PC.value,watchdog_pc,emu.time()-watchdog_time))end
end)
'''
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/stage.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua)).replace('audit_current_sonya_toasty_72_cadence_runtime','audit_current_sonya_smoke_transition_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared exact successful route through23797 then released physical inputs;28000fields/90sec/320MiB/no media')
