-- Whole5993 successor: both pre/post actor records contain the same text.
-- Preserve the failed frame0 source; add stage words to both actual records.
local root=assert(os.getenv('MK2KS_BASIC_ROOT'))
local path=root..'/mk2ks_basic_ground_shadow_v5993.lua'
local reader=assert(io.open(path,'r'));local source=reader:read('*a');reader:close()
local before="local index=assert(source:find(before,1,true));assert(not source:find(before,index+1,true))\nsource=source:sub(1,index-1)..after..source:sub(index+#before)"
local after=[[local index=assert(source:find(before,1,true));local second=assert(source:find(before,index+1,true));assert(not source:find(before,second+1,true))
source=source:sub(1,second-1)..after..source:sub(second+#before)
source=source:sub(1,index-1)..after..source:sub(index+#before)]]
local index=assert(source:find(before,1,true));assert(not source:find(before,index+1,true))
source=source:sub(1,index-1)..after..source:sub(index+#before)
assert(load(source,'@'..path..'::both_actual_actor_records_v5997','t',_ENV))()
