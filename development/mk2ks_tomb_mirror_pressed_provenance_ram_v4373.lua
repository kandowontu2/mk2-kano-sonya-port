-- Entire original PC-qualified mirror motion/branch observer, new input driver.
local f=assert(io.open('mk2ks_tomb_mirror_provenance_ram_v4341.lua','rb'))
local source=f:read('a');f:close()
local old='mk2ks_tomb_mirror_driver_ram_v4340.lua'
local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
source=source:sub(1,first-1)..'mk2ks_tomb_mirror_pressed_driver_ram_v4372.lua'..source:sub(last+1)
assert(not source:find(':write_',1,true)and not source:find('set_value',1,true))
assert(load(source,'@complete4341_pressed_mirror_provenance_4373','t',_ENV))()
