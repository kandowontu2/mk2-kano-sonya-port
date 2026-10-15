-- Whole4706 observer; add read-only actual display-register stores.
local h=assert(io.open('mk2ks_ending_raster_clock_ram_v4706.lua','r'))
local source=h:read('a');h:close()
local boundary='\n]=]\nlocal first,last='
local addition=[=[
once('-- Observe the original shift-register clear, not an inferred erase rectangle.',[[
local raster_registers={[0xc0000080]='control',[0xc00001b0]='tap',[0xc00001e0]='dpyadr'}
taps[#taps+1]=p:install_write_tap(0xc0000080,0xc00001ef,'read-only original display control/tap/address stores',function(at,data,mask)
 local register=raster_registers[at]
 if not register or not active()then return end
 ensure_base()
 log('FLOOR_RASTER_IO',string.format('epoch=1 event=%d at=%08X register=%s before=%04X value=%04X mask=%04X pc=%08X',
  next_event(),at,register,p:read_u16(at),data,mask,cpu.PC.value))
end)
-- Observe the original shift-register clear, not an inferred erase rectangle.
]])
]=]
local first,last=assert(source:find(boundary,1,true))
assert(not source:find(boundary,last+1,true),'Unique whole4706 adapter suffix')
source=source:sub(1,first-1)..'\n'..addition..source:sub(first)
assert(load(source,'@whole4706_read_only_actual_display_IO_4719','t',_ENV))()
