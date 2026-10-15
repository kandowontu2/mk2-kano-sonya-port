-- Same actual forward-jump-kick inputs as v1648; native hitbox reads only.
dofile('mk2ks_launch_interruption_v1648.lua')
local frame,tap=0,nil
local cpu=manager.machine.devices[':maincpu']
local p=cpu.spaces.program
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  tap=p:install_read_tap(0xff835440,0xff83544f,'actual original hit descriptor',function(at)
   if at~=0xff835440 or cpu.state.PC.value~=0xff835450 or frame<1570 or frame>1595 then return end
   local actor,main,descriptor=cpu.state.A8.value,cpu.state.A13.value,cpu.state.A0.value
   if actor<0x01000000 or actor>=0x01100000 or main<0x01000000 or main>=0x01100000 then return end
   local words={}
   if descriptor>=0xff800000 then
    for n=0,8 do words[#words+1]=string.format('%04X',p:read_u16(descriptor+n*16))end
   end
   print(string.format('MK2_NATIVE_COUNTER_DESCRIPTOR frame=%d at=%08X pc=%08X actor=%08X main=%08X owner=%08X id=%d descriptor=%08X words=%s writes=0 assistance=none',frame,at,cpu.state.PC.value,actor,main,p:read_u32(main+0xc0),p:read_u16(actor+0x1f0),descriptor,table.concat(words,',')))
  end)
 end
end)
emu.register_stop(function()if tap then tap:remove()end end)
