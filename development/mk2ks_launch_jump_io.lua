-- Existing genuine forward-jump/kick controller, corrected real IN0/IN2 taps.
-- Retain the entire original driver, guest/GFX/body and source audio inventory.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a'):gsub('\r\n','\n');f:close();return s
end
local function change(source,before,after)
 local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
 return source:sub(1,a-1)..after..source:sub(b+1)
end
local source=read('mk2ks_launch_ground_io_v6706.lua')
source=change(source,"'extra..'+string.format","'extra..'..string.format")
source=change(source,"local adapter=read('mk2ks_launch_ground_counter_v6703.lua')",
 "local adapter=read('mk2ks_launch_jump_interrupt_v6693.lua')")
assert(load(source,'@whole_jump_counter_corrected_native_button_ports','t',_G))()
