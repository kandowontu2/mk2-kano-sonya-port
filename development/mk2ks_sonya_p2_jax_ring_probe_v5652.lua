-- Bounded next-context comparison. Existing Ring policy now includes Jax11;
-- preserve the Jax native observer and every other controller/game byte.
local path='mk2ks_sonya_p2_kitana_ring_probe_v5636.lua'
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local function once(before,after)
 local a,b=source:find(before,1,true)
 assert(a and not source:find(before,b+1,true),'Unique declared Jax input context boundary')
 source=source:sub(1,a-1)..after..source:sub(b+1)
end
once('other.roster==4 or other.roster==5 or other.roster==10',
 'other.roster==4 or other.roster==5 or other.roster==10 or other.roster==11')
once('(target.roster~=4 and target.roster~=5 and target.roster~=10)',
 '(target.roster~=4 and target.roster~=5 and target.roster~=10 and target.roster~=11)')
once('((target.roster==4 and target.id~=4) or (target.roster==5 and target.id~=5))',
 '((target.roster==4 and target.id~=4) or (target.roster==5 and target.id~=5) or (target.roster==11 and target.id~=11))')
local before=" if path=='mk2ks_sonya_extended_kitana_ram_v5202.lua' then\n"
local addition=[==[
 if path=='mk2ks_sonya_extended_jax_ram_v5203.lua' then
  source=once(source,"once('local replacement=[[\\n','local replacement=[[\\n'..jax)",
   "once('local replacement=[[\\n','local replacement=[[\\n')")
 end
]==]
once(before,addition..before)
once('if stage==2 and mode==2','if stage==4 and mode==2')
once('p:read_u16(0x01060280)==4','p:read_u16(0x01060280)==11')
once('stage==3 and mode==2','stage==5 and mode==2')
once('stage==2 and mode==3','stage==4 and mode==3')
once('MK2_KITANA_RING_PROBE_BOUNDARY','MK2_JAX_RING_PROBE_BOUNDARY')
assert(load(source,'@'..path..'::existing_Ring_spacing_for_Jax11_only','t',_ENV))()
