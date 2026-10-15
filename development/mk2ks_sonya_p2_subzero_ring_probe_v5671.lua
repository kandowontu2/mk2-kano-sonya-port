-- Bounded physical-policy comparison at true native Sub-Zero8/stage7.
-- Preserve the exact qualified Kitana/Jax inputs, guest, schedule and observers.
-- Add only context8 to existing Ring spacing; disable its close-guard branch.
local path='mk2ks_sonya_p2_jax_ring_bound_probe_v5657.lua'
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local site="assert(load(source,'@'..path..'::keep_SubZero_insertion_anchor_disable_Jax_guard_only','t',_ENV))()"
local a,b=source:find(site,1,true)
assert(a and not source:find(site,b+1,true),'One actual bound-source loader')
local addition=[====[
local function outer_once(before,after)
 local a,b=source:find(before,1,true)
 assert(a and not source:find(before,b+1,true),'Unique Sub-Zero physical context adaptation')
 source=source:sub(1,a-1)..after..source:sub(b+1)
end
outer_once("'other.roster==4 or other.roster==5 or other.roster==10 or other.roster==11')",
 "'other.roster==4 or other.roster==5 or other.roster==10 or other.roster==11 or other.roster==8')")
outer_once("'(target.roster~=4 and target.roster~=5 and target.roster~=10 and target.roster~=11)')",
 "'(target.roster~=4 and target.roster~=5 and target.roster~=10 and target.roster~=11 and target.roster~=8)')")
outer_once("'((target.roster==4 and target.id~=4) or (target.roster==5 and target.id~=5) or (target.roster==11 and target.id~=11))')",
 "'((target.roster==4 and target.id~=4) or (target.roster==5 and target.id~=5) or (target.roster==11 and target.id~=11) or (target.roster==8 and target.id~=8))')")
local needle=" if path=='mk2ks_sonya_extended_jax_ram_v5203.lua' then\n"
local disable=[==[
 if path=='mk2ks_sonya_extended_subzero_ram_v5204.lua' then
  source=once(source,"once('local replacement=[[\\n','local replacement=[[\\n'..subzero)",
   [=[subzero=subzero:gsub('other%.roster==8 then','other.roster==8 and false then',1)
once('local replacement=[[\n','local replacement=[[\n'..subzero)]=])
 end
]==]
outer_once(needle,disable..needle)
outer_once("once('if stage==2 and mode==2','if stage==4 and mode==2')",
 "once('if stage==2 and mode==2','if stage==7 and mode==2')")
outer_once("once('p:read_u16(0x01060280)==4','p:read_u16(0x01060280)==11')",
 "once('p:read_u16(0x01060280)==4','p:read_u16(0x01060280)==8')")
outer_once("once('stage==3 and mode==2','stage==5 and mode==2')",
 "once('stage==3 and mode==2','stage==8 and mode==2')")
outer_once("once('stage==2 and mode==3','stage==4 and mode==3')",
 "once('stage==2 and mode==3','stage==7 and mode==3')")
outer_once("once('MK2_KITANA_RING_PROBE_BOUNDARY','MK2_JAX_RING_PROBE_BOUNDARY')",
 "once('MK2_KITANA_RING_PROBE_BOUNDARY','MK2_SUBZERO_RING_PROBE_BOUNDARY')")
]====]
source=source:sub(1,a-1)..addition..source:sub(a)
assert(load(source,'@'..path..'::existing_Ring_spacing_SubZero8_only','t',_ENV))()
