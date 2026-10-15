-- Observe an actual subsequent selection/live-match phase, not loading pixels.
local file=assert(io.open('mk2ks_native_subzero_shatter_lifecycle_v4943.lua','rb'))
local source=file:read('a');file:close()
local function replace(before,after)
 local first,last=source:find(before,1,true)
 assert(first and not source:find(before,last+1,true),'Unique actual transition anchor')
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
replace('if frame-natural==60 then',[[
   local mode=p:read_u16(0x010601d0)
   if frame-natural>=60 and (mode==4 or (mode==2 and p:read_u16(slots[winner].state)==1 and p:read_u16(slots[side].state)==1))then]])
replace('frame-deep>=1200','frame-deep>=1800')
assert(load(source,'@native_shatter_actual_next_phase_v4947','t',_ENV))()
