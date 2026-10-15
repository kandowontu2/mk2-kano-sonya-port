-- Whole original4090 six-panel read-only observer, stock Jax selector only.
local file=assert(io.open('mk2ks_jax_arms_stock_corner_ram_v4090.lua','rb'))
local source=file:read('a');file:close()
local original="dofile('mk2ks_stock_extended_earned_ram_v3958.lua')"
local first,last=assert(source:find(original,1,true))
assert(not source:find(original,last+1,true))
source=source:sub(1,first-1).."dofile('mk2ks_stock_jax_profile_driver_v6159.lua')"..source:sub(last+1)
assert(load(source,'@whole_original4090_stock_Jax_corner_readonly','t',_ENV))()
