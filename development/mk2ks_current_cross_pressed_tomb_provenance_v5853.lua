-- Whole4341 source-PC-qualified observer; actual opposite-character driver.
local f=assert(io.open('mk2ks_tomb_mirror_provenance_ram_v4341.lua','rb'))
local source=f:read('a');f:close()
local old='mk2ks_tomb_mirror_driver_ram_v4340.lua'
local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
source=source:sub(1,first-1)..'mk2ks_current_cross_pressed_tomb_driver_v5852.lua'..source:sub(last+1)
-- Check real mutator names, not literal guard text inherited from the observer.
assert(not source:find('set_value(',1,true)and not source:find('write_u%d+'))
assert(load(source,'@complete4341_pressed_actual_cross_provenance_5853','t',_ENV))()
