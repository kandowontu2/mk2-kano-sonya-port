-- Preserve failed observer; repair only its two outer Lua string delimiters.
local file=assert(io.open('mk2ks_native_selector_sonya_death_raw_drain.lua','rb'))
local source=file:read('a'):gsub('\r\n','\n');file:close()
local opens,closes
source,opens=source:gsub(',%[%[\n',',[=[\n')
source,closes=source:gsub('\n%]%]%)','\n]=])')
assert(opens==2 and closes==2,'Exact two long source-insertion strings only')
assert(load(source,'@original_bulk_drain_observer_correct_outer_delimiters','t',_G))()
