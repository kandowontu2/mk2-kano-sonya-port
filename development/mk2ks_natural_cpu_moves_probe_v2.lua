-- Add read-only actual native caller provenance to the existing natural CPU probe.
dofile('mk2ks_natural_cpu_moves_probe.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,taps=0,{}
emu.register_frame(function() frame=frame+1 end)
taps[#taps+1]=p:install_read_tap(0xff838790,0xff83879f,'CPU body animation native callers',function(at)
 if at~=0xff838790 or cpu.PC.value~=0xff8387a0 then return end
 local actor,main=p:read_u32(0x01060df0),p:read_u32(0x01060e30)
 if actor<0x01000000 or actor>=0x01100000 or main<0x01000000 or main>=0x01100000 then return end
 if cpu.A8.value~=actor or cpu.A13.value~=main or p:read_u16(0x01060dc0)~=0 then return end
 local id=p:read_u16(actor+0x1f0)
 if id~=17 and id~=18 then return end
 print(string.format('MK2_NAT_CPU_CANCEL_DRAW frame=%d actor=%08X main=%08X id=%d action=%04X group=%08X pc=%08X sp=%08X callers=%08X,%08X,%08X,%08X writes=0',
  frame,actor,main,id,p:read_u16(main+0x1f0),cpu.A0.value,cpu.PC.value,cpu.SP.value,
  p:read_u32(cpu.SP.value),p:read_u32(cpu.SP.value+32),p:read_u32(cpu.SP.value+64),p:read_u32(cpu.SP.value+96)))
end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
