-- Whole current startup/guard/body/child/pool/control chain, no game writes.
dofile('mk2ks_native_selector_cpu_startup_guard.lua')
-- Capture actual executing first-round projectile phases even when the
-- original live predicate is false at the native mode7-to2 entry boundary.
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,serial=0,0
local taps,marks={},{}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
for _,item in ipairs({{'knife',0xffffb000},{'ring',0xffffb400}})do
 taps[#taps+1]=p:install_read_tap(item[2],item[2]+15,'actual round-start projectile raster',function(at,data,mask)
  if at~=item[2]or cpu.PC.value~=at+16 then return end
  local a,m=cpu.A8.value,cpu.A13.value
  if not valid(a)or not valid(m)then return end
  serial=serial+1
  print(string.format('MK2_FIRST_PROJECTILE_ENTRY frame=%d serial=%d kind=%s actor=%08X main=%08X owner=%08X id=%d mode=%d opcode=%04X mask=%04X writes=0 assistance=none',
   frame,serial,item[1],a,m,p:read_u32(m+0xc0),p:read_u16(a+0x1f0),p:read_u16(0x010601d0),data&0xffff,mask))
  for _,age in ipairs({0,3,6,9,12,16,20,24,28,32,40,48,49,50,64})do
   marks[frame+age]=string.format('first_projectile_%s_%d_age%d',item[1],serial,age)
  end
 end)
end
emu.register_frame(function()frame=frame+1 end)
emu.register_frame_done(function()
 local label=marks[frame]
 if not label then return end
 marks[frame]=nil
 local raw,w,h=manager.machine.screens[':screen']:pixels()
 assert(w==400 and h==254 and #raw==406400)
 local hex=raw:gsub('.',function(c)return string.format('%02X',c:byte())end)
 print(string.format('MK2_KNIFE_RAM_RGB frame=%d label=%s width=%d height=%d bytes=%d hex=%s',frame,label,w,h,#raw,hex))
end)
emu.register_stop(function()
 for _,tap in ipairs(taps)do tap:remove()end
 print(string.format('MK2_FIRST_PROJECTILE_RESULT frame=%d observed_entries=%d writes=0 assistance=none',frame,serial))
end)
