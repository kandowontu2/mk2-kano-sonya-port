-- Whole failed controller successor: correct only the nested reader scope.
local path='mk2ks_native_paired_stumble_subzero_forward_jump.lua'
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local before="local common=read('mk2ks_natural_campaign_shao_ring_retreat_v3485.lua')"
local after="local common_file=assert(io.open('mk2ks_natural_campaign_shao_ring_retreat_v3485.lua','rb'));local common=common_file:read('a');common_file:close()"
local a,b=source:find(before,1,true)
assert(a and not source:find(before,b+1,true),'One actual nested physical routine reader scope correction')
source=source:sub(1,a-1)..after..source:sub(b+1)
assert(load(source,'@'..path..'::whole_original_feedback_bound_file_reader','t',_ENV))()
