-- Full campaign with independently qualified Kitana physical Ring strategy.
-- Remove only the probe's host encounter-exit observer; no game writes.
local path='mk2ks_sonya_p2_kitana_ring_probe_v5636.lua'
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local marker="local p=manager.machine.devices[':maincpu'].spaces.program\n"
local first=assert(source:find(marker,1,true))
assert(not source:find(marker,first+1,true),'Exactly one final probe-only observer')
local observer=source:sub(first)
assert(observer:find('MK2_KITANA_RING_PROBE_BOUNDARY',1,true))
assert(not observer:find('set_value',1,true) and not observer:find('clear_value',1,true))
assert(load(source:sub(1,first-1),'@'..path..'::same_verified_inputs_full_campaign_no_probe_exit','t',_ENV))()
