-- Same real selected Liu1 and passive inventories. Use F,F,LP against the
-- compact roll; preserve F,F,HP for Bicycle. No game-state assignments.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a'):gsub('\r\n','\n');f:close();return s
end
local function change(source,before,after)
 local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
 return source:sub(1,a-1)..after..source:sub(b+1)
end
local source=read('mk2ks_launch_fireball_counter.lua')
source=change(source,"local controller=read('mk2ks_launch_ground_counter_v6703.lua')",[[local controller=read('mk2ks_launch_ground_counter_v6703.lua')
controller=change(controller,"local port=button=='Low Kick'and':IN2'or':IN0'",
 "local port=(button=='Low Kick'or button=='Low Punch')and':IN2'or':IN0'")]])
source=change(source,"if age>=6 and age<9 then press('High Punch')end",
 "if age>=6 and age<9 then press(move=='ball'and'Low Punch'or'High Punch')end")
assert(load(source,'@whole_launch_counter_real_low_fireball_physical_inputs','t',_G))()
