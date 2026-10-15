-- Exact qualified Kitana/Jax/Sub-Zero Ring contexts; ordinary full campaign.
-- Remove only the final probe-only host-exit observer. No guest mutation.
local path='mk2ks_sonya_p2_subzero_ring_probe_v5671.lua'
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local marker=']====]\nsource=source:sub(1,a-1)..addition..source:sub(a)'
local a,b=source:find(marker,1,true)
assert(a and not source:find(marker,b+1,true),'One qualified source assembly')
local addition=[======[
local inner_site="assert(load(source,'@'..path..'::existing_Ring_spacing_for_Jax11_only','t',_ENV))()"
local ia,ib=source:find(inner_site,1,true)
assert(ia and not source:find(inner_site,ib+1,true),'One actual inner source-loader boundary')
local full_campaign=[=[
local exit_marker="local p=manager.machine.devices[':maincpu'].spaces.program\n"
local exit_at=assert(source:find(exit_marker,1,true))
assert(not source:find(exit_marker,exit_at+1,true),'One final probe-only observer')
local tail=source:sub(exit_at)
assert(tail:find('MK2_SUBZERO_RING_PROBE_BOUNDARY',1,true))
assert(not tail:find('set_value',1,true) and not tail:find('clear_value',1,true))
source=source:sub(1,exit_at-1)
]=]
source=source:sub(1,ia-1)..full_campaign..source:sub(ia)
]======]
source=source:sub(1,a-1)..addition..source:sub(a)
assert(load(source,'@'..path..'::same_qualified_buttons_full_campaign','t',_ENV))()
