-- Preserve the original pregame loader rejection. Its helper declaration
-- accidentally also matched the later exact dofile-assignment search.
local f=assert(io.open('mk2ks_native_selector_sonya_choice_shadow_bound.lua','rb'))
local source=f:read('a'):gsub('\r\n','\n');f:close()
local before='local original_dofile=function(path)'
local at=assert(source:find(before,1,true));assert(not source:find(before,at+1,true))
source=source:sub(1,at-1)..'local function original_dofile(path)'..source:sub(at+#before)
assert(load(source,'@whole_explicit_environment_no_helper_search_collision','t',_G))()
