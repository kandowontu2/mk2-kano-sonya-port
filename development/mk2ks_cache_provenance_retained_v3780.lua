-- Read-only native Mileena victim/cache provenance; retain every tap handle.
assert(not rawget(_G,'MK2_CACHE_PROVENANCE_V3780_ACTIVE'))
rawset(_G,'MK2_CACHE_PROVENANCE_V3780_ACTIVE',true)
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,records,bad,busy=0,0,nil,false
local taps={}
local minimum=tonumber(os.getenv('MK2KS_PROVENANCE_MIN_FRAME')or'0')
local function valid(a) return a>=0x01000000 and a<0x01100000 end
local function victim()
 local a=cpu.A8.value
 return valid(a) and p:read_u16(a+0x1f0)>=17 and p:read_u16(a+0x1f0)<=18
end
local function log(tag,detail)
 print(string.format('MK2_CACHE_V3780_%s frame=%d seconds=%.9f pc=%08X a0=%08X a1=%08X a5=%08X a6=%08X a7=%08X a8=%08X a9=%08X a13=%08X writes=0 assistance=none %s',
  tag,frame,manager.machine.time:as_double(),cpu.PC.value,cpu.A0.value,cpu.A1.value,cpu.A5.value,cpu.A6.value,cpu.A7.value,cpu.A8.value,cpu.A9.value,cpu.A13.value,detail or''))
end
local function words(a,n)
 if a<0xff000000 or a>0xffffffff-n*32 then return 'outside_rom' end
 local result={}
 for i=0,n-1 do result[#result+1]=string.format('%08X',p:read_u32(a+i*32)) end
 return table.concat(result,',')
end
local function scoped() return frame>=minimum and p:read_u16(0x01061b00)==3 end
taps[#taps+1]=p:install_read_tap(0xff9060a0,0xff9060af,'owned native animation lookup',function(at)
 if busy or at~=0xff9060a0 or not scoped() or not victim() or records>=150 then return end
 busy=true;records=records+1;log('ANIMATION','requested='..cpu.A9.value);busy=false
end)
taps[#taps+1]=p:install_read_tap(0xff8387a0,0xff8387af,'owned native composite cache entry',function(at)
 if busy or at~=0xff8387a0 or not scoped() or not victim() or records>=200 then return end
 busy=true;records=records+1
 log('GROUP',string.format('group=%s cache=%08X pose=%08X',words(cpu.A0.value,12),p:read_u32(cpu.A8.value+0x1a0),p:read_u32(cpu.A8.value+0x1d0)))
 busy=false
end)
taps[#taps+1]=p:install_read_tap(0xff9e9140+17*32,0xff9e9140+19*32-1,'actual unextended victim rows',function(at,data,mask)
 if busy or not scoped() or not victim() then return end
 busy=true;log('ROW',string.format('at=%08X data=%04X mask=%04X row=%d id=%d',at,data&0xffff,mask,(at-0xff9e9140)//32,p:read_u16(cpu.A8.value+0x1f0)));busy=false
end)
taps[#taps+1]=p:install_read_tap(0xff9e7d70,0xff9e7d7f,'actual native eaten victim task',function(at)
 if busy or at~=0xff9e7d70 or not victim() then return end
 busy=true;log('EATEN_TASK','id='..p:read_u16(cpu.A8.value+0x1f0));busy=false
end)
taps[#taps+1]=p:install_write_tap(0x01060000,0x01061fff,'actual global cache overrun',function(at,data,mask)
 if busy or cpu.PC.value~=0xff838860 then return end
 busy=true;if not bad then bad=frame end
 if records<230 then records=records+1;log('OVERRUN',string.format('at=%08X data=%04X mask=%04X group=%s descriptor=%s',at,data&0xffff,mask,words(cpu.A0.value,8),words(cpu.A5.value,6)))end
 busy=false
end)
emu.register_frame(function() assert(#taps==5,'Retain native tap userdata throughout capture');frame=frame+1 end)
emu.register_frame_done(function()
 if bad and frame>=bad+40 then log('HOST_EXIT','bad_frame='..bad..' records='..records);manager.machine:exit()end
end)
emu.register_stop(function() log('RESULT','bad_frame='..(bad or-1)..' records='..records);for _,tap in ipairs(taps)do tap:remove()end end)
