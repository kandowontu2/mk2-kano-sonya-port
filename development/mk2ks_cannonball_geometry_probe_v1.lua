-- Read-only geometry/pose correlation over the unchanged real-input fixture.
-- Images are callback snapshots, not a claim of instruction-time raster state.
dofile('mk2ks_human_special_negative_v9.lua')
local cpu=manager.machine.devices[':maincpu']
local p,r=cpu.spaces.program,cpu.state
local screen=manager.machine.screens[':screen']
local side=assert(tonumber(os.getenv('MK2KS_HUMAN_SPECIAL_SIDE')))
local slots={{0x01060220,0x01060260},{0x01060df0,0x01060e30}}
local frame,pending,taps=0,nil,{}
emu.register_frame(function()
 frame=frame+1
 if pending then
  local name=string.format('ball_geometry_%04d.png',pending)
  screen:snapshot(name)
  print(string.format('MK2_BALL_DETAIL_SNAPSHOT callback=%d comparison=%d file=%s writes=0',frame,pending,name))
  pending=nil
 end
end)
taps[#taps+1]=p:install_read_tap(0xff835b70,0xff835b7f,'native ball pose and geometry detail',function(at)
 if at~=0xff835b70 or r.PC.value~=0xff835b80 then return end
 local own,main=p:read_u32(slots[side][1]),p:read_u32(slots[side][2])
 if own~=r.A8.value or main~=r.A13.value or p:read_u16(main+0x1f0)~=0x20b then return end
 local victim,vm=p:read_u32(slots[3-side][1]),p:read_u32(slots[3-side][2])
 print(string.format('MK2_BALL_DETAIL frame=%d side=%d actor=%08X main=%08X pose=%08X list=%08X x=%d y=%d floor=%d victim=%08X victim_main=%08X victim_pose=%08X victim_list=%08X victim_x=%d victim_y=%d victim_floor=%d victim_flags=%04X victim_body=%04X victim_min=%08X victim_max=%08X attack_min=%08X attack_max=%08X pc=%08X writes=0',
  frame,side,own,main,p:read_u32(own+0x1d0),p:read_u32(main+0x170),p:read_i16(own+0x90),p:read_i16(own+0xb0),p:read_i16(main+0x200),
  victim,vm,p:read_u32(victim+0x1d0),p:read_u32(vm+0x170),p:read_i16(victim+0x90),p:read_i16(victim+0xb0),p:read_i16(vm+0x200),
  p:read_u16(vm+0x210),p:read_u16(victim+0x160),r.A2.value,r.A3.value,r.A4.value,r.A5.value,r.PC.value))
 pending=frame
end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
