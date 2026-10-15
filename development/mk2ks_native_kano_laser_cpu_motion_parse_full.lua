-- The older body-name matcher also matched a loader's quoted literals.
-- Require the real final native LIVE predicate, not an outer wrapper.
local filename='mk2ks_native_kano_laser_cpu_motion_parse.lua'
local file=assert(io.open(filename,'r'));local source=file:read('a');file:close()
local before="source:find('local function postending_join()',1,true) and source:find('local function sample(',1,true)"
local after="source:find('if mode==2 and state==1 and p:read_u16(slots[opponent].state)==0 and human and other and human.owner==human.actor and other.owner==other.actor then',1,true)"
local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
source=source:sub(1,a-1)..after..source:sub(b+1)
assert(load(source,'@'..filename..'::actual_final_native_controller_predicate','t',_G))()
