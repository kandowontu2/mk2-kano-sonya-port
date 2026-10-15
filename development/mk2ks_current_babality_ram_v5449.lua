-- Full stock six-bit palette observation; original controller unchanged.
local file=assert(io.open('mk2ks_current_babality_ram_v5446.lua','rb'))
local wrapper=file:read('*a');file:close()
local before="assert(load(transport..source,'@entire_original_babality_controller_RAM_sinks_only','t',_ENV))()"
local after=[[
replace_once('for index=0,31 do colors[#colors+1]', 'for index=0,63 do colors[#colors+1]')
assert(load(transport..source,'@entire_original_babality_controller_full_stock_palette_RAM_only','t',_ENV))()
]]
local first,last=assert(wrapper:find(before,1,true));assert(not wrapper:find(before,last+1,true))
wrapper=wrapper:sub(1,first-1)..after..wrapper:sub(last+1)
assert(load(wrapper,'@only_passive_palette_observation_extended_to_native64','t',_ENV))()
