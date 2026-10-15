-- Original cold Sonya P2 controls. Read-only cache/animation provenance.
if rawget(_G,'MK2_CACHE_PROVENANCE_V3776_ACTIVE') then return end
rawset(_G,'MK2_CACHE_PROVENANCE_V3776_ACTIVE',true)
local f=assert(io.open('mk2ks_natural_campaign_shao_ring_retreat_v3485.lua','r'))
local source=f:read('*a');f:close()
local adapted,count=source:gsub('screen:snapshot%(', '_diag_no_raster(')
assert(count==6,'Only six raster sinks replaced; original controls untouched')
local prefix=[[local function _diag_no_raster(name)
 print('MK2_CACHE_PROVENANCE_RASTER_SUPPRESSED filename='..name..' writes=0 assistance=none')
end
]]
assert(load(prefix..adapted,'@3485::six_raster_sinks_suppressed','t',_ENV))()
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local taps={}
local frame,bad,records,busy=0,nil,0,false
local function valid(a) return a>=0x01000000 and a<0x01100000 end
local function victim()
 local a=cpu.A8.value
 return valid(a) and p:read_u16(a+0x1f0)==18
end
local function log(tag,detail)
 print(string.format('MK2_CACHE_PROVENANCE_%s frame=%d seconds=%.9f pc=%08X a0=%08X a1=%08X a5=%08X a6=%08X a7=%08X a8=%08X a9=%08X a13=%08X writes=0 assistance=none %s',
  tag,frame,manager.machine.time:as_double(),cpu.PC.value,cpu.A0.value,cpu.A1.value,cpu.A5.value,cpu.A6.value,cpu.A7.value,cpu.A8.value,cpu.A9.value,cpu.A13.value,detail or''))
end
local function words(a,n)
 if a<0xff000000 or a>0xffffffff-n*32 then return 'outside_rom' end
 local result={}
 for i=0,n-1 do result[#result+1]=string.format('%08X',p:read_u32(a+i*32)) end
 return table.concat(result,',')
end
taps[#taps+1]=p:install_read_tap(0xff842da0,0xff842daf,'actual owned animation lookup',function(at)
 if busy or at~=0xff842da0 or not victim() or frame<220000 or records>=180 then return end
 busy=true;records=records+1
 log('ANIMATION','requested='..cpu.A9.value..' stack='..words(cpu.SP.value,6))
 busy=false
end)
taps[#taps+1]=p:install_read_tap(0xff8387a0,0xff8387af,'actual owned composite cache entry',function(at)
 if busy or at~=0xff8387a0 or not victim() or frame<223300 or records>=200 then return end
 busy=true;records=records+1
 log('GROUP',string.format('group=%s cache=%08X pose=%08X',words(cpu.A0.value,12),
  p:read_u32(cpu.A8.value+0x1a0),p:read_u32(cpu.A8.value+0x1d0)))
 busy=false
end)
taps[#taps+1]=p:install_write_tap(0x01060000,0x01061fff,'actual cache overrun provenance',function(at,data,mask)
 if busy or cpu.PC.value~=0xff838860 then return end
 busy=true
 if not bad then bad=frame end
 if records<230 then
  records=records+1
  log('OVERRUN',string.format('at=%08X data=%04X mask=%04X group=%s descriptor=%s',
   at,data&0xffff,mask,words(cpu.A0.value,8),words(cpu.A5.value,6)))
 end
 busy=false
end)
emu.register_frame(function() frame=frame+1 end)
emu.register_frame_done(function()
 if bad and frame>=bad+40 or manager.machine.time:as_double()>=4400 then
  log('HOST_EXIT','bad_frame='..(bad or-1)..' records='..records)
  manager.machine:exit()
 end
end)
emu.register_stop(function() log('RESULT','bad_frame='..(bad or-1)..' records='..records) end)
