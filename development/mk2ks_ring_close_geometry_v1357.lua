-- Add actual native collision rectangles to the unchanged physical uppercut,
-- retry and full-display observers. No guest writes or synthetic collisions.
dofile('mk2ks_human_ring_close_display_v1356.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local side=assert(tonumber(os.getenv('MK2KS_HUMAN_SPECIAL_SIDE')))
local frame,taps=0,{}
emu.register_frame(function()frame=frame+1 end)
taps[#taps+1]=p:install_read_tap(0xff835b70,0xff835b7f,'native ring startup/travel rectangles',function(at)
 if at~=0xff835b70 or cpu.PC.value~=0xff835b80 or frame<1500 then return end
 local a,m=cpu.A8.value,cpu.A13.value
 if a<0x01000000 or a>=0x01100000 or m<0x01000000 or m>=0x01100000 then return end
 local own=p:read_u32(side==1 and 0x01060220 or 0x01060df0)
 if a==own or p:read_u16(a+0x1f0)~=18 or p:read_u32(m+0x230)~=own then return end
 local descriptor=p:read_u32(m+0x100)
 print(string.format('MK2_NAT_CAMPAIGN_FLOOR_PROJECTILE_RECT frame=%d human_slot=%d fighter=sonya writes=0 assistance=none actor=%08X main=%08X parent=%08X descriptor=%08X edge=%d top=%d width=%d height=%d victim_min=%08X victim_max=%08X attack_min=%08X attack_max=%08X x=%d y=%d pc=%08X',
  frame,side,a,m,own,descriptor,p:read_i16(descriptor),p:read_i16(descriptor+16),p:read_u16(descriptor+32),p:read_u16(descriptor+48),cpu.A2.value,cpu.A3.value,cpu.A4.value,cpu.A5.value,p:read_i16(a+0x90),p:read_i16(a+0xb0),cpu.PC.value))
end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
