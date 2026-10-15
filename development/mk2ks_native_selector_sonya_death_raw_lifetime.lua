-- Prelaunch lifetime correction: native pool addresses can legitimately reuse.
local file=assert(io.open('mk2ks_native_selector_sonya_death_raw_objects.lua','rb'))
local source=file:read('a'):gsub('\r\n','\n');file:close()
local before='assert(valid(a)and a~=subject and not objects[a])'
local at,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
source=source:sub(1,at-1)..'assert(valid(a)and a~=subject and(not objects[a]or objects[a].retired))'..source:sub(last+1)
local count=0
source=source:gsub('if not item then return end',function()
 count=count+1;return 'if not item or item.retired then return end'
end)
assert(count==2,'Both removal and drawing callbacks reject retired-address aliases')
assert(load(source,'@whole_original_raw_observer_legitimate_pool_reuse','t',_G))()
