-- Keep the exact qualified Kitana/Jax physical policy; remove only the final
-- Jax probe's host encounter-exit observer for an ordinary full campaign.
local path='mk2ks_sonya_p2_jax_ring_bound_probe_v5657.lua'
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local site="assert(load(source,'@'..path..'::keep_SubZero_insertion_anchor_disable_Jax_guard_only','t',_ENV))()"
local a,b=source:find(site,1,true)
assert(a and not source:find(site,b+1,true),'One exact bound probe loader')
local addition=[====[
local inner_site="assert(load(source,'@'..path..'::existing_Ring_spacing_for_Jax11_only','t',_ENV))()"
local ia,ib=source:find(inner_site,1,true)
assert(ia and not source:find(inner_site,ib+1,true),'One inner source-loader boundary')
local full_campaign=[=[
local exit_marker="local p=manager.machine.devices[':maincpu'].spaces.program\n"
local exit_at=assert(source:find(exit_marker,1,true))
assert(not source:find(exit_marker,exit_at+1,true),'One final probe-only observer')
local tail=source:sub(exit_at)
assert(tail:find('MK2_JAX_RING_PROBE_BOUNDARY',1,true))
assert(not tail:find('set_value',1,true) and not tail:find('clear_value',1,true))
source=source:sub(1,exit_at-1)
]=]
source=source:sub(1,ia-1)..full_campaign..source:sub(ia)
]====]
source=source:sub(1,a-1)..addition..source:sub(a)
assert(load(source,'@'..path..'::same_qualified_inputs_full_campaign_only','t',_ENV))()
