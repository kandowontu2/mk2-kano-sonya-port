-- One original physical controller, full original19-channel PCM/DAC/ROM.
-- Correct only the passive shadow observer's true17-human/18-CPU filters.
local original_dofile=dofile
local function replace(source,before,after)
 local first,last=assert(source:find(before,1,true))
 assert(not source:find(before,last+1,true),'One exact passive boundary')
 return source:sub(1,first-1)..after..source:sub(last+1)
end
dofile=function(path)
 if path~='mk2ks_native_selector_cpu_guard_shadow.lua' then return original_dofile(path) end
 local file=assert(io.open(path,'rb'));local source=file:read('a'):gsub('\r\n','\n');file:close()
 source=replace(source,'a.id==17 and b.id==17 and','a.id==17 and b.id==18 and')
 source=replace(source,'a.roster==17 and b.roster==17 and','a.roster==17 and b.roster==18 and')
 local marker=']==]\nroot=root:sub(1,first-1)'
 local additions=[==[
change('a.id==17 and b.id==17 and a.roster==17 and b.roster==17',
       'a.id==17 and b.id==18 and a.roster==17 and b.roster==18')
change('own.id~=17 or own.roster~=17','own.id~=18 or own.roster~=18')
change("{{'knife',0xffffb000},{'ball',0xffffde00},\n                     {'blade',0xfff8cc00},{'choke',0xfff91400}}",
       "{{'ring',0xffffb400},{'square',0xffffca00},\n                     {'bicycle',0xfff9a400},{'leg',0xfff80800}}")
]==]
 source=replace(source,marker,additions..'\n'..marker)
 return assert(load(source,'@whole_passive_true17_18_shadow_and_sonya_phase_windows','t',_G))()
end
original_dofile('mk2ks_native_selector_cpu_projectile_pcm_startup_direct.lua')
dofile=original_dofile
-- Preserve Kano-only choice result, add entire original actual Sonya observer.
local file=assert(io.open('mk2ks_native_selector_sonya_cpu_choices.lua','rb'))
local source=file:read('a'):gsub('\r\n','\n');file:close()
source=replace(source,"dofile('mk2ks_native_selector_cpu_first_round_projectile.lua')",'')
assert(load(source,'@whole_sonya_native_choice_observer_no_second_controller','t',_G))()
-- Independent native fall-instruction provenance, never synthesized from pose.
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local taps={};local frame=0
emu.register_frame(function()frame=frame+1 end)
for _,item in ipairs({{'fall',0xff876660},{'landing',0xff876420}})do
 taps[#taps+1]=p:install_read_tap(item[2],item[2]+15,'actual owned Sonya '..item[1],function(at,data,mask)
  if at~=item[2] or cpu.PC.value~=at+16 then return end
  local a,m=cpu.A8.value,cpu.A13.value
  if a~=p:read_u32(0x01060df0) or m~=p:read_u32(0x01060e30) or
     a<0x01000000 or a>=0x01100000 or m<0x01000000 or m>=0x01100000 or
     p:read_u16(a+0x1f0)~=18 or p:read_u32(m+0xc0)~=a then return end
  print(string.format('MK2_SONYA_NATIVE_FALL frame=%d kind=%s entry=%08X pc=%08X opcode=%04X mask=%04X actor=%08X main=%08X owner=%08X id=18 action=%04X a0=%08X a1=%08X a2=%08X a3=%08X a6=%08X writes=0 assistance=none',
   frame,item[1],at,cpu.PC.value,data&65535,mask,a,m,p:read_u32(m+0xc0),p:read_u16(m+0x1f0),
   cpu.A0.value,cpu.A1.value,cpu.A2.value,cpu.A3.value,cpu.A6.value))
 end)
end
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
