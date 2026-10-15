-- The causal replay's ordinary physical inputs remain unchanged.
-- Stop after an observed owned finish and native winner handoff, not an assumed timeout victory.
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,started,completed,busy=0,nil,nil,false
local taps={}
local function owns_kano()
 local a=cpu.A8.value
 return a>=0x01000000 and a<0x01100000 and p:read_u16(a+0x1f0)==17 and
  p:read_u32(0x01060df0)==a and p:read_u16(0x01060e50)==17 and
  p:read_u16(0x010601d0)==2 and p:read_u16(0x010601f0)==1 and p:read_u16(0x01060280)==18
end
local function log(tag)
 print(string.format('MK2_FINISH_DISPATCH_REGRESSION_%s frame=%d pc=%08X actor=%08X main=%08X id=%d roster=%d health=%d,%d mode=%d state=%d a0=%08X a1=%08X writes=0 assistance=none',
 tag,frame,cpu.PC.value,cpu.A8.value,cpu.A13.value,p:read_u16(cpu.A8.value+0x1f0),
 p:read_u16(0x01060e50),p:read_u16(0x010602f0),p:read_u16(0x01060ec0),
 p:read_u16(0x010601d0),p:read_u16(0x01060dc0),cpu.A0.value,cpu.A1.value))
end
taps[#taps+1]=p:install_read_tap(0xff83b850,0xff83b85f,'readonly repaired real-ID finish lookup result',function(at)
 if busy or at~=0xff83b850 or cpu.PC.value~=0xff83b860 or not owns_kano()then return end
 if cpu.A1.value==0xfffa1900 or cpu.A1.value==0xfffa1b60 then
  busy=true;log('LOOKUP');busy=false
 end
end)
for _,entry in ipairs({{0xfffaae00,'OWN_FINISH'},{0xffa14860,'WINNER_HANDOFF'},
 {0xff8d2410,'WRONG_MILEENA_ENTRY'}})do
 local at,kind=entry[1],entry[2]
 taps[#taps+1]=p:install_read_tap(at,at+15,'readonly owned CPU finisher regression',function(address)
  if busy or address~=at or cpu.PC.value~=at+16 or not owns_kano()then return end
  busy=true
  if kind=='OWN_FINISH' and not started then started=frame;log(kind)
  elseif kind=='WINNER_HANDOFF' and started and not completed then completed=frame;log(kind)
  elseif kind=='WRONG_MILEENA_ENTRY'then log(kind);manager.machine:exit()end
  busy=false
 end)
end
local function image(age)
 local screen=manager.machine.screens[':screen'];local raw,w,h=screen:pixels()
 assert(w==400 and h==254 and #raw==406400)
 local hex=raw:gsub('.',function(c)return string.format('%02X',string.byte(c))end)
 print(string.format('MK2_CAMPAIGN_RAM_FRAME filename=postjoin_finisher_regression_age%d.png seconds=%.9f width=400 height=254 bytes=406400 hex=%s',
 age,manager.machine.time:as_double(),hex))
end
emu.register_frame_done(function()
 frame=frame+1;assert(#taps==4,'All passive finish handoff taps retained')
 if started then
  local age=frame-started
  if age==1 or age==30 or age==90 or age==180 or age==330 or age==900 then image(age)end
  if completed and age>=900 then log('STOP');manager.machine:exit()end
 end
end)
emu.register_stop(function()
 print(string.format('MK2_FINISH_DISPATCH_REGRESSION_RESULT frame=%d started=%d completed=%d writes=0 assistance=none',frame,started or -1,completed or -1))
 for _,tap in ipairs(taps)do tap:remove()end
end)
dofile('mk2ks_native_cpu_kano_finish_lookup_cause.lua')
