-- Whole4542/2062 renderer, actual4613 hardware and read-only raster clocks.
local h=assert(io.open('mk2ks_ending_display_ram_v4542.lua','r'))
local source=h:read('a');h:close()
local boundary="assert(not source:find('io.open',1,true)"
local addition=[=[
once("log('FLOOR_DISPLAY',", "log('FLOOR_SCANOUT',string.format('epoch=1 start=%04X dpyadr=%04X control=%04X tap=%04X vcount=%d vsblnk=%d veblnk=%d',p:read_u16(0xc0000090),p:read_u16(0xc00001e0),p:read_u16(0xc0000080),p:read_u16(0xc00001b0),p:read_u16(0xc00001d0),p:read_u16(0xc0000060),p:read_u16(0xc0000050)))\n log('FLOOR_DISPLAY',")
once('local frame,command,ending_completed,ending_ko,own_wins,seen_live=0,nil,nil,nil,0,false',
 'local raster_clock\nlocal frame,command,ending_completed,ending_ko,own_wins,seen_live=0,nil,nil,nil,0,false')
once('emu.register_frame(function()frame=frame+1 end)',
 "emu.register_frame(function()frame=frame+1;if raster_clock then raster_clock('field')end end)")
once('local function next_event()event=event+1;return event end',
 "local function next_event()raster_clock('before');event=event+1;return event end")
once('-- Observe the original shift-register clear, not an inferred erase rectangle.',[[
local raster_last,raster_sequence=nil,0
raster_clock=function(reason)
 if not active()then return end
 local beam=p:read_u16(0xc00001d0)
 local start,address,control,tap=p:read_u16(0xc0000090),p:read_u16(0xc00001e0),p:read_u16(0xc0000080),p:read_u16(0xc00001b0)
 local first,last,total=p:read_u16(0xc0000050),p:read_u16(0xc0000060),p:read_u16(0xc0000070)
 local key=string.format('%d_%d_%d_%04X_%04X_%04X_%04X_%d_%d_%d',frame,screen:frame_number(),beam,start,address,control,tap,first,last,total)
 if key==raster_last and reason=='before'then return end
 raster_last=key;raster_sequence=raster_sequence+1
 local seconds=manager.machine.time:as_double()
 log('FLOOR_RASTER_CLOCK',string.format('epoch=1 sequence=%d next_event=%d reason=%s start=%04X dpyadr=%04X control=%04X tap=%04X vcount=%d vsblnk=%d veblnk=%d vtotal=%d seconds=%.15f next_vblank=%.15f scan_period=%.15f frame_period=%.15f',
  raster_sequence,event+1,reason,start,address,control,tap,beam,last,first,total,seconds,seconds+screen:time_until_pos(last),screen.scan_period,screen.frame_period))
end
-- Observe the original shift-register clear, not an inferred erase rectangle.
]])
once('command=frame;origin=frame;ensure_base()',"command=frame;origin=frame;ensure_base();raster_clock('begin')")
once('emu.register_frame_done(function()\n if not active()then return end',
 "emu.register_frame_done(function()\n if not active()then return end\n raster_clock('finish')")
]=]
local first,last=assert(source:find(boundary,1,true))
assert(not source:find(boundary,last+1,true),'Unique whole read-only ending adapter boundary')
source=source:sub(1,first-1)..addition..source:sub(first)
assert(load(source,'@whole4542_actual_hardware_and_operation_clock_RAM_4706','t',_ENV))()
