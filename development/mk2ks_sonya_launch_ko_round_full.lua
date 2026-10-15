-- Correct only the passive observer slice. Preserve original failed source.
local f=assert(io.open('mk2ks_sonya_launch_ko_round.lua','rb'));local source=f:read('a'):gsub('\r\n','\n');f:close()
local before=[[local observer=template:sub(assert(template:find("local p=manager.machine.devices[':maincpu'].spaces.program",boundary,true)))]]
local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
source=source:sub(1,a-1)..[[local observer_at=assert(template:find("local p=manager.machine.devices[':maincpu'].spaces.program",boundary,true))
local observer=template:sub(observer_at)]]..source:sub(b+1)
assert(load(source,'@whole_Sonya_KO_with_complete_passive_physical_observer','t',_G))()
