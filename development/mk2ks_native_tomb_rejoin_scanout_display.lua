-- Retain the entire timing capture. Use the34010 register order, not34020.
local f=assert(io.open('mk2ks_native_tomb_rejoin_timing_display.lua','rb'))
local source=f:read('a'):gsub('\r\n','\n');f:close()
local function once(old,new)
 local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
 source=source:sub(1,first-1)..new..source:sub(last+1)
end
once('frame=frame,vcount=p:read_u16(0xc00001c0),dpyadr=',
 'frame=frame,vcount=p:read_u16(0xc00001d0),hcount=p:read_u16(0xc00001c0),dpyadr=')
once('vcount=%04X dpyadr=%04X dpystart=',
 'vcount=%04X hcount=%04X veblnk=%04X vsblnk=%04X vtotal=%04X dpyadr=%04X dpystart=')
once('frame,p:read_u16(0xc00001c0),p:read_u16(0xc00001e0),',
 'frame,p:read_u16(0xc00001d0),p:read_u16(0xc00001c0),p:read_u16(0xc0000050),p:read_u16(0xc0000060),p:read_u16(0xc0000070),p:read_u16(0xc00001e0),')
once('flip_vcount=%04X flip_dpyadr=', 'flip_vcount=%04X flip_hcount=%04X flip_dpyadr=')
once('post_latch and post_latch.vcount or 0,post_latch and post_latch.dpyadr or 0,',
 'post_latch and post_latch.vcount or 0,post_latch and post_latch.hcount or 0,post_latch and post_latch.dpyadr or 0,')
assert(load(source,'@whole_timing_capture_correct34010_register_order_and_native_visible_interval','t',_ENV))()
