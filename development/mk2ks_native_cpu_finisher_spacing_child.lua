-- Independent passive object link, not an assumption about the saved A8 value.
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,started=0,nil
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local tap=p:install_read_tap(0xfffaae00,0xfffaae0f,'readonly exact true CPU finisher child provenance',function(at)
 if at~=0xfffaae00 or cpu.PC.value~=0xfffaae10 or started then return end
 local a,m=p:read_u32(0x01060df0),p:read_u32(0x01060e30)
 if valid(a)and valid(m)and cpu.A8.value==a and cpu.A13.value==m and
  p:read_u16(a+0x1f0)==17 and p:read_u16(0x01060e50)==17 and
  p:read_u16(0x010601d0)==2 and p:read_u16(0x01060dc0)==0 then started=frame end
end)
emu.register_frame_done(function()
 frame=frame+1
 if not started or frame-started>330 then return end
 local a,m=p:read_u32(0x01060df0),p:read_u32(0x01060e30)
 if not valid(a)or not valid(m)or p:read_u16(a+0x1f0)~=17 or p:read_u16(0x01060e50)~=17 then return end
 local child=p:read_u32(m+0x190);local exists=valid(child)
 print(string.format('MK2_FINISH_CHILD_FIELD frame=%d age=%d mode=%d k_actor=%08X k_main=%08X saved_a8=%08X child=%08X child_valid=%d child_x=%d child_y=%d child_pose=%08X child_body=%04X child_bank=%04X k_x=%d k_y=%d k_body=%04X k_bank=%04X writes=0 assistance=none',
 frame,frame-started,p:read_u16(0x010601d0),a,m,p:read_u32(m+0xc0),child,exists and 1 or 0,
 exists and p:read_i16(child+0x90)or -32768,exists and p:read_i16(child+0xb0)or -32768,
 exists and p:read_u32(child+0x1d0)or 0,exists and p:read_u16(child+0x160)or 0,
 exists and p:read_u16(child+0x140)or 0,p:read_i16(a+0x90),p:read_i16(a+0xb0),
 p:read_u16(a+0x160),p:read_u16(a+0x140)))
end)
emu.register_stop(function()tap:remove()end)
dofile('mk2ks_native_cpu_finisher_spacing.lua')
