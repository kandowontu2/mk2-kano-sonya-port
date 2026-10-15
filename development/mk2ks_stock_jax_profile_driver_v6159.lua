-- Preserve whole original physical1021/3958 driver, allow true stock Jax11.
local file=assert(io.open('mk2ks_stock_extended_earned_ram_v3958.lua','rb'))
local transport=file:read('a');file:close()
local marker="assert(load(source,'@mk2ks_stock_fatality_v1021_RAM_image_sink','t',_ENV))()"
local first,last=assert(transport:find(marker,1,true))
assert(not transport:find(marker,last+1,true))
local addition=[[
local original="local identity=assert(({kano=17,sonya=18,liu_kang=1,kitana=4})[name])"
local first,last=assert(source:find(original,1,true))
assert(not source:find(original,last+1,true))
source=source:sub(1,first-1).."local identity=assert(({kano=17,sonya=18,liu_kang=1,kitana=4,jax=11})[name])"..source:sub(last+1)
print('MK2_TRUE_STOCK_JAX_PROFILE_DRIVER selector_extension_only=1 writes=0 assistance=none')
]]
transport=transport:sub(1,first-1)..addition..transport:sub(first)
assert(load(transport,'@whole_original_3958_1021_true_stock_Jax_selector','t',_ENV))()
