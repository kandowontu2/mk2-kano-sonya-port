-- Original-game controls unchanged; sound-port and caller observation only.
local family=assert(os.getenv('MK3_AUDIO_FAMILY'))
local sources={choke='mk3_choke_reference.lua',leg='mk3_leggrab_reference.lua',bicycle='mk3_bicycle_reference.lua'}
dofile(assert(sources[family]))
local frame,tap=0,nil
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  local cpu=manager.machine.devices[':maincpu'];local p=cpu.spaces.program
  tap=p:install_write_tap(0x01680000,0x0168001f,'original special actual sound',function(at,data,mask)
   if at==0x01680000 and mask&255~=0 and frame>=3890 and frame<=4200 then
    local stack={};for i=0,7 do stack[#stack+1]=string.format('%08X',p:read_u32(cpu.state.SP.value+i*32))end
    print(string.format('MK3_SPECIAL_AUDIO_SOUND frame=%d family=%s seconds=%.12f byte=%02X mask=%04X pc=%08X a8=%08X a13=%08X callers=%s writes=0 assistance=none',frame,family,emu.time(),data&255,mask,cpu.state.PC.value,cpu.state.A8.value,cpu.state.A13.value,table.concat(stack,',')))
   end
  end)
 end
 if frame==4651 then manager.machine:exit()end
end)
emu.register_stop(function()
 print(string.format('MK3_SPECIAL_AUDIO_RESULT frame=%d family=%s seconds=%.12f writes=0 assistance=none',frame,family,emu.time()))
 if tap then tap:remove()end
end)
